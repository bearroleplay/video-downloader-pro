#!/usr/bin/env python3
"""
Скрипт для локальной сборки .exe
"""

import subprocess
import sys
import os
from pathlib import Path

def build_exe():
    """Собрать .exe файл"""
    
    # Проверяем PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Установите PyInstaller: pip install pyinstaller")
        sys.exit(1)
    
    # Создаем папку для сборки
    build_dir = Path("build")
    dist_dir = Path("dist")
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    
    # Команда сборки
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=VideoDownloader",
        "--windowed",
        "--clean",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "src/video_downloader.py"
    ]
    
    # Добавляем иконку если есть
    icon_path = Path("assets/icon.ico")
    if icon_path.exists():
        cmd.extend(["--icon", str(icon_path)])
    
    print(f"🔨 Сборка .exe...")
    print(f"Команда: {' '.join(cmd)}")
    
    # Запускаем сборку
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Сборка завершена успешно!")
        print(f"📁 Файл: {dist_dir / 'VideoDownloader.exe'}")
    else:
        print("❌ Ошибка сборки:")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build_exe()