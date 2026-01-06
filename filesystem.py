import os
import shutil
import tarfile

class FileSystemManager:
    def __init__(self, base_dir="./containers", images_dir="./images"):
        self.base_dir = base_dir
        self.images_dir = images_dir
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

    def create_rootfs(self, name, image_name=None):
        """
        Create a rootfs folder for the container.
        If image_name is provided, copy from that image.
        Otherwise, create a minimal rootfs structure.
        """
        rootfs_path = os.path.join(self.base_dir, name, "rootfs")
        
        if image_name:
            # Create container from image
            image_path = os.path.join(self.images_dir, image_name)
            if os.path.exists(image_path):
                # Copy image rootfs to container
                if os.path.isdir(image_path):
                    # Image is a directory
                    shutil.copytree(image_path, rootfs_path, dirs_exist_ok=True)
                elif image_path.endswith('.tar') or image_path.endswith('.tar.gz'):
                    # Image is a tar file
                    os.makedirs(rootfs_path, exist_ok=True)
                    with tarfile.open(image_path, 'r:*') as tar:
                        tar.extractall(rootfs_path)
                else:
                    # Fallback: create minimal structure
                    os.makedirs(rootfs_path, exist_ok=True)
                    self._create_minimal_rootfs(rootfs_path)
            else:
                # Image not found, create minimal structure
                os.makedirs(rootfs_path, exist_ok=True)
                self._create_minimal_rootfs(rootfs_path)
        else:
            # Create minimal rootfs structure
            os.makedirs(rootfs_path, exist_ok=True)
            self._create_minimal_rootfs(rootfs_path)
        
        return rootfs_path
    
    def _create_minimal_rootfs(self, rootfs_path):
        """Create a minimal rootfs directory structure."""
        for folder in ["bin", "etc", "usr", "lib", "lib64", "tmp", "var", "proc", "sys"]:
            os.makedirs(os.path.join(rootfs_path, folder), exist_ok=True)
        
        # Create a basic /etc/passwd and /etc/group for compatibility
        etc_dir = os.path.join(rootfs_path, "etc")
        with open(os.path.join(etc_dir, "passwd"), "w") as f:
            f.write("root:x:0:0:root:/root:/bin/sh\n")
        with open(os.path.join(etc_dir, "group"), "w") as f:
            f.write("root:x:0:\n")

    def delete_rootfs(self, name):
        """Delete a container's rootfs folder."""
        path = os.path.join(self.base_dir, name)
        if os.path.exists(path):
            shutil.rmtree(path)

    def open_rootfs(self, name):
        """Get the container's rootfs folder path."""
        path = os.path.join(self.base_dir, name, "rootfs")
        if os.path.exists(path):
            return path
        return None

    def choose_image(self, image_path=None):
        """Get image path (for web interface, path is provided directly)."""
        return image_path
    
    def save_image(self, image_name, source_path):
        """
        Save an image from a source path (directory or tar file).
        Images are stored in the images directory.
        """
        image_dest = os.path.join(self.images_dir, image_name)
        
        if os.path.isdir(source_path):
            # Copy directory to images
            if os.path.exists(image_dest):
                shutil.rmtree(image_dest)
            shutil.copytree(source_path, image_dest)
        elif source_path.endswith('.tar') or source_path.endswith('.tar.gz') or source_path.endswith('.tgz'):
            # Copy tar file to images
            shutil.copy2(source_path, os.path.join(self.images_dir, f"{image_name}.tar"))
        else:
            raise ValueError(f"Unsupported image format: {source_path}")
        
        return image_dest
    
    def list_images(self):
        """List all available images."""
        images = []
        if os.path.exists(self.images_dir):
            for item in os.listdir(self.images_dir):
                item_path = os.path.join(self.images_dir, item)
                if os.path.isdir(item_path):
                    images.append(item)
                elif item.endswith(('.tar', '.tar.gz', '.tgz')):
                    images.append(item.rsplit('.', 1)[0])  # Remove extension
        return images
