from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time
import os
import platform
from container import SimulatedContainer
from filesystem import FileSystemManager
from container_manager import ContainerManager

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mini-docker-secret-key-2024'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Initialize SocketIO for real-time updates
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Initialize managers
fs = FileSystemManager()
manager = ContainerManager()
containers = {}

def get_container_status(container):
    """Get current status of a container"""
    if not container:
        return {"status": "Unknown", "pid": "-", "uptime": "0s", "cpu": "0.0%", "memory": "0MB"}
    
    pid = str(container.process.pid) if container.process and container.process.poll() is None else "-"
    
    uptime = "0s"
    if container.start_time:
        elapsed = int(time.time() - container.start_time)
        if elapsed < 60:
            uptime = f"{elapsed}s"
        elif elapsed < 3600:
            uptime = f"{elapsed//60}m {elapsed%60}s"
        else:
            uptime = f"{elapsed//3600}h {(elapsed%3600)//60}m"
    
    cpu_percent = "0.0%"
    memory_usage = "0MB"
    if container.process and container.process.poll() is None:
        try:
            import psutil
            proc = psutil.Process(container.process.pid)
            cpu_percent = f"{proc.cpu_percent(interval=0.1):.1f}%"
            memory_usage = f"{proc.memory_info().rss / (1024*1024):.1f}MB"
        except:
            pass
    
    last_started = "Never"
    if hasattr(container, 'last_started') and container.last_started:
        elapsed = int(time.time() - container.last_started)
        if elapsed < 60:
            last_started = f"{elapsed}s ago"
        elif elapsed < 3600:
            last_started = f"{elapsed//60}m ago"
        elif elapsed < 86400:
            last_started = f"{elapsed//3600}h ago"
        else:
            days = elapsed // 86400
            last_started = f"{days}d ago"
    
    # Get latest log
    latest_log = "Ready"
    try:
        if os.path.exists(container.log_file):
            with open(container.log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    for line in reversed(lines):
                        line = line.strip()
                        if line and not line.startswith("==="):
                            if "] " in line:
                                latest_log = line.split("] ", 1)[1]
                            else:
                                latest_log = line
                            break
                    if len(latest_log) > 50:
                        latest_log = latest_log[:47] + "..."
    except:
        pass
    
    return {
        "status": container.status,
        "pid": pid,
        "uptime": uptime,
        "cpu": cpu_percent,
        "memory": memory_usage,
        "last_started": last_started,
        "latest_log": latest_log
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/containers', methods=['GET'])
def get_containers():
    """Get list of all containers"""
    container_list = []
    for name, container in containers.items():
        meta = manager.get_container_by_name(name)
        if meta:
            status_info = get_container_status(container)
            container_list.append({
                "id": container.container_id[:12],
                "name": name,
                "command": container.command[:40] + "..." if len(container.command) > 40 else container.command,
                "status": status_info["status"],
                "pid": status_info["pid"],
                "uptime": status_info["uptime"],
                "resources": f"{container.mem_limit_mb}MB/{container.cpu_limit_percent}%",
                "cpu": status_info["cpu"],
                "last_started": status_info["last_started"],
                "latest_log": status_info["latest_log"]
            })
    return jsonify(container_list)

@app.route('/api/containers', methods=['POST'])
def create_container():
    """Create a new container"""
    data = request.json
    name = data.get('name')
    command = data.get('command')
    mem_limit = int(data.get('mem_limit', 100))
    cpu_limit = int(data.get('cpu_limit', 50))
    volumes = data.get('volumes', [])
    env_vars = data.get('env_vars', {})
    
    if not name or not command:
        return jsonify({"error": "Name and command are required"}), 400
    
    existing = manager.get_container_by_name(name)
    if existing or name in containers:
        return jsonify({"error": f"Container '{name}' already exists"}), 400
    
    try:
        container_id = manager.create_container(
            name=name,
            command=command,
            mem_limit=mem_limit,
            cpu_limit=cpu_limit,
            volumes=volumes,
            env_vars=env_vars
        )
        
        meta = manager.get_container(container_id)
        rootfs_path = fs.create_rootfs(name)
        
        container = SimulatedContainer(
            container_id=container_id,
            name=name,
            command=command,
            rootfs_path=rootfs_path,
            mem_limit_mb=mem_limit,
            cpu_limit_percent=cpu_limit,
            volumes=volumes,
            env_vars=env_vars,
            log_file=meta["log_file"],
            ui_callback=lambda n, m, s=None: socketio.emit('log_update', {'name': n, 'message': m, 'status': s})
        )
        container.status = "Created"
        container.last_started = None
        containers[name] = container
        
        socketio.emit('container_created', {'name': name})
        return jsonify({"success": True, "id": container_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/containers/<name>/start', methods=['POST'])
def start_container(name):
    """Start a container"""
    if name not in containers:
        return jsonify({"error": "Container not found"}), 404
    
    container = containers[name]
    
    # Start container in background and notify after it actually starts
    def start_and_notify():
        try:
            container.run()
            container.last_started = time.time()
            
            # Wait a moment to verify container actually started
            time.sleep(0.8)
            
            # Check if container is running
            if container.status == "Running" and container.process and container.process.poll() is None:
                socketio.emit('container_started', {
                    'name': name,
                    'message': f'Container "{name}" started successfully!',
                    'status': 'success'
                })
            else:
                socketio.emit('container_started', {
                    'name': name,
                    'message': f'Container "{name}" failed to start',
                    'status': 'error'
                })
            
            socketio.emit('container_updated', {'name': name})
        except Exception as e:
            socketio.emit('container_started', {
                'name': name,
                'message': f'Error starting container: {str(e)}',
                'status': 'error'
            })
    
    # Start in background thread
    threading.Thread(target=start_and_notify, daemon=True).start()
    
    return jsonify({"success": True, "message": "Starting container..."})

@app.route('/api/containers/<name>/stop', methods=['POST'])
def stop_container(name):
    """Stop a container"""
    if name not in containers:
        return jsonify({"error": "Container not found"}), 404
    
    container = containers[name]
    container.stop()
    socketio.emit('container_updated', {'name': name})
    return jsonify({"success": True})

@app.route('/api/containers/<name>/pause', methods=['POST'])
def pause_container(name):
    """Pause a container"""
    if name not in containers:
        return jsonify({"error": "Container not found"}), 404
    
    container = containers[name]
    container.pause()
    socketio.emit('container_updated', {'name': name})
    return jsonify({"success": True})

@app.route('/api/containers/<name>/resume', methods=['POST'])
def resume_container(name):
    """Resume a container"""
    if name not in containers:
        return jsonify({"error": "Container not found"}), 404
    
    container = containers[name]
    container.resume()
    socketio.emit('container_updated', {'name': name})
    return jsonify({"success": True})

@app.route('/api/containers/<name>/restart', methods=['POST'])
def restart_container(name):
    """Restart a container"""
    if name not in containers:
        return jsonify({"error": "Container not found"}), 404
    
    container = containers[name]
    container.restart()
    container.last_started = time.time()
    socketio.emit('container_updated', {'name': name})
    return jsonify({"success": True})

@app.route('/api/containers/<name>', methods=['DELETE'])
def delete_container(name):
    """Delete a container"""
    # Decode URL-encoded container name
    from urllib.parse import unquote
    name = unquote(name)
    
    # Stop container if it's running
    if name in containers:
        container = containers[name]
        container.stop()
        del containers[name]
    
    # Remove from JSON metadata (by name - more reliable)
    removed = manager.remove_container_by_name(name)
    if not removed:
        # Try to find and remove by ID if name lookup failed
        meta = manager.get_container_by_name(name)
        if meta:
            manager.remove_container(meta["id"])
    
    # Delete container filesystem
    try:
        fs.delete_rootfs(name)
    except Exception as e:
        print(f"Warning: Could not delete rootfs for {name}: {e}")
    
    socketio.emit('container_deleted', {'name': name})
    return jsonify({"success": True})

@app.route('/api/containers/<name>/logs', methods=['GET'])
def get_logs(name):
    """Get container logs"""
    # Decode URL-encoded container name
    from urllib.parse import unquote
    name = unquote(name)
    
    if name not in containers:
        return jsonify({"error": f"Container '{name}' not found"}), 404
    
    container = containers[name]
    tail = int(request.args.get('tail', 500))
    
    # Verify log file exists and belongs to this container
    if not os.path.exists(container.log_file):
        return jsonify({"logs": "No logs available yet"}), 200
    
    logs = container.get_logs(tail=tail)
    return jsonify({"logs": logs, "container_name": name, "log_file": container.log_file})

@app.route('/api/containers/<name>/rootfs', methods=['POST'])
def open_rootfs(name):
    """Open container rootfs in file explorer"""
    if name not in containers:
        return jsonify({"error": "Container not found"}), 404
    
    try:
        fs.open_rootfs(name)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def load_existing_containers():
    """Load existing containers on startup"""
    all_containers_meta = manager.list_containers(all_containers=True)
    for meta in all_containers_meta:
        name = meta["name"]
        if name not in containers:
            try:
                rootfs_path = fs.create_rootfs(name, image_name=None)
                container = SimulatedContainer(
                    container_id=meta["id"],
                    name=name,
                    command=meta["command"],
                    rootfs_path=rootfs_path,
                    mem_limit_mb=meta.get("mem_limit_mb", meta.get("mem_limit", 100)),
                    cpu_limit_percent=meta.get("cpu_limit_percent", meta.get("cpu_limit", 50)),
                    volumes=meta.get("volumes", []),
                    env_vars=meta.get("env_vars", {}),
                    log_file=meta.get("log_file"),
                    ui_callback=lambda n, m, s=None: socketio.emit('log_update', {'name': n, 'message': m, 'status': s})
                )
                container.status = meta.get("status", "Stopped")
                containers[name] = container
            except Exception as e:
                print(f"Error loading container {name}: {e}")

def background_update():
    """Background thread to update container status"""
    while True:
        time.sleep(1)
        for name, container in list(containers.items()):
            status_info = get_container_status(container)
            socketio.emit('status_update', {
                'name': name,
                'status': status_info
            })

if __name__ == '__main__':
    load_existing_containers()
    threading.Thread(target=background_update, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

