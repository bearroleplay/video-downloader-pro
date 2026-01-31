# 🎬 VideoDownloader

![Build Status](https://github.com/bearroleplay/video-downloader/actions/workflows/build.yml/badge.svg)
![Tests Status](https://github.com/bearroleplay/video-downloader/actions/workflows/test.yml/badge.svg)
![PyPI Version](https://img.shields.io/pypi/v/videodownloader)
![License](https://img.shields.io/github/license/bearroleplay/video-downloader)

Автоматическая сборка .exe при каждом пуше в main branch!

## 🔧 Автосборка

При каждом:
- **Push в main** → Собирается .exe (артефакт в Actions)
- **Создании релиза** → Автоматически прикрепляется .exe
- **Pull Request** → Запускаются тесты и линтеры

## 🚀 Быстрый старт

### Скачать готовый .exe
1. Перейдите в [Releases](https://github.com/bearroleplay/video-downloader/releases)
2. Скачайте `VideoDownloader.exe`
3. Запустите!

### Установка из исходников
```bash
git clone https://github.com/bearroleplay/video-downloader.git
cd video-downloader
pip install -e .
videodownloader
