# Mini Docker

> **A simple containerization tool for learning how containers work**

Mini Docker is a simplified version of Docker that helps you understand how containers work. It's perfect for beginners who want to learn about containerization without the complexity of real Docker.

---

## What is Mini Docker?

Think of Mini Docker as a **lightweight version of Docker** that's easier to understand. Just like Docker, it lets you:

- **Run programs in isolated environments** (containers)
- **Limit how much memory and CPU** each container can use
- **Share files** between your computer and containers
- **Manage multiple containers** easily

**The main difference?** Mini Docker is simpler and designed for learning, not for production use.

---

## Quick Start

### Step 1: Install Python

Make sure you have Python 3.7 or higher installed on your computer.

**Check if you have Python:**
```bash
python --version
```

If you don't have Python, download it from [python.org](https://www.python.org/downloads/)

### Step 2: Install Dependencies

Open a terminal/command prompt in the project folder and run:

```bash
pip install -r requirements.txt
```

This installs all the necessary Python packages.

### Step 3: Start Mini Docker

Run this command:

```bash
python main.py
```

### Step 4: Open the Dashboard

Open your web browser and go to:

**http://localhost:5000**

You'll see a web interface where you can create and manage containers!

---

## How to Use

### Creating Your First Container

1. **Open the dashboard** at http://localhost:5000
2. Click on **"Create Container"** tab
3. Fill in the details:
   - **Container Name**: Give it a name (e.g., "my-first-container")
   - **Command**: What to run (e.g., `python -c "print('Hello World!')"`)
   - **Memory Limit**: How much RAM to use (e.g., 100 MB)
   - **CPU Limit**: How much CPU to use (e.g., 50%)
4. Click **"Create Container"**
5. Select your container and click **"Start"**

That's it! Your container is now running!

### Example Commands

Here are some simple commands you can run in containers:

**Print a message:**
```
python -c "print('Hello from Mini Docker!')"
```

**Count numbers:**
```
python -c "for i in range(1, 11): print(f'Number {i}')"
```

**Create a file:**
```
python -c "with open('test.txt', 'w') as f: f.write('Hello!'); print('File created!')"
```

**Run a web server:**
```
python -m http.server 8000
```
*(Note: This will run until you stop it)*

### Managing Containers

- **Start**: Start a stopped container
- **Stop**: Stop a running container
- **Pause**: Pause a container (freeze it)
- **Resume**: Resume a paused container
- **Restart**: Restart a container
- **View Logs**: See what the container printed
- **View Stats**: See detailed container statistics and resource usage
- **Export**: Export container configuration to reuse later
- **Exec**: Execute commands inside a running container (Linux only)
- **Delete**: Delete a container (removes all its data)

---

## What Can You Do?

### 1. Share Files (Volume Mounts)

Volume mounts let you share folders between your computer and the container. This means:
- Files you create on your computer appear in the container
- Files created in the container appear on your computer
- Changes are saved permanently (even after container is deleted)

#### Step-by-Step Guide:

**Step 1: Create a folder on your computer**
- Create a folder anywhere, for example: `C:\MyData` or `D:\Projects\MyApp`
- You can put any files you want in this folder

**Step 2: Create a container**
- Go to the "Create Container" tab
- Fill in the basic details (name, command, etc.)

**Step 3: Add volume mount**
- Click **"Advanced Options"**
- Click **"+ Add Volume"**
- Enter the volume in this format: `YourComputerPath:ContainerPath`
  - Example: `C:\MyData:/app/data`
  - Left side (`C:\MyData`) = folder on your computer
  - Right side (`/app/data`) = where it appears inside the container

**Step 4: Use the shared folder in your command**
- In your container command, access files at the container path
- Example: `python -c "with open('/app/data/output.txt', 'w') as f: f.write('Hello!')"`
- This will create `output.txt` in your `C:\MyData` folder!

#### Examples:

**Example 1: Share a data folder**
- **Your computer:** `C:\MyData`
- **Container path:** `/app/data`
- **Volume mount:** `C:\MyData:/app/data`
- **Command:** `python -c "import os; print(os.listdir('/app/data'))"`
- This lists all files in your `C:\MyData` folder!

**Example 2: Share a project folder**
- **Your computer:** `D:\MyProject`
- **Container path:** `/app`
- **Volume mount:** `D:\MyProject:/app`
- **Command:** `python -c "with open('/app/result.txt', 'w') as f: f.write('Done!')"`
- Creates `result.txt` in your `D:\MyProject` folder!

**Example 3: Share multiple folders**
You can add multiple volumes:
- `C:\Data:/app/data`
- `C:\Logs:/var/log`
- `C:\Config:/etc/config`

#### Important Tips:

**Do this:**
- Create the folder on your computer BEFORE creating the container
- Use full paths: `C:\MyData` not `MyData`
- Use forward slashes or backslashes: `C:\MyData` or `C:/MyData` both work

**Don't do this:**
- Don't use relative paths like `./data` (use full paths)
- Don't mount system folders like `C:\Windows` (can cause problems)
- Don't forget the colon (`:`) between paths

#### Real-World Example:

Let's say you want to process files from your computer:

1. **Create folder:** `C:\Documents\ToProcess`
2. **Put some files** in that folder (e.g., `file1.txt`, `file2.txt`)
3. **Create container with:**
   - Name: `file-processor`
   - Command: `python -c "import os; files = os.listdir('/app/files'); print(f'Found {len(files)} files: {files}')"`
   - Volume: `C:\Documents\ToProcess:/app/files`
4. **Start the container**
5. **Result:** The container will list all files from your `C:\Documents\ToProcess` folder!

### 2. Use Environment Variables

Environment variables are like settings or configuration that your program can read. Think of them as notes you pass to your program.

#### What are Environment Variables?

Environment variables are key-value pairs (like `KEY=VALUE`) that your program can access. They're useful for:
- **Configuration**: Change how your program behaves without changing code
- **Secrets**: Store passwords or API keys (though Mini Docker is for learning, not production)
- **Settings**: Pass different settings for different environments

#### How to Add Environment Variables:

1. Click **"Advanced Options"** when creating a container
2. Click **"+ Add Variable"**
3. Enter in format: `KEY=VALUE`
   - Example: `MODE=production`
   - Example: `DEBUG=true`
   - Example: `PORT=8080`

#### How to Use in Your Code:

**In Python:**
```python
import os

# Get an environment variable
mode = os.environ.get('MODE')  # Returns 'production' if MODE=production
port = os.environ.get('PORT', '8000')  # Returns '8000' if PORT not set

# Use it in your program
if mode == 'production':
    print('Running in production mode')
```

**Important:** Always use quotes around the variable name in Python:
- Correct: `os.environ.get('MODE')` or `os.environ.get("MODE")`
- Wrong: `os.environ.get(MODE)`  ← This will cause a NameError!

#### Common Examples:

**Example 1: Application Mode**
- Variable: `MODE=production`
- Code: `os.environ.get('MODE')` → Returns `'production'`

**Example 2: Debug Flag**
- Variable: `DEBUG=true`
- Code: `os.environ.get('DEBUG')` → Returns `'true'`

**Example 3: Port Number**
- Variable: `PORT=8080`
- Code: `int(os.environ.get('PORT', '8000'))` → Returns `8080`

**Example 4: Database URL**
- Variable: `DATABASE_URL=localhost:5432`
- Code: `os.environ.get('DATABASE_URL')` → Returns `'localhost:5432'`

#### Multiple Environment Variables:

You can add as many as you need:
```
MODE=production
DEBUG=false
PORT=8080
API_KEY=abc123
```

Your program can read all of them:
```python
import os
mode = os.environ.get('MODE')
debug = os.environ.get('DEBUG')
port = os.environ.get('PORT')
api_key = os.environ.get('API_KEY')
```

### 3. Set Resource Limits

Resource limits control how much of your computer's resources (memory and CPU) each container can use. This prevents one container from using all your computer's power.

#### Memory Limit (RAM)

**What it does:**
- Controls how much RAM (memory) the container can use
- If the container tries to use more, it will be stopped
- Measured in Megabytes (MB)

**How to choose:**
- **Small scripts** (simple Python commands): 50-100 MB
- **Web servers**: 100-512 MB
- **Data processing**: 256-1024 MB
- **Heavy applications**: 512-2048 MB

**Example:**
- Set to 100 MB for a simple script
- Set to 512 MB for a web server
- Set to 1024 MB (1 GB) for heavy processing

**What happens if limit is exceeded?**
- The container will be stopped automatically
- You'll see an error in the logs
- The container status will show "Stopped"

#### CPU Limit

**What it does:**
- Controls how much processing power (CPU) the container can use
- Expressed as a percentage
- Prevents one container from slowing down your computer

**Understanding percentages:**
- **25%**: Quarter of one CPU core (good for background tasks)
- **50%**: Half of one CPU core (normal for most programs)
- **75%**: Three-quarters of one CPU core (for heavy tasks)
- **100%**: Full use of one CPU core (maximum for single core)
- **200%**: Full use of two CPU cores (if you have multiple cores)

**How to choose:**
- **Background tasks**: 25-50%
- **Normal programs**: 50-75%
- **Heavy computations**: 75-100%
- **Very intensive tasks**: 100-200% (if you have multiple CPU cores)

**Example:**
- Set to 25% for a simple script
- Set to 50% for a web server
- Set to 100% for video processing

**What happens if limit is exceeded?**
- The container's tasks will run slower (throttled)
- Your computer stays responsive
- The container doesn't stop, just runs slower

#### Tips for Setting Limits:

**Do this:**
- Start with lower limits and increase if needed
- Check your computer's available resources first
- Leave some resources for your operating system
- Monitor container usage in the dashboard

**Don't do this:**
- Don't set limits higher than your computer has
- Don't allocate all resources to one container
- Don't forget that your OS needs resources too

---

## Understanding Rootfs (Root File System)

### What is Rootfs?

**Rootfs** (Root File System) is the container's isolated file system. Think of it as a **separate hard drive** that belongs only to your container.

### Simple Explanation:

Imagine your computer has folders like `C:\`, `D:\`, etc. A container has its own root folder called `/` (rootfs). They are completely separate!

**Real-world analogy:**
- Your computer = Your house with your rooms
- Container rootfs = A separate apartment with its own rooms
- They don't share anything unless you explicitly connect them (via volume mounts)

### Where is Rootfs Located?

When you create a container named "my-container", Mini Docker creates:
```
containers/
└── my-container/
    └── rootfs/
        ├── bin/          # Executable programs
        ├── etc/          # Configuration files
        ├── usr/          # User programs
        ├── lib/          # Libraries
        ├── tmp/          # Temporary files
        ├── var/          # Variable data
        └── ...           # Other system directories
```

### What's Inside Rootfs?

**bin/**: Basic executable programs (like `sh`, `ls`, `cat`)
- These are the commands your container can run

**etc/**: Configuration files
- System settings and configuration
- User accounts information

**usr/**: Additional programs and libraries
- Extra software and tools

**lib/**: Shared libraries
- Code libraries that programs need to run

**tmp/**: Temporary files
- Files that are created temporarily
- Usually cleared when container stops

**var/**: Variable data
- Data that changes during container operation
- Logs and other changing information

### How Rootfs Works:

1. **Isolation**: 
   - Files you create in rootfs are isolated from your computer
   - Your computer can't see files in rootfs (unless you use volume mounts)
   - Container can't see files on your computer (unless you use volume mounts)

2. **Persistence**:
   - Files in rootfs persist while container exists
   - When you delete container, rootfs is deleted too
   - This is why volume mounts are important for important data!

3. **Clean Environment**:
   - Each container starts with a fresh rootfs
   - No leftover files from previous runs
   - Predictable and reproducible

### Rootfs vs Volume Mounts:

| Feature | Rootfs | Volume Mount |
|---------|--------|--------------|
| **Location** | Inside container only | Shared with your computer |
| **Persistence** | Deleted when container deleted | Stays on your computer |
| **Access** | Container only | Both container and your computer |
| **Purpose** | Isolation | Data sharing |
| **When to use** | Temporary files, container-specific data | Important data, files you want to keep |

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
   - Volume: `C:\MyData:/data`
   - Command: `python -c "with open('/data/data.txt', 'w') as f: f.write('Hello')"`
   - File created: `C:\MyData\data.txt` (on your computer!)
   - Also accessible in container as `/data/data.txt`
   - Persists even if container is deleted

### Important Points:

- **Rootfs is isolated**: Container files stay in rootfs, not on your computer
- **Use volume mounts for important data**: Rootfs is deleted when container is deleted
- **Each container has its own rootfs**: Containers don't share rootfs
- **Rootfs is temporary**: Designed for container-specific files, not permanent storage

### Viewing Rootfs:

You can view your container's rootfs by:
1. Going to the `containers/` folder in the project directory
2. Opening the folder with your container's name
3. Looking inside the `rootfs/` folder

**Note:** On Windows, you can use the "Open Rootfs" button in the dashboard to open the folder in File Explorer.

---

## Understanding Container States

Containers can be in different states. Understanding these helps you manage them better:

### Container States:

1. **Created**
   - Container is created but not started yet
   - No program is running
   - Ready to be started

2. **Running**
   - Container is active and running your program
   - Program is executing
   - Using resources (memory/CPU)

3. **Stopped**
   - Container was running but is now stopped
   - Program has finished or was stopped
   - Not using any resources
   - Data is still saved

4. **Paused**
   - Container is frozen (temporarily stopped)
   - Program is paused but not terminated
   - Can be resumed exactly where it was
   - Still using some memory

5. **Error**
   - Something went wrong
   - Check logs to see what happened
   - May need to fix the command or settings

### What Happens When:

**Container finishes its command:**
- State changes from "Running" to "Stopped"
- This is normal! The program completed successfully

**You stop a container:**
- State changes from "Running" to "Stopped"
- Program is terminated
- All data is saved

**You pause a container:**
- State changes from "Running" to "Paused"
- Program is frozen but not killed
- Can resume later

**Container runs out of memory:**
- State changes to "Stopped" or "Error"
- Check logs to see the error
- Increase memory limit if needed

---

## Working with Logs

Logs show you everything your container printed or any errors that occurred.

### How to View Logs:

1. **In the Dashboard:**
   - Click on your container
   - Click **"View Logs"** button
   - A window will show all the logs

2. **What You'll See:**
   - All output from your program
   - Error messages (if any)
   - Timestamps
   - Container information

### Understanding Logs:

**Normal Output:**
```
=== Container abc123 started at 2026-01-06 12:00:00 ===
Command: python -c "print('Hello')"
Hello
=== Container exited with code 0 ===
```

**Error Output:**
```
=== Container abc123 started at 2026-01-06 12:00:00 ===
Command: python -c "print('Hello')"
Traceback (most recent call last):
  File "<string>", line 1
    print('Hello')
    ^
SyntaxError: invalid syntax
=== Container exited with code 1 ===
```

**Exit Codes:**
- **0**: Success (program completed normally)
- **1 or higher**: Error (something went wrong)

### Tips for Logs:

- **Check logs when container stops unexpectedly** - They show why
- **Logs are saved** - Even after container stops, logs remain
- **Large outputs** - If your program prints a lot, logs can get long
- **Clear logs** - Delete and recreate container to clear logs

---

## Common Examples

### Example 1: Simple Script

**Container Name:** `hello-world`  
**Command:** `python -c "print('Hello from Mini Docker!')"`  
**Memory:** 50 MB  
**CPU:** 25%

This will print a message and exit immediately.

### Example 2: Web Server

**Container Name:** `web-server`  
**Command:** `python -m http.server 8000`  
**Memory:** 100 MB  
**CPU:** 50%

This starts a web server on port 8000. It will keep running until you stop it.

### Example 3: With Environment Variables

**Container Name:** `my-app`  
**Command:** `python -c "import os; print(f'Mode: {os.environ.get(\"MODE\")}')"`  
**Memory:** 100 MB  
**CPU:** 50%  
**Environment Variables:** `MODE=production`

This will print "Mode: production" because we set the MODE variable.

### Example 4: Sharing Files with Volume Mount

**Container Name:** `file-sharer`  
**Command:** `python -c "with open('/app/data/hello.txt', 'w') as f: f.write('Hello from container!'); print('File created!')"`  
**Memory:** 100 MB  
**CPU:** 50%  
**Volume Mount:** `C:\MyData:/app/data`

**Before running:**
1. Create folder `C:\MyData` on your computer
2. The folder can be empty or have files in it

**After running:**
- The container creates `hello.txt` in `/app/data`
- You'll find `hello.txt` in your `C:\MyData` folder on your computer!
- The file persists even after you delete the container

**To verify:**
- Open `C:\MyData` folder on your computer
- You should see `hello.txt` with the content "Hello from container!"

### Example 5: Processing Files with Volume Mount

**Container Name:** `file-processor`  
**Command:** `python -c "import os; files = [f for f in os.listdir('/app/input') if f.endswith('.txt')]; print(f'Found {len(files)} text files'); [open(f'/app/output/{f}', 'w').write(f'Processed: {f}') for f in files]"`  
**Memory:** 200 MB  
**CPU:** 50%  
**Volume Mounts:** 
- `C:\InputFiles:/app/input`
- `C:\OutputFiles:/app/output`

**What this does:**
- Reads all `.txt` files from `C:\InputFiles`
- Processes them
- Saves results to `C:\OutputFiles`

### Example 6: Web Server with Custom Port

**Container Name:** `my-webserver`  
**Command:** `python -c "import os, http.server, socketserver; port = int(os.environ.get('PORT', 8000)); httpd = socketserver.TCPServer(('', port), http.server.SimpleHTTPRequestHandler); print(f'Server running on port {port}'); httpd.serve_forever()"`  
**Memory:** 100 MB  
**CPU:** 50%  
**Environment Variables:** `PORT=9000`

This starts a web server on port 9000 (instead of default 8000).

### Example 7: Data Analysis with Environment Variables

**Container Name:** `data-analyzer`  
**Command:** `python -c "import os; mode = os.environ.get('MODE', 'normal'); limit = int(os.environ.get('LIMIT', '10')); print(f'Mode: {mode}, Processing {limit} items')"`  
**Memory:** 150 MB  
**CPU:** 75%  
**Environment Variables:** 
- `MODE=fast`
- `LIMIT=100`

This shows how to use multiple environment variables together.

---

## Understanding the Dashboard

The Mini Docker dashboard is your control center for managing containers. Here's what everything means:

### Main Sections:

1. **Container List Tab**
   - Shows all your containers
   - See their status, resources, and information
   - Select containers to manage them

2. **Create Container Tab**
   - Form to create new containers
   - Fill in name, command, and limits
   - Advanced options for volumes and environment variables

### Container Information Displayed:

- **Container ID**: Unique identifier (first 12 characters shown)
- **Name**: The name you gave it
- **Status**: Current state (Running, Stopped, Paused, etc.)
- **Command**: What the container runs
- **Resources**: Memory and CPU limits
- **CPU %**: Current CPU usage (if running)
- **Uptime**: How long it's been running
- **Last Started**: When it was last started

### Action Buttons:

- **Start**: Makes a stopped container run
- **Stop**: Stops a running container
- **Pause**: Freezes a running container
- **Resume**: Unfreezes a paused container
- **Restart**: Stops and starts again
- **View Logs**: Shows all output and errors
- **Delete**: Permanently removes container

### Tips for Using Dashboard:

- **Select multiple containers** - Click checkboxes to select several at once
- **Real-time updates** - Status updates automatically every few seconds
- **Color coding** - Different colors show different states
- **Context menu** - Right-click (or long-press) for quick actions

---

## Common Mistakes and How to Avoid Them

### Mistake 1: Forgetting Quotes in Python Commands

**Wrong:**
```
python -c "print(os.environ.get(MODE))"
```

**Right:**
```
python -c "print(os.environ.get('MODE'))"
```

**Why:** Python needs quotes around string literals. Without quotes, Python thinks `MODE` is a variable name, not a string.

### Mistake 2: Using Relative Paths for Volumes

**Wrong:**
```
./data:/app/data
```

**Right:**
```
C:\MyData:/app/data
```

**Why:** Use full absolute paths. Relative paths can cause confusion about where files actually are.

### Mistake 3: Setting Resource Limits Too High

**Wrong:**
- Memory: 10000 MB (on a computer with only 8 GB RAM)
- CPU: 500% (on a computer with only 4 cores)

**Right:**
- Memory: 100-1000 MB (depending on your computer)
- CPU: 25-200% (depending on your CPU cores)

**Why:** Setting limits higher than your computer has can cause problems or prevent the container from starting.

### Mistake 4: Not Creating Volume Folders First

**Wrong:**
- Adding volume `C:\NewFolder:/app/data` without creating `C:\NewFolder` first

**Right:**
- Create `C:\NewFolder` on your computer first
- Then add it as a volume

**Why:** The folder needs to exist before the container can use it.

### Mistake 5: Expecting Container to Keep Running

**Wrong:**
- Running `python -c "print('Hello')"` and expecting it to stay running

**Right:**
- For long-running programs, use commands that don't exit immediately
- Example: `python -m http.server 8000` (keeps running)

**Why:** Containers stop when their command finishes. Simple print commands finish immediately.

### Mistake 6: Not Checking Logs When Something Fails

**Wrong:**
- Container shows "Error" but you don't check logs

**Right:**
- Always click "View Logs" when something goes wrong
- Logs show exactly what went wrong

**Why:** Logs contain error messages that tell you what to fix.

---

## Best Practices

### 1. Naming Containers

**Good names:**
- `my-web-server`
- `data-processor`
- `test-container-1`

**Bad names:**
- `container` (too generic)
- `test` (not descriptive)
- `abc123` (not meaningful)

**Tip:** Use descriptive names that tell you what the container does.

### 2. Resource Management

**Do:**
- Start with lower limits and increase if needed
- Monitor resource usage in dashboard
- Stop containers you're not using

**Don't:**
- Set limits too high
- Leave many containers running unnecessarily
- Ignore resource warnings

### 3. Organizing Files

**Do:**
- Use volume mounts for important data
- Organize volume folders logically
- Keep container commands simple

**Don't:**
- Store important data only in containers (use volumes)
- Create containers with very long commands (use scripts instead)
- Mix different purposes in one container

### 4. Testing and Debugging

**Do:**
- Test commands in a simple container first
- Check logs regularly
- Start with simple examples

**Don't:**
- Create complex containers without testing
- Ignore error messages
- Skip reading logs when things fail

---

## Frequently Asked Questions

**Q: What's the difference between Mini Docker and Docker?**  
A: Mini Docker is simpler and designed for learning. Real Docker is more powerful but also more complex.

**Q: Can I use this for real projects?**  
A: No, Mini Docker is for learning only. Use real Docker for actual projects.

**Q: Why does my container show "Stopped"?**  
A: Containers stop when their command finishes. If you run a script that prints something and exits, the container will stop automatically.

**Q: How do I see what my container printed?**  
A: Click **"View Logs"** on your container to see all its output.

**Q: Can I run multiple containers at once?**  
A: Yes! You can create and run as many containers as you want.

**Q: What happens when I delete a container?**  
A: All the container's data, files, and logs are permanently deleted. However, files in volume-mounted folders are NOT deleted (they stay on your computer).

**Q: How do I share files between my computer and container?**  
A: Use volume mounts! Create a folder on your computer, then add it as a volume when creating the container. Format: `YourComputerPath:ContainerPath` (e.g., `C:\MyData:/app/data`).

**Q: Can I access files from my computer inside the container?**  
A: Yes! Use volume mounts. Files in the mounted folder are accessible inside the container at the path you specify.

**Q: What happens to files in volume mounts when I delete the container?**  
A: Files in volume-mounted folders stay on your computer. Only files created inside the container (not in mounted folders) are deleted.

**Q: Why did my container stop immediately?**  
A: Your command probably finished executing. Commands like `print('Hello')` finish quickly. Use commands that keep running (like web servers) if you want the container to stay active.

**Q: Can I change container settings after creating it?**  
A: No, you need to delete and recreate the container with new settings. Containers are immutable (can't be changed after creation).

**Q: How do I know if my container is using too much memory?**  
A: Check the CPU % in the dashboard. If it's consistently high, your container might be working hard. Check logs for memory-related errors.

**Q: Can I run the same container multiple times?**  
A: No, each container name must be unique. But you can create multiple containers with the same command but different names.

**Q: What's the difference between Pause and Stop?**  
A: Pause freezes the container temporarily (can resume exactly where it was). Stop terminates the program completely (starts fresh when restarted).

**Q: How do I see what resources my container is using?**  
A: Look at the dashboard - it shows CPU % and you can see memory usage in the logs. The dashboard updates in real-time.

**Q: Can I use Mini Docker on a Mac?**  
A: Yes, but it runs in simulation mode (like Windows). Full features work best on Linux.

**Q: What if my container command has errors?**  
A: Check the logs! They show the exact error message. Fix the command and recreate the container.

**Q: How many containers can I run at once?**  
A: As many as your computer can handle! Just make sure you don't exceed your total memory and CPU.

---

## Requirements

- **Python 3.7 or higher**
- **Windows, Linux, or Mac**
- **Web browser** (Chrome, Firefox, Edge, etc.)

**Note:** On Windows, Mini Docker runs in "simulation mode" which means some advanced features work differently than on Linux.

---

## Project Structure

```
Mini Docker/
├── main.py              # Start the web server
├── container.py         # Container logic
├── web_server.py        # Web interface backend
├── templates/           # Web page templates
├── static/              # CSS and JavaScript
└── containers/          # Your containers are stored here
```

---

## Learning Resources

### What is a Container?

Think of a container like a **small, isolated room** for your program:
- Your program runs inside this "room"
- It can't see or affect other programs outside
- It has its own "space" (filesystem)
- You control how much "resources" (memory/CPU) it can use

**Real-world analogy:**
- Your computer = A big apartment building
- Container = One apartment in the building
- Each apartment is separate and isolated
- But they all share the building's infrastructure (electricity, water = your computer's resources)

### Why Use Containers?

1. **Isolation**
   - Programs can't interfere with each other
   - If one crashes, others keep running
   - Security: programs can't access each other's data

2. **Portability**
   - Same container works on different computers
   - Easy to share and move between systems
   - Consistent environment everywhere

3. **Resource Control**
   - Limit how much memory/CPU each container uses
   - Prevent one program from slowing down your computer
   - Better resource management

4. **Easy Management**
   - Start, stop, pause containers easily
   - Delete containers when done
   - Clean up is simple

### Key Concepts Explained:

**Container:**
- An isolated environment running a program
- Like a virtual box that holds your application
- Has its own filesystem and settings

**Image:**
- A template for creating containers
- Like a blueprint or recipe
- In Mini Docker, we use a default image

**Volume:**
- A way to share files between your computer and container
- Like a shared folder
- Files persist even after container is deleted

**Environment Variable:**
- A setting or configuration value
- Like a note you pass to your program
- Your program can read these values

**Resource Limits:**
- Controls on how much memory/CPU a container can use
- Like setting a budget
- Prevents containers from using too much

**Logs:**
- All output and messages from your container
- Like a diary of what happened
- Shows errors and normal output

**Rootfs:**
- The container's isolated filesystem
- Like a separate hard drive for your container
- Each container has its own rootfs directory
- Files created in rootfs stay isolated from your computer

---

## Glossary

**Container:** An isolated environment where your program runs

**Dashboard:** The web interface for managing containers

**Environment Variable:** A key-value pair that provides configuration to your program

**Image:** A template used to create containers

**Logs:** All output, messages, and errors from a container

**Memory Limit:** Maximum amount of RAM a container can use

**CPU Limit:** Maximum amount of processing power a container can use

**Volume Mount:** A way to share folders between your computer and container

**Rootfs:** The container's isolated filesystem (root file system) - see detailed explanation below

**Status:** Current state of a container (Running, Stopped, Paused, etc.)

**PID:** Process ID - a unique number identifying a running process

**Namespace:** A way to isolate different aspects of a container (processes, network, etc.)

**cgroup:** Control group - a way to limit and monitor resource usage

---

## Tips and Tricks

### Tip 1: Start Simple

When learning, start with the simplest examples:
1. First: `python -c "print('Hello')"`
2. Then: Add environment variables
3. Then: Add volume mounts
4. Finally: Combine everything

### Tip 2: Use Descriptive Names

Good container names help you remember what they do:
- `my-web-server` (clear purpose)
- `data-processor-v1` (version included)
- `test` (not descriptive)
- `container1` (not meaningful)

### Tip 3: Test Commands First

Before putting a command in a container, test it in your terminal:
```bash
python -c "your command here"
```

If it works in terminal, it will work in container!

### Tip 4: Check Logs Regularly

Logs are your best friend:
- They show what's happening
- They show errors clearly
- They help you debug problems

### Tip 5: Use Volume Mounts for Important Data

Don't store important data only in containers:
- Containers can be deleted
- Use volume mounts to save data on your computer
- Data in volumes persists even after container deletion

### Tip 6: Monitor Resource Usage

Keep an eye on resource usage:
- High CPU % = container is working hard
- Check if limits are appropriate
- Adjust limits based on actual usage

### Tip 7: Clean Up Regularly

Delete containers you're not using:
- Frees up resources
- Keeps dashboard clean
- Prevents confusion

### Tip 8: Read Error Messages

When something fails:
- Read the error message carefully
- It usually tells you what's wrong
- Fix the specific issue mentioned

### Tip 9: Use Environment Variables for Configuration

Instead of hardcoding values:
- Use environment variables
- Easy to change without editing code
- Different values for different containers

### Tip 10: Start with Lower Resource Limits

Better to start low and increase:
- Prevents resource exhaustion
- Easier to identify problems
- Can always increase if needed

---

## Advanced Features

### Container Statistics

View detailed information about your containers:
- **Resource Usage**: Current memory and CPU usage
- **Uptime**: How long the container has been running
- **Restart Count**: How many times it has restarted
- **Health Status**: Current health check status
- **Configuration**: All settings (limits, volumes, env vars, etc.)

**How to view:**
- Click on a container in the dashboard
- Use the context menu (right-click) and select "View Stats"
- Or use the API: `GET /api/containers/<name>/stats`

### Container Export and Import

**Export Container:**
- Save container configuration to reuse later
- Exports: name, command, limits, volumes, environment variables
- Useful for backing up configurations or sharing with others

**Import Container:**
- Create a new container from exported configuration
- Use the API: `POST /api/containers/import` with the exported JSON
- Great for recreating containers with the same settings

**Example Export:**
```json
{
  "name": "my-web-server",
  "command": "python -m http.server 8000",
  "mem_limit_mb": 100,
  "cpu_limit_percent": 50,
  "volumes": ["C:\\Data:/app/data"],
  "env_vars": {"PORT": "8000"},
  "exported_at": "2026-01-06 12:00:00"
}
```

### Container Templates

**What are Templates?**
- Saved container configurations you can reuse
- Quick way to create containers with common settings
- Pre-defined templates for common use cases

**Built-in Templates:**
1. **Python Web Server** - Simple HTTP server
2. **Data Processor** - Example data processing script
3. **File Watcher** - Simple file watching example

**Save Your Own Templates:**
- Create a container with your preferred settings
- Export the container configuration
- Save it as a template for future use

**Use Templates:**
- When creating a container, select a template
- Template fills in the configuration automatically
- You can still modify settings before creating

### Container Exec (Execute Commands)

**What is Exec?**
- Run commands inside a running container
- Like opening a terminal inside the container
- Useful for debugging and inspection

**How to Use:**
- Container must be running
- Use the API: `POST /api/containers/<name>/exec` with command
- Returns the command output

**Example:**
```bash
# Execute a command in running container
POST /api/containers/my-container/exec
Body: {"command": "ls -la /app"}
```

**Note:** Exec is only supported on Linux systems. On Windows, containers run in simulation mode.

### Container Networking Information

View networking details for containers:
- **IP Address**: Container's network IP (if assigned)
- **Port Mappings**: Which ports are mapped
- **Network Mode**: Bridge, host, or none

**How to view:**
- Check container stats for networking information
- Network details shown in the statistics view

---

## Important Notes

- **This is for learning only** - Don't use Mini Docker for real projects
- **Containers are isolated** - Files created inside containers stay in containers
- **Use volume mounts** - If you want to share files, use volume mounts
- **Check resource limits** - Make sure you don't set limits too high for your computer
- **Exec requires Linux** - Container exec feature only works on Linux systems

---

## Troubleshooting

### Problem: Container Won't Start

**Possible causes:**
1. **Command has syntax errors**
   - **Solution:** Check the command syntax, especially quotes
   - **Check:** View logs to see the exact error

2. **Resource limits too high**
   - **Solution:** Lower memory or CPU limits
   - **Check:** Make sure limits are less than your computer's total resources

3. **Volume folder doesn't exist**
   - **Solution:** Create the folder on your computer first
   - **Check:** Verify the folder path is correct

### Problem: Container Stops Immediately

**Possible causes:**
1. **Command finished executing**
   - **Solution:** This is normal! Your command completed successfully
   - **Check:** View logs to see the output

2. **Command has an error**
   - **Solution:** Fix the command syntax or logic
   - **Check:** View logs to see the error message

### Problem: Can't See Files in Volume Mount

**Possible causes:**
1. **Wrong path in container**
   - **Solution:** Make sure you're using the container path (right side of `:`)
   - **Example:** If volume is `C:\Data:/app/data`, use `/app/data` in your command

2. **Folder not created on computer**
   - **Solution:** Create the folder on your computer first
   - **Check:** Verify the folder exists before creating container

### Problem: Environment Variable Not Working

**Possible causes:**
1. **Forgot quotes in Python**
   - **Solution:** Always use quotes: `os.environ.get('MODE')` not `os.environ.get(MODE)`
   - **Check:** Python syntax requires quotes around string literals

2. **Variable name typo**
   - **Solution:** Check spelling matches exactly (case-sensitive)
   - **Check:** Variable name in code must match what you set

### Problem: Dashboard Not Loading

**Possible causes:**
1. **Server not running**
   - **Solution:** Make sure `python main.py` is running
   - **Check:** Look for errors in the terminal

2. **Port already in use**
   - **Solution:** Close other programs using port 5000
   - **Check:** Try a different port or restart your computer

3. **Wrong URL**
   - **Solution:** Use exactly `http://localhost:5000`
   - **Check:** Make sure you're using `http://` not `https://`

### Problem: Container Using Too Much Memory

**Possible causes:**
1. **Memory limit too high**
   - **Solution:** Lower the memory limit
   - **Check:** Start with 100 MB and increase if needed

2. **Program needs more memory**
   - **Solution:** Increase memory limit (if your computer has enough)
   - **Check:** Make sure you have enough RAM available

### Getting More Help:

1. **Check the logs** - Always start here! Logs show what went wrong
2. **Check resource limits** - Make sure they're reasonable
3. **Restart the server** - Stop `main.py` (Ctrl+C) and start again
4. **Check Python version** - Run `python --version` (need 3.7+)
5. **Recreate container** - Sometimes deleting and recreating fixes issues
6. **Check command syntax** - Make sure your command is correct
7. **Test with simple example** - Try the "Hello World" example first

---

## License

This is an educational project - feel free to use it for learning!

---

**Happy Learning!**

*Remember: Mini Docker is designed to help you understand how containers work. Once you're comfortable with it, you can move on to learning real Docker!*
