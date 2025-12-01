import os
from pathlib import Path

src_dir = Path("src")
print(f"检查目录: {src_dir.absolute()}")
print(f"目录是否存在: {src_dir.exists()}")

if src_dir.exists():
    for file in src_dir.iterdir():
        print(f"文件: {file.name}")
        print(f"  路径: {file}")
        print(f"  存在: {file.exists()}")
        print(f"  大小: {file.stat().st_size if file.exists() else 0} bytes")
        print()