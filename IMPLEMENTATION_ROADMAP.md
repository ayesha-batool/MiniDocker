# 🎓 Mini Docker - OS Lab Implementation Roadmap

> **Based on OS Lab Instructor Requirements**  
> This document maps instructor expectations to implementation tasks and tracks progress.

---

## 📊 Current Implementation Status

### ✅ Already Implemented

| Feature | Status | Location | Notes |
|---------|--------|----------|-------|
| **PID Namespace** | ✅ Partial | `container.py:122` | Uses `unshare --pid` |
| **Mount Namespace** | ✅ Partial | `container.py:122` | Uses `unshare --mount` |
| **UTS Namespace** | ✅ Partial | `container.py:122` | Uses `unshare --uts` |
| **cgroups v1 (Memory)** | ✅ Implemented | `container.py:54-72` | `memory.limit_in_bytes` |
| **cgroups v1 (CPU)** | ✅ Implemented | `container.py:66-67` | `cpu.shares` |
| **Volume Mounting** | ✅ Implemented | `container.py:86-101` | Bind mounts |
| **Process Lifecycle** | ✅ Implemented | `container.py:142-357` | Start/stop/pause/resume |
| **Resource Monitoring** | ✅ Implemented | `container.py:358-382` | CPU/Memory tracking |
| **Restart Policies** | ✅ Implemented | `container.py:430-448` | `always`, `on-failure`, `unless-stopped` |
| **Health Checks** | ✅ Implemented | `container.py:384-428` | Periodic health monitoring |
| **Logging System** | ✅ Implemented | `container.py:472-479` | Container logs |
| **Web Dashboard** | ✅ Implemented | `web_server.py`, `templates/` | Flask + WebSocket UI |

### ⚠️ Partially Implemented

| Feature | Status | Location | Issues |
|---------|--------|----------|--------|
| **Network Namespace** | ⚠️ Partial | `networking.py` | Basic implementation, needs isolation |
| **cgroups v2** | ❌ Not Supported | - | Only v1 supported |
| **User Namespace** | ❌ Not Implemented | - | Missing UID/GID mapping |
| **IPC Namespace** | ❌ Not Implemented | - | No IPC isolation |

### ❌ Not Implemented

- User Namespace Support
- IPC Namespace Isolation
- cgroups v2 Support
- Container `exec` Command
- CPU Scheduling Policy Control
- Zombie Process Handling
- Overlay Filesystem (OverlayFS)
- Read-only Root Filesystem
- File Capability Restrictions
- Network Namespace Isolation (proper)
- Container-to-Container Communication
- Port Collision Detection
- Crash Recovery (enhanced)
- Checkpoint & Restore (CRIU)
- System Call Tracing (strace)
- Resource Violation Alerts
- Seccomp Filters
- Attack Demonstration & Mitigation

---

## 🎯 Implementation Roadmap by Priority

### **Phase 1: Core OS Concepts (High Priority - 35% Weight)**

#### 1.1 User Namespace Support ⭐⭐⭐
**Priority:** Critical  
**Estimated Effort:** 8-12 hours  
**Files to Modify:** `container.py`, `filesystem.py`

**Implementation Steps:**
1. Add user namespace creation using `unshare --user`
2. Implement UID/GID mapping:
   - Read `/proc/[pid]/uid_map` and `/proc/[pid]/gid_map`
   - Map container UID 0 → host unprivileged UID
   - Document mapping logic
3. Update `_build_container_command()` to include `--user`
4. Test with non-root user inside container

**Acceptance Criteria:**
- Container runs as non-root inside
- UID 0 in container maps to unprivileged UID on host
- Documentation includes `/proc/[pid]/uid_map` explanation

**Files:**
- `container.py` - Add user namespace support
- `IMPLEMENTATION_NOTES.md` - Document UID mapping

---

#### 1.2 IPC Namespace Isolation ⭐⭐⭐
**Priority:** High  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container.py`

**Implementation Steps:**
1. Add `--ipc` flag to `unshare` command
2. Create test script to verify isolation:
   - Create shared memory segment outside container
   - Verify it's invisible inside container
   - Use `ipcs` command for verification
3. Document IPC isolation mechanism

**Acceptance Criteria:**
- IPC objects (shm, sem, msg) are isolated per container
- `ipcs` shows different objects inside vs outside
- Test evidence included in documentation

**Files:**
- `container.py` - Add IPC namespace
- `tests/test_ipc_isolation.py` - Verification tests

---

#### 1.3 Proper cgroups v2 Support ⭐⭐⭐
**Priority:** High  
**Estimated Effort:** 6-8 hours  
**Files to Modify:** `container.py`, `utils.py`

**Implementation Steps:**
1. Detect cgroup version dynamically:
   ```python
   def detect_cgroup_version():
       if os.path.exists("/sys/fs/cgroup/cgroup.controllers"):
           return "v2"
       return "v1"
   ```
2. Implement v2 support:
   - `memory.max` instead of `memory.limit_in_bytes`
   - `cpu.max` instead of `cpu.shares`
   - Unified hierarchy structure
3. Graceful fallback to v1 if v2 not available
4. Update documentation

**Acceptance Criteria:**
- Automatically detects cgroup version
- Supports both v1 and v2
- Falls back gracefully
- Documentation explains differences

**Files:**
- `container.py` - Add cgroup v2 detection and support
- `utils.py` - Add `detect_cgroup_version()` helper

---

### **Phase 2: Process & Scheduler Awareness (Medium Priority - 20% Weight)**

#### 2.1 Container `exec` Command ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 6-8 hours  
**Files to Modify:** `container.py`, `web_server.py`, `mini_docker_cli.py`

**Implementation Steps:**
1. Add `exec()` method to `SimulatedContainer`:
   ```python
   def exec(self, command):
       # Use setns() to enter existing namespaces
       # Handle PTY for interactive commands
   ```
2. Implement namespace entry using `setns` syscall
3. Add PTY handling for interactive commands
4. Add CLI command: `mini_docker exec <container> <command>`
5. Add Web UI button for exec

**Acceptance Criteria:**
- Can execute commands in running container
- Correctly attaches to existing namespaces
- PTY works for interactive commands (bash, etc.)
- Works from both CLI and Web UI

**Files:**
- `container.py` - Add `exec()` method
- `mini_docker_cli.py` - Add exec command
- `web_server.py` - Add exec endpoint
- `static/app.js` - Add exec UI

---

#### 2.2 CPU Scheduling Policy Control ⭐
**Priority:** Low  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container.py`, `web_server.py`

**Implementation Steps:**
1. Add scheduling parameters to container config:
   - CFS shares
   - Nice value
   - Optional: real-time scheduling
2. Apply via cgroups or `sched_setscheduler()`
3. Document scheduling policies

**Acceptance Criteria:**
- Can set CPU shares and nice values
- Scheduling policy is applied correctly
- Documentation explains CFS and nice values

**Files:**
- `container.py` - Add scheduling control
- `web_server.py` - Add scheduling parameters to API

---

#### 2.3 Zombie Process Handling ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container.py`

**Implementation Steps:**
1. Implement init-like behavior:
   - Reap child processes using `waitpid()`
   - Handle SIGCHLD signals
2. Create test with fork bomb (controlled)
3. Verify no zombie processes accumulate

**Acceptance Criteria:**
- Container reaps all child processes
- No zombie processes accumulate
- Test demonstrates fork bomb handling

**Files:**
- `container.py` - Add zombie reaping logic
- `tests/test_zombie_handling.py` - Fork bomb test

---

### **Phase 3: Filesystem & Storage (High Priority - 15% Weight)**

#### 3.1 Overlay Filesystem (OverlayFS) ⭐⭐⭐
**Priority:** Critical  
**Estimated Effort:** 10-14 hours  
**Files to Modify:** `filesystem.py`, `container.py`

**Implementation Steps:**
1. Implement OverlayFS mount:
   ```bash
   mount -t overlay overlay \
     -o lowerdir=<image>,upperdir=<container>,workdir=<work> \
     <mountpoint>
   ```
2. Structure:
   - `lowerdir`: Base image (read-only)
   - `upperdir`: Container writable layer
   - `workdir`: OverlayFS work directory
3. Update `filesystem.py` to create overlay structure
4. Clean teardown on container deletion

**Acceptance Criteria:**
- Base image is read-only
- Container has writable layer
- Changes persist in upperdir
- Clean teardown removes overlay mounts

**Files:**
- `filesystem.py` - Add OverlayFS creation
- `container.py` - Update mount logic
- `IMPLEMENTATION_NOTES.md` - Document OverlayFS

---

#### 3.2 Read-only Root Filesystem Mode ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 3-4 hours  
**Files to Modify:** `container.py`, `web_server.py`

**Implementation Steps:**
1. Add `--read-only` flag to container config
2. Mount rootfs as read-only
3. Create writable `/tmp` and `/var/tmp` if needed
4. Only mounted volumes are writable

**Acceptance Criteria:**
- Root filesystem is read-only
- `/tmp` and volumes remain writable
- Error if trying to write to read-only filesystem

**Files:**
- `container.py` - Add read-only mode
- `web_server.py` - Add read-only option to API

---

#### 3.3 File Capability Restrictions ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container.py`

**Implementation Steps:**
1. Use `libcap` or `capsh` to drop capabilities
2. Drop dangerous capabilities:
   - `CAP_SYS_ADMIN` (mount, unmount)
   - `CAP_NET_ADMIN` (network configuration)
   - `CAP_SYS_MODULE` (load modules)
3. Create test demonstrating capability restrictions
4. Document which capabilities are dropped

**Acceptance Criteria:**
- Dangerous capabilities are dropped
- Test shows failure when trying to use dropped capabilities
- Documentation lists dropped capabilities

**Files:**
- `container.py` - Add capability dropping
- `tests/test_capabilities.py` - Capability tests

---

### **Phase 4: Networking (Medium-High Priority - 15% Weight)**

#### 4.1 Network Namespace Isolation ⭐⭐⭐
**Priority:** High  
**Estimated Effort:** 8-10 hours  
**Files to Modify:** `networking.py`, `container.py`

**Implementation Steps:**
1. Create network namespace per container:
   ```bash
   ip netns add <container_name>
   ```
2. Create veth pair:
   ```bash
   ip link add veth0 type veth peer name veth1
   ip link set veth1 netns <container_name>
   ```
3. Set up bridge connectivity
4. Assign IP addresses

**Acceptance Criteria:**
- Each container has isolated network namespace
- Containers can communicate via bridge
- Network isolation verified with `ip netns list`

**Files:**
- `networking.py` - Complete network namespace implementation
- `container.py` - Integrate network namespace

---

#### 4.2 Container-to-Container Communication ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 6-8 hours  
**Files to Modify:** `networking.py`

**Implementation Steps:**
1. Set up bridge network
2. Assign IPs to containers
3. Implement basic DNS resolution (container name → IP)
4. Test container-to-container ping/communication

**Acceptance Criteria:**
- Containers can ping each other by name
- Basic DNS resolution works
- Communication via bridge network

**Files:**
- `networking.py` - Add container-to-container networking
- `tests/test_container_networking.py` - Networking tests

---

#### 4.3 Port Collision Detection ⭐
**Priority:** Low  
**Estimated Effort:** 2-3 hours  
**Files to Modify:** `networking.py`, `web_server.py`

**Implementation Steps:**
1. Track used ports in `networking.py`
2. Check before binding new port
3. Return meaningful error if collision detected

**Acceptance Criteria:**
- Prevents two containers from using same host port
- Clear error message on collision
- Port tracking is persistent

**Files:**
- `networking.py` - Add port collision detection
- `web_server.py` - Handle port collision errors

---

### **Phase 5: Reliability & Fault Tolerance (Medium Priority - 10% Weight)**

#### 5.1 Crash Recovery ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container.py`, `container_manager.py`

**Implementation Steps:**
1. Detect abnormal termination (SIGSEGV, SIGABRT)
2. Apply restart policies correctly:
   - `on-failure`: Only restart on non-zero exit
   - `unless-stopped`: Restart unless manually stopped
3. Log crash events
4. Track restart count

**Acceptance Criteria:**
- Detects crashes correctly
- Restart policies work as documented
- Crash events are logged

**Files:**
- `container.py` - Enhance crash detection
- `container_manager.py` - Track crash events

---

#### 5.2 Checkpoint & Restore (CRIU) ⭐ (Bonus)
**Priority:** Low (Bonus)  
**Estimated Effort:** 12-16 hours  
**Files to Modify:** `container.py`, new `checkpoint.py`

**Implementation Steps:**
1. Install CRIU (if available)
2. Implement checkpoint:
   ```bash
   criu dump -t <pid> -D <checkpoint_dir>
   ```
3. Implement restore:
   ```bash
   criu restore -D <checkpoint_dir>
   ```
4. Test checkpoint/restore cycle

**Acceptance Criteria:**
- Can checkpoint running container
- Can restore from checkpoint
- State is preserved correctly

**Files:**
- `checkpoint.py` - New file for CRIU integration
- `container.py` - Add checkpoint/restore methods

---

### **Phase 6: Observability & Debugging (Medium Priority - 10% Weight)**

#### 6.1 System Call Tracing (strace) ⭐
**Priority:** Low  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container.py`, `web_server.py`

**Implementation Steps:**
1. Add `--strace` flag to container config
2. Wrap command with `strace`:
   ```bash
   strace -o <trace_file> -f <command>
   ```
3. Store trace file in container directory
4. Add UI to view traces

**Acceptance Criteria:**
- Can enable strace for containers
- Trace files are stored and viewable
- Documentation explains syscall tracing

**Files:**
- `container.py` - Add strace support
- `web_server.py` - Add strace endpoint
- `static/app.js` - Add trace viewer

---

#### 6.2 Resource Violation Alerts ⭐⭐
**Priority:** Medium  
**Estimated Effort:** 3-4 hours  
**Files to Modify:** `container.py`, `web_server.py`

**Implementation Steps:**
1. Detect OOM kills:
   - Monitor `/sys/fs/cgroup/memory/.../memory.oom_control`
   - Log OOM events
2. Detect CPU throttling:
   - Monitor `cpu.stat` in cgroups
   - Log throttling events
3. Send alerts via WebSocket

**Acceptance Criteria:**
- OOM kills are detected and logged
- CPU throttling is detected
- Alerts appear in UI

**Files:**
- `container.py` - Add violation detection
- `web_server.py` - Send violation alerts

---

#### 6.3 Timeline View ⭐
**Priority:** Low  
**Estimated Effort:** 4-6 hours  
**Files to Modify:** `container_manager.py`, `static/app.js`

**Implementation Steps:**
1. Track container lifecycle events:
   - created → running → paused → stopped
2. Store timestamps for each transition
3. Create timeline visualization in UI

**Acceptance Criteria:**
- Lifecycle events are tracked
- Timeline view shows container history
- Works in both CLI and web UI

**Files:**
- `container_manager.py` - Track lifecycle events
- `static/app.js` - Add timeline visualization

---

### **Phase 7: Security & Isolation (Critical - 15% Weight)**

#### 7.1 Seccomp Filters ⭐⭐⭐
**Priority:** Critical  
**Estimated Effort:** 8-10 hours  
**Files to Modify:** `container.py`, new `seccomp.py`

**Implementation Steps:**
1. Create seccomp filter JSON:
   ```json
   {
     "defaultAction": "SCMP_ACT_ALLOW",
     "syscalls": [
       {"names": ["reboot", "mount"], "action": "SCMP_ACT_ERRNO"}
     ]
   }
   ```
2. Apply filter using `seccomp` library or `libseccomp`
3. Test blocked syscalls
4. Document blocked syscalls

**Acceptance Criteria:**
- Dangerous syscalls are blocked
- Test demonstrates blocked syscall error
- Documentation lists blocked syscalls

**Files:**
- `seccomp.py` - New file for seccomp filters
- `container.py` - Apply seccomp filters
- `tests/test_seccomp.py` - Seccomp tests

---

#### 7.2 Attack Demonstration & Mitigation ⭐⭐⭐
**Priority:** Critical  
**Estimated Effort:** 6-8 hours  
**Files to Modify:** Documentation, new `tests/`

**Implementation Steps:**
1. Document container escape attempt:
   - Example: Trying to access host filesystem
   - Example: Trying to break out of namespace
2. Explain why it fails:
   - Namespace isolation
   - Capability restrictions
   - Seccomp filters
3. Create test demonstrating failed escape

**Acceptance Criteria:**
- At least one escape attempt documented
- Explanation of why it fails
- Test demonstrates mitigation

**Files:**
- `SECURITY.md` - New security documentation
- `tests/test_security.py` - Security tests

---

### **Phase 8: Documentation & Analysis (Mandatory - 15% Weight)**

#### 8.1 Design Report ⭐⭐⭐
**Priority:** Critical  
**Estimated Effort:** 8-10 hours  
**Files to Create:** `DESIGN_REPORT.md`

**Required Sections:**
1. Architecture diagram (ASCII or image)
2. Namespace usage explanation
3. cgroup hierarchy diagram
4. Trade-offs vs Docker
5. Design decisions and rationale

**Files:**
- `DESIGN_REPORT.md` - Comprehensive design document

---

#### 8.2 Comparative Analysis ⭐⭐⭐
**Priority:** Critical  
**Estimated Effort:** 6-8 hours  
**Files to Create:** `COMPARATIVE_ANALYSIS.md`

**Required Comparisons:**
- Mini Docker vs Docker
- Mini Docker vs LXC
- Mini Docker vs Podman

**Comparison Dimensions:**
- Isolation strength
- Performance
- Complexity
- Use cases

**Files:**
- `COMPARATIVE_ANALYSIS.md` - Comparison document

---

#### 8.3 Failure Case Documentation ⭐⭐
**Priority:** High  
**Estimated Effort:** 4-6 hours  
**Files to Create:** `FAILURE_CASES.md`

**Required:**
- At least 3 failure scenarios
- For each:
  - What failed
  - Why it failed
  - How kernel behaved
  - How it was handled

**Files:**
- `FAILURE_CASES.md` - Failure analysis document

---

## 📈 Progress Tracking

### Overall Progress: ~25%

| Category | Progress | Status |
|----------|----------|--------|
| OS Concepts | 30% | ⚠️ Partial |
| Process & Scheduler | 40% | ⚠️ Partial |
| Filesystem & Storage | 20% | ⚠️ Partial |
| Networking | 30% | ⚠️ Partial |
| Reliability | 50% | ✅ Good |
| Observability | 40% | ⚠️ Partial |
| Security | 10% | ❌ Needs Work |
| Documentation | 60% | ✅ Good |

---

## 🎯 Recommended Implementation Order

### **Week 1-2: Foundation (Critical Features)**
1. User Namespace Support (1.1)
2. IPC Namespace Isolation (1.2)
3. cgroups v2 Support (1.3)

### **Week 3-4: Filesystem & Networking**
4. Overlay Filesystem (3.1)
5. Network Namespace Isolation (4.1)
6. Container-to-Container Communication (4.2)

### **Week 5-6: Security & Process Management**
7. Seccomp Filters (7.1)
8. Container `exec` (2.1)
9. Zombie Process Handling (2.3)

### **Week 7-8: Polish & Documentation**
10. Design Report (8.1)
11. Comparative Analysis (8.2)
12. Failure Cases (8.3)
13. Attack Demonstration (7.2)

---

## 📝 Notes

- **Estimated Total Effort:** 120-160 hours
- **Priority:** Focus on Phase 1, 3, 4, 7, 8 for maximum marks
- **Testing:** Each feature should include tests
- **Documentation:** Document as you implement, not after

---

## 🔗 Related Documents

- [USAGE_GUIDE.md](USAGE_GUIDE.md) - User guide
- [README.md](README.md) - Main documentation
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference
- [COMMON_ERRORS.md](COMMON_ERRORS.md) - Common errors

---

**Last Updated:** 2026-01-06  
**Status:** Active Development

