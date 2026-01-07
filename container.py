import subprocess
import threading
import time
import psutil
import os
import platform
import shutil
try:
    from networking import network
except ImportError:
    network = None
# WSL support removed - using Windows simulation mode only

class SimulatedContainer:
    def __init__(self, container_id, name, command, rootfs_path, mem_limit_mb=100, 
                 cpu_limit_percent=50, volumes=None, env_vars=None, log_file=None, ui_callback=None,
                 ports=None, restart_policy='no', health_check=None, network='bridge',
                 read_only=False, use_user_ns=True, use_ipc_ns=True, use_net_ns=True,
                 drop_capabilities=None, enable_strace=False, cpu_shares=None, nice_value=None):
        self.container_id = container_id
        self.name = name
        self.command = command
        self.rootfs_path = rootfs_path
        self.mem_limit_mb = mem_limit_mb
        self.cpu_limit_percent = cpu_limit_percent
        self.volumes = volumes or []
        self.env_vars = env_vars or {}
        self.ports = ports or []  # List of (host_port, container_port) tuples
        self.restart_policy = restart_policy  # 'no', 'always', 'on-failure', 'unless-stopped'
        self.health_check = health_check  # {'cmd': 'command', 'interval': 30, 'timeout': 10, 'retries': 3}
        self.network = network
        self.log_file = log_file or os.path.join(os.path.dirname(rootfs_path), "container.log")
        self.process = None
        self.ui_callback = ui_callback
        self.status = "Stopped"
        self.is_linux = platform.system() == "Linux"
        self.cgroup_path = None
        self.cgroup_version = None
        self.start_time = None
        self.restart_count = 0
        self.health_status = "unknown"  # 'healthy', 'unhealthy', 'starting', 'unknown'
        self.last_health_check = None
        self.metrics = {
            'cpu_percent': 0.0,
            'memory_mb': 0.0,
            'network_rx': 0,
            'network_tx': 0,
            'disk_read': 0,
            'disk_write': 0
        }
        self.health_check_thread = None
        self.restart_thread = None
        self.read_only = read_only
        self.use_user_ns = use_user_ns
        self.use_ipc_ns = use_ipc_ns
        self.use_net_ns = use_net_ns
        self.drop_capabilities = drop_capabilities or []
        self.enable_strace = enable_strace
        self.cpu_shares = cpu_shares
        self.nice_value = nice_value
        self.lifecycle_events = []  # Track container lifecycle for timeline
        self.oom_detected = False
        self.cpu_throttled = False
        self.zombie_reaper_thread = None
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        self._record_lifecycle_event("created")

    # WSL methods removed - using Windows simulation mode only

    def _setup_cgroup(self):
        """Setup cgroup with v1 or v2 support"""
        if not self.is_linux:
            return None
        try:
            from utils import detect_cgroup_version
            self.cgroup_version = detect_cgroup_version()
            cgroup_name = f"minidocker_{self.name}"
            
            if self.cgroup_version == "v2":
                # cgroups v2 unified hierarchy
                cgroup_base = "/sys/fs/cgroup"
                cgroup_path = os.path.join(cgroup_base, cgroup_name)
                os.makedirs(cgroup_path, exist_ok=True)
                
                # Enable controllers
                with open(os.path.join(cgroup_path, "cgroup.subtree_control"), "w") as f:
                    f.write("+memory +cpu")
                
                # Set memory limit
                with open(os.path.join(cgroup_path, "memory.max"), "w") as f:
                    f.write(str(self.mem_limit_mb * 1024 * 1024))
                
                # Set CPU limit (format: "max 50000" = 50% of CPU)
                cpu_max = int(self.cpu_limit_percent * 1000)  # Convert to millicores
                with open(os.path.join(cgroup_path, "cpu.max"), "w") as f:
                    f.write(f"{cpu_max * 10000} 100000")  # Format: quota period
                
                self.cgroup_path = cgroup_path
                return cgroup_path
            else:
                # cgroups v1 (fallback)
                cgroup_base = "/sys/fs/cgroup"
                mem_cgroup = os.path.join(cgroup_base, "memory", cgroup_name)
                cpu_cgroup = os.path.join(cgroup_base, "cpu", cgroup_name)
                os.makedirs(mem_cgroup, exist_ok=True)
                os.makedirs(cpu_cgroup, exist_ok=True)
                
                with open(os.path.join(mem_cgroup, "memory.limit_in_bytes"), "w") as f:
                    f.write(str(self.mem_limit_mb * 1024 * 1024))
                
                # CPU shares or CPU quota
                if self.cpu_shares:
                    with open(os.path.join(cpu_cgroup, "cpu.shares"), "w") as f:
                        f.write(str(self.cpu_shares))
                else:
                    with open(os.path.join(cpu_cgroup, "cpu.shares"), "w") as f:
                        f.write(str(int(self.cpu_limit_percent * 10.24)))
                
                self.cgroup_path = cgroup_name
                return cgroup_name
        except Exception as e:
            self._notify(f"Warning: Could not setup cgroup: {e}")
            return None

    def _cleanup_cgroup(self):
        """Cleanup cgroup (v1 or v2)"""
        if not self.is_linux or not self.cgroup_path:
            return
        try:
            if self.cgroup_version == "v2":
                # v2: single unified path
                if os.path.exists(self.cgroup_path):
                    shutil.rmtree(self.cgroup_path)
            else:
                # v1: separate hierarchies
                cgroup_base = "/sys/fs/cgroup"
                for cg_type in ["memory", "cpu"]:
                    cg_path = os.path.join(cgroup_base, cg_type, self.cgroup_path)
                    if os.path.exists(cg_path):
                        shutil.rmtree(cg_path)
        except:
            pass

    def _setup_volumes(self):
        if not self.volumes or not self.is_linux:
            return
        from utils import parse_volume
        for volume in self.volumes:
            try:
                host_path, container_path = parse_volume(volume)
                host_path = os.path.abspath(host_path)
                container_path = os.path.join(self.rootfs_path, container_path.lstrip("/"))
                os.makedirs(container_path, exist_ok=True)
                if os.path.exists(host_path):
                    subprocess.run(["mount", "--bind", host_path, container_path],
                                check=True, capture_output=True)
                    self._notify(f"Mounted volume: {host_path} -> {container_path}")
            except Exception as e:
                self._notify(f"Error setting up volume {volume}: {e}")
    
    # WSL volume setup removed - volumes not supported in Windows simulation mode
    def _cleanup_volumes(self):
        if not self.volumes or not self.is_linux:
            return
        for volume in self.volumes:
            try:
                _, container_path = (volume.split(":", 1) if ":" in volume else (volume, volume))
                container_path = os.path.join(self.rootfs_path, container_path.lstrip("/"))
                if os.path.ismount(container_path):
                    subprocess.run(["umount", container_path], check=False, capture_output=True)
            except:
                pass

    def _build_container_command(self):
        """Build container command with namespaces and security features"""
        if self.is_linux:
            if not os.path.exists(self.rootfs_path):
                self._notify(f"Error: rootfs not found at {self.rootfs_path}")
                return None
            self._setup_volumes()
            
            # Build unshare command with namespaces
            unshare_args = ["unshare", "--pid", "--mount", "--uts"]
            
            # Add user namespace if enabled
            if self.use_user_ns:
                unshare_args.append("--user")
            
            # Add IPC namespace if enabled
            if self.use_ipc_ns:
                unshare_args.append("--ipc")
            
            # Add network namespace if enabled
            if self.use_net_ns:
                unshare_args.append("--net")
            
            unshare_args.append("--fork")
            
            # Add capability dropping if specified
            cap_args = []
            if self.drop_capabilities:
                caps_to_drop = ",".join(self.drop_capabilities)
                cap_args = ["--drop-capability", caps_to_drop]
            
            # Add read-only mount if specified
            mount_args = []
            if self.read_only:
                mount_args = ["--read-only"]
            
            # Add strace if enabled
            if self.enable_strace:
                trace_file = os.path.join(os.path.dirname(self.rootfs_path), "strace.log")
                base_cmd = ["strace", "-o", trace_file, "-f", "-e", "trace=all"]
                return base_cmd + unshare_args + ["chroot", self.rootfs_path, "/bin/sh", "-c", self.command]
            
            # Build final command
            cmd = unshare_args + ["chroot", self.rootfs_path, "/bin/sh", "-c", self.command]
            return cmd
        else:
            # Windows simulation mode - no WSL, just run commands directly
            # Rootfs is created but not used in simulation mode - no need to check for it
            # For Windows simulation mode, use shlex to properly parse quoted strings
            import shlex
            try:
                cmd_parts = shlex.split(self.command)
                if not cmd_parts:
                    return None
                if cmd_parts[0] == "python" and len(cmd_parts) > 1 and cmd_parts[1] == "-c":
                    if len(cmd_parts) > 2:
                        code = cmd_parts[2]
                        return ["python", "-c", code]
                    return None
                return cmd_parts
            except:
                # Fallback: return as string for shell to handle
                return self.command

    def run(self):
        if self.process and self.process.poll() is None:
            self._notify("Already running!")
            return
        self._notify(f"Starting container: {self.command}")
        if self.is_linux:
            self._setup_cgroup()
        cmd_parts = self._build_container_command()
        if not cmd_parts:
            return
        try:
            env = os.environ.copy()
            if not self.is_linux:
                # Windows simulation mode - add env vars directly
                if self.env_vars:
                    for key, value in self.env_vars.items():
                        log_fd.write(f"Environment variable: {key} = {value}\n")
                        env[str(key)] = str(value)  # Ensure both key and value are strings
            log_fd = open(self.log_file, 'a')
            log_fd.write(f"\n=== Container {self.container_id} started at {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            log_fd.write(f"Command: {self.command}\n")
            if self.env_vars:
                log_fd.write(f"Environment: {self.env_vars}\n")
            if self.volumes:
                log_fd.write(f"Volumes: {self.volumes}\n")
            log_fd.flush()
            # Use shell=True for Windows simulation mode to handle quotes properly
            use_shell = not self.is_linux
            if use_shell and isinstance(cmd_parts, str):
                # Already a string, use as-is with shell=True
                # Environment variables are passed via env parameter
                self.process = subprocess.Popen(cmd_parts, stdout=log_fd, stderr=subprocess.STDOUT,
                                              env=env, shell=True, text=True)
            elif use_shell and isinstance(cmd_parts, list):
                # For Windows with list, use shell=False to ensure env vars are passed correctly
                # This works better than shell=True for environment variable inheritance
                self.process = subprocess.Popen(cmd_parts, stdout=log_fd, stderr=subprocess.STDOUT,
                                              env=env, shell=False, text=True)
            else:
                # List of command parts for Linux
                self.process = subprocess.Popen(cmd_parts, stdout=log_fd, stderr=subprocess.STDOUT,
                                              env=env, shell=use_shell, text=True)
            if self.is_linux and self.cgroup_path:
                try:
                    if self.cgroup_version == "v2":
                        # v2: use cgroup.procs in unified hierarchy
                        with open(os.path.join(self.cgroup_path, "cgroup.procs"), "w") as f:
                            f.write(str(self.process.pid))
                    else:
                        # v1: use memory cgroup
                        with open(f"/sys/fs/cgroup/memory/{self.cgroup_path}/cgroup.procs", "w") as f:
                            f.write(str(self.process.pid))
                except:
                    pass
            
            # Setup user namespace mapping if enabled
            if self.is_linux and self.use_user_ns and self.process:
                self._setup_user_namespace_mapping()
            
            # Setup zombie reaper if on Linux
            if self.is_linux:
                self._start_zombie_reaper()
            
            # Setup resource violation monitoring
            if self.is_linux:
                threading.Thread(target=self._monitor_resource_violations, daemon=True).start()
            threading.Thread(target=self._monitor_logs, args=(log_fd,), daemon=True).start()
            self.status = "Running"
            self.start_time = time.time()
            self._record_lifecycle_event("started")
            self._notify(f"Container started with PID: {self.process.pid}", status="Running")
            
            # Setup networking
            try:
                from networking import network
                if network and self.ports:
                    network.bind_ports(self.name, self.ports)
                    ip = network.allocate_ip(self.name)
                    network.containers[self.name] = {'ip': ip, 'ports': self.ports}
            except:
                pass
            
            # Start monitoring threads
            threading.Thread(target=self._monitor_resources, daemon=True).start()
            threading.Thread(target=self._monitor_process, daemon=True).start()
            
            # Start health check if configured
            if self.health_check:
                threading.Thread(target=self._health_check_loop, daemon=True).start()
            
            # Handle restart policy
            if self.restart_policy != 'no':
                threading.Thread(target=self._restart_monitor, daemon=True).start()
        except Exception as e:
            self._notify(f"Error starting container: {str(e)}")
            self.status = "Error"
            try:
                with open(self.log_file, 'a') as f:
                    f.write(f"\n=== ERROR: {str(e)} ===\n")
            except:
                pass
            self._cleanup_cgroup()

    def _monitor_logs(self, log_fd):
        if not self.process:
            return
        try:
            exit_code = self.process.wait()
            log_fd.write(f"\n=== Container exited with code {exit_code} ===\n")
            log_fd.close()
        except Exception as e:
            log_fd.write(f"\n=== Error: {e} ===\n")
            log_fd.close()
    
    def _monitor_process(self):
        if not self.process:
            return
        try:
            exit_code = self.process.wait()
            process_ref = self.process  # Keep reference before cleanup
            self.status = "Stopped"
            self._record_lifecycle_event("stopped")
            self._notify(f"Container process exited with code {exit_code}", status="Stopped")
            self.process = None
            self.start_time = None
            self._cleanup_cgroup()
            self._cleanup_volumes()
            
            # Release networking
            try:
                from networking import network
                if network:
                    network.release_ports(self.name)
                    if self.name in network.containers:
                        del network.containers[self.name]
            except:
                pass
        except Exception as e:
            self._notify(f"Error monitoring process: {e}", status="Error")
            self.process = None
            self.start_time = None

    def stop(self):
        if self.process:
            if self.process.poll() is None:
                self._notify("Stopping container...")
                try:
                    if self.is_linux:
                        os.kill(self.process.pid, 15)
                    else:
                        self.process.terminate()
                    try:
                        self.process.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        if self.is_linux:
                            os.kill(self.process.pid, 9)
                        else:
                            self.process.kill()
                        self.process.wait()
                    self._notify("Container stopped.")
                    
                    # Release networking
                    if network:
                        network.release_ports(self.name)
                        if self.name in network.containers:
                            del network.containers[self.name]
                except (ProcessLookupError, Exception) as e:
                    self._notify(f"Error stopping: {e}" if isinstance(e, Exception) else "Process already stopped.")
            else:
                self._notify("Container already stopped.")
        else:
            self._notify("Container already stopped.")
        self.process = None
        self.status = "Stopped"
        self.start_time = None
        self._record_lifecycle_event("stopped")
        self._cleanup_cgroup()
        self._cleanup_volumes()

    def pause(self):
        if self.process and self.process.poll() is None:
            try:
                if self.is_linux:
                    try:
                        freezer = f"/sys/fs/cgroup/freezer/minidocker_{self.name}"
                        os.makedirs(freezer, exist_ok=True)
                        with open(os.path.join(freezer, "freezer.state"), "w") as f:
                            f.write("FROZEN")
                        self.status = "Paused"
                        self._record_lifecycle_event("paused")
                        self._notify("Container paused.")
                    except:
                        psutil.Process(self.process.pid).suspend()
                        self.status = "Paused"
                        self._record_lifecycle_event("paused")
                        self._notify("Container paused.")
                else:
                    psutil.Process(self.process.pid).suspend()
                    self.status = "Paused"
                    self._record_lifecycle_event("paused")
                    self._notify("Container paused.")
            except psutil.NoSuchProcess:
                self._notify("Cannot pause: process not found.")
        else:
            self._notify("Cannot pause: container not running.")

    def resume(self):
        if self.process and self.process.poll() is None:
            try:
                if self.is_linux:
                    try:
                        freezer = f"/sys/fs/cgroup/freezer/minidocker_{self.name}"
                        if os.path.exists(freezer):
                            with open(os.path.join(freezer, "freezer.state"), "w") as f:
                                f.write("THAWED")
                            self.status = "Running"
                            self._record_lifecycle_event("resumed")
                            self._notify("Container resumed.")
                        else:
                            psutil.Process(self.process.pid).resume()
                            self.status = "Running"
                            self._record_lifecycle_event("resumed")
                            self._notify("Container resumed.")
                    except:
                        psutil.Process(self.process.pid).resume()
                        self.status = "Running"
                        self._record_lifecycle_event("resumed")
                        self._notify("Container resumed.")
                else:
                    psutil.Process(self.process.pid).resume()
                    self.status = "Running"
                    self._record_lifecycle_event("resumed")
                    self._notify("Container resumed.")
            except psutil.NoSuchProcess:
                self._notify("Cannot resume: process not found.")
        else:
            self._notify("Cannot resume: container not running.")

    def restart(self):
        self._notify("Restarting container...")
        self.stop()
        time.sleep(0.5)
        self.run()

    def _monitor_resources(self):
        if not self.process:
            return
        try:
            proc = psutil.Process(self.process.pid)
        except psutil.NoSuchProcess:
            return
        while self.process and self.process.poll() is None:
            try:
                mem = proc.memory_info().rss / (1024*1024)
                cpu = proc.cpu_percent(interval=1)
                uptime = f"{int(time.time() - self.start_time)}s" if self.start_time else ""
                self._notify(f"Usage: {mem:.1f} MB RAM, {cpu:.1f}% CPU, Uptime: {uptime}")
                if mem > self.mem_limit_mb:
                    self._notify(f"Memory limit exceeded! Stopping container.")
                    self.stop()
                    break
                if cpu > self.cpu_limit_percent:
                    self._notify(f"CPU usage high ({cpu:.1f}%)")
                time.sleep(2)
            except psutil.NoSuchProcess:
                break
            except Exception as e:
                self._notify(f"Error monitoring: {e}")
                break

    def _health_check_loop(self):
        """Run health checks periodically"""
        if not self.health_check:
            return
        
        cmd = self.health_check.get('cmd', 'true')
        interval = self.health_check.get('interval', 30)
        timeout = self.health_check.get('timeout', 10)
        retries = self.health_check.get('retries', 3)
        consecutive_failures = 0
        
        while self.status == "Running" and self.process and self.process.poll() is None:
            try:
                time.sleep(interval)
                if self.status != "Running":
                    break
                
                # Run health check command
                result = subprocess.run(cmd, shell=True, capture_output=True, timeout=timeout)
                self.last_health_check = time.time()
                
                if result.returncode == 0:
                    consecutive_failures = 0
                    if self.health_status != "healthy":
                        self.health_status = "healthy"
                        self._notify("Container is healthy")
                else:
                    consecutive_failures += 1
                    if consecutive_failures >= retries:
                        self.health_status = "unhealthy"
                        self._notify(f"Container is unhealthy (failed {consecutive_failures} times)")
                        if self.restart_policy == 'on-failure':
                            self.restart_count += 1
                            self._notify("Restarting container due to health check failure...")
                            self.stop()
                            time.sleep(2)
                            self.run()
                            consecutive_failures = 0
            except subprocess.TimeoutExpired:
                consecutive_failures += 1
                self.health_status = "unhealthy"
                self._notify(f"Health check timed out")
            except Exception as e:
                self._notify(f"Health check error: {e}")
                time.sleep(interval)
    
    def _restart_monitor(self):
        """Monitor container and restart based on policy"""
        while True:
            if self.status == "Stopped" and self.restart_policy != 'no':
                if self.restart_policy == 'always':
                    self._notify("Restarting container (always policy)...")
                    time.sleep(2)
                    self.run()
                elif self.restart_policy == 'on-failure':
                    # Handled in health check
                    pass
                elif self.restart_policy == 'unless-stopped':
                    # Only restart if not manually stopped
                    if self.restart_count < 10:  # Prevent infinite loops
                        self._notify("Restarting container (unless-stopped policy)...")
                        time.sleep(2)
                        self.run()
                        self.restart_count += 1
            time.sleep(5)
    
    def update_metrics(self):
        """Update container metrics"""
        if not self.process or self.process.poll() is not None:
            return
        
        try:
            proc = psutil.Process(self.process.pid)
            self.metrics['cpu_percent'] = proc.cpu_percent(interval=0.1)
            self.metrics['memory_mb'] = proc.memory_info().rss / (1024 * 1024)
            
            # Network stats (if available)
            try:
                io_counters = proc.io_counters()
                self.metrics['disk_read'] = io_counters.read_bytes
                self.metrics['disk_write'] = io_counters.write_bytes
            except:
                pass
        except psutil.NoSuchProcess:
            pass
        except Exception:
            pass
    
    def get_logs(self, tail=100):
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    return ''.join(f.readlines()[-tail:])
            except Exception as e:
                return f"Error reading logs: {e}"
        return "No logs available"
    
    def _setup_user_namespace_mapping(self):
        """Setup UID/GID mapping for user namespace"""
        if not self.is_linux or not self.process:
            return
        try:
            from utils import get_unprivileged_uid, get_unprivileged_gid
            host_uid = get_unprivileged_uid()
            host_gid = get_unprivileged_gid()
            
            # Write UID map: container UID 0 -> host unprivileged UID
            uid_map_path = f"/proc/{self.process.pid}/uid_map"
            if os.path.exists(uid_map_path):
                with open(uid_map_path, 'w') as f:
                    f.write(f"0 {host_uid} 1\n")  # Map container UID 0 to host UID
            
            # Write GID map: container GID 0 -> host unprivileged GID
            gid_map_path = f"/proc/{self.process.pid}/gid_map"
            if os.path.exists(gid_map_path):
                with open(gid_map_path, 'w') as f:
                    f.write(f"0 {host_gid} 1\n")  # Map container GID 0 to host GID
            
            self._notify(f"User namespace mapping: container 0 -> host {host_uid}:{host_gid}")
        except Exception as e:
            self._notify(f"Warning: Could not setup user namespace mapping: {e}")
    
    def _start_zombie_reaper(self):
        """Start thread to reap zombie processes"""
        if not self.is_linux:
            return
        def reap_zombies():
            import signal
            while self.process and self.process.poll() is None:
                try:
                    # Reap any zombie children
                    pid, status = os.waitpid(-1, os.WNOHANG)
                    if pid > 0:
                        self._notify(f"Reaped zombie process {pid}")
                except (ChildProcessError, OSError):
                    # No children to reap
                    pass
                time.sleep(1)
        
        self.zombie_reaper_thread = threading.Thread(target=reap_zombies, daemon=True)
        self.zombie_reaper_thread.start()
    
    def _monitor_resource_violations(self):
        """Monitor for OOM kills and CPU throttling"""
        if not self.is_linux or not self.process:
            return
        
        while self.process and self.process.poll() is None:
            try:
                # Check for OOM kill
                if self.cgroup_version == "v2":
                    oom_file = os.path.join(self.cgroup_path, "memory.events")
                else:
                    oom_file = f"/sys/fs/cgroup/memory/{self.cgroup_path}/memory.oom_control"
                
                if os.path.exists(oom_file):
                    with open(oom_file, 'r') as f:
                        content = f.read()
                        if "oom_kill" in content.lower() or "oom" in content.lower():
                            if not self.oom_detected:
                                self.oom_detected = True
                                self._notify("ALERT: Out-of-memory (OOM) kill detected!", status="Error")
                                self._record_lifecycle_event("oom_killed")
                
                # Check for CPU throttling
                if self.cgroup_version == "v2":
                    cpu_stat_file = os.path.join(self.cgroup_path, "cpu.stat")
                else:
                    cpu_stat_file = f"/sys/fs/cgroup/cpu/{self.cgroup_path}/cpu.stat"
                
                if os.path.exists(cpu_stat_file):
                    with open(cpu_stat_file, 'r') as f:
                        content = f.read()
                        if "throttled" in content.lower():
                            throttled_count = 0
                            for line in content.split('\n'):
                                if 'throttled' in line.lower():
                                    try:
                                        throttled_count = int(line.split()[-1])
                                        break
                                    except:
                                        pass
                            if throttled_count > 0 and not self.cpu_throttled:
                                self.cpu_throttled = True
                                self._notify(f"ALERT: CPU throttling detected ({throttled_count} times)!", status="Warning")
                                self._record_lifecycle_event("cpu_throttled")
                
                time.sleep(5)  # Check every 5 seconds
            except Exception as e:
                self._notify(f"Error monitoring resource violations: {e}")
                time.sleep(5)
    
    def _record_lifecycle_event(self, event_type):
        """Record a lifecycle event for timeline view"""
        event = {
            'type': event_type,
            'timestamp': time.time(),
            'status': self.status
        }
        self.lifecycle_events.append(event)
    
    def get_lifecycle_timeline(self):
        """Get container lifecycle timeline"""
        return self.lifecycle_events.copy()
    
    def exec(self, command, interactive=False):
        """Execute command in running container (Linux only)"""
        if not self.is_linux:
            self._notify("exec is only supported on Linux")
            return None
        
        if not self.process or self.process.poll() is not None:
            self._notify("Container must be running to exec commands")
            return None
        
        try:
            # Use nsenter to enter container namespaces
            nsenter_cmd = ["nsenter"]
            
            # Enter all namespaces of the container process
            nsenter_cmd.extend(["-t", str(self.process.pid)])
            nsenter_cmd.extend(["-m", "-u", "-i", "-p", "-n"])  # mount, UTS, IPC, PID, network
            
            # Add chroot
            nsenter_cmd.extend(["chroot", self.rootfs_path])
            
            # Add command
            if interactive:
                nsenter_cmd.extend(["/bin/sh", "-c", command])
            else:
                nsenter_cmd.extend(["/bin/sh", "-c", command])
            
            # Execute
            result = subprocess.run(nsenter_cmd, capture_output=True, text=True, timeout=30)
            return result
        except Exception as e:
            self._notify(f"Error executing command: {e}")
            return None
    
    def _notify(self, msg, status=None):
        print(f"[{self.container_id[:12]}] [{self.name}] {msg}")
        try:
            with open(self.log_file, 'a') as f:
                f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        except:
            pass
        if self.ui_callback:
            self.ui_callback(self.name, msg, status if status is not None else self.status)
