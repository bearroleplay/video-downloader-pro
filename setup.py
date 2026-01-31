from setuptools import setup, find_packages

setup(
    name="videodownloader",
    version="1.0.0",
    packages=find_packages(where="."),
    package_dir={"": "src"},
    install_requires=[
        "yt-dlp>=2023.11.16",
    ],
    extras_require={
        "gui": ["PyQt5>=5.15.0"],
        "notifications": ["win10toast>=0.9"],
        "clipboard": ["pyperclip>=1.8.2"],
        "dev": ["pytest>=7.0", "black>=23.0", "flake8>=6.0", "mypy>=1.0"],
    },
    entry_points={
        "console_scripts": [
            "videodownloader=videodownloader.main:main",
        ],
    },
    python_requires=">=3.7",
)