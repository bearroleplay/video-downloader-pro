#!/usr/bin/env python3
"""
📥 VideoDownloader - Универсальный загрузчик видео
One-File Edition
Поддерживает: YouTube, RuTube, VK, Одноклассники
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import threading
import subprocess
import sys
import os
from pathlib import Path
import json
import webbrowser

class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 VideoDownloader v1.0")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        # Установка иконки (если есть)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Настройка стилей
        self.setup_styles()
        
        # Создание интерфейса
        self.create_widgets()
        
        # Настройки
        self.settings_file = Path.home() / ".videodownloader_settings.json"
        self.load_settings()
        
        print("✅ VideoDownloader запущен!")
    
    def setup_styles(self):
        """Настройка стилей элементов"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цвета
        self.colors = {
            'primary': '#4CAF50',
            'secondary': '#2196F3',
            'danger': '#f44336',
            'warning': '#ff9800',
            'dark': '#333333',
            'light': '#f8f9fa'
        }
    
    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        
        # Главный контейнер
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🎬 VideoDownloader",
            font=("Arial", 24, "bold"),
            fg=self.colors['dark'],
            bg=self.colors['light']
        )
        title_label.pack(side=tk.LEFT)
        
        version_label = tk.Label(
            title_frame,
            text="v1.0",
            font=("Arial", 10),
            fg=self.colors['secondary'],
            bg=self.colors['light']
        )
        version_label.pack(side=tk.RIGHT)
        
        # Карточка выбора сервиса
        service_card = tk.LabelFrame(
            main_frame,
            text="📺 Выберите сервис",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        service_card.pack(fill=tk.X, pady=(0, 15))
        
        # Кнопки сервисов
        services_frame = ttk.Frame(service_card)
        services_frame.pack()
        
        self.services = {
            "YouTube": {"color": "#FF0000", "icon": "▶️"},
            "RuTube": {"color": "#FF6B00", "icon": "🔴"},
            "VK": {"color": "#0077FF", "icon": "🔷"},
            "OK": {"color": "#FF9800", "icon": "👥"}
        }
        
        self.service_var = tk.StringVar(value="youtube")
        
        row = 0
        col = 0
        for name, data in self.services.items():
            service_id = name.lower().replace(" ", "")
            btn = tk.Radiobutton(
                services_frame,
                text=f"{data['icon']} {name}",
                variable=self.service_var,
                value=service_id,
                font=("Arial", 11),
                bg="white",
                selectcolor=data['color'],
                indicatoron=0,
                width=15,
                height=2,
                relief=tk.RAISED
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            col += 1
            if col > 1:
                col = 0
                row += 1
        
        # Карточка ввода ссылки
        url_card = tk.LabelFrame(
            main_frame,
            text="🔗 Ссылка на видео",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        url_card.pack(fill=tk.X, pady=(0, 15))
        
        # Поле для ссылки
        self.url_entry = tk.Entry(
            url_card,
            font=("Arial", 11),
            relief=tk.SUNKEN,
            bd=2
        )
        self.url_entry.pack(fill=tk.X, pady=(0, 10))
        self.url_entry.insert(0, "https://youtu.be/dQw4w9WgXcQ")  # Пример ссылки
        
        # Кнопка вставить из буфера
        paste_frame = ttk.Frame(url_card)
        paste_frame.pack(fill=tk.X)
        
        ttk.Button(
            paste_frame,
            text="📋 Вставить из буфера",
            command=self.paste_from_clipboard,
            width=20
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            paste_frame,
            text="🧹 Очистить",
            command=self.clear_url,
            width=10
        ).pack(side=tk.LEFT)
        
        # Карточка настроек
        settings_card = tk.LabelFrame(
            main_frame,
            text="⚙️ Настройки скачивания",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        settings_card.pack(fill=tk.X, pady=(0, 15))
        
        # Выбор качества
        quality_frame = ttk.Frame(settings_card)
        quality_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            quality_frame,
            text="Качество:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="best")
        qualities = ["best", "1080p", "720p", "480p", "360p", "audio only"]
        
        quality_combo = ttk.Combobox(
            quality_frame,
            textvariable=self.quality_var,
            values=qualities,
            state="readonly",
            width=15
        )
        quality_combo.pack(side=tk.LEFT)
        
        # Выбор папки сохранения
        folder_frame = ttk.Frame(settings_card)
        folder_frame.pack(fill=tk.X)
        
        tk.Label(
            folder_frame,
            text="Папка сохранения:",
            font=("Arial", 10),
            bg="white"
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        self.folder_var = tk.StringVar(value=str(Path.home() / "Downloads" / "VideoDownloader"))
        
        folder_entry = tk.Entry(
            folder_frame,
            textvariable=self.folder_var,
            font=("Arial", 10),
            width=40
        )
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(
            folder_frame,
            text="📁 Выбрать",
            command=self.choose_folder,
            width=10
        ).pack(side=tk.RIGHT)
        
        # Кнопка скачивания
        self.download_btn = tk.Button(
            main_frame,
            text="🚀 СКАЧАТЬ ВИДЕО",
            font=("Arial", 14, "bold"),
            bg=self.colors['primary'],
            fg="white",
            relief=tk.RAISED,
            bd=3,
            cursor="hand2",
            command=self.download_video,
            height=2
        )
        self.download_btn.pack(fill=tk.X, pady=(0, 15))
        
        # Прогресс
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=100
        )
        
        self.status_label = tk.Label(
            main_frame,
            text="Готов к работе",
            font=("Arial", 10),
            fg=self.colors['dark'],
            bg=self.colors['light']
        )
        
        # Консоль вывода
        console_card = tk.LabelFrame(
            main_frame,
            text="📝 Лог выполнения",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        console_card.pack(fill=tk.BOTH, expand=True)
        
        self.console = scrolledtext.ScrolledText(
            console_card,
            height=8,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white"
        )
        self.console.pack(fill=tk.BOTH, expand=True)
        
        # Статус бар
        self.status_bar = tk.Label(
            self.root,
            text="✅ Готов к работе | Выберите сервис и вставьте ссылку",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg=self.colors['light']
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def paste_from_clipboard(self):
        """Вставить ссылку из буфера обмена"""
        try:
            # Для Windows
            import win32clipboard
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, data)
            self.log("✅ Ссылка вставлена из буфера обмена")
        except:
            # Альтернативный способ
            try:
                import pyperclip
                data = pyperclip.paste()
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, data)
                self.log("✅ Ссылка вставлена из буфера обмена")
            except:
                messagebox.showwarning("Ошибка", "Не удалось получить доступ к буферу обмена")
                self.log("⚠️ Не удалось вставить из буфера")
    
    def clear_url(self):
        """Очистить поле ссылки"""
        self.url_entry.delete(0, tk.END)
        self.log("🧹 Поле ссылки очищено")
    
    def choose_folder(self):
        """Выбрать папку для сохранения"""
        folder = filedialog.askdirectory(
            title="Выберите папку для сохранения видео",
            initialdir=self.folder_var.get()
        )
        if folder:
            self.folder_var.set(folder)
            self.log(f"📁 Папка сохранения изменена: {folder}")
    
    def log(self, message):
        """Добавить сообщение в лог"""
        self.console.insert(tk.END, f"[{self.get_time()}] {message}\n")
        self.console.see(tk.END)
        self.status_bar.config(text=message)
        self.root.update()
    
    def get_time(self):
        """Получить текущее время"""
        from datetime import datetime
        return datetime.now().strftime("%H:%M:%S")
    
    def download_video(self):
        """Запустить скачивание видео"""
        url = self.url_entry.get().strip()
        service = self.service_var.get()
        quality = self.quality_var.get()
        folder = self.folder_var.get()
        
        if not url:
            messagebox.showerror("Ошибка", "Введите ссылку на видео!")
            return
        
        if not folder:
            folder = Path.home() / "Downloads" / "VideoDownloader"
            self.folder_var.set(str(folder))
        
        # Создаем папку если её нет
        Path(folder).mkdir(parents=True, exist_ok=True)
        
        # Отображаем прогресс
        self.download_btn.config(state='disabled', text="⏬ СКАЧИВАНИЕ...")
        self.progress.pack(fill=tk.X, pady=(0, 5))
        self.progress.start()
        self.status_label.pack(fill=tk.X)
        
        self.log("=" * 50)
        self.log(f"🚀 Начинаю скачивание:")
        self.log(f"   Сервис: {service.upper()}")
        self.log(f"   Качество: {quality}")
        self.log(f"   Папка: {folder}")
        self.log(f"   Ссылка: {url}")
        
        # Запускаем в отдельном потоке
        thread = threading.Thread(
            target=self._download_thread,
            args=(url, service, quality, folder),
            daemon=True
        )
        thread.start()
    
    def _download_thread(self, url, service, quality, folder):
        """Поток для скачивания видео"""
        try:
            # Формируем команду для yt-dlp
            cmd = [
                "yt-dlp",
                "-o", f"{folder}/%(title)s.%(ext)s",
                "--no-warnings",
                "--progress",
                "--newline"
            ]
            
            # Добавляем качество
            if quality == "best":
                cmd.extend(["-f", "best"])
            elif quality == "audio only":
                cmd.extend(["-f", "bestaudio", "-x", "--audio-format", "mp3"])
            elif quality.endswith("p"):
                cmd.extend(["-f", f"best[height<={quality[:-1]}]"])
            
            # Добавляем ссылку
            cmd.append(url)
            
            self.log(f"🔧 Команда: {' '.join(cmd)}")
            
            # Запускаем процесс
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            # Читаем вывод в реальном времени
            for line in process.stdout:
                if line.strip():
                    self.log(line.strip())
                    self.root.after(0, self.update_ui_from_log, line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, self._download_complete, True, "Скачивание завершено успешно!")
            else:
                self.root.after(0, self._download_complete, False, "Ошибка скачивания")
                
        except Exception as e:
            self.root.after(0, self._download_complete, False, f"Ошибка: {str(e)}")
    
    def update_ui_from_log(self, line):
        """Обновить UI на основе лога"""
        if "ETA" in line or "%" in line:
            self.status_label.config(text=line.strip())
    
    def _download_complete(self, success, message):
        """Завершение скачивания"""
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.pack_forget()
        self.download_btn.config(state='normal', text="🚀 СКАЧАТЬ ВИДЕО")
        
        if success:
            self.log(f"✅ {message}")
            self.log("=" * 50)
            self.status_bar.config(text="✅ Скачивание завершено успешно!")
            
            # Показать уведомление
            if self._check_notifications():
                try:
                    from win10toast import ToastNotifier
                    toaster = ToastNotifier()
                    toaster.show_toast(
                        "VideoDownloader",
                        "Видео скачано успешно!",
                        duration=5,
                        icon_path=None,
                        threaded=True
                    )
                except:
                    pass
            
            # Открыть папку с видео
            if messagebox.askyesno("Готово!", f"{message}\n\nОткрыть папку с видео?"):
                folder = self.folder_var.get()
                webbrowser.open(f"file://{folder}")
        else:
            self.log(f"❌ {message}")
            self.log("=" * 50)
            self.status_bar.config(text=f"❌ Ошибка: {message}")
            messagebox.showerror("Ошибка", message)
    
    def _check_notifications(self):
        """Проверить, доступны ли уведомления"""
        try:
            import win10toast
            return True
        except:
            return False
    
    def load_settings(self):
        """Загрузить настройки"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.folder_var.set(settings.get('folder', str(Path.home() / "Downloads" / "VideoDownloader")))
                    self.quality_var.set(settings.get('quality', 'best'))
                    self.log("⚙️ Настройки загружены")
        except:
            pass
    
    def save_settings(self):
        """Сохранить настройки"""
        try:
            settings = {
                'folder': self.folder_var.get(),
                'quality': self.quality_var.get()
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
            self.log("⚙️ Настройки сохранены")
        except:
            pass
    
    def on_closing(self):
        """Действия при закрытии окна"""
        self.save_settings()
        self.root.destroy()

def check_dependencies():
    """Проверить установлены ли зависимости"""
    try:
        # Проверяем yt-dlp
        subprocess.run(["yt-dlp", "--version"], 
                      capture_output=True, 
                      check=True)
        print("✅ yt-dlp установлен")
        return True
    except:
        print("❌ yt-dlp не найден")
        
        answer = messagebox.askyesno(
            "Установка зависимостей",
            "yt-dlp не найден. Установить автоматически?\n\n"
            "Программа не будет работать без yt-dlp!"
        )
        
        if answer:
            try:
                import pip
                subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
                messagebox.showinfo("Успех", "yt-dlp успешно установлен!")
                return True
            except:
                messagebox.showerror(
                    "Ошибка",
                    "Не удалось установить yt-dlp.\n"
                    "Установите вручную:\n"
                    "pip install yt-dlp"
                )
                return False
        else:
            messagebox.showinfo(
                "Информация",
                "Установите yt-dlp вручную:\n"
                "1. Откройте командную строку (cmd)\n"
                "2. Введите: pip install yt-dlp\n"
                "3. Перезапустите программу"
            )
            return False

def main():
    """Главная функция"""
    # Проверяем зависимости
    if not check_dependencies():
        return
    
    # Создаем окно
    root = tk.Tk()
    
    # Создаем приложение
    app = VideoDownloader(root)
    
    # Обработчик закрытия окна
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Запускаем главный цикл
    root.mainloop()

if __name__ == "__main__":
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # Режим командной строки
        import argparse
        parser = argparse.ArgumentParser(description='VideoDownloader CLI')
        parser.add_argument('url', help='Ссылка на видео')
        parser.add_argument('-s', '--service', default='auto', 
                          help='Сервис (youtube, rutube, vk, ok)')
        parser.add_argument('-q', '--quality', default='best',
                          help='Качество (best, 1080p, 720p, etc)')
        parser.add_argument('-o', '--output', 
                          default=str(Path.home() / "Downloads" / "VideoDownloader"),
                          help='Папка для сохранения')
        
        args = parser.parse_args()
        
        # Скачиваем видео
        cmd = ["yt-dlp", "-o", f"{args.output}/%(title)s.%(ext)s"]
        if args.quality != "best":
            cmd.extend(["-f", args.quality])
        cmd.append(args.url)
        
        print(f"⏬ Скачивание: {args.url}")
        print(f"📁 В папку: {args.output}")
        print(f"🎯 Качество: {args.quality}")
        
        subprocess.run(cmd)
    else:
        # Запускаем GUI
        main()