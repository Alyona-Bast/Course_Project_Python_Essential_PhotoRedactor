from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook
from PIL import Image, ImageTk, ImageOps, ImageFilter
import os


class PhotoRedactor:
    def __init__(self):
        self.root = Tk()
        self.image_tabs = Notebook(self.root)
        self.opened_images = []

        self.init()

    def init(self):
        """Настройки вікна"""
        self.root.title("Фоторедактор")
        self.root.iconphoto(True, PhotoImage(file="img/icon.png"))
        self.image_tabs.enable_traversal()

        self.root.bind("<Escape>", self._close)             #Закрити вікно ескейпом
        self.root.protocol("WM_DELETE_WINDOW", self._close)

    def run(self):
        self.draw_menu()
        self.draw_widgets()

        self.root.mainloop()

    def draw_menu(self):
        menu_bar = Menu(self.root)
#-----------------------------------------------------------------
        #Меню Файл
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Відкрити", command=self.open_new_images)
        file_menu.add_command(label="Зберегти", command=self.save_current_image)
        file_menu.add_command(label="Зберегти як", command=self.save_image_as)
        file_menu.add_command(label="Зберегти всі", command=self.save_all_changes)
        file_menu.add_separator()
        file_menu.add_command(label="Вийти", command=self._close)
        menu_bar.add_cascade(label="Файл", menu=file_menu)
# -----------------------------------------------------------------
        # Повернути зображення
        rotate_menu = Menu(menu_bar, tearoff=0)
        rotate_menu.add_command(label="Вліво на 90°", command=lambda: self.rotate_current_image(90))
        rotate_menu.add_command(label="Вправо на 90°", command=lambda: self.rotate_current_image(-90))
        rotate_menu.add_command(label="Вліво на 180°", command=lambda: self.rotate_current_image(180))
        rotate_menu.add_command(label="Вправо на 180°", command=lambda: self.rotate_current_image(-180))
        menu_bar.add_cascade(label="Повернути", menu=rotate_menu)
# -----------------------------------------------------------------
        # Відзеркалити зображення
        flip_menu = Menu(menu_bar, tearoff=0)
        flip_menu.add_command(label="Горизонтально", command=lambda: self.flip_current_image("horizontally"))
        flip_menu.add_command(label="Вертикально", command=lambda: self.flip_current_image("vertically"))
        menu_bar.add_cascade(label="Відзеркалити", menu=flip_menu)
# -----------------------------------------------------------------
        # Змінити розмір зображення
        resize_menu = Menu(menu_bar, tearoff=0)
        resize_menu.add_command(label="25%", command=lambda: self.resize_current_image(25))
        resize_menu.add_command(label="50%", command=lambda: self.resize_current_image(50))
        resize_menu.add_command(label="75%", command=lambda: self.resize_current_image(75))
        resize_menu.add_command(label="125%", command=lambda: self.resize_current_image(125))
        resize_menu.add_command(label="150%", command=lambda: self.resize_current_image(150))
        resize_menu.add_command(label="200%", command=lambda: self.resize_current_image(200))
        menu_bar.add_cascade(label="Розмір", menu=resize_menu)
# -----------------------------------------------------------------
        # Фільтри
        filter_menu = Menu(menu_bar, tearoff=0)
        filter_menu.add_command(label="BLUR", command=lambda: self.apply_filter_to_current_image(ImageFilter.BLUR))
        filter_menu.add_command(label="SHARPEN",
                                command=lambda: self.apply_filter_to_current_image(ImageFilter.SHARPEN))
        filter_menu.add_command(label="CONTOUR",
                                command=lambda: self.apply_filter_to_current_image(ImageFilter.CONTOUR))
        filter_menu.add_command(label="DETAIL", command=lambda: self.apply_filter_to_current_image(ImageFilter.DETAIL))
        filter_menu.add_command(label="SMOOTH", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH))
        filter_menu.add_command(label="EDGE_ENHANCE", command=lambda: self.apply_filter_to_current_image(ImageFilter.EDGE_ENHANCE))
        filter_menu.add_command(label="EMBOSS", command=lambda: self.apply_filter_to_current_image(ImageFilter.EMBOSS))
        filter_menu.add_command(label="FIND_EDGES", command=lambda: self.apply_filter_to_current_image(ImageFilter.FIND_EDGES))
        menu_bar.add_cascade(label="Фільтри", menu=filter_menu)
# -----------------------------------------------------------------

        self.root.configure(menu=menu_bar)

    def draw_widgets(self):
        self.image_tabs.pack(fill="both", expand=1)

    def open_new_images(self):
        """Відкрити зображення"""
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        for image_path in image_paths:
            self.add_new_image(image_path)

    def add_new_image(self, image_path):
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(image)
        self.opened_images.append([image_path, image])

        image_tab = Frame(self.image_tabs)

        image_label = Label(image_tab, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side="bottom", fill="both", expand="yes")

        self.image_tabs.add(image_tab, text=image_path.split('/')[-1])
        self.image_tabs.select(image_tab)

    def get_current_working_data(self):
        """Отримати повний шлях файлу"""
        current_tab = self.image_tabs.select()
        if not current_tab:
            return None, None, None
        tab_number = self.image_tabs.index(current_tab)
        path, image = self.opened_images[tab_number]

        return current_tab, path, image

    def save_current_image(self):
        """Зберегти зображення"""
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        if path[-1] == '*':
            path = path[:-1]
            self.opened_images[tab_number][0] = path
            image.save(path)
            self.image_tabs.add(current_tab, text=path.split('/')[-1])

    def save_image_as(self):
        """Зберегти як"""
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        old_path, old_ext = os.path.splitext(path)
        if '*' in old_ext:
            old_ext = old_ext[:-1]

        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpeg;*.jpg;*.png"),))
        if not new_path:
            return

        new_path, new_ext = os.path.splitext(new_path)
        if not new_ext:
            new_ext = old_ext
        elif old_ext != new_ext:
            mb.showerror("Некоректне розширення", f"Уведене розширення некоректне: {new_ext}. "
                                                  f"Файл має розширення: {old_ext}")
            return

        image.save(new_path + new_ext)
        image.close()

        del self.opened_images[tab_number]
        self.image_tabs.forget(current_tab)

        self.add_new_image(new_path + new_ext)

    def save_all_changes(self):
        """Зберегти все"""
        for index, (path, image) in enumerate(self.opened_images):
            if path[-1] != '*':
                continue
            path = path[:-1]
            self.opened_images[index][0] = path
            image.save(path)
            self.image_tabs.tab(index, text=path.split('/')[-1])

    def update_image_inside_app(self, current_tab, image):
        """Змінити файл"""
        tab_number = self.image_tabs.index(current_tab)
        tab_frame = self.image_tabs.children[current_tab[current_tab.rfind('!'):]]
        label = tab_frame.children['!label']

        self.opened_images[tab_number][1] = image

        image_tk = ImageTk.PhotoImage(image)
        label.configure(image=image_tk)
        label.image = image_tk

        image_path = self.opened_images[tab_number][0]
        if image_path[-1] != '*':
            image_path += '*'
            self.opened_images[tab_number][0] = image_path
            image_name = image_path.split('/')[-1]
            self.image_tabs.tab(current_tab, text=image_name)

    def rotate_current_image(self, degrees):
        """Повернути зображення"""
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        image = image.rotate(degrees)
        self.update_image_inside_app(current_tab, image)

    def flip_current_image(self, flip_type):
        """Відзеркалити"""
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        if flip_type == "horizontally":
            image = ImageOps.mirror(image)
        elif flip_type == "vertically":
            image = ImageOps.flip(image)

        self.update_image_inside_app(current_tab, image)

    def resize_current_image(self, percents):
        """Змінити розмір"""
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        w, h = image.size
        w = (w * percents) // 100
        h = (h * percents) // 100

        image = image.resize((w, h), Image.ANTIALIAS)
        self.update_image_inside_app(current_tab, image)

    def apply_filter_to_current_image(self, filter_type):
        """Фільтри"""
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        image = image.filter(filter_type)
        self.update_image_inside_app(current_tab, image)

    def unsaved_images(self):
        """Зміни не збережені"""
        for path, _ in self.opened_images:
            if path[-1] == "*":
                return True
        return False

    def _close(self, event=None):
        """Закриття"""
        if self.unsaved_images():
            if not mb.askyesno("Зміни не збережено", "Ви не зберегли зміни!\n"
                                                     "Ви дійсно хочете вийти?"):
                return

        self.root.quit()


if __name__ == "__main__":
    PhotoRedactor().run()

