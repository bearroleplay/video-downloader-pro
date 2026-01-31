"""
Конфигурация тестов
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock

# Добавляем src в путь
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def mock_tkinter():
    """Фикстура для мока tkinter"""
    tk_mock = Mock()
    ttk_mock = Mock()
    messagebox_mock = Mock()
    
    sys.modules['tkinter'] = tk_mock
    sys.modules['tkinter.ttk'] = ttk_mock
    sys.modules['tkinter.messagebox'] = messagebox_mock
    
    yield {
        'tk': tk_mock,
        'ttk': ttk_mock,
        'messagebox': messagebox_mock
    }
    
    # Очистка
    del sys.modules['tkinter']
    del sys.modules['tkinter.ttk']
    del sys.modules['tkinter.messagebox']

@pytest.fixture
def temp_folder():
    """Фикстура для временной папки"""
    from pathlib import Path
    temp_dir = Path("test_temp")
    temp_dir.mkdir(exist_ok=True)
    
    yield temp_dir
    
    # Очистка после теста
    if temp_dir.exists():
        for file in temp_dir.iterdir():
            file.unlink()
        temp_dir.rmdir()