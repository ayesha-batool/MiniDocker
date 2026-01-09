"""
Container Manager - Handles container persistence, IDs, and lifecycle
"""
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional

class ContainerManager:
    """Manages container metadata, persistence, and lifecycle"""
    
    def __init__(self, storage_dir="./containers_meta"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.meta_file = os.path.join(storage_dir, "containers.json")
        self.containers = self._load_containers()
    
    def _load_containers(self) -> Dict:
        """Load containers from JSON file"""
        if os.path.exists(self.meta_file):
            try:
                with open(self.meta_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_containers(self):
        """Save containers to JSON file"""
        with open(self.meta_file, 'w') as f:
            json.dump(self.containers, f, indent=2)
    
    def generate_id(self) -> str:
        """Generate a unique container ID (first 12 chars of UUID)"""
        return str(uuid.uuid4())[:12]
    
    def create_container(self, name: str, command: str, image: str = None, 
                        mem_limit: int = 100, cpu_limit: int = 50,
                        volumes: List[str] = None, env_vars: Dict[str, str] = None) -> str:
        """Create a new container entry and return its ID"""
        container_id = self.generate_id()
        
        container_meta = {
            "id": container_id,
            "name": name,
            "command": command,
            "image": image or "default",
            "status": "Created",
            "created_at": datetime.now().isoformat(),
            "started_at": None,
            "stopped_at": None,
            "pid": None,
            "mem_limit_mb": mem_limit,
            "cpu_limit_percent": cpu_limit,
            "volumes": volumes or [],
            "env_vars": env_vars or {},
            "log_file": f"./containers/{name}/container.log"
        }
        
        self.containers[container_id] = container_meta
        self._save_containers()
        return container_id
    
    def update_container(self, container_id: str, **kwargs):
        """Update container metadata"""
        if container_id in self.containers:
            self.containers[container_id].update(kwargs)
            self._save_containers()
    
    def get_container(self, container_id: str) -> Optional[Dict]:
        """Get container metadata by ID"""
        return self.containers.get(container_id)
    
    def get_container_by_name(self, name: str) -> Optional[Dict]:
        """Get container metadata by name"""
        for container in self.containers.values():
            if container.get("name") == name:
                return container
        return None
    
    def list_containers(self, all_containers: bool = False) -> List[Dict]:
        """List containers (running only or all)"""
        if all_containers:
            return list(self.containers.values())
        else:
            return [c for c in self.containers.values() if c.get("status") == "Running"]
    
    def remove_container(self, container_id: str) -> bool:
        """Remove container from metadata by ID"""
        if container_id in self.containers:
            del self.containers[container_id]
            self._save_containers()
            return True
        return False
    
    def remove_container_by_name(self, name: str) -> bool:
        """Remove container from metadata by name"""
        container = self.get_container_by_name(name)
        if container:
            container_id = container["id"]
            return self.remove_container(container_id)
        return False
    
    def get_log_path(self, container_id: str) -> str:
        """Get log file path for container"""
        container = self.get_container(container_id)
        if container:
            return container.get("log_file", f"./containers/{container['name']}/container.log")
        return None


