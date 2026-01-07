# Mini Docker - Design Report

## 1. Architecture Overview

Mini Docker is a lightweight containerization system that demonstrates core OS concepts including namespaces, cgroups, and filesystem isolation.

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

## 2. Namespace Usage

### 2.1 Process ID (PID) Namespace
- **Purpose**: Isolate process trees
- **Implementation**: `unshare --pid`
- **Effect**: Container processes see only their own PID namespace
- **Usage**: Each container has isolated process tree

### 2.2 Mount Namespace
- **Purpose**: Isolate filesystem mounts
- **Implementation**: `unshare --mount`
- **Effect**: Container has isolated mount points
- **Usage**: Volume mounts are isolated per container

### 2.3 UTS Namespace
- **Purpose**: Isolate hostname
- **Implementation**: `unshare --uts`
- **Effect**: Container can have different hostname
- **Usage**: Each container can set its own hostname

### 2.4 User Namespace
- **Purpose**: Map container UIDs to host UIDs
- **Implementation**: `unshare --user` + `/proc/[pid]/uid_map`
- **Effect**: Container UID 0 maps to unprivileged host UID
- **Usage**: Security - containers run as non-root on host

### 2.5 IPC Namespace
- **Purpose**: Isolate IPC objects (shared memory, semaphores, message queues)
- **Implementation**: `unshare --ipc`
- **Effect**: IPC objects are isolated per container
- **Usage**: Containers cannot access each other's IPC

### 2.6 Network Namespace
- **Purpose**: Isolate network stack
- **Implementation**: `ip netns add` + veth pairs
- **Effect**: Each container has isolated network interface
- **Usage**: Container-to-container communication via bridge

## 3. cgroup Hierarchy

### cgroups v1 Structure
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

### cgroups v2 Structure (Unified Hierarchy)
```
/sys/fs/cgroup/
└── minidocker_<name>/
    ├── cgroup.controllers
    ├── cgroup.subtree_control
    ├── memory.max
    ├── cpu.max
    └── cgroup.procs
```

### Resource Limits
- **Memory**: Set via `memory.limit_in_bytes` (v1) or `memory.max` (v2)
- **CPU**: Set via `cpu.shares` (v1) or `cpu.max` (v2)
- **Process Assignment**: Write PID to `cgroup.procs`

## 4. Filesystem Isolation

### 4.1 chroot
- **Purpose**: Change root directory
- **Implementation**: `chroot <rootfs_path>`
- **Effect**: Container sees only its rootfs
- **Usage**: Basic filesystem isolation

### 4.2 Overlay Filesystem
- **Purpose**: Read-only base image + writable container layer
- **Structure**:
  - `lowerdir`: Base image (read-only)
  - `upperdir`: Container writable layer
  - `workdir`: OverlayFS work directory
  - `merged`: Final mount point
- **Implementation**: `mount -t overlay`
- **Effect**: Changes persist in upperdir, base remains read-only

## 5. Trade-offs vs Docker

### Advantages of Mini Docker
1. **Simplicity**: Easier to understand and learn
2. **Transparency**: Code shows how containers work internally
3. **Educational**: Designed for learning OS concepts
4. **Lightweight**: Minimal dependencies

### Limitations vs Docker
1. **Security**: Less hardened (educational project)
2. **Features**: Missing many Docker features (layers, registry, etc.)
3. **Performance**: Not optimized for production
4. **Compatibility**: Not Docker-compatible
5. **Networking**: Simplified networking model

## 6. Design Decisions

### 6.1 Why Python?
- Cross-platform support
- Easy to understand
- Good for educational purposes
- Rich standard library

### 6.2 Why Flask?
- Lightweight web framework
- Easy to understand
- Good for REST APIs
- WebSocket support via Flask-SocketIO

### 6.3 Why Web UI?
- Better user experience
- Real-time updates
- Easier to demonstrate features
- Modern interface

### 6.4 Why Both v1 and v2 cgroups?
- Compatibility with different Linux distributions
- Some systems still use v1
- v2 is the future, but v1 is still common
- Graceful fallback ensures compatibility

## 7. Security Considerations

### Implemented
- User namespace mapping (non-root containers)
- Capability dropping (planned)
- Seccomp filters (planned)
- Read-only rootfs option

### Not Implemented (Educational Project)
- Full capability management
- AppArmor/SELinux integration
- Image signing/verification
- Network policies

## 8. Future Enhancements

1. **Checkpoint/Restore**: CRIU integration
2. **Image Layers**: Proper layer management
3. **Registry**: Image registry support
4. **Compose**: Multi-container orchestration
5. **Plugins**: Extensible plugin system

---

**Last Updated**: 2026-01-06

