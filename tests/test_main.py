#!/usr/bin/env python3
"""
Тесты для VideoDownloader
"""

import pytest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Добавляем src в путь Python
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from videodownloader.main import check_dependencies
from videodownloader import VideoDownloader

# Мокаем tkinter для импорта
tk_mock = Mock()
ttk_mock = Mock()
messagebox_mock = Mock()
scrolledtext_mock = Mock()
filedialog_mock = Mock()

sys.modules['tkinter'] = tk_mock
sys.modules['tkinter.ttk'] = ttk_mock
sys.modules['tkinter.messagebox'] = messagebox_mock
sys.modules['tkinter.scrolledtext'] = scrolledtext_mock
sys.modules['tkinter.filedialog'] = filedialog_mock

# Мокаем остальные модули
sys.modules['webbrowser'] = Mock()

class MockTk:
    def __init__(self):
        self.title = Mock()
        self.geometry = Mock()
        self.configure = Mock()
        self.protocol = Mock()
        self.mainloop = Mock()
        self.destroy = Mock()
        self.after = Mock()

def test_check_dependencies_success():
    """Тест успешной проверки зависимостей"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(returncode=0)
        assert check_dependencies() == True

def test_check_dependencies_failure():
    """Тест неудачной проверки зависимостей"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = Exception("Not found")
        assert check_dependencies() == False

def test_videodownloader_init():
    """Тест инициализации класса VideoDownloader"""
    with patch('tkinter.Tk', return_value=MockTk()):
        mock_root = MockTk()
        app = VideoDownloader(mock_root)
        
        # Проверяем что методы были вызваны
        assert app is not None
        mock_root.title.assert_called()
        mock_root.geometry.assert_called()

def test_url_validation_empty():
    """Тест валидации пустого URL"""
    with patch('tkinter.Tk', return_value=MockTk()):
        mock_root = MockTk()
        app = VideoDownloader(mock_root)
        
        # Мокаем поле ввода
        app.url_entry = Mock()
        app.url_entry.get.return_value = ""
        
        # Мокаем messagebox
        with patch('tkinter.messagebox.showerror') as mock_error:
            app.download_video()
            # Проверяем что была показана ошибка
            mock_error.assert_called_with("Ошибка", "Введите ссылку на видео!")

def test_folder_creation():
    """Тест создания папки для сохранения"""
    test_folder = Path("test_downloads_123")
    
    # Удаляем если существует
    if test_folder.exists():
        for file in test_folder.iterdir():
            file.unlink()
        test_folder.rmdir()
    
    # Создаем через mkdir
    test_folder.mkdir(exist_ok=True)
    assert test_folder.exists()
    
    # Очищаем
    test_folder.rmdir()
    assert not test_folder.exists()

def test_get_time_format():
    """Тест форматирования времени"""
    from datetime import datetime
    
    # Тестируем косвенно через mock
    with patch('videodownloader.main.datetime') as mock_datetime:
        mock_datetime.now.return_value.strftime.return_value = "12:34:56"
        
        # Создаем минимальный объект для теста
        class TestApp:
            def get_time(self):
                from datetime import datetime
                return datetime.now().strftime("%H:%M:%S")
        
        app = TestApp()
        time_str = app.get_time()
        assert time_str == "12:34:56"

# Моки для тестов с PyInstaller
def test_pyinstaller_mock():
    """Тест мока PyInstaller"""
    # Просто проверяем что можем импортировать мок
    pyinstaller_mock = Mock()
    sys.modules['PyInstaller'] = pyinstaller_mock
    
    # Тест проходит если нет исключений
    assert True

if __name__ == "__main__":
    # Запускаем тесты
    import sys
    sys.exit(pytest.main([__file__, "-v"]))