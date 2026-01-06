# 📖 Mini Docker - Usage Guide & Examples

## Table of Contents
1. [Demo Commands](#demo-commands)
2. [Volume Mounts](#volume-mounts)
3. [Environment Variables](#environment-variables)
4. [Resource Limits](#resource-limits)
5. [Rootfs Explained](#rootfs-explained)

---

## 🚀 Demo Commands

### Basic Commands

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

---

## 💾 Volume Mounts

### What is a Volume Mount?

**Volume Mount** allows you to share files and directories between your host machine (your computer) and the container. It's like creating a bridge between two folders.

**Think of it like this:**
- **Host Path**: A folder on your computer (e.g., `C:\MyData`)
- **Container Path**: A folder inside the container (e.g., `/app/data`)
- **Volume Mount**: Connects these two folders so they share the same files

### Why Use Volume Mounts?

1. **Persistent Data**: Data saved in a volume persists even after the container stops
2. **File Sharing**: Share files between your computer and the container
3. **Data Backup**: Easy to backup data from your host machine
4. **Development**: Edit files on your computer and see changes in the container

### Demo Examples

#### Example 1: Basic Volume Mount
```
Host Path: C:\MyData
Container Path: /app/data
```
**Format:** `C:\MyData:/app/data`

**What it does:**
- The folder `C:\MyData` on your computer is accessible as `/app/data` inside the container
- Any file you put in `C:\MyData` appears in `/app/data` in the container
- Any file created in `/app/data` in the container appears in `C:\MyData` on your computer

#### Example 2: Log Directory
```
Host Path: C:\Logs
Container Path: /var/log
```
**Format:** `C:\Logs:/var/log`

**Use Case:** Store application logs on your computer for easy access.

#### Example 3: Configuration Files
```
Host Path: C:\Config
Container Path: /etc/config
```
**Format:** `C:\Config:/etc/config`

**Use Case:** Share configuration files between host and container.

#### Example 4: Project Directory
```
Host Path: F:\Projects\MyApp
Container Path: /app
```
**Format:** `F:\Projects\MyApp:/app`

**Use Case:** Develop code on your computer and run it in the container.

#### Example 5: Database Data
```
Host Path: C:\Database
Container Path: /data/db
```
**Format:** `C:\Database:/data/db`

**Use Case:** Store database files persistently on your computer.

### How to Use Volume Mounts

1. **Create the folder on your computer first:**
   ```
   C:\MyData
   ```

2. **Add volume mount in Mini Docker:**
   - Click "⚙️ Advanced Options"
   - Click "+ Add Volume"
   - Enter: `C:\MyData:/app/data`

3. **Use in your command:**
   ```
   python -c "with open('/app/data/output.txt', 'w') as f: f.write('Hello from container!')"
   ```

4. **Check your computer:**
   - Open `C:\MyData\output.txt`
   - You'll see "Hello from container!" written there!

---

## 🌍 Environment Variables

### What are Environment Variables?

**Environment Variables** are key-value pairs that provide configuration to your container. They're like settings that your application can read.

**Think of it like this:**
- **Key**: The name of the setting (e.g., `DATABASE_URL`)
- **Value**: The actual value (e.g., `localhost:5432`)
- **Usage**: Your application reads these variables to know how to behave

### Why Use Environment Variables?

1. **Configuration**: Change app behavior without modifying code
2. **Secrets**: Store sensitive information (passwords, API keys)
3. **Flexibility**: Same code works in different environments
4. **Security**: Keep secrets out of your code

### Demo Examples

#### Example 1: Database Configuration
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

#### Example 2: Application Mode
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

#### Example 3: API Key
```
Variable Name: API_KEY
Variable Value: abc123xyz789
```
**Format:** `API_KEY=abc123xyz789`

**In your Python code:**
```python
import os
api_key = os.environ.get('API_KEY')
print(f'API Key: {api_key}')
```

#### Example 4: Port Number
```
Variable Name: PORT
Variable Value: 8080
```
**Format:** `PORT=8080`

**In your Python code:**
```python
import os
port = int(os.environ.get('PORT', 8000))
print(f'Server running on port {port}')
```

#### Example 5: Debug Mode
```
Variable Name: DEBUG
Variable Value: true
```
**Format:** `DEBUG=true`

**In your Python code:**
```python
import os
debug = os.environ.get('DEBUG', 'false').lower() == 'true'
if debug:
    print('Debug mode enabled')
```

#### Example 6: Multiple Variables
You can add multiple environment variables:
```
DATABASE_URL=postgresql://localhost/mydb
API_KEY=secret123
MODE=development
DEBUG=true
```

**In your Python code:**
```python
import os
db_url = os.environ.get('DATABASE_URL')
api_key = os.environ.get('API_KEY')
mode = os.environ.get('MODE')
debug = os.environ.get('DEBUG') == 'true'

print(f'Database: {db_url}')
print(f'Mode: {mode}')
print(f'Debug: {debug}')
```

### How to Use Environment Variables

1. **Add in Mini Docker:**
   - Click "⚙️ Advanced Options"
   - Click "+ Add Variable"
   - Enter: `MODE=production`

2. **Access in your command:**
   ```
   python -c "import os; print(f'Mode: {os.environ.get(\"MODE\", \"not set\")}')"
   ```
   
   **⚠️ Important:** Always use quotes around environment variable names:
   - ✅ Correct: `os.environ.get("MODE")` 
   - ❌ Wrong: `os.environ.get(MODE)`  # Causes NameError!

---

## 📊 Resource Limits

### Memory Limit

#### What is Memory Limit?

**Memory Limit** controls how much RAM (memory) your container can use. It prevents a container from using all available memory on your system.

**Units:** Megabytes (MB)

#### Available System Resources

To determine appropriate memory limits, you need to know your system's available resources:

**How to Check Available Memory:**

1. **Windows (PowerShell):**
   ```powershell
   # Check total RAM
   (Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB
   
   # Check available RAM
   (Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB
   ```

2. **Windows (Command Prompt):**
   ```cmd
   systeminfo | findstr /C:"Total Physical Memory"
   ```

3. **Linux/Mac:**
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
- Example: On 8 GB system, allocate max 5-6 GB total across all containers

#### Why Use Memory Limits?

1. **Prevent Resource Exhaustion**: Stop one container from using all RAM
2. **Fair Resource Sharing**: Multiple containers can run simultaneously
3. **System Stability**: Prevents your computer from freezing
4. **Cost Control**: In cloud environments, limits costs

#### Examples

**Example 1: Small Container (50 MB)**
```
Memory Limit: 50 MB
```
**Use Case:** Simple scripts, text processing, small utilities

**Example 2: Medium Container (100 MB)**
```
Memory Limit: 100 MB
```
**Use Case:** Web servers, small applications, data processing

**Example 3: Large Container (512 MB)**
```
Memory Limit: 512 MB
```
**Use Case:** Databases, large applications, image processing

**Example 4: Very Large Container (1024 MB = 1 GB)**
```
Memory Limit: 1024 MB
```
**Use Case:** Heavy applications, machine learning, video processing

#### What Happens if Limit is Exceeded?

- Container may be killed by the system
- Application may crash
- Performance degrades

**Recommendation:** Set limit slightly higher than expected usage.

---

### CPU Limit

#### What is CPU Limit?

**CPU Limit** controls how much CPU (processor) power your container can use. It's expressed as a percentage of total CPU capacity.

**Units:** Percentage (%)

#### Available CPU Resources

To determine appropriate CPU limits, you need to know your system's CPU capabilities:

**How to Check Available CPU:**

1. **Windows (PowerShell):**
   ```powershell
   # Check number of CPU cores
   (Get-CimInstance Win32_ComputerSystem).NumberOfLogicalProcessors
   
   # Check CPU usage
   Get-Counter '\Processor(_Total)\% Processor Time'
   ```

2. **Windows (Task Manager):**
   - Press `Ctrl + Shift + Esc`
   - Go to "Performance" tab
   - See "Logical processors" count

3. **Linux/Mac:**
   ```bash
   # Check number of CPU cores
   nproc
   # or
   lscpu | grep "^CPU(s):"
   
   # Check CPU usage
   top
   # or
   htop
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
- Example: On 4-core system, allocate max 3 cores (300%) total across all containers

#### Why Use CPU Limits?

1. **Fair CPU Sharing**: Multiple containers share CPU fairly
2. **Prevent CPU Starvation**: One container can't hog all CPU
3. **Performance Predictability**: Consistent performance for all containers
4. **System Responsiveness**: Your computer stays responsive

#### Examples

**Example 1: Low CPU (25%)**
```
CPU Limit: 25%
```
**Use Case:** Background tasks, scheduled jobs, low-priority processes

**Example 2: Medium CPU (50%)**
```
CPU Limit: 50%
```
**Use Case:** Web servers, standard applications, normal workloads

**Example 3: High CPU (75%)**
```
CPU Limit: 75%
```
**Use Case:** Data processing, calculations, CPU-intensive tasks

**Example 4: Maximum CPU (100%)**
```
CPU Limit: 100%
```
**Use Case:** Heavy computations, video encoding, scientific calculations

#### How CPU Limit Works

- **50% CPU Limit** means the container can use up to half of one CPU core
- If you have 4 CPU cores, 50% = 2 cores maximum
- CPU is shared fairly among all running containers
- CPU limits are "soft" limits - containers can briefly exceed them during spikes

#### Resource Monitoring in Mini Docker

Mini Docker displays real-time resource usage for all containers:

**Available Resource Information:**
- **Memory Usage**: Shows current RAM usage vs. limit (e.g., "45 MB / 100 MB")
- **CPU Usage**: Shows current CPU percentage (e.g., "12.5%")
- **Uptime**: Shows how long the container has been running (e.g., "2m 30s")
- **PID**: Process ID for system monitoring
- **Status**: Current container state (Running, Stopped, Paused, etc.)
- **Last Started**: Timestamp of when container was last started

**Where to View Resources:**
1. **Container Table**: Check the "Resources" column for memory/CPU limits
2. **CPU % Column**: Monitor real-time CPU usage percentage
3. **Uptime Column**: See how long containers have been running
4. **Container Logs**: View detailed resource information in logs

**Example Resource Display in UI:**
```
Resources: 100MB/50%    (Memory Limit: 100MB, CPU Limit: 50%)
CPU %: 12.5%            (Current CPU usage)
Uptime: 2m 30s          (Running for 2 minutes 30 seconds)
PID: 12345              (Process ID)
Status: Running          (Current state)
```

**Monitoring Tips:**
- Monitor CPU % to see if containers are hitting their limits
- Check memory usage to ensure containers aren't running out of RAM
- Use uptime to track container stability
- View logs for detailed resource consumption patterns

#### What Happens if Limit is Exceeded?

- Container's CPU usage is throttled (slowed down)
- Tasks take longer to complete
- System remains stable (unlike memory limits)

**Recommendation:** 
- **Light tasks**: 25-50%
- **Normal tasks**: 50-75%
- **Heavy tasks**: 75-100%

---

## 📁 Rootfs Explained

### What is Rootfs?

**Rootfs** (Root File System) is the container's isolated file system. It's like a separate hard drive for your container.

**Think of it like this:**
- Your computer has folders: `C:\`, `D:\`, etc.
- The container has its own root folder: `/` (rootfs)
- They are completely separate!

### Why Rootfs?

1. **Isolation**: Container can't access your files (security)
2. **Clean Environment**: Each container starts fresh
3. **Portability**: Container works the same on any machine
4. **Reproducibility**: Same filesystem = same behavior

### Rootfs Structure

When you create a container, Mini Docker creates this structure:

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

### What's Inside Rootfs?

#### `/bin/` - Executables
Contains basic commands like `sh`, `ls`, `cat`, etc.

#### `/etc/` - Configuration
Contains system configuration files:
- `/etc/passwd` - User accounts
- `/etc/group` - User groups

#### `/usr/` - User Programs
Contains additional programs and libraries.

#### `/lib/` - Libraries
Contains shared libraries needed by programs.

#### `/tmp/` - Temporary Files
Temporary files created by the container.

#### `/var/` - Variable Data
Data that changes during container operation (logs, etc.).

#### `/proc/` - Process Info
Virtual filesystem showing running processes.

#### `/sys/` - System Info
Virtual filesystem showing system information.

### How Rootfs Works

1. **Container Creation:**
   ```
   You create container "my-app"
   → Mini Docker creates: containers/my-app/rootfs/
   ```

2. **Container Runs:**
   ```
   Command: python -c "print('Hello')"
   → Runs inside: containers/my-app/rootfs/
   → Can only see files in rootfs
   → Cannot access your C:\ drive
   ```

3. **Isolation:**
   ```
   Your Computer: C:\MyFiles\document.txt
   Container Rootfs: /document.txt
   → These are DIFFERENT files!
   → Container cannot see C:\MyFiles\
   ```

### Volume Mounts vs Rootfs

| Feature | Rootfs | Volume Mount |
|---------|--------|--------------|
| **Location** | Inside container only | Shared with host |
| **Persistence** | Deleted with container | Persists on host |
| **Access** | Container only | Both host and container |
| **Purpose** | Isolation | Data sharing |

### Example: Understanding Rootfs

**Scenario:** You create a container named "test"

1. **Rootfs Created:**
   ```
   containers/test/rootfs/
   ```

2. **Your Command:**
   ```
   python -c "with open('/data.txt', 'w') as f: f.write('Hello')"
   ```

3. **File Created:**
   ```
   containers/test/rootfs/data.txt
   ```

4. **On Your Computer:**
   - You CANNOT see this file in `C:\`
   - It only exists in the container's rootfs
   - If you delete the container, this file is deleted too

5. **With Volume Mount:**
   ```
   Volume: C:\MyData:/data
   Command: python -c "with open('/data/data.txt', 'w') as f: f.write('Hello')"
   ```
   - File created: `C:\MyData\data.txt` (on your computer!)
   - Also accessible in container as `/data/data.txt`
   - Persists even if container is deleted

---

## 🎯 Complete Example

### Creating a Container with All Features

**Container Name:** `my-app`

**Command:**
```
python -c "import os, time; print(f'Mode: {os.environ.get(\"MODE\", \"not set\")}'); time.sleep(10)"
```

**⚠️ Important:** Always use quotes around environment variable names:
- ✅ Correct: `os.environ.get("MODE")` or `os.environ.get('MODE')`
- ❌ Wrong: `os.environ.get(MODE)`  # This causes NameError!

**Memory Limit:** `100 MB`

**CPU Limit:** `50%`

**Volume Mounts:**
```
C:\MyData:/app/data
C:\Logs:/var/log
```

**Environment Variables:**
```
MODE=production
DEBUG=false
PORT=8080
```

**What Happens:**
1. Container is created with rootfs at `containers/my-app/rootfs/`
2. Memory limited to 100 MB
3. CPU limited to 50%
4. `C:\MyData` is accessible as `/app/data` in container
5. `C:\Logs` is accessible as `/var/log` in container
6. Environment variables `MODE`, `DEBUG`, `PORT` are available
7. Command runs with these settings

---

## 💡 Quick Reference

### Command Examples
- Simple: `python -c "print('Hello')"`
- With sleep: `python -c "import time; time.sleep(5)"`
- Web server: `python -m http.server 8000`
- File ops: `python -c "open('file.txt', 'w').write('data')"`

### Volume Mount Format
```
Windows Path:Container Path
C:\MyData:/app/data
```

### Environment Variable Format
```
KEY=VALUE
MODE=production
```

### Resource Limits
- **Memory**: 50-1024 MB (typical: 100-512 MB)
- **CPU**: 25-100% (typical: 50-75%)

### Rootfs
- Location: `containers/<name>/rootfs/`
- Purpose: Isolated filesystem for container
- Deleted when container is deleted

---

## ❓ Common Questions

**Q: Can I access files from my computer in the container?**
A: Yes! Use volume mounts to share folders.

**Q: What happens to files created in rootfs?**
A: They stay in rootfs and are deleted when container is deleted.

**Q: How much memory should I allocate?**
A: Start with 100 MB, increase if needed.

**Q: Can I change limits after creating container?**
A: No, you need to recreate the container with new limits.

**Q: Do environment variables persist?**
A: Yes, they're saved with container metadata.

---

*This guide covers all the essential concepts for using Mini Docker effectively!*

