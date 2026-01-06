#!/usr/bin/env python3
"""
Mini Docker CLI - Command-line interface for container management
Commands: ps, stop, rm, logs, inspect
"""
import sys
import argparse
from container_manager import ContainerManager
from container import SimulatedContainer
from filesystem import FileSystemManager

def cmd_ps(args):
    """List containers (mini-docker ps)"""
    manager = ContainerManager()
    containers = manager.list_containers(all_containers=args.all)
    
    if not containers:
        print("No containers found.")
        return
    
    # Print header
    print(f"{'CONTAINER ID':<15} {'NAME':<20} {'STATUS':<15} {'COMMAND':<40}")
    print("-" * 90)
    
    for container in containers:
        container_id = container["id"][:12]
        name = container.get("name", "N/A")[:20]
        status = container.get("status", "Unknown")[:15]
        command = container.get("command", "N/A")[:40]
        print(f"{container_id:<15} {name:<20} {status:<15} {command:<40}")

def cmd_stop(args):
    """Stop a container (mini-docker stop <id|name>)"""
    manager = ContainerManager()
    container_id = args.container
    
    # Try to find by ID or name
    container = manager.get_container(container_id)
    if not container:
        container = manager.get_container_by_name(container_id)
        if container:
            container_id = container["id"]
    
    if not container:
        print(f"Error: Container '{args.container}' not found.")
        sys.exit(1)
    
    # Load container instance and stop it
    # Note: In a real implementation, we'd need to track running containers
    print(f"Stopping container {container_id[:12]} ({container['name']})...")
    print("Note: Use the dashboard to stop containers, or implement process tracking.")
    # For now, just update status
    manager.update_container(container_id, status="Stopped")
    print(f"Container {container_id[:12]} stopped.")

def cmd_rm(args):
    """Remove a container (mini-docker rm <id|name>)"""
    manager = ContainerManager()
    container_id = args.container
    
    # Try to find by ID or name
    container = manager.get_container(container_id)
    if not container:
        container = manager.get_container_by_name(container_id)
        if container:
            container_id = container["id"]
    
    if not container:
        print(f"Error: Container '{args.container}' not found.")
        sys.exit(1)
    
    if container.get("status") == "Running" and not args.force:
        print(f"Error: Cannot remove running container. Use -f to force.")
        sys.exit(1)
    
    # Remove container filesystem
    fs = FileSystemManager()
    fs.delete_rootfs(container["name"])
    
    # Remove from metadata
    if manager.remove_container(container_id):
        print(f"Container {container_id[:12]} removed.")
    else:
        print(f"Error: Failed to remove container.")
        sys.exit(1)

def cmd_logs(args):
    """View container logs (mini-docker logs <id|name>)"""
    manager = ContainerManager()
    container_id = args.container
    
    # Try to find by ID or name
    container = manager.get_container(container_id)
    if not container:
        container = manager.get_container_by_name(container_id)
        if container:
            container_id = container["id"]
    
    if not container:
        print(f"Error: Container '{args.container}' not found.")
        sys.exit(1)
    
    log_file = container.get("log_file", f"./containers/{container['name']}/container.log")
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
            if args.tail:
                lines = lines[-args.tail:]
            print(''.join(lines))
    except FileNotFoundError:
        print(f"Log file not found: {log_file}")
    except Exception as e:
        print(f"Error reading logs: {e}")

def cmd_inspect(args):
    """Inspect a container (mini-docker inspect <id|name>)"""
    manager = ContainerManager()
    container_id = args.container
    
    # Try to find by ID or name
    container = manager.get_container(container_id)
    if not container:
        container = manager.get_container_by_name(container_id)
        if container:
            container_id = container["id"]
    
    if not container:
        print(f"Error: Container '{args.container}' not found.")
        sys.exit(1)
    
    import json
    print(json.dumps(container, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Mini Docker CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # ps command
    ps_parser = subparsers.add_parser("ps", help="List containers")
    ps_parser.add_argument("-a", "--all", action="store_true", help="Show all containers")
    
    # stop command
    stop_parser = subparsers.add_parser("stop", help="Stop a container")
    stop_parser.add_argument("container", help="Container ID or name")
    
    # rm command
    rm_parser = subparsers.add_parser("rm", help="Remove a container")
    rm_parser.add_argument("container", help="Container ID or name")
    rm_parser.add_argument("-f", "--force", action="store_true", help="Force remove running container")
    
    # logs command
    logs_parser = subparsers.add_parser("logs", help="View container logs")
    logs_parser.add_argument("container", help="Container ID or name")
    logs_parser.add_argument("--tail", type=int, help="Number of lines to show from end")
    
    # inspect command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a container")
    inspect_parser.add_argument("container", help="Container ID or name")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == "ps":
        cmd_ps(args)
    elif args.command == "stop":
        cmd_stop(args)
    elif args.command == "rm":
        cmd_rm(args)
    elif args.command == "logs":
        cmd_logs(args)
    elif args.command == "inspect":
        cmd_inspect(args)

if __name__ == "__main__":
    main()


