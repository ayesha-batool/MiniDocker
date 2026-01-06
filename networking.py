"""Networking support for Mini Docker containers"""
import subprocess
import platform
import os
import socket

class ContainerNetwork:
    """Manage container networking"""
    
    def __init__(self):
        self.bridge_name = "minidocker0"
        self.containers = {}  # container_name -> {'ip': '...', 'ports': [...]}
        self.port_bindings = {}  # host_port -> container_name
    
    def setup_bridge(self):
        """Setup bridge network (Linux only)"""
        if platform.system() != "Linux":
            return False
        
        try:
            # Check if bridge exists
            result = subprocess.run(["ip", "link", "show", self.bridge_name], 
                                  capture_output=True)
            if result.returncode != 0:
                # Create bridge
                subprocess.run(["ip", "link", "add", self.bridge_name, "type", "bridge"], 
                             check=True)
                subprocess.run(["ip", "link", "set", self.bridge_name, "up"], check=True)
            return True
        except:
            return False
    
    def allocate_ip(self, container_name):
        """Allocate IP address for container (simplified)"""
        # Simple IP allocation: 172.17.0.X
        base_ip = "172.17.0"
        container_num = len(self.containers) + 1
        ip = f"{base_ip}.{container_num}"
        return ip
    
    def bind_ports(self, container_name, ports):
        """Bind host ports to container ports"""
        # On Windows/WSL, we simulate port binding
        # In real Docker, this uses iptables/port forwarding
        for host_port, container_port in ports:
            if host_port in self.port_bindings:
                raise ValueError(f"Port {host_port} already in use")
            self.port_bindings[host_port] = {
                'container': container_name,
                'container_port': container_port
            }
            self._log(f"Port mapping: {host_port} -> {container_name}:{container_port}")
    
    def release_ports(self, container_name):
        """Release port bindings for container"""
        ports_to_remove = []
        for host_port, binding in self.port_bindings.items():
            if binding['container'] == container_name:
                ports_to_remove.append(host_port)
        
        for port in ports_to_remove:
            del self.port_bindings[port]
    
    def get_container_info(self, container_name):
        """Get networking info for container"""
        return self.containers.get(container_name, {})
    
    def list_port_mappings(self):
        """List all port mappings"""
        return self.port_bindings.copy()
    
    def check_port_available(self, port):
        """Check if a port is available"""
        if port in self.port_bindings:
            return False
        
        # Also check if port is actually listening
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result != 0  # Port is available if connection fails
        except:
            return True
    
    def _log(self, message):
        """Log networking events"""
        print(f"[Network] {message}")

# Global network instance
network = ContainerNetwork()

