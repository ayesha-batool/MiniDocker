# 🐳 Mini Docker

> **A lightweight, educational containerization platform inspired by Docker**

A simplified containerization system that demonstrates core Docker principles including process isolation, filesystem isolation, resource limiting, and container lifecycle management. Perfect for learning how containers work internally.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Problem Statement & Research](#problem-statement--research)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Web Dashboard](#web-dashboard)
  - [CLI Commands](#cli-commands)
- [Usage Guide & Examples](USAGE_GUIDE.md) - **📖 Complete guide with demo commands, volume mounts, env vars, and explanations**
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)

---

## 🎯 Overview

Mini Docker is an educational containerization system that implements the core features of Docker in a simplified, understandable way. It demonstrates:

- **Container Isolation** using Linux namespaces (PID, Mount, UTS)
- **Filesystem Isolation** using chroot
- **Resource Limiting** using cgroups (Memory, CPU)
- **Volume Mounting** using bind mounts
- **Container Lifecycle Management** with persistence
- **Logging System** for container output
- **Web & GUI Interfaces** for container management

---

## 📚 Problem Statement & Research

### Problem Identification

Containerization has transformed software development, but existing solutions (Docker, Podman, LXC) present challenges:

1. **Complexity**: Docker has 100+ commands and complex configuration
2. **Abstraction**: Internal mechanisms are hidden, making learning difficult
3. **Resource Overhead**: Full Docker installations require significant resources
4. **Educational Gap**: No lightweight tools that balance simplicity with functionality

### Research-Based Solution

This project addresses these challenges by:

- **Transparent Implementation**: Code demonstrates containerization internals
- **Simplified Architecture**: Core features without unnecessary complexity
- **Educational Focus**: Designed for learning, not production use
- **Cross-Platform**: Works on Linux and Windows (with WSL)

### Technology Choices

- **Backend**: Python 3.7+ (system programming, cross-platform)
- **Web Framework**: Flask (lightweight, easy to understand)
- **Frontend**: HTML/CSS/JavaScript (no build step, accessible)
- **Isolation**: Linux namespaces via `unshare` command
- **Resources**: cgroups for CPU and memory limits
- **Platform Support**: WSL integration for Windows

---

## ✨ Features

### Core Features

1. **Container Isolation** 🔒
   - Process ID namespace isolation
   - Mount namespace for filesystem isolation
   - UTS namespace for hostname isolation
   - Uses `unshare` command for namespace creation

2. **Process Management** ⚙️
   - Start, stop, pause, resume, and restart containers
   - Graceful shutdown with SIGTERM/SIGKILL
   - Process monitoring and status tracking

3. **File System Isolation** 📁
   - Each container has its own rootfs directory
   - Uses `chroot` to isolate filesystem
   - Rootfs structure: `bin/`, `etc/`, `usr/`, `lib/`, etc.

4. **Resource Limiting** 📊
   - Memory limits via cgroups
   - CPU limits via cgroups
   - Automatic resource monitoring

5. **Platform Support** 💻
   - Native Linux support with full features
   - Windows with WSL support
   - Fallback simulation mode for Windows without WSL

### Advanced Features

6. **Container IDs & Naming** 🏷️
   - Unique 12-character container IDs (UUID-based)
   - Containers can be referenced by ID or name

7. **Logging System** 📝
   - All stdout/stderr redirected to log files
   - Logs stored in `./containers/<name>/container.log`
   - View logs via CLI, GUI, or web dashboard

8. **Volume Mounting** 💾
   - Bind mount support: `host_path:container_path`
   - Persistent data sharing between host and container
   - Automatic mount/unmount on container lifecycle

9. **Environment Variables** 🌍
   - Pass environment variables to containers
   - Format: `KEY=VALUE`
   - Configured via dashboard or CLI

10. **Container Persistence** 💿
    - Container metadata stored in JSON
    - Tracks: ID, name, status, PID, created_at, volumes, env_vars
    - Persists across application restarts

11. **Health Checks** 🏥
    - Periodic command execution
    - Configurable interval, timeout, and retries
    - Health status tracking

12. **Auto-Restart Policies** 🔄
    - `no`, `always`, `on-failure`, `unless-stopped`
    - Automatic container restart on failure

13. **Networking** 🌐
    - Port mapping (host:container)
    - Bridge network simulation
    - Port management

14. **Container Templates** 📄
    - YAML/JSON configuration files
    - Reusable container definitions
    - Support for volumes, env vars, health checks

15. **Metrics & Monitoring** 📈
    - CPU usage percentage
    - Memory usage
    - Network I/O
    - Disk I/O
    - Real-time updates

---

## 📦 Requirements

### System Requirements

- **Linux**: Full support with all features
- **Windows**: Requires WSL (Windows Subsystem for Linux) for full features
- **macOS**: Limited support (simulation mode)

### Software Requirements

- Python 3.7+
- Required Python packages:
  - `psutil` - Process and system utilities
  - `Flask` - Web framework
  - `flask-socketio` - WebSocket support for real-time updates

### Linux-Specific Requirements

For full containerization features on Linux:
- `unshare` command (part of util-linux)
- cgroups support (usually available by default)
- Root/sudo access for some operations (namespaces, cgroups)

---

## 🚀 Installation

1. **Clone or download the project**
   ```bash
   cd "Mini Docker"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This installs:
   - `psutil` - Process and system utilities
   - `Flask` - Web framework
   - `flask-socketio` - WebSocket support
   - `python-socketio` - Socket.IO client
   - `eventlet` - Async networking library

3. **Start the web server**
   ```bash
   python main.py
   ```

4. **Open in browser**
   Navigate to: **http://localhost:5000**

### WSL Setup for Windows

Mini Docker requires WSL for full features on Windows:

1. **Install WSL**:
   ```powershell
   wsl --install
   ```
   Restart your computer if prompted.

2. **Install util-linux in WSL**:
   ```bash
   wsl sudo apt-get update
   wsl sudo apt-get install util-linux
   ```

3. **Verify Installation**:
   ```powershell
   wsl unshare --version
   python test_wsl.py
   ```

---

## 📖 Usage

### Web Dashboard

Launch the web dashboard:

```bash
python main.py
```

Then open your browser to: **http://localhost:5000**

#### Creating a Container

1. Click on the "➕ Create Container" tab
2. Fill in container details:
   - **Container Name**: Unique name for your container
   - **Command**: Command to run in the container
   - **Memory Limit**: Memory limit in MB
   - **CPU Limit**: CPU limit percentage
3. (Optional) Click "⚙️ Advanced Options" to configure:
   - **Volumes**: Add volume mounts (one per line)
     ```
     /host/data:/container/data
     /host/logs:/var/log
     ```
   - **Environment Variables**: Add env vars (one per line)
     ```
     DB_HOST=localhost
     MODE=production
     ```
4. Click "Create Container"
5. Select container and click "▶️ Start"

#### Container Management

- **▶️ Start**: Start selected containers
- **⏹️ Stop**: Stop selected containers
- **⏸️ Pause**: Pause running containers
- **▶️ Resume**: Resume paused containers
- **🔄 Restart**: Restart containers
- **📄 View Logs**: View container logs in modal window
- **📁 Open Rootfs**: Get container rootfs folder path
- **🗑️ Delete**: Delete containers

#### Features

- ✨ Modern web-based UI with HTML, CSS, and JavaScript
- 🔄 Real-time updates via WebSockets
- 📊 Container management (create, start, stop, pause, resume, restart, delete)
- 📈 Resource monitoring (CPU, memory, uptime)
- 📄 Log viewing in modal window
- ✅ Multi-container selection
- 🎨 Color-coded status indicators

#### Creating a Container (Web)

1. Click on the "➕ Create Container" tab
2. Fill in container details:
   - Container Name
   - Command
   - Memory Limit (MB)
   - CPU Limit (%)
3. (Optional) Click "⚙️ Advanced Options" for volumes and env vars
4. Click "Create Container"

### CLI Commands

Use the command-line interface:

```bash
python mini_docker_cli.py <command> [options]
```

#### List Containers

```bash
# List running containers
python mini_docker_cli.py ps

# List all containers (including stopped)
python mini_docker_cli.py ps -a
```

#### Stop Container

```bash
python mini_docker_cli.py stop <container_id|name>
```

#### Remove Container

```bash
# Remove container
python mini_docker_cli.py rm <container_id|name>

# Force remove running container
python mini_docker_cli.py rm -f <container_id|name>
```

#### View Logs

```bash
# View all logs
python mini_docker_cli.py logs <container_id|name>

# View last N lines
python mini_docker_cli.py logs <container_id|name> --tail 50
```

#### Inspect Container

```bash
python mini_docker_cli.py inspect <container_id|name>
```

---

## 🏗️ Architecture

### Core Components

1. **SimulatedContainer** (`container.py`)
   - Main container class
   - Handles isolation, resource limiting, lifecycle
   - Manages volumes, environment variables, logging

2. **ContainerManager** (`container_manager.py`)
   - Manages container metadata
   - Handles persistence (JSON storage)
   - Generates container IDs
   - Provides container lookup and listing

3. **FileSystemManager** (`filesystem.py`)
   - Manages rootfs creation
   - Handles image loading and storage
   - Provides filesystem operations

4. **Web Server** (`web_server.py`)
   - Flask backend with REST API
   - WebSocket support for real-time updates
   - Serves web dashboard (HTML/CSS/JavaScript)

5. **Mini Docker CLI** (`mini_docker_cli.py`)
   - Command-line interface
   - Container lifecycle commands

### Container Isolation

```
┌─────────────────────────────────────┐
│         Host System                 │
│  ┌───────────────────────────────┐  │
│  │   Mini Docker                │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Container (Namespace)  │  │  │
│  │  │  - PID namespace        │  │  │
│  │  │  - Mount namespace      │  │  │
│  │  │  - UTS namespace        │  │  │
│  │  │  - chroot (rootfs)     │  │  │
│  │  │  - cgroup (resources)  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

### Data Flow

```
User Input → Dashboard/CLI → ContainerManager → SimulatedContainer
                                                      ↓
                                            Linux Namespaces + chroot
                                                      ↓
                                            Container Process
                                                      ↓
                                            Logs → container.log
```

---

## 🔌 API Documentation

### REST API Endpoints

#### GET Endpoints

| Endpoint | Description | Response |
|----------|-------------|----------|
| `/` | Main dashboard page | HTML template |
| `/api/health` | Health check | JSON status |
| `/api/containers` | Get all containers | JSON array |
| `/api/containers/<name>/logs` | Get container logs | JSON with logs |

#### POST Endpoints

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/api/containers` | Create container | `{name, command, mem_limit, cpu_limit, volumes, env_vars}` |
| `/api/containers/<name>/start` | Start container | None |
| `/api/containers/<name>/stop` | Stop container | None |
| `/api/containers/<name>/pause` | Pause container | None |
| `/api/containers/<name>/resume` | Resume container | None |
| `/api/containers/<name>/restart` | Restart container | None |
| `/api/containers/<name>/rootfs` | Open rootfs | None |

#### DELETE Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/containers/<name>` | Delete container |

### WebSocket Events

#### Server → Client

- `container_created` - Emitted when a container is created
- `container_updated` - Emitted when container status changes
- `container_deleted` - Emitted when a container is deleted
- `status_update` - Real-time status updates (every 2 seconds)
- `log_update` - Real-time log updates

### Example API Usage

#### Create Container

```bash
curl -X POST http://localhost:5000/api/containers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-container",
    "command": "python -c \"print('Hello')\"",
    "mem_limit": 100,
    "cpu_limit": 50
  }'
```

#### Start Container

```bash
curl -X POST http://localhost:5000/api/containers/my-container/start
```

#### Get All Containers

```bash
curl http://localhost:5000/api/containers
```

---

## 💡 Examples

### Example 1: Simple Container

```bash
# Via Dashboard:
# Name: hello
# Command: echo "Hello from container!"
# Memory: 50 MB
# CPU: 30%
```

### Example 2: Container with Volume

```bash
# Via Dashboard:
# Name: data-processor
# Command: python process_data.py
# Advanced Options:
#   Volumes: /host/data:/app/data
#   Env Vars: MODE=production
```

### Example 3: Long-Running Service

```bash
# Via Dashboard:
# Name: web-server
# Command: python -m http.server 8000
# Memory: 100 MB
# CPU: 50%
# Advanced Options:
#   Env Vars: PORT=8000
```

### Example 4: Using CLI

```bash
# List all containers
python mini_docker_cli.py ps -a

# View logs
python mini_docker_cli.py logs web-server

# Inspect container
python mini_docker_cli.py inspect web-server

# Stop and remove
python mini_docker_cli.py stop web-server
python mini_docker_cli.py rm web-server
```

### Example 5: Container from Config File

Create `my-container.yaml`:
```yaml
name: webserver
command: python -m http.server 8080
mem_limit_mb: 200
cpu_limit_percent: 50
ports:
  - "8080:8080"
volumes:
  - "./data:/app/data"
env_vars:
  MODE: production
restart_policy: always
```

Load and create:
```python
from config_loader import ContainerConfigLoader
config = ContainerConfigLoader.load_config("my-container.yaml")
# Use config to create container via dashboard or API
```

---

## 📂 Project Structure

```
Mini Docker/
├── main.py                 # Entry point (Flask web server)
├── container.py            # Container implementation
├── container_manager.py    # Container metadata management
├── filesystem.py           # Filesystem and image management
├── web_server.py          # Flask backend server
├── mini_docker_cli.py      # CLI tool
├── config_loader.py        # YAML/JSON config loader
├── networking.py           # Networking support
├── utils.py               # Utility functions
├── test_wsl.py            # WSL test script
├── requirements.txt       # Python dependencies
├── containers/            # Container rootfs directories
│   └── <name>/
│       └── rootfs/
├── containers_meta/       # Container metadata (JSON)
│   └── containers.json
├── images/                # Container images
├── volumes/               # Volume mounts
├── templates/             # Flask HTML templates
│   └── index.html
├── static/                # Flask static files
│   ├── style.css
│   └── app.js
├── example_config.yaml    # Example YAML config
├── example_config.json    # Example JSON config
└── README.md             # This file
```

---

## 🗺️ Roadmap

### ✅ Implemented Features

- ✅ Container isolation (namespaces, chroot)
- ✅ Resource limiting (cgroups)
- ✅ Volume mounting
- ✅ Environment variables
- ✅ Logging system
- ✅ Container lifecycle management
- ✅ Container persistence
- ✅ WSL integration
- ✅ Health checks
- ✅ Auto-restart policies
- ✅ Basic networking (port mapping)
- ✅ Container templates (YAML/JSON)
- ✅ Metrics monitoring
- ✅ GUI dashboard (Tkinter)
- ✅ Web dashboard (Flask)
- ✅ CLI interface

### 🚀 Planned Features

1. **Docker Compose Support** - Multi-container applications
2. **Container Exec** - Interactive shell access
3. **Enhanced Networking Dashboard** - Visual network topology
4. **Resource Monitoring Graphs** - Real-time metrics visualization
5. **Image Registry** - Local image storage and sharing
6. **Container Snapshots** - Checkpoint/restore functionality
7. **Security Enhancements** - Basic security sandboxing

---

## 🔧 Implementation Details

### Namespaces

- **PID Namespace**: Isolates process IDs
  ```bash
  unshare --pid --fork
  ```

- **Mount Namespace**: Isolates filesystem mounts
  ```bash
  unshare --mount
  ```

- **UTS Namespace**: Isolates hostname
  ```bash
  unshare --uts
  ```

### Resource Limiting

- **Memory**: `/sys/fs/cgroup/memory/<name>/memory.limit_in_bytes`
- **CPU**: `/sys/fs/cgroup/cpu/<name>/cpu.shares`

### Volume Mounting

- Uses Linux `mount --bind` for bind mounts
- Format: `mount --bind /host/path /container/path`
- Automatically unmounted on container stop

### Logging

- All stdout/stderr redirected to `container.log`
- Logs include timestamps and container metadata
- Accessible via dashboard, CLI, or API

---

## 🎓 Educational Value

This project demonstrates:

1. **Containerization Principles**: How containers provide isolation
2. **Linux Namespaces**: Process, mount, and UTS namespaces
3. **chroot**: Filesystem isolation technique
4. **cgroups**: Resource limiting mechanism
5. **Bind Mounts**: Volume mounting implementation
6. **Container Lifecycle**: Start, stop, pause, resume operations
7. **Web Development**: Flask backend, REST API, WebSockets
8. **System Programming**: Process management, namespace manipulation

---

## ⚠️ Limitations

- **Security**: This is an educational project, not production-ready
- **Networking**: Basic networking only (no bridge networks)
- **Images**: Simplified image system (no layers)
- **Windows**: Requires WSL for full features
- **Root Access**: Some operations may require sudo on Linux

---

## 🤝 Contributing

This is an educational project. Feel free to:
- Report issues
- Suggest improvements
- Add features
- Improve documentation

---

## 📝 License

Educational project - use freely for learning purposes.

---

## 🙏 Acknowledgments

Inspired by Docker and containerization technologies. Built for educational purposes to understand container internals.

---

**Note**: This is a simplified containerization system for educational purposes. For production use, please use Docker or other production-grade containerization tools.
