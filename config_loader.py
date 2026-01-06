"""Container configuration file loader for YAML/JSON templates"""
import json
import yaml
import os

class ContainerConfigLoader:
    """Load container configurations from YAML/JSON files"""
    
    @staticmethod
    def load_config(config_path):
        """Load configuration from YAML or JSON file"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.endswith('.yaml') or config_path.endswith('.yml'):
                try:
                    return yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
            elif config_path.endswith('.json'):
                return json.load(f)
            else:
                raise ValueError("Config file must be .yaml, .yml, or .json")
    
    @staticmethod
    def validate_config(config):
        """Validate container configuration"""
        required_fields = ['name', 'command']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Set defaults
        config.setdefault('mem_limit_mb', 100)
        config.setdefault('cpu_limit_percent', 50)
        config.setdefault('volumes', [])
        config.setdefault('env_vars', {})
        config.setdefault('ports', [])
        config.setdefault('restart_policy', 'no')
        config.setdefault('health_check', None)
        
        return config
    
    @staticmethod
    def parse_ports(ports_config):
        """Parse port mapping configuration
        Examples:
        - "8080:80" -> (8080, 80)
        - ["8080:80", "8443:443"] -> [(8080, 80), (8443, 443)]
        """
        if isinstance(ports_config, str):
            ports_config = [ports_config]
        
        parsed_ports = []
        for port_mapping in ports_config:
            if ':' in port_mapping:
                host_port, container_port = port_mapping.split(':')
                parsed_ports.append((int(host_port), int(container_port)))
            else:
                # Single port means same for host and container
                port = int(port_mapping)
                parsed_ports.append((port, port))
        
        return parsed_ports
    
    @staticmethod
    def parse_volumes(volumes_config):
        """Parse volume mapping configuration
        Examples:
        - "./data:/app/data" -> ("/path/to/data", "/app/data")
        - ["/host:/container", "/host2:/container2"]
        """
        if isinstance(volumes_config, str):
            volumes_config = [volumes_config]
        
        parsed_volumes = []
        for volume in volumes_config:
            if ':' in volume:
                host_path, container_path = volume.split(':', 1)
                # Expand relative paths
                if not os.path.isabs(host_path):
                    host_path = os.path.abspath(host_path)
                parsed_volumes.append((host_path, container_path))
            else:
                # Just container path, create temp host path
                parsed_volumes.append((None, volume))
        
        return parsed_volumes
    
    @staticmethod
    def parse_env_vars(env_config):
        """Parse environment variables configuration
        Examples:
        - {"KEY": "value"} -> {"KEY": "value"}
        - ["KEY=value", "KEY2=value2"] -> {"KEY": "value", "KEY2": "value2"}
        """
        if isinstance(env_config, dict):
            return env_config
        elif isinstance(env_config, list):
            env_vars = {}
            for item in env_config:
                if '=' in item:
                    key, value = item.split('=', 1)
                    env_vars[key] = value
            return env_vars
        return {}

