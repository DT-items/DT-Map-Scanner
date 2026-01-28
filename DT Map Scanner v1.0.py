import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu, Toplevel, Label
from pywinauto.application import Application
from PIL import Image, ImageGrab, ImageTk
import os
import sys
import time
import shutil
import io 
import base64
import webbrowser
from datetime import datetime
import ctypes # НУЖНО ДЛЯ ИКОНКИ В ПАНЕЛИ ЗАДАЧ

# --- КОНСТАНТЫ ---
TILE_W = 32
TILE_H = 22
OVERLAP = 3 
CROP_LEFT = 0
CROP_TOP = 0
CROP_RIGHT = 1 
CROP_BOTTOM = 1 
DISCORD_LIMIT_MB = 9.9

# Сюда вставьте вашу строку Base64. 
# Сейчас здесь закодирована простая стандартная иконка для примера.
LOGO_BASE64 = """
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
"""

# WinAPI
SBM_SETPOS = 0x00E0
WM_HSCROLL = 0x0114
WM_VSCROLL = 0x0115
SB_THUMBPOSITION = 4

def resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу, работает и для dev, и для PyInstaller """
    try:
        # PyInstaller создает временную папку _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class AutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DT Map Scanner v1.0")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        # --- НАСТРОЙКА ИКОНКИ ---
        myappid = 'mycompany.dtscanner.gui.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        
        try:
            icon_path = resource_path("icon.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass 

        # --- МЕНЮ ---
        menubar = Menu(root)
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Справка", menu=help_menu)
        root.config(menu=menubar)

        # --- ПЕРЕМЕННЫЕ ---
        self.map_width_var = tk.IntVar(value=0) 
        self.map_height_var = tk.IntVar(value=0)
        self.clean_temp_var = tk.BooleanVar(value=True) 
        self.compress_discord_var = tk.BooleanVar(value=False)
        self.resize_half_var = tk.BooleanVar(value=False)
        self.open_image_var = tk.BooleanVar(value=True)
        self.open_folder_var = tk.BooleanVar(value=False)
        # Флаг для предупреждения
        self.first_run_warning_shown = False


        # --- GUI: Выбор размера ---
        frame_size = tk.LabelFrame(root, text="Размер карты (клеток)", padx=10, pady=10)
        frame_size.pack(fill=tk.X, padx=10, pady=5)

        # --- Стандартные размеры (Верхний ряд) ---
        frame_standard = tk.Frame(frame_size)
        frame_standard.pack(pady=(0, 10), anchor='center')
        sizes = [50, 100, 200, 400]
        for size in sizes:
            btn = tk.Button(frame_standard, text=f"{size}x{size}", width=10,
                            command=lambda s=size: self.set_map_size(s, s))
            btn.pack(side=tk.LEFT, padx=5)

        # --- Кастомный размер (Нижний ряд) ---
        frame_custom = tk.Frame(frame_size)
        frame_custom.pack(anchor='center')

        tk.Label(frame_custom, text="Свой:").pack(side=tk.LEFT, padx=(0, 5))
        self.entry_custom_w = tk.Entry(frame_custom, textvariable=self.map_width_var, width=6, justify='center')
        self.entry_custom_w.pack(side=tk.LEFT)
        tk.Label(frame_custom, text="x").pack(side=tk.LEFT, padx=5)
        self.entry_custom_h = tk.Entry(frame_custom, textvariable=self.map_height_var, width=6, justify='center')
        self.entry_custom_h.pack(side=tk.LEFT)

        self.btn_apply_custom = tk.Button(frame_custom, text="Применить", command=self.apply_custom_size)
        self.btn_apply_custom.pack(side=tk.LEFT, padx=(10, 0))


        # --- GUI: Настройки ---
        frame_opts = tk.LabelFrame(root, text="Настройки", padx=10, pady=10)
        frame_opts.pack(fill=tk.X, padx=10, pady=5)
        
        cb_clean = tk.Checkbutton(frame_opts, text="Удалить временные файлы (тайлы) после склейки", 
                                  variable=self.clean_temp_var,
                                  command=self.toggle_open_folder_checkbox)
        cb_clean.pack(anchor="w", pady=2)
        
        self.cb_open_folder = tk.Checkbutton(frame_opts, text="Открыть папку с временными файлами", 
                                             variable=self.open_folder_var, state="disabled")
        self.cb_open_folder.pack(anchor="w", padx=20, pady=2)

        cb_compress = tk.Checkbutton(frame_opts, text="Сжать для Discord (Макс. качество < 9.9 MB)", 
                                     variable=self.compress_discord_var,
                                     command=self.toggle_resize_checkbox)
        cb_compress.pack(anchor="w", pady=(10, 2))

        self.cb_resize = tk.Checkbutton(frame_opts, text="Дополнительно создать уменьшенную копию (50%, Bicubic)", 
                                        variable=self.resize_half_var, state="disabled")
        self.cb_resize.pack(anchor="w", padx=20, pady=2)

        cb_open_img = tk.Checkbutton(frame_opts, text="Открыть итоговую картинку после завершения",
                                     variable=self.open_image_var)
        cb_open_img.pack(anchor="w", pady=(10, 2))


        # --- Кнопка старта ---
        self.btn_start = tk.Button(root, text="НАЧАТЬ СКАНИРОВАНИЕ И СКЛЕЙКУ", 
                                   command=self.run_process, 
                                   bg="#aaccff", font=("Arial", 12, "bold"), height=2)
        self.btn_start.pack(fill=tk.X, padx=10, pady=10)

        self.log_area = scrolledtext.ScrolledText(root, state='disabled', height=20)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.toggle_open_folder_checkbox()

    def show_about(self):
        about_window = Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("400x370")
        about_window.resizable(False, False)

        main_text = (
            "\n"
            "Discord Times Map Scanner\n"
            "Версия: 1.0\n\n"
            "Рекомендуется использовать модифицированный редактор карт\n"
            "от @Halazar6, в котором удалены иконки событий и армий.\n"
            "Эта версия редактора поставляется в комплекте.\n"
        )
        Label(about_window, text=main_text, justify="center", wraplength=400, font=("Arial", 10)).pack()

        link_text = "https://discord.gg/wmMksmWFDM"
        lbl_info = Label(about_window, text="Присоединяйтесь к Discord серверу игры Времена раздора!:", font=("Arial", 10))
        lbl_info.pack(pady=(10, 0))
        url_label = Label(about_window, text=link_text, fg="blue", cursor="hand2", font=("Arial", 10, "underline"))
        url_label.pack()
        url_label.bind("<Button-1>", lambda e: webbrowser.open_new(link_text))

        try:
            img_data = base64.b64decode(LOGO_BASE64)
            pil_image = Image.open(io.BytesIO(img_data))
            img = ImageTk.PhotoImage(pil_image)
            img_lbl = Label(about_window, image=img)
            img_lbl.image = img
            img_lbl.pack(pady=10)
        except Exception as e:
            print(f"Ошибка загрузки Base64 картинки: {e}")
            Label(about_window, text="[Нет логотипа]").pack(pady=10)

        footer_text = (
            "\n\nАвторы: mr.Hessen & Gemini 3\n"
            "Сделано с помощью Python & PyWinAuto"
        )
        Label(about_window, text=footer_text, fg="gray", font=("Arial", 8)).pack(side="bottom", pady=10)

    def show_cursor_warning(self):
        """Создает и показывает модальное окно с предупреждением о курсоре."""
        warning_window = Toplevel(self.root)
        warning_window.title("Внимание!")
        warning_window.geometry("450x150")
        warning_window.resizable(False, False)
        
        warning_window.grab_set()
        warning_window.transient(self.root)

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_w = self.root.winfo_width()
        root_h = self.root.winfo_height()
        win_w = 450
        win_h = 150
        x = root_x + (root_w - win_w) // 2
        y = root_y + (root_h - win_h) // 2
        warning_window.geometry(f'{win_w}x{win_h}+{x}+{y}')

        bold_font = ("Arial", 12, "bold")
        
        label1 = Label(warning_window, text="!! - Убери курсор в сторону от видимой области карты - !!", font=bold_font, fg="red")
        label1.pack(pady=(20, 5))
        
        label2 = Label(warning_window, text="Уведи в угол экрана, или ещё куда.")
        label2.pack()

        ok_button = tk.Button(warning_window, text="Так точно, уяснил", command=warning_window.destroy, width=20)
        ok_button.pack(pady=20)
        
        self.root.wait_window(warning_window)

    def toggle_open_folder_checkbox(self):
        if self.clean_temp_var.get():
            self.cb_open_folder.config(state="disabled")
            self.open_folder_var.set(False)
        else:
            self.cb_open_folder.config(state="normal")

    def toggle_resize_checkbox(self):
        if self.compress_discord_var.get():
            self.cb_resize.config(state="normal")
        else:
            self.cb_resize.config(state="disabled")
            self.resize_half_var.set(False)

    def log(self, message):
        print(message)
        self.log_area.configure(state='normal')
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')
        self.root.update()

    def set_map_size(self, width, height):
        self.map_width_var.set(width)
        self.map_height_var.set(height)
        self.log(f"Выбран размер карты: {width}x{height}")

    def apply_custom_size(self):
        try:
            width = self.map_width_var.get()
            height = self.map_height_var.get()
            if width <= 0 or height <= 0:
                messagebox.showerror("Ошибка", "Размеры должны быть положительными числами.")
                return
            self.set_map_size(width, height)
        except tk.TclError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения для ширины и высоты.")

    def connect_app(self):
        try:
            return Application(backend="win32").connect(path="DTMapEdit.exe")
        except:
            try:
                return Application(backend="win32").connect(title_re=".*Discord Times.*", class_name="TGameEdit")
            except:
                return None

    def set_scroll(self, parent_dlg, scrollbar_elem, position, direction):
        try:
            scrollbar_elem.send_message(SBM_SETPOS, position, 1)
            w_param = SB_THUMBPOSITION | (position << 16)
            l_param = scrollbar_elem.handle
            msg = WM_HSCROLL if direction == 'H' else WM_VSCROLL
            parent_dlg.send_message(msg, w_param, l_param)
        except Exception as e:
            self.log(f"Ошибка прокрутки: {e}")

    def run_process(self):
        if not self.first_run_warning_shown:
            self.show_cursor_warning()
            self.first_run_warning_shown = True

        self.log("="*40)
        self.log("ЭТАП 1: Сканирование...")
        
        app = self.connect_app()
        if not app:
            self.log("ОШИБКА: Редактор не найден.")
            messagebox.showerror("Ошибка", "Редактор карт DTMapEdit.exe не найден. Убедитесь, что он запущен.")
            return

        dlg = app.top_window()
        try: dlg.set_focus()
        except: pass
        
        try:
            sb_horz = dlg.TScrollBar1
            sb_vert = dlg.TScrollBar2
        except Exception as e:
            self.log(f"ОШИБКА поиска скроллбаров: {e}")
            messagebox.showerror("Ошибка", f"Не удалось найти скроллбары в окне редактора. Ошибка: {e}")
            return

        rect_h = sb_horz.rectangle()
        rect_v = sb_vert.rectangle()
        bbox = (rect_h.left, rect_v.top, rect_v.left, rect_h.top)
        viewport_w_px = rect_v.left - rect_h.left
        viewport_h_px = rect_h.top - rect_v.top
        viewport_tiles_w = int(viewport_w_px // TILE_W)
        viewport_tiles_h = int(viewport_h_px // TILE_H)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_dir = os.path.join(os.getcwd(), f"scan_{timestamp}")
        os.makedirs(save_dir, exist_ok=True)
        self.log(f"Папка: {save_dir}")

        map_width = self.map_width_var.get()
        map_height = self.map_height_var.get()
        if map_width <= 0 or map_height <= 0:
            self.log("ОШИБКА: Размеры карты должны быть больше нуля.")
            messagebox.showerror("Ошибка", "Размеры карты должны быть больше нуля. Установите корректный размер.")
            return
            
        step_x = viewport_tiles_w - OVERLAP
        step_y = viewport_tiles_h - OVERLAP
        
        if step_x <= 0 or step_y <= 0:
            self.log("ОШИБКА: Окно редактора слишком маленькое для сканирования!")
            messagebox.showerror("Ошибка", "Окно редактора слишком маленькое. Увеличьте его размер.")
            return

        self.set_scroll(dlg, sb_horz, 0, 'H')
        self.set_scroll(dlg, sb_vert, 0, 'V')
        time.sleep(1.0) 

        current_y = 0
        while True: 
            set_y = min(current_y, map_height - viewport_tiles_h)
            if set_y < 0: set_y = 0
            self.set_scroll(dlg, sb_vert, set_y, 'V')
            
            current_x = 0
            while True:
                set_x = min(current_x, map_width - viewport_tiles_w)
                if set_x < 0: set_x = 0
                self.set_scroll(dlg, sb_horz, set_x, 'H')
                time.sleep(0.5) 
                img = ImageGrab.grab(bbox=bbox)
                w, h = img.size
                img_cropped = img.crop((CROP_LEFT, CROP_TOP, w - CROP_RIGHT, h - CROP_BOTTOM))
                filename = f"tile_y{set_y:03d}_x{set_x:03d}.png"
                full_path = os.path.join(save_dir, filename)
                img_cropped.save(full_path)
                self.log(f"Saved: {filename}")
                if set_x >= (map_width - viewport_tiles_w): break 
                current_x += step_x
            if set_y >= (map_height - viewport_tiles_h): break
            current_y += step_y

        self.log("\nЭТАП 2: Склейка карты...")
        self.stitch_images(save_dir, map_width, map_height)

    def stitch_images(self, folder, map_width, map_height):
        try:
            total_w = map_width * TILE_W
            total_h = map_height * TILE_H
            self.log(f"Создание холста: {total_w}x{total_h} пикселей...")
            full_map = Image.new('RGB', (total_w, total_h))

            files = [f for f in os.listdir(folder) if f.endswith('.png') and f.startswith('tile_')]
            total_files = len(files)
            
            for i, filename in enumerate(files):
                try:
                    parts = filename.replace('.png', '').split('_')
                    y_tile = int(parts[1][1:])
                    x_tile = int(parts[2][1:])
                except: continue 
                paste_x = x_tile * TILE_W
                paste_y = y_tile * TILE_H
                img_path = os.path.join(folder, filename)
                chunk = Image.open(img_path)
                full_map.paste(chunk, (paste_x, paste_y))
                chunk.close() 
                if i % 10 == 0: self.log(f"Склейка: {i+1}/{total_files}...")

            base_name = f"Map_{map_width}x{map_height}_{datetime.now().strftime('%H-%M-%S')}"
            png_path = os.path.join(os.getcwd(), base_name + ".png")
            self.log(f"Сохранение оригинала: {png_path}")
            full_map.save(png_path)

            # --- НОВАЯ ЛОГИКА СЖАТИЯ ---
            png_size_mb = os.path.getsize(png_path) / (1024 * 1024)
            self.log(f"Размер PNG файла: {png_size_mb:.2f} MB")

            create_main_jpg = self.compress_discord_var.get() and png_size_mb >= DISCORD_LIMIT_MB
            create_mini_jpg = self.resize_half_var.get()
            
            quality_for_mini = 90  # Качество по умолчанию для mini, если основной JPG не создается

            if create_main_jpg:
                self.log(f"\nПоиск лучшего сжатия для Discord (< {DISCORD_LIMIT_MB} MB)...")
                best_q = self.find_best_quality(full_map)
                quality_for_mini = best_q  # Mini будет использовать то же качество
                
                jpg_path = os.path.join(os.getcwd(), base_name + "_DISCORD.jpg")
                self.log(f"Сохранение Discord версии (Quality={best_q})...")
                full_map.save(jpg_path, format='JPEG', quality=best_q, optimize=True)
            elif self.compress_discord_var.get():
                self.log("\nPNG файл уже подходит для Discord, полноразмерный JPG не создается.")

            if create_mini_jpg:
                self.log(f"\nСоздание копии 50% (Bicubic)...")
                new_size = (total_w // 2, total_h // 2)
                try:
                    resample_method = Image.Resampling.BICUBIC
                except AttributeError:
                    resample_method = Image.BICUBIC
                resized_map = full_map.resize(new_size, resample_method)
                
                mini_path = os.path.join(os.getcwd(), base_name + "_MINI.jpg")
                self.log(f"Сохранение Mini версии (Quality={quality_for_mini})...")
                resized_map.save(mini_path, format='JPEG', quality=quality_for_mini, optimize=True)

            if self.clean_temp_var.get():
                self.log(f"\nУдаление временной папки...")
                try:
                    shutil.rmtree(folder)
                except Exception as e:
                    self.log(f"Ошибка удаления: {e}")
            
            self.log("\nПроцесс завершен.")
            if os.path.exists(png_path):
                if self.open_folder_var.get():
                    self.log(f"Открытие папки с временными файлами: {folder}")
                    os.startfile(folder)
                if self.open_image_var.get():
                    self.log(f"Открытие итогового изображения: {png_path}")
                    os.startfile(png_path)
                
                messagebox.showinfo("Готово!", f"Процесс завершен! Результаты сохранены в папке:\n{os.getcwd()}")
            else:
                messagebox.showwarning("Завершено с ошибкой", "Итоговый файл карты не был создан.")

        except Exception as e:
            self.log(f"ОШИБКА СКЛЕЙКИ: {e}")
            messagebox.showerror("Ошибка", f"Произошла ошибка во время склейки: {str(e)}")

    def find_best_quality(self, image_obj):
        if image_obj.mode != 'RGB':
            image_obj = image_obj.convert('RGB')
        current_q = 95
        best_found_q = 10 
        while current_q >= 10:
            size_mb = self._check_size_mb(image_obj, current_q)
            self.log(f"  Проверка Q={current_q}: {size_mb:.2f} MB")
            if size_mb < DISCORD_LIMIT_MB:
                best_found_q = current_q
                self.log(f"  -> Влезает! Попытка улучшить качество...")
                for offset in range(1, 5): 
                    test_q = current_q + offset
                    if test_q > 100: break
                    size_mb_fine = self._check_size_mb(image_obj, test_q)
                    self.log(f"    Уточнение Q={test_q}: {size_mb_fine:.2f} MB")
                    if size_mb_fine < DISCORD_LIMIT_MB:
                        best_found_q = test_q
                    else:
                        break
                break
            current_q -= 5
        return best_found_q

    def _check_size_mb(self, img, quality):
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=quality, optimize=True)
        return buf.getbuffer().nbytes / (1024 * 1024)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutomationApp(root)
    root.mainloop()