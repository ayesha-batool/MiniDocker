# Mini Docker - Security Documentation

## Security Features

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

3. **AppArmor/SELinux**
   - Mandatory access control
   - Not implemented (complexity)

---

## Attack Demonstration & Mitigation

### Attack 1: Container Escape via Host Filesystem Access

#### Attack Attempt
```bash
# Attacker tries to access host filesystem
container$ cat /etc/passwd
container$ ls /host
```

#### Why It Fails
1. **Mount Namespace Isolation**: Container has isolated mount namespace
2. **chroot**: Container rootfs is isolated from host
3. **Result**: Container cannot access host filesystem

#### Mitigation
- Mount namespace prevents seeing host mounts
- chroot changes root directory
- Container only sees its own rootfs

#### Evidence
```bash
# Inside container
$ mount
overlay on / type overlay ...
# Only container filesystem visible

# On host
$ ps aux | grep container
# Container process isolated
```

---

### Attack 2: Privilege Escalation via User Namespace

#### Attack Attempt
```bash
# Attacker tries to become root
container$ id
uid=0(root) gid=0(root)
container$ whoami
root
```

#### Why It Fails
1. **User Namespace Mapping**: Container UID 0 maps to unprivileged host UID
2. **Host Process**: Container process runs as non-root on host
3. **Result**: Even as "root" in container, no privileges on host

#### Mitigation
- User namespace maps container UID 0 → host unprivileged UID
- Container root has no privileges on host
- Prevents privilege escalation

#### Evidence
```bash
# Inside container
$ id
uid=0(root) gid=0(root)

# On host (check actual UID)
$ ps aux | grep container
user   1234  ...  # Runs as unprivileged user
```

---

### Attack 3: Resource Exhaustion Attack

#### Attack Attempt
```bash
# Attacker tries to exhaust memory
container$ python -c "x = 'a' * 10**9"  # Allocate 1GB
```

#### Why It Fails
1. **cgroup Memory Limit**: Container has memory limit
2. **OOM Killer**: Kernel kills process if limit exceeded
3. **Result**: Process killed, container stopped

#### Mitigation
- Memory limits via cgroups
- OOM detection and alerting
- Automatic process termination

#### Evidence
```bash
# Container log
[Container] ALERT: Out-of-memory (OOM) kill detected!
[Container] Container process exited with code 137 (SIGKILL)
```

---

### Attack 4: Network Isolation Bypass

#### Attack Attempt
```bash
# Attacker tries to access host network
container$ ping 8.8.8.8
container$ curl http://localhost:8080
```

#### Why It Fails
1. **Network Namespace**: Container has isolated network namespace
2. **veth Pairs**: Container network isolated via veth
3. **Result**: Container cannot access host network directly

#### Mitigation
- Network namespace isolation
- veth pairs for network separation
- Bridge network for controlled communication

#### Evidence
```bash
# Inside container
$ ip addr
1: lo: ...  # Only container interfaces
2: veth_container: ...  # Isolated interface

# On host
$ ip netns list
minidocker_container1  # Isolated namespace
```

---

### Attack 5: IPC Object Access

#### Attack Attempt
```bash
# Attacker tries to access host IPC
container$ ipcs -a
container$ ipcrm -m <shmid>
```

#### Why It Fails
1. **IPC Namespace**: Container has isolated IPC namespace
2. **Isolation**: IPC objects are namespace-specific
3. **Result**: Container cannot see host IPC objects

#### Mitigation
- IPC namespace isolation
- Separate IPC objects per container
- No cross-container IPC access

#### Evidence
```bash
# On host
$ ipcs -a
# Shows host IPC objects

# Inside container
$ ipcs -a
# Shows only container IPC objects (empty if none)
```

---

## Security Best Practices

### 1. Run as Non-Root
- Use user namespaces
- Map container root to unprivileged host UID
- Prevents privilege escalation

### 2. Set Resource Limits
- Set memory limits
- Set CPU limits
- Prevent resource exhaustion attacks

### 3. Use Read-only Rootfs
- Enable read-only rootfs when possible
- Only allow writes to `/tmp` and volumes
- Prevents filesystem tampering

### 4. Drop Capabilities
- Drop dangerous capabilities (CAP_SYS_ADMIN, etc.)
- Use minimal capability set
- Reduce attack surface

### 5. Monitor Resources
- Monitor for OOM kills
- Monitor for CPU throttling
- Alert on violations

### 6. Isolate Networks
- Use network namespaces
- Isolate container networks
- Control network access

---

## Limitations

### Educational Project
Mini Docker is an **educational project**, not production-ready. It demonstrates concepts but may have security vulnerabilities.

### Not Recommended For
- Production workloads
- Hosting untrusted code
- Multi-tenant environments
- Sensitive data

### Recommended For
- Learning container internals
- Understanding OS concepts
- Educational purposes
- Development/testing

---

## Security Comparison

| Feature | Mini Docker | Docker | LXC | Podman |
|---------|-------------|--------|-----|--------|
| **User Namespaces** | ✅ | ✅ | ✅ | ✅ |
| **Seccomp** | ⚠️ | ✅ | ✅ | ✅ |
| **Capabilities** | ⚠️ | ✅ | ✅ | ✅ |
| **AppArmor** | ❌ | ✅ | ✅ | ✅ |
| **SELinux** | ❌ | ✅ | ✅ | ✅ |
| **Rootless** | ⚠️ | ⚠️ | ✅ | ✅ |

**Verdict**: Mini Docker has basic security but lacks advanced hardening. Use Docker/Podman for production.

---

**Last Updated**: 2026-01-06

