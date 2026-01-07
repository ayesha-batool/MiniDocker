"""Networking support for Mini Docker containers"""
import subprocess
import platform
import os
import socket
import ipaddress

class ContainerNetwork:
    """Manage container networking"""
    
    def __init__(self):
        self.bridge_name = "minidocker0"
        self.bridge_ip = "172.17.0.1"
        self.containers = {}  # container_name -> {'ip': '...', 'ports': [...], 'netns': '...', 'veth_host': '...', 'veth_container': '...'}
        self.port_bindings = {}  # host_port -> container_name
        self.is_linux = platform.system() == "Linux"
        self.next_ip = 2  # Start from 172.17.0.2
    
    def setup_bridge(self):
        """Setup bridge network (Linux only)"""
        if not self.is_linux:
            return False
        
        try:
            # Check if bridge exists
            result = subprocess.run(["ip", "link", "show", self.bridge_name], 
                                  capture_output=True)
            if result.returncode != 0:
                # Create bridge
                subprocess.run(["ip", "link", "add", self.bridge_name, "type", "bridge"], 
                             check=True)
                subprocess.run(["ip", "addr", "add", f"{self.bridge_ip}/16", 
                              "dev", self.bridge_name], check=True)
                subprocess.run(["ip", "link", "set", self.bridge_name, "up"], check=True)
            return True
        except Exception as e:
            print(f"[Network] Error setting up bridge: {e}")
            return False
    
    def get_container_ip(self, container_name):
        """Get IP address of container"""
        if container_name in self.containers:
            return self.containers[container_name].get('ip')
        return None
    
    def can_communicate(self, container1, container2):
        """Check if two containers can communicate (same bridge network)"""
        if container1 in self.containers and container2 in self.containers:
            return True  # Both on same bridge
        return False
    
    def allocate_ip(self, container_name):
        """Allocate IP address for container"""
        # Simple IP allocation: 172.17.0.X
        ip = f"172.17.0.{self.next_ip}"
        self.next_ip += 1
        if self.next_ip > 254:
            self.next_ip = 2  # Wrap around
        return ip
    
    def setup_network_namespace(self, container_name, container_pid=None):
        """Create network namespace for container"""
        if not self.is_linux:
            return False
        
        try:
            # Create network namespace
            netns_name = f"minidocker_{container_name}"
            result = subprocess.run(["ip", "netns", "add", netns_name], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Create veth pair
                veth_host = f"veth_{container_name}_host"
                veth_container = f"veth_{container_name}_container"
                
                # Create veth pair
                subprocess.run(["ip", "link", "add", veth_host, "type", "veth", 
                              "peer", "name", veth_container], check=True)
                
                # Move container end to namespace
                subprocess.run(["ip", "link", "set", veth_container, 
                              "netns", netns_name], check=True)
                
                # Setup bridge if needed
                self.setup_bridge()
                
                # Add host end to bridge
                subprocess.run(["ip", "link", "set", veth_host, "master", 
                              self.bridge_name], check=True)
                subprocess.run(["ip", "link", "set", veth_host, "up"], check=True)
                
                # Configure container end in namespace
                ip = self.allocate_ip(container_name)
                subprocess.run(["ip", "netns", "exec", netns_name,
                              "ip", "addr", "add", f"{ip}/16", "dev", veth_container], check=True)
                subprocess.run(["ip", "netns", "exec", netns_name,
                              "ip", "link", "set", veth_container, "up"], check=True)
                subprocess.run(["ip", "netns", "exec", netns_name,
                              "ip", "link", "set", "lo", "up"], check=True)
                
                # Store networking info
                if container_name not in self.containers:
                    self.containers[container_name] = {}
                self.containers[container_name].update({
                    'ip': ip,
                    'netns': netns_name,
                    'veth_host': veth_host,
                    'veth_container': veth_container
                })
                
                return True
        except Exception as e:
            print(f"[Network] Error setting up network namespace: {e}")
            return False
    
    def cleanup_network_namespace(self, container_name):
        """Cleanup network namespace for container"""
        if not self.is_linux:
            return
        
        try:
            if container_name in self.containers:
                info = self.containers[container_name]
                
                # Remove veth pair
                if 'veth_host' in info:
                    try:
                        subprocess.run(["ip", "link", "delete", info['veth_host']], 
                                      capture_output=True)
                    except:
                        pass
                
                # Remove network namespace
                if 'netns' in info:
                    try:
                        subprocess.run(["ip", "netns", "delete", info['netns']], 
                                      capture_output=True)
                    except:
                        pass
        except Exception as e:
            print(f"[Network] Error cleaning up network namespace: {e}")
    
    def bind_ports(self, container_name, ports):
        """Bind host ports to container ports"""
        # Check for port collisions
        for host_port, container_port in ports:
            if host_port in self.port_bindings:
                raise ValueError(f"Port {host_port} already in use by container {self.port_bindings[host_port]['container']}")
            if not self.check_port_available(host_port):
                raise ValueError(f"Port {host_port} is already in use on the host")
        
        # Bind ports
        for host_port, container_port in ports:
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

