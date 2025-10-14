import os
import shutil

def copy_recursive(src, dst):
    if not os.path.exists(src):
        raise ValueError(f"Source directory {src} does not exist")
    if not os.path.isdir(src):
        raise ValueError(f"Source {src} is not a directory")
    if os.path.exists(dst):
        if not os.path.isdir(dst):
            raise ValueError(f"Destination {dst} is not a directory")
        shutil.rmtree(dst)
    os.makedirs(dst)
    
    for filename in os.listdir(src):
        src_file = os.path.join(src, filename)
        dst_file = os.path.join(dst, filename)
        if os.path.isfile(src_file):
            shutil.copy(src_file, dst_file)
        elif os.path.isdir(src_file):
            copy_recursive(src_file, dst_file)
