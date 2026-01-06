# ⚡ Quick Reference Card

## 🚀 Demo Commands

```
# Simple print
python -c "print('Hello from Mini Docker!')"

# With delay
python -c "print('Starting...'); import time; time.sleep(5); print('Done!')"

# Web server (runs until stopped)
python -m http.server 8000

# File operations
python -c "with open('test.txt', 'w') as f: f.write('Hello'); print('File created!')"

# List directory
python -c "import os; print('\n'.join(os.listdir('.')))"

# Count numbers
python -c "for i in range(1, 11): print(f'Number {i}')"

# Environment check
python -c "import os; print(f'Directory: {os.getcwd()}')"

# JSON example
python -c "import json; print(json.dumps({'name': 'Mini Docker'}, indent=2))"
```

---

## 💾 Volume Mount Examples

**Format:** `HostPath:ContainerPath`

```
C:\MyData:/app/data
C:\Logs:/var/log
C:\Config:/etc/config
F:\Projects:/app
C:\Database:/data/db
```

**How to use:**
1. Create folder on your computer: `C:\MyData`
2. Add volume: `C:\MyData:/app/data`
3. Access in container: `/app/data`

---

## 🌍 Environment Variable Examples

**Format:** `KEY=VALUE`

```
MODE=production
DEBUG=true
PORT=8080
DB_HOST=localhost
API_KEY=abc123xyz789
DATABASE_URL=postgresql://localhost/mydb
```

**Access in Python:**
```python
import os
mode = os.environ.get('MODE')  # Note: 'MODE' must be in quotes!
port = int(os.environ.get('PORT', 8000))  # 'PORT' must be in quotes!
```

**⚠️ Always quote environment variable names:**
- ✅ `os.environ.get('MODE')`
- ❌ `os.environ.get(MODE)`  # NameError!

---

## 📊 Resource Limits

### Memory Limit
- **Small**: 50 MB (simple scripts)
- **Medium**: 100 MB (web servers, apps)
- **Large**: 512 MB (databases, heavy apps)
- **Very Large**: 1024 MB (ML, video processing)

### CPU Limit
- **Low**: 25% (background tasks)
- **Medium**: 50% (normal apps)
- **High**: 75% (CPU-intensive)
- **Max**: 100% (heavy computations)

---

## 📁 Rootfs Explained

**What it is:** Container's isolated file system

**Location:** `containers/<name>/rootfs/`

**Structure:**
```
rootfs/
├── bin/    # Executables
├── etc/    # Config files
├── usr/    # Programs
├── lib/    # Libraries
├── tmp/    # Temp files
└── var/    # Variable data
```

**Key Points:**
- ✅ Isolated from your computer
- ✅ Deleted when container is deleted
- ✅ Use volume mounts to share files

---

## 🎯 Complete Exampl

**Container Name:** `my-app`

**Command:**
```
python -c "import os; print(f'Mode: {os.environ.get(\"MODE\")}')"
```

**Memory:** 100 MB  
**CPU:** 50%  
**Volumes:** `C:\MyData:/app/data`  
**Env Vars:** `MODE=production`

---

## 💡 Tips

- **Start simple**: Use basic commands first
- **Test volumes**: Create folder on host before mounting
- **Check limits**: Monitor container resources
- **Use env vars**: Keep config out of code
- **Understand rootfs**: Files in rootfs are isolated

---

*For detailed explanations, see [USAGE_GUIDE.md](USAGE_GUIDE.md)*

