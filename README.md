# 🐳 Mini Docker

> **A simple containerization tool for learning how containers work**

Mini Docker is a simplified version of Docker that helps you understand how containers work. It's perfect for beginners who want to learn about containerization without the complexity of real Docker.

---

## 🤔 What is Mini Docker?

Think of Mini Docker as a **lightweight version of Docker** that's easier to understand. Just like Docker, it lets you:

- **Run programs in isolated environments** (containers)
- **Limit how much memory and CPU** each container can use
- **Share files** between your computer and containers
- **Manage multiple containers** easily

**The main difference?** Mini Docker is simpler and designed for learning, not for production use.

---

## 🚀 Quick Start

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

## 📖 How to Use

### Creating Your First Container

1. **Open the dashboard** at http://localhost:5000
2. Click on **"➕ Create Container"** tab
3. Fill in the details:
   - **Container Name**: Give it a name (e.g., "my-first-container")
   - **Command**: What to run (e.g., `python -c "print('Hello World!')"`)
   - **Memory Limit**: How much RAM to use (e.g., 100 MB)
   - **CPU Limit**: How much CPU to use (e.g., 50%)
4. Click **"Create Container"**
5. Select your container and click **"▶️ Start"**

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

- **▶️ Start**: Start a stopped container
- **⏹️ Stop**: Stop a running container
- **⏸️ Pause**: Pause a container (freeze it)
- **▶️ Resume**: Resume a paused container
- **🔄 Restart**: Restart a container
- **📄 View Logs**: See what the container printed
- **🗑️ Delete**: Delete a container (removes all its data)

---

## 💡 What Can You Do?

### 1. Share Files (Volume Mounts)

You can share folders between your computer and the container:

1. Create a folder on your computer (e.g., `C:\MyData`)
2. When creating a container, click **"⚙️ Advanced Options"**
3. Add a volume: `C:\MyData:/app/data`
4. Now files in `C:\MyData` are accessible in the container at `/app/data`

**Example:**
- Host folder: `C:\MyData`
- Container path: `/app/data`
- Volume mount: `C:\MyData:/app/data`

### 2. Use Environment Variables

Environment variables are like settings for your container:

1. Click **"⚙️ Advanced Options"** when creating a container
2. Add environment variables like: `MODE=production` or `DEBUG=true`
3. Your program can read these using: `os.environ.get('MODE')`

**Important:** Always use quotes around the variable name in Python:
- ✅ Correct: `os.environ.get('MODE')`
- ❌ Wrong: `os.environ.get(MODE)`  ← This will cause an error!

### 3. Set Resource Limits

**Memory Limit:**
- Controls how much RAM the container can use
- Typical values: 50-1000 MB
- Example: 100 MB for a simple script, 512 MB for a web server

**CPU Limit:**
- Controls how much processing power the container can use
- Expressed as a percentage (25%, 50%, 75%, 100%)
- Example: 50% means the container can use half of one CPU core

---

## 🎯 Common Examples

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

---

## ❓ Frequently Asked Questions

**Q: What's the difference between Mini Docker and Docker?**  
A: Mini Docker is simpler and designed for learning. Real Docker is more powerful but also more complex.

**Q: Can I use this for real projects?**  
A: No, Mini Docker is for learning only. Use real Docker for actual projects.

**Q: Why does my container show "Stopped"?**  
A: Containers stop when their command finishes. If you run a script that prints something and exits, the container will stop automatically.

**Q: How do I see what my container printed?**  
A: Click **"📄 View Logs"** on your container to see all its output.

**Q: Can I run multiple containers at once?**  
A: Yes! You can create and run as many containers as you want.

**Q: What happens when I delete a container?**  
A: All the container's data, files, and logs are permanently deleted.

---

## 🛠️ Requirements

- **Python 3.7 or higher**
- **Windows, Linux, or Mac**
- **Web browser** (Chrome, Firefox, Edge, etc.)

**Note:** On Windows, Mini Docker runs in "simulation mode" which means some advanced features work differently than on Linux.

---

## 📁 Project Structure

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

## 🎓 Learning Resources

**What is a container?**
- A container is like a lightweight virtual machine
- It runs programs in isolation from your main computer
- Each container has its own filesystem and environment

**Why use containers?**
- **Isolation**: Programs can't interfere with each other
- **Portability**: Same container works on different computers
- **Resource Control**: Limit how much memory/CPU each container uses

**Key Concepts:**
- **Container**: An isolated environment running a program
- **Image**: A template for creating containers
- **Volume**: A way to share files between your computer and container
- **Environment Variable**: A setting that your program can read

---

## ⚠️ Important Notes

- **This is for learning only** - Don't use Mini Docker for real projects
- **Containers are isolated** - Files created inside containers stay in containers
- **Use volume mounts** - If you want to share files, use volume mounts
- **Check resource limits** - Make sure you don't set limits too high for your computer

---

## 🤝 Need Help?

If you encounter any problems:

1. **Check the logs** - Click "View Logs" to see error messages
2. **Check resource limits** - Make sure you have enough memory/CPU available
3. **Restart the server** - Stop `main.py` and start it again
4. **Check Python version** - Make sure you have Python 3.7+

---

## 📝 License

This is an educational project - feel free to use it for learning!

---

**Happy Learning! 🎉**

*Remember: Mini Docker is designed to help you understand how containers work. Once you're comfortable with it, you can move on to learning real Docker!*
