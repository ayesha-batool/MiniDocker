# Mini Docker - Failure Cases Documentation

## Overview

This document describes failure scenarios encountered during Mini Docker development, their root causes, kernel behavior, and how they were handled.

---

## Failure Case 1: Out-of-Memory (OOM) Kill

### What Failed
Container exceeded memory limit and was killed by the kernel OOM killer.

### Why It Failed
1. Container process allocated more memory than the cgroup limit
2. Kernel's OOM killer detected the violation
3. Process was terminated with SIGKILL

### How Kernel Behaved
```
[Kernel] OOM killer activated
[Kernel] Process <pid> killed (memory limit exceeded)
[Kernel] cgroup memory.oom_control: oom_kill = 1
```

### How It Was Handled
1. **Detection**: Monitor `memory.oom_control` (v1) or `memory.events` (v2)
2. **Alert**: Log OOM event and notify user
3. **Recovery**: Container status set to "Stopped"
4. **Restart Policy**: If `on-failure` or `always`, container can be restarted

### Code Implementation
```python
def _monitor_resource_violations(self):
    # Check for OOM kill
    oom_file = os.path.join(self.cgroup_path, "memory.events")
    with open(oom_file, 'r') as f:
        if "oom_kill" in f.read():
            self.oom_detected = True
            self._notify("ALERT: Out-of-memory (OOM) kill detected!")
```

### Prevention
- Set appropriate memory limits
- Monitor memory usage
- Use restart policies for automatic recovery

---

## Failure Case 2: CPU Throttling

### What Failed
Container exceeded CPU limit and was throttled by the kernel scheduler.

### Why It Failed
1. Container process consumed more CPU than allocated
2. cgroup CPU controller throttled the process
3. Process execution was paused periodically

### How Kernel Behaved
```
[Kernel] CPU throttling activated for cgroup
[Kernel] Process <pid> throttled (CPU limit exceeded)
[Kernel] cgroup cpu.stat: nr_throttled = <count>
```

### How It Was Handled
1. **Detection**: Monitor `cpu.stat` for throttling events
2. **Alert**: Log throttling count and notify user
3. **Monitoring**: Track throttling frequency
4. **Adjustment**: User can increase CPU limit if needed

### Code Implementation
```python
def _monitor_resource_violations(self):
    cpu_stat_file = os.path.join(self.cgroup_path, "cpu.stat")
    with open(cpu_stat_file, 'r') as f:
        for line in f:
            if 'throttled' in line:
                throttled_count = int(line.split()[-1])
                if throttled_count > 0:
                    self._notify(f"ALERT: CPU throttling detected!")
```

### Prevention
- Set appropriate CPU limits
- Monitor CPU usage
- Adjust limits based on workload

---

## Failure Case 3: Network Namespace Creation Failure

### What Failed
Failed to create network namespace for container.

### Why It Failed
1. Insufficient permissions (requires root or CAP_NET_ADMIN)
2. Network namespace limit reached
3. System resource exhaustion

### How Kernel Behaved
```
[Kernel] Failed to create network namespace
[Kernel] Error: Operation not permitted (if not root)
[Kernel] Error: Too many namespaces (if limit reached)
```

### How It Was Handled
1. **Error Detection**: Catch subprocess errors
2. **Fallback**: Continue without network namespace (simulation mode)
3. **Logging**: Log error for debugging
4. **User Notification**: Inform user of limitation

### Code Implementation
```python
def setup_network_namespace(self, container_name):
    try:
        result = subprocess.run(["ip", "netns", "add", netns_name], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[Network] Failed to create namespace: {result.stderr}")
            return False
    except Exception as e:
        print(f"[Network] Error: {e}")
        return False
```

### Prevention
- Run with appropriate permissions
- Monitor namespace usage
- Handle errors gracefully

---

## Failure Case 4: User Namespace Mapping Failure

### What Failed
Failed to write UID/GID maps for user namespace.

### Why It Failed
1. `/proc/[pid]/uid_map` can only be written once
2. Insufficient permissions
3. Invalid UID/GID values

### How Kernel Behaved
```
[Kernel] Failed to write uid_map: Operation not permitted
[Kernel] Failed to write uid_map: Invalid argument
```

### How It Was Handled
1. **Error Detection**: Catch IOError when writing maps
2. **Graceful Degradation**: Continue without user namespace mapping
3. **Warning**: Log warning but don't fail container creation
4. **Documentation**: Document requirement for proper setup

### Code Implementation
```python
def _setup_user_namespace_mapping(self):
    try:
        with open(uid_map_path, 'w') as f:
            f.write(f"0 {host_uid} 1\n")
    except (IOError, PermissionError) as e:
        self._notify(f"Warning: Could not setup user namespace mapping: {e}")
        # Continue without mapping
```

### Prevention
- Ensure proper permissions
- Write maps before process starts
- Validate UID/GID values

---

## Failure Case 5: OverlayFS Mount Failure

### What Failed
Failed to mount OverlayFS for container.

### Why It Failed
1. OverlayFS not supported in kernel
2. Insufficient permissions
3. Invalid mount options
4. Filesystem errors

### How Kernel Behaved
```
[Kernel] mount: overlay filesystem not supported
[Kernel] mount: Operation not permitted
[Kernel] mount: Invalid argument
```

### How It Was Handled
1. **Error Detection**: Check mount command return code
2. **Fallback**: Use regular rootfs (copy instead of overlay)
3. **Logging**: Log error for debugging
4. **User Notification**: Inform user of fallback

### Code Implementation
```python
def _create_overlay_rootfs(self, name, image_name, container_dir):
    try:
        result = subprocess.run(mount_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"[OverlayFS] Failed to mount: {result.stderr}")
            # Fallback to regular rootfs
            return self.create_rootfs(name, image_name, use_overlay=False)
    except Exception as e:
        print(f"[OverlayFS] Error: {e}")
        return self.create_rootfs(name, image_name, use_overlay=False)
```

### Prevention
- Check kernel support for OverlayFS
- Ensure proper permissions
- Validate mount options
- Handle errors gracefully

---

## Common Patterns

### 1. Graceful Degradation
When a feature fails, fall back to a simpler implementation rather than failing completely.

### 2. Error Logging
Always log errors with context for debugging.

### 3. User Notification
Inform users of failures and limitations.

### 4. Resource Monitoring
Monitor resources to prevent failures before they occur.

### 5. Permission Handling
Handle permission errors gracefully and provide clear messages.

---

## Lessons Learned

1. **Always have fallbacks**: Not all systems support all features
2. **Monitor resources**: Prevent failures before they occur
3. **Handle errors gracefully**: Don't crash on non-critical failures
4. **Document limitations**: Users should know what works and what doesn't
5. **Test edge cases**: Failure scenarios reveal important issues

---

**Last Updated**: 2026-01-06

