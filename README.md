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
- [Usage Guide & Examples](#usage-guide--examples)
- [Architecture & Design Report](#architecture--design-report)
- [Comparative Analysis](#comparative-analysis)
- [Security Documentation](#security-documentation)
- [Failure Cases](#failure-cases)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Quick Reference](#quick-reference)
- [GitHub Setup](#github-setup)
- [Contributing](#contributing)

---

## 🎯 Overview

Mini Docker is an educational containerization system that implements the core features of Docker in a simplified, understandable way. It demonstrates:

- **Container Isolation** using Linux namespaces (PID, Mount, UTS, User, IPC, Network)
- **Filesystem Isolation** using chroot and OverlayFS
- **Resource Limiting** using cgroups (Memory, CPU) - v1 and v2 support
- **Volume Mounting** using bind mounts
- **Container Lifecycle Management** with persistence
- **Logging System** for container output
- **Web Dashboard** for container management
- **Security Features** including user namespaces, capability dropping, and Seccomp filters

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
- **Cross-Platform**: Works on Linux and Windows (simulation mode)

### Technology Choices

- **Backend**: Python 3.7+ (system programming, cross-platform)
- **Web Framework**: Flask (lightweight, easy to understand)
- **Frontend**: HTML/CSS/JavaScript (no build step, accessible)
- **Isolation**: Linux namespaces via `unshare` command
- **Resources**: cgroups for CPU and memory limits (v1 and v2)
- **Platform Support**: Windows simulation mode for development

---

## ✨ Features

### Core Features

1. **Container Isolation** 🔒
   - Process ID namespace isolation
   - Mount namespace for filesystem isolation
   - UTS namespace for hostname isolation
   - User namespace for non-root execution
   - IPC namespace for shared memory isolation
   - Network namespace for network isolation
   - Uses `unshare` command for namespace creation

2. **Process Management** ⚙️
   - Start, stop, pause, resume, and restart containers
   - Graceful shutdown with SIGTERM/SIGKILL
   - Process monitoring and status tracking
   - Container exec for interactive process injection
   - Zombie process handling (init-like behavior)

3. **File System Isolation** 📁
   - Each container has its own rootfs directory
   - Uses `chroot` to isolate filesystem
   - OverlayFS support for read-only base images + writable layers
   - Read-only rootfs mode (optional)
   - Rootfs structure: `bin/`, `etc/`, `usr/`, `lib/`, etc.

4. **Resource Limiting** 📊
   - Memory limits via cgroups (v1 and v2)
   - CPU limits via cgroups (v1 and v2)
   - Automatic resource monitoring
   - OOM kill detection and alerts
   - CPU throttling detection

5. **Platform Support** 💻
   - Native Linux support with full features
   - Windows simulation mode (no WSL required)
   - Graceful fallback for unsupported features

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
    - Network namespace isolation
    - veth pairs for container networking
    - Bridge network for host-container communication
    - Port collision detection

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

16. **Security Features** 🔐
    - User namespace mapping (non-root containers)
    - Seccomp filters (planned)
    - Capability dropping (planned)
    - Read-only rootfs option

17. **Observability** 👁️
    - System call tracing (strace) support
    - Resource violation alerts
    - Timeline view for container lifecycle
    - Container lifecycle events

---

## 📦 Requirements

### System Requirements

- **Linux**: Full support with all features
- **Windows**: Simulation mode (no WSL required)
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

## 📖 Usage Guide & Examples

### Demo Commands

#### 1. **Simple Print Command**
```
python -c "print('Hello from Mini Docker!')"
```
**What it does:** Prints a message and exits immediately.

#### 2. **Python Script with Sleep**
```
python -c "print('Starting...'); import time; time.sleep(5); print('Done!')"
```
**What it does:** Prints a message, waits 5 seconds, then prints another message.

#### 3. **Python Calculator**
```
python -c "result = 2 + 2; print(f'2 + 2 = {result}')"
```
**What it does:** Performs a calculation and prints the result.

#### 4. **List Directory Contents**
```
python -c "import os; print('\n'.join(os.listdir('.')))"
```
**What it does:** Lists all files and directories in the current directory.

#### 5. **Simple Web Server**
```
python -m http.server 8000
```
**What it does:** Starts a web server on port 8000. **Note:** This will run indefinitely until stopped.

#### 6. **Count Numbers**
```
python -c "for i in range(1, 11): print(f'Number {i}')"
```
**What it does:** Prints numbers from 1 to 10.

#### 7. **File Operations**
```
python -c "with open('test.txt', 'w') as f: f.write('Hello World'); print('File created!')"
```
**What it does:** Creates a file called `test.txt` with "Hello World" content.

#### 8. **Environment Check**
```
python -c "import os; print(f'Current directory: {os.getcwd()}'); print(f'Python version: {os.sys.version}')"
```
**What it does:** Shows current directory and Python version.

#### 9. **Simple Loop with Delay**
```
python -c "import time; [print(f'Tick {i}') or time.sleep(1) for i in range(5)]"
```
**What it does:** Prints "Tick 0" through "Tick 4" with 1 second delay between each.

#### 10. **JSON Processing**
```
python -c "import json; data = {'name': 'Mini Docker', 'version': '1.0'}; print(json.dumps(data, indent=2))"
```
**What it does:** Creates a JSON object and prints it in formatted form.

### Volume Mounts

#### What is a Volume Mount?

**Volume Mount** allows you to share files and directories between your host machine (your computer) and the container. It's like creating a bridge between two folders.

**Think of it like this:**
- **Host Path**: A folder on your computer (e.g., `C:\MyData`)
- **Container Path**: A folder inside the container (e.g., `/app/data`)
- **Volume Mount**: Connects these two folders so they share the same files

#### Why Use Volume Mounts?

1. **Persistent Data**: Data saved in a volume persists even after the container stops
2. **File Sharing**: Share files between your computer and the container
3. **Data Backup**: Easy to backup data from your host machine
4. **Development**: Edit files on your computer and see changes in the container

#### Demo Examples

**Example 1: Basic Volume Mount**
```
Host Path: C:\MyData
Container Path: /app/data
```
**Format:** `C:\MyData:/app/data`

**Example 2: Log Directory**
```
Host Path: C:\Logs
Container Path: /var/log
```
**Format:** `C:\Logs:/var/log`

**Example 3: Configuration Files**
```
Host Path: C:\Config
Container Path: /etc/config
```
**Format:** `C:\Config:/etc/config`

**Example 4: Project Directory**
```
Host Path: F:\Projects\MyApp
Container Path: /app
```
**Format:** `F:\Projects\MyApp:/app`

**Example 5: Database Data**
```
Host Path: C:\Database
Container Path: /data/db
```
**Format:** `C:\Database:/data/db`

### Environment Variables

#### What are Environment Variables?

**Environment Variables** are key-value pairs that provide configuration to your container. They're like settings that your application can read.

**Think of it like this:**
- **Key**: The name of the setting (e.g., `DATABASE_URL`)
- **Value**: The actual value (e.g., `localhost:5432`)
- **Usage**: Your application reads these variables to know how to behave

#### Why Use Environment Variables?

1. **Configuration**: Change app behavior without modifying code
2. **Secrets**: Store sensitive information (passwords, API keys)
3. **Flexibility**: Same code works in different environments
4. **Security**: Keep secrets out of your code

#### Demo Examples

**Example 1: Database Configuration**
```
Variable Name: DB_HOST
Variable Value: localhost
```
**Format:** `DB_HOST=localhost`

**In your Python code:**
```python
import os
db_host = os.environ.get('DB_HOST', 'default_host')
print(f'Connecting to database at {db_host}')
```

**Example 2: Application Mode**
```
Variable Name: MODE
Variable Value: production
```
**Format:** `MODE=production`

**In your Python code:**
```python
import os
mode = os.environ.get('MODE', 'development')  # Note: 'MODE' must be in quotes!
if mode == 'production':
    print('Running in production mode')
```

**⚠️ Important:** Always use quotes around the environment variable name:
- ✅ Correct: `os.environ.get('MODE')`
- ❌ Wrong: `os.environ.get(MODE)`  # This will cause NameError!

**Example 3: API Key**
```
Variable Name: API_KEY
Variable Value: abc123xyz789
```
**Format:** `API_KEY=abc123xyz789`

**Example 4: Port Number**
```
Variable Name: PORT
Variable Value: 8080
```
**Format:** `PORT=8080`

**Example 5: Debug Mode**
```
Variable Name: DEBUG
Variable Value: true
```
**Format:** `DEBUG=true`

### Resource Limits

#### Memory Limit

**What is Memory Limit?**

**Memory Limit** controls how much RAM (memory) your container can use. It prevents a container from using all available memory on your system.

**Units:** Megabytes (MB)

**How to Check Available Memory:**

1. **Windows (PowerShell):**
   ```powershell
   # Check total RAM
   (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
   
   # Check available RAM
   (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
   ```

2. **Linux/Mac:**
   ```bash
   # Check total and available memory
   free -h
   # or
   cat /proc/meminfo | grep MemAvailable
   ```

**Typical System Memory:**
- **4 GB RAM**: Limit containers to 100-500 MB each
- **8 GB RAM**: Limit containers to 200-1000 MB each
- **16 GB RAM**: Limit containers to 500-2000 MB each
- **32 GB+ RAM**: Limit containers to 1000-4000 MB each

**Recommendation:** 
- Reserve at least 2-4 GB for your operating system
- Don't allocate more than 70% of total RAM to all containers combined

**Examples:**
- **Small Container (50 MB)**: Simple scripts, text processing
- **Medium Container (100 MB)**: Web servers, small applications
- **Large Container (512 MB)**: Databases, large applications
- **Very Large Container (1024 MB = 1 GB)**: Heavy applications, machine learning

#### CPU Limit

**What is CPU Limit?**

**CPU Limit** controls how much CPU (processor) power your container can use. It's expressed as a percentage of total CPU capacity.

**Units:** Percentage (%)

**How to Check Available CPU:**

1. **Windows (PowerShell):**
   ```powershell
   # Check number of CPU cores
   (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
   ```

2. **Linux/Mac:**
   ```bash
   # Check number of CPU cores
   nproc
   # or
   lscpu | grep "^CPU(s):"
   ```

**Understanding CPU Limits:**
- **100% CPU Limit** = Full use of 1 CPU core
- **50% CPU Limit** = Half of 1 CPU core
- **200% CPU Limit** = Full use of 2 CPU cores (if available)

**Typical CPU Configurations:**
- **2 Cores**: Limit containers to 25-100% each
- **4 Cores**: Limit containers to 25-200% each
- **6 Cores**: Limit containers to 25-300% each
- **8+ Cores**: Limit containers to 25-400% each

**Recommendation:**
- Reserve at least 1-2 cores for your operating system
- Don't allocate more than 80% of total CPU capacity to all containers

**Examples:**
- **Low CPU (25%)**: Background tasks, scheduled jobs
- **Medium CPU (50%)**: Web servers, standard applications
- **High CPU (75%)**: Data processing, calculations
- **Maximum CPU (100%)**: Heavy computations, video encoding

### Rootfs Explained

**What is Rootfs?**

**Rootfs** (Root File System) is the container's isolated file system. It's like a separate hard drive for your container.

**Think of it like this:**
- Your computer has folders: `C:\`, `D:\`, etc.
- The container has its own root folder: `/` (rootfs)
- They are completely separate!

**Why Rootfs?**

1. **Isolation**: Container can't access your files (security)
2. **Clean Environment**: Each container starts fresh
3. **Portability**: Container works the same on any machine
4. **Reproducibility**: Same filesystem = same behavior

**Rootfs Structure:**
```
containers/
└── your-container-name/
    └── rootfs/
        ├── bin/          # Executable programs
        ├── etc/          # Configuration files
        ├── usr/          # User programs
        ├── lib/          # Libraries
        ├── tmp/          # Temporary files
        ├── var/          # Variable data
        ├── proc/         # Process information
        └── sys/          # System information
```

---

## 🏗️ Architecture & Design Report

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Dashboard (UI)                    │
│              (HTML/CSS/JavaScript + Flask)               │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│                  Flask Web Server                          │
│              (REST API + WebSocket)                        │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Container Manager                            │
│         (Metadata Persistence)                           │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│            SimulatedContainer Class                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Namespaces  │  │   cgroups    │  │  Filesystem  │  │
│  │  (PID, Mount,│  │  (Memory,    │  │  (chroot,    │  │
│  │   UTS, User, │  │   CPU)       │  │   OverlayFS) │  │
│  │   IPC, Net)  │  │              │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│              Linux Kernel                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Namespaces  │  │   cgroups    │  │  Filesystem   │  │
│  │  API         │  │   API        │  │  API          │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└──────────────────────────────────────────────────────────┘
```

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
   - OverlayFS support

4. **Web Server** (`web_server.py`)
   - Flask backend with REST API
   - WebSocket support for real-time updates
   - Serves web dashboard (HTML/CSS/JavaScript)

5. **Networking** (`networking.py`)
   - Network namespace management
   - veth pair creation
   - Bridge network setup
   - Port mapping

### Namespace Usage

#### Process ID (PID) Namespace
- **Purpose**: Isolate process trees
- **Implementation**: `unshare --pid`
- **Effect**: Container processes see only their own PID namespace

#### Mount Namespace
- **Purpose**: Isolate filesystem mounts
- **Implementation**: `unshare --mount`
- **Effect**: Container has isolated mount points

#### UTS Namespace
- **Purpose**: Isolate hostname
- **Implementation**: `unshare --uts`
- **Effect**: Container can have different hostname

#### User Namespace
- **Purpose**: Map container UIDs to host UIDs
- **Implementation**: `unshare --user` + `/proc/[pid]/uid_map`
- **Effect**: Container UID 0 maps to unprivileged host UID

#### IPC Namespace
- **Purpose**: Isolate IPC objects (shared memory, semaphores, message queues)
- **Implementation**: `unshare --ipc`
- **Effect**: IPC objects are isolated per container

#### Network Namespace
- **Purpose**: Isolate network stack
- **Implementation**: `ip netns add` + veth pairs
- **Effect**: Each container has isolated network interface

### cgroup Hierarchy

#### cgroups v1 Structure
```
/sys/fs/cgroup/
├── memory/
│   └── minidocker_<name>/
│       ├── memory.limit_in_bytes
│       └── cgroup.procs
└── cpu/
    └── minidocker_<name>/
        ├── cpu.shares
        └── cgroup.procs
```

#### cgroups v2 Structure (Unified Hierarchy)
```
/sys/fs/cgroup/
└── minidocker_<name>/
    ├── cgroup.controllers
    ├── cgroup.subtree_control
    ├── memory.max
    ├── cpu.max
    └── cgroup.procs
```

### Filesystem Isolation

#### chroot
- **Purpose**: Change root directory
- **Implementation**: `chroot <rootfs_path>`
- **Effect**: Container sees only its rootfs

#### Overlay Filesystem
- **Purpose**: Read-only base image + writable container layer
- **Structure**:
  - `lowerdir`: Base image (read-only)
  - `upperdir`: Container writable layer
  - `workdir`: OverlayFS work directory
  - `merged`: Final mount point
- **Implementation**: `mount -t overlay`
- **Effect**: Changes persist in upperdir, base remains read-only

### Trade-offs vs Docker

#### Advantages of Mini Docker
1. **Simplicity**: Easier to understand and learn
2. **Transparency**: Code shows how containers work internally
3. **Educational**: Designed for learning OS concepts
4. **Lightweight**: Minimal dependencies

#### Limitations vs Docker
1. **Security**: Less hardened (educational project)
2. **Features**: Missing many Docker features (layers, registry, etc.)
3. **Performance**: Not optimized for production
4. **Compatibility**: Not Docker-compatible
5. **Networking**: Simplified networking model

### Design Decisions

#### Why Python?
- Cross-platform support
- Easy to understand
- Good for educational purposes
- Rich standard library

#### Why Flask?
- Lightweight web framework
- Easy to understand
- Good for REST APIs
- WebSocket support via Flask-SocketIO

#### Why Web UI?
- Better user experience
- Real-time updates
- Easier to demonstrate features
- Modern interface

#### Why Both v1 and v2 cgroups?
- Compatibility with different Linux distributions
- Some systems still use v1
- v2 is the future, but v1 is still common
- Graceful fallback ensures compatibility

---

## 📊 Comparative Analysis

### Mini Docker vs Docker vs LXC vs Podman

| Feature | Mini Docker | Docker | LXC | Podman |
|---------|------------|--------|-----|--------|
| **Purpose** | Educational | Production | System containers | Rootless containers |
| **Complexity** | Simple | Complex | Moderate | Moderate |
| **Isolation** | Basic | Strong | Strong | Strong |
| **Security** | Basic | Advanced | Advanced | Advanced |
| **Performance** | Good | Excellent | Excellent | Excellent |
| **Ecosystem** | None | Large | Moderate | Docker-compatible |
| **Root Required** | Some ops | Daemon | Some ops | No (rootless) |
| **Image Layers** | Basic | Advanced | Advanced | Advanced |
| **Networking** | Basic | Advanced | Advanced | Advanced |
| **Orchestration** | None | Kubernetes | LXD | Kubernetes |

### When to Use Each

#### Use Mini Docker When:
- Learning container internals
- Understanding OS concepts
- Educational projects
- Prototyping simple containerization

#### Use Docker When:
- Production deployments
- CI/CD pipelines
- Microservices architecture
- Cloud-native applications
- Need Docker ecosystem

#### Use LXC When:
- System containers
- Full OS virtualization alternative
- Resource-intensive workloads
- Need lightweight VMs

#### Use Podman When:
- Rootless containers
- Security-focused deployments
- Docker-compatible alternative
- Kubernetes (CRI-O)
- Need daemonless architecture

### Summary

**Mini Docker** is designed for **education and learning**, not production. It demonstrates container concepts transparently but lacks the security, features, and performance optimizations of production tools.

**Docker** is the industry standard for application containers with a rich ecosystem.

**LXC** excels at system containers and lightweight virtualization.

**Podman** offers Docker compatibility with rootless, daemonless architecture.

Each tool serves different purposes, and Mini Docker fills the educational gap in understanding how containers work internally.

---

## 🔐 Security Documentation

### Implemented Security Features

1. **User Namespace Support**
   - Container UID 0 maps to unprivileged host UID
   - Prevents privilege escalation
   - Implementation: `/proc/[pid]/uid_map` and `/proc/[pid]/gid_map`

2. **Namespace Isolation**
   - PID, Mount, UTS, IPC, Network namespaces
   - Prevents container escape
   - Isolates processes, filesystem, and network

3. **Resource Limits (cgroups)**
   - Memory limits prevent OOM attacks
   - CPU limits prevent resource exhaustion
   - Implementation: cgroups v1/v2

4. **Read-only Root Filesystem**
   - Optional read-only rootfs
   - Prevents filesystem tampering
   - Only `/tmp` and volumes writable

### Planned Security Features

1. **Seccomp Filters**
   - Block dangerous syscalls
   - Implementation: libseccomp or seccomp JSON

2. **Capability Dropping**
   - Drop dangerous capabilities
   - Implementation: `capsh` or `libcap`

### Attack Demonstration & Mitigation

#### Attack 1: Container Escape via Host Filesystem Access

**Attack Attempt:**
```bash
container$ cat /etc/passwd
container$ ls /host
```

**Why It Fails:**
1. **Mount Namespace Isolation**: Container has isolated mount namespace
2. **chroot**: Container rootfs is isolated from host
3. **Result**: Container cannot access host filesystem

**Mitigation:**
- Mount namespace prevents seeing host mounts
- chroot changes root directory
- Container only sees its own rootfs

#### Attack 2: Privilege Escalation via User Namespace

**Attack Attempt:**
```bash
container$ id
uid=0(root) gid=0(root)
```

**Why It Fails:**
1. **User Namespace Mapping**: Container UID 0 maps to unprivileged host UID
2. **Host Process**: Container process runs as non-root on host
3. **Result**: Even as "root" in container, no privileges on host

**Mitigation:**
- User namespace maps container UID 0 → host unprivileged UID
- Container root has no privileges on host
- Prevents privilege escalation

#### Attack 3: Resource Exhaustion Attack

**Attack Attempt:**
```bash
container$ python -c "x = 'a' * 10**9"  # Allocate 1GB
```

**Why It Fails:**
1. **cgroup Memory Limit**: Container has memory limit
2. **OOM Killer**: Kernel kills process if limit exceeded
3. **Result**: Process killed, container stopped

**Mitigation:**
- Memory limits via cgroups
- OOM detection and alerting
- Automatic process termination

#### Attack 4: Network Isolation Bypass

**Attack Attempt:**
```bash
container$ ping 8.8.8.8
container$ curl http://localhost:8080
```

**Why It Fails:**
1. **Network Namespace**: Container has isolated network namespace
2. **veth Pairs**: Container network isolated via veth
3. **Result**: Container cannot access host network directly

**Mitigation:**
- Network namespace isolation
- veth pairs for network separation
- Bridge network for controlled communication

#### Attack 5: IPC Object Access

**Attack Attempt:**
```bash
container$ ipcs -a
container$ ipcrm -m <shmid>
```

**Why It Fails:**
1. **IPC Namespace**: Container has isolated IPC namespace
2. **Isolation**: IPC objects are namespace-specific
3. **Result**: Container cannot see host IPC objects

**Mitigation:**
- IPC namespace isolation
- Separate IPC objects per container
- No cross-container IPC access

### Security Best Practices

1. **Run as Non-Root**: Use user namespaces, map container root to unprivileged host UID
2. **Set Resource Limits**: Set memory and CPU limits, prevent resource exhaustion attacks
3. **Use Read-only Rootfs**: Enable read-only rootfs when possible, only allow writes to `/tmp` and volumes
4. **Drop Capabilities**: Drop dangerous capabilities (CAP_SYS_ADMIN, etc.), use minimal capability set
5. **Monitor Resources**: Monitor for OOM kills and CPU throttling, alert on violations
6. **Isolate Networks**: Use network namespaces, isolate container networks, control network access

### Limitations

Mini Docker is an **educational project**, not production-ready. It demonstrates concepts but may have security vulnerabilities.

**Not Recommended For:**
- Production workloads
- Hosting untrusted code
- Multi-tenant environments
- Sensitive data

**Recommended For:**
- Learning container internals
- Understanding OS concepts
- Educational purposes
- Development/testing

---

## ⚠️ Failure Cases

### Failure Case 1: Out-of-Memory (OOM) Kill

**What Failed:**
Container exceeded memory limit and was killed by the kernel OOM killer.

**Why It Failed:**
1. Container process allocated more memory than the cgroup limit
2. Kernel's OOM killer detected the violation
3. Process was terminated with SIGKILL

**How Kernel Behaved:**
```
[Kernel] OOM killer activated
[Kernel] Process <pid> killed (memory limit exceeded)
[Kernel] cgroup memory.oom_control: oom_kill = 1
```

**How It Was Handled:**
1. **Detection**: Monitor `memory.oom_control` (v1) or `memory.events` (v2)
2. **Alert**: Log OOM event and notify user
3. **Recovery**: Container status set to "Stopped"
4. **Restart Policy**: If `on-failure` or `always`, container can be restarted

**Prevention:**
- Set appropriate memory limits
- Monitor memory usage
- Use restart policies for automatic recovery

### Failure Case 2: CPU Throttling

**What Failed:**
Container exceeded CPU limit and was throttled by the kernel scheduler.

**Why It Failed:**
1. Container process consumed more CPU than allocated
2. cgroup CPU controller throttled the process
3. Process execution was paused periodically

**How Kernel Behaved:**
```
[Kernel] CPU throttling activated for cgroup
[Kernel] Process <pid> throttled (CPU limit exceeded)
[Kernel] cgroup cpu.stat: nr_throttled = <count>
```

**How It Was Handled:**
1. **Detection**: Monitor `cpu.stat` for throttling events
2. **Alert**: Log throttling count and notify user
3. **Monitoring**: Track throttling frequency
4. **Adjustment**: User can increase CPU limit if needed

**Prevention:**
- Set appropriate CPU limits
- Monitor CPU usage
- Adjust limits based on workload

### Failure Case 3: Network Namespace Creation Failure

**What Failed:**
Failed to create network namespace for container.

**Why It Failed:**
1. Insufficient permissions (requires root or CAP_NET_ADMIN)
2. Network namespace limit reached
3. System resource exhaustion

**How Kernel Behaved:**
```
[Kernel] Failed to create network namespace
[Kernel] Error: Operation not permitted (if not root)
[Kernel] Error: Too many namespaces (if limit reached)
```

**How It Was Handled:**
1. **Error Detection**: Catch subprocess errors
2. **Fallback**: Continue without network namespace (simulation mode)
3. **Logging**: Log error for debugging
4. **User Notification**: Inform user of limitation

**Prevention:**
- Run with appropriate permissions
- Monitor namespace usage
- Handle errors gracefully

### Failure Case 4: User Namespace Mapping Failure

**What Failed:**
Failed to write UID/GID maps for user namespace.

**Why It Failed:**
1. `/proc/[pid]/uid_map` can only be written once
2. Insufficient permissions
3. Invalid UID/GID values

**How Kernel Behaved:**
```
[Kernel] Failed to write uid_map: Operation not permitted
[Kernel] Failed to write uid_map: Invalid argument
```

**How It Was Handled:**
1. **Error Detection**: Catch IOError when writing maps
2. **Graceful Degradation**: Continue without user namespace mapping
3. **Warning**: Log warning but don't fail container creation
4. **Documentation**: Document requirement for proper setup

**Prevention:**
- Ensure proper permissions
- Write maps before process starts
- Validate UID/GID values

### Failure Case 5: OverlayFS Mount Failure

**What Failed:**
Failed to mount OverlayFS for container.

**Why It Failed:**
1. OverlayFS not supported in kernel
2. Insufficient permissions
3. Invalid mount options
4. Filesystem errors

**How Kernel Behaved:**
```
[Kernel] mount: overlay filesystem not supported
[Kernel] mount: Operation not permitted
[Kernel] mount: Invalid argument
```

**How It Was Handled:**
1. **Error Detection**: Check mount command return code
2. **Fallback**: Use regular rootfs (copy instead of overlay)
3. **Logging**: Log error for debugging
4. **User Notification**: Inform user of fallback

**Prevention:**
- Check kernel support for OverlayFS
- Ensure proper permissions
- Validate mount options
- Handle errors gracefully

### Common Patterns

1. **Graceful Degradation**: When a feature fails, fall back to a simpler implementation rather than failing completely.
2. **Error Logging**: Always log errors with context for debugging.
3. **User Notification**: Inform users of failures and limitations.
4. **Resource Monitoring**: Monitor resources to prevent failures before they occur.
5. **Permission Handling**: Handle permission errors gracefully and provide clear messages.

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
- `container_started` - Emitted when container successfully starts

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
├── seccomp.py             # Seccomp filters (planned)
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

## ⚡ Quick Reference

### Demo Commands

```
# Simple print
python -c "print('Hello from Mini Docker!')"

# With delay
python -c "print('Starting...'); import time; time.sleep(5); print('Done!')"

# Web server (runs until stopped)
python -m http.server 8000

# File operations
python -c "with open('test.txt', 'w') as f: f.write('Hello'); print('File created!')"

# Environment check
python -c "import os; print(f'Mode: {os.environ.get(\"MODE\")}')"
```

### Volume Mount Examples

**Format:** `HostPath:ContainerPath`

```
C:\MyData:/app/data
C:\Logs:/var/log
C:\Config:/etc/config
```

### Environment Variable Examples

**Format:** `KEY=VALUE`

```
MODE=production
DEBUG=true
PORT=8080
DB_HOST=localhost
```

**Access in Python:**
```python
import os
mode = os.environ.get('MODE')  # Note: 'MODE' must be in quotes!
```

**⚠️ Always quote environment variable names:**
- ✅ `os.environ.get('MODE')`
- ❌ `os.environ.get(MODE)`  # NameError!

### Resource Limits

**Memory Limit:**
- Small: 50 MB (simple scripts)
- Medium: 100 MB (web servers, apps)
- Large: 512 MB (databases, heavy apps)
- Very Large: 1024 MB (ML, video processing)

**CPU Limit:**
- Low: 25% (background tasks)
- Medium: 50% (normal apps)
- High: 75% (CPU-intensive)
- Max: 100% (heavy computations)

---

## 🚀 GitHub Setup

### Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Fill in the details:
   - **Repository name**: `mini-docker` (or your preferred name)
   - **Description**: "A lightweight, educational containerization system inspired by Docker"
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **"Create repository"**

### Step 2: Push to GitHub

After creating the repository, use these commands:

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/mini-docker.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 3: Verify

1. Go to your GitHub repository page
2. You should see all your files uploaded
3. The README.md will be displayed on the repository homepage

### Troubleshooting

**Error: "remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/mini-docker.git
```

**Error: "failed to push some refs"**
```bash
git pull origin main --rebase
git push -u origin main
```

---

## 🎓 Educational Value

This project demonstrates:

1. **Containerization Principles**: How containers provide isolation
2. **Linux Namespaces**: Process, mount, UTS, User, IPC, and Network namespaces
3. **chroot**: Filesystem isolation technique
4. **cgroups**: Resource limiting mechanism (v1 and v2)
5. **OverlayFS**: Layered filesystem for images
6. **Bind Mounts**: Volume mounting implementation
7. **Container Lifecycle**: Start, stop, pause, resume operations
8. **Web Development**: Flask backend, REST API, WebSockets
9. **System Programming**: Process management, namespace manipulation

---

## ⚠️ Limitations

- **Security**: This is an educational project, not production-ready
- **Networking**: Basic networking only (no bridge networks)
- **Images**: Simplified image system (no layers)
- **Windows**: Simulation mode only (no full containerization)
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

**Last Updated**: 2026-01-06
