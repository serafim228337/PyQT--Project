import sqlite3
import sys
from PyQt6.QtWidgets import (
    QApplication, QLineEdit, QGridLayout,
    QComboBox, QMessageBox, QListWidget, QListWidgetItem,
    QWidget, QHBoxLayout, QDialog,
    QPushButton, QVBoxLayout, QLabel, QTextEdit, QInputDialog
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

recipes = {
    "Wooden Sword": [["Wood x10"], "Image/item/Wooden_Sword.png"],
    "Copper Shortsword": [["Copper_Bar x5"], "Image/item/Copper_Shortsword.png"],
    "Iron Shortsword": [["Iron_Bar x6"], "Image/item/Iron_Shortsword.png"],
    "Silver Shortsword": [["Silver_Bar x6"], "Image/item/Silver_Shortsword.png"],
    "Gold Shortsword": [["Gold_Bar x6"], "Image/item/Gold_Shortsword.png"],
    "Copper Axe": [["Copper_Bar x6", "Wood x3"], "Image/item/Copper_Axe.png"],
    "Iron Axe": [["Iron_Bar x8", "Wood x3"], "Image/item/Iron_Axe.png"],
    "Silver Axe": [["Silver_Bar x8", "Wood x3"], "Image/item/Silver_Axe.png"],
    "Gold Axe": [["Gold_Bar x8", "Wood x3"], "Image/item/Gold_Axe.png"],
    "Copper Pickaxe": [["Copper_Bar x8", "Wood x4"], "Image/item/Copper_Pickaxe.png"],
    "Iron Pickaxe": [["Iron_Bar x8", "Wood x4"], "Image/item/Iron_Pickaxe.png"],
    "Silver Pickaxe": [["Silver_Bar x8", "Wood x4"], "Image/item/Silver_Pickaxe.png"],
    "Gold Pickaxe": [["Gold_Bar x8", "Wood x4"], "Image/item/Gold_Pickaxe.png"],
    "Amethyst Staff": [["Copper_Bar x10", "Amethyst x8", ], "Image/item/Amethyst_Staff.png"],
    "Zenith": [
        ["Terra_Blade x1", "Meowmere x1", "Star_Wrath x1", "Influx_Waver x1", "The_Horsemans_Blade x1", "Seedler x1",
         "Starfury x1", "Bee_Keeper x1", "Enchanted_Sword x1", "Copper_Shortsword x1"], "Image/item/Zenith.png"],
    "Terra_Blade": [["Broken_Hero_Sword x1", "True_Excalibur x1", "True_Nights_Edge x1", ],
                    "Image/item/Terra_Blade.png"],
}


class IntroWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добро пожаловать в Terraria Crafting App!")

        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        # Создаем таблицу пользователей
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )
                """)
        # Создаем таблицу избранных рецептов
        self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS favorite_recipes (
                        user_id INTEGER,
                        recipe_name TEXT
                    )
                """)
        self.conn.commit()
        self.conn.close()

        # Создаем QLabel для заголовка
        self.title_label = QLabel("Terraria Crafting App")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Создаем QLabel для информации о приложении
        self.info_label = QLabel("Приложение для поиска рецептов в игре Terraria")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Устанавливаем размер шрифта
        self.font = self.info_label.font()
        self.font.setPointSize(10)
        self.info_label.setFont(self.font)

        # Создаем кнопку "Info"
        self.info_button = QPushButton("Информация об игре")
        self.info_button.clicked.connect(self.show_info)

        self.start_button = QPushButton("Начать") #после нужно убрать
        self.start_button.clicked.connect(self.open_crafting_app)
        # Создаем кнопку "Вход"
        self.login_button = QPushButton("Вход")
        self.login_button.clicked.connect(self.show_login_dialog)
        # Создаем кнопку "Регистрация"
        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.show_register_dialog)

        # Создаем вертикальный макет для элементов
        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.info_label)
        vbox.addWidget(self.info_button)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.register_button)
        vbox.addWidget(self.start_button) #после нужно убрать
        vbox.addStretch()  # Добавляем растягивающий элемент для выравнивания

        self.setLayout(vbox)

    def show_login_dialog(self):
        # Открываем новое соединение с базой данных в IntroWindow
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        username, ok = QInputDialog.getText(self, "Вход", "Введите имя пользователя:")
        if ok and username:
            password, ok = QInputDialog.getText(self, "Вход", "Введите пароль:")  # Убираем EchoMode.Password
            if ok and password:
                self.authenticate_user(username, password)
        self.conn.close()

    def show_register_dialog(self):
        # Открываем новое соединение с базой данных в IntroWindow
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        # Создаем диалоговое окно для регистрации
        dialog = QDialog(self)
        dialog.setWindowTitle("Регистрация")

        # Создаем элементы диалогового окна
        username_label = QLabel("Имя пользователя:")
        password_label = QLabel("Пароль:")
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)  # Устанавливаем режим маскировки пароля
        register_button = QPushButton("Зарегистрироваться")

        # Создаем макет диалогового окна
        grid = QGridLayout()
        grid.addWidget(username_label, 0, 0)
        grid.addWidget(username_input, 0, 1)
        grid.addWidget(password_label, 1, 0)
        grid.addWidget(password_input, 1, 1)
        grid.addWidget(register_button, 2, 0, 1, 2)

        dialog.setLayout(grid)

        # Обрабатываем нажатие на кнопку регистрации
        register_button.clicked.connect(lambda: self.register_user(username_input.text(), password_input.text()))

        # Отображаем диалоговое окно
        dialog.exec()
        self.conn.close()

    def authenticate_user(self, username, password):
        # Проверяем, есть ли пользователь в базе данных
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user:
            # Проверяем пароль
            if password == user[2]:  # Замените `user[2]` на индекс, где хранится хеш пароля
                self.user_id = user[0]  # Сохраняем ID пользователя
                self.open_crafting_app(self.user_id)  # Передаем user_id
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")

    def register_user(self, username, password):
        # Проверяем, существует ли пользователь с таким именем
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone():
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует!")
            return

        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        QMessageBox.information(self, "Успешно", "Пользователь успешно зарегистрирован!")
        # Закрываем соединение с базой данных в IntroWindow после регистрации
        self.conn.close()

    def show_info(self):
        # Создаем диалоговое окно для информации
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle("О Terraria")

        # Добавляем текст описания Terraria
        text_edit = QTextEdit(info_dialog)
        text_edit.setText("Terraria - это инди игра в жанре песочницы с элементами экшена и приключений. \n"
                          "Игрок создает своего персонажа, исследует мир, строит дома, "
                          "создает оружие и сражается с разнообразными монстрами. \n"
                          "Игра отличается большой свободой действий, "
                          "возможностью крафта и исследования огромного мира. \n")
        text_edit.setReadOnly(True)  # Делаем текст нередактируемым

        # Добавляем кнопку "Закрыть"
        close_button = QPushButton("Закрыть", info_dialog)
        close_button.clicked.connect(info_dialog.close)

        # Создаем вертикальный макет для элементов диалогового окна
        vbox = QVBoxLayout()
        vbox.addWidget(text_edit)
        vbox.addWidget(close_button)

        info_dialog.setLayout(vbox)
        info_dialog.exec()

    def open_crafting_app(self, user_id):
        #открываем основное окно
        self.close()
        global window
        window = TerrariaCraftingApp(user_id)
        window.show()

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


class TerrariaCraftingApp(QWidget):
    def __init__(self, user_id):
        super().__init__()

        self.setWindowTitle("Terraria Crafting")

        self.user_id = user_id
        print(self.user_id)

        # Крафт
        self.craft_label = QLabel("Выбранный предмет:")
        self.craft_input = QLineEdit("Wooden Sword")
        self.craft_input.setReadOnly(True)  # Делаем поле ввода только для чтения
        self.craft_button = QPushButton("Крафт")
        self.craft_button.clicked.connect(self.show_recipe)
        self.craft_button.clicked.connect(self.update_materials_list)  # Добавили в сигнал

        self.recipe_label = QLabel("Рецепт:")
        self.recipe_list = QComboBox()
        self.recipe_list.addItems(recipes.keys())
        self.recipe_list.currentTextChanged.connect(self.set_craft_input)
        self.recipe_list.currentTextChanged.connect(self.update_image)
        self.recipe_list.currentTextChanged.connect(self.update_materials_list)  # Добавили в сигнал

        self.recipe_image_label = QLabel()
        self.recipe_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Список материалов
        self.materials_label = QLabel("Материалы:")
        self.materials_list = QListWidget()
        self.update_materials_list()

        # Макет
        grid = QGridLayout()

        grid.addWidget(self.craft_label, 0, 0)
        grid.addWidget(self.craft_input, 0, 1)
        grid.addWidget(self.craft_button, 1, 0, 1, 2)
        grid.addWidget(self.recipe_label, 2, 0)
        grid.addWidget(self.recipe_list, 2, 1)
        grid.addWidget(self.recipe_image_label, 3, 0, 1, 2)
        grid.addWidget(self.materials_label, 4, 0)
        grid.addWidget(self.materials_list, 5, 0, 1, 2)  # Разместили список материалов

        self.setLayout(grid)

        # Начальное обновление изображения
        self.update_image()

    def update_image(self):
        '''Обновление изображения'''
        selected_item = self.recipe_list.currentText()
        if selected_item in recipes:
            image_path = recipes[selected_item][1]
            try:
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(100, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.recipe_image_label.setPixmap(pixmap)
            except FileNotFoundError:
                print(f"Image not found for {selected_item} at {image_path}")
                self.recipe_image_label.clear()

    def show_recipe(self):
        '''Выводим рецепт после нажатия на кнопку крафт'''
        selected_item = self.recipe_list.currentText()
        if selected_item in recipes:
            string = "\n".join(recipes[selected_item][0])
            QMessageBox.information(self, "Recipe", string)
        else:
            QMessageBox.warning(self, "Error", "Item not found!")

    def set_craft_input(self, text):
        self.craft_input.setText(text)

    def update_materials_list(self):
        """Постоянно обновляющийся список материалов на выбранный крафт"""
        selected_item = self.recipe_list.currentText()
        if selected_item in recipes:
            self.materials_list.clear()
            for materials in recipes[selected_item][0]:
                material = materials.split(" x")
                material_name, material_count = material[0], material[1]

                image_path = f"Image/Materials/{material_name}.png"
                image_label = QLabel()
                try:
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                except FileNotFoundError:
                    image_label.setText("")  # Если изображение не найдено, просто оставляем пустое место

                hbox = QHBoxLayout()
                hbox.setSpacing(10)  # Устанавливаем отступ в 10 пикселей

                # Добавляем изображение слева от текста
                hbox.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignLeft)

                # Добавляем текст с выравниванием влево

                text_label = QLabel(f"{material_name} x {material_count}")
                text_label.setFixedSize(200, 20)
                text_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                hbox.addWidget(text_label)

                # Создаем новый QWidget, чтобы установить в нем макет
                widget = QWidget()
                widget.setLayout(hbox)  # Устанавливаем hbox в качестве макета для widget

                # Создаем новый элемент QListWidgetItem с использованием widget
                item = QListWidgetItem()
                item.setSizeHint(QSize(150, 50))  # Устанавливаем размер элемента
                self.materials_list.addItem(item)
                self.materials_list.setItemWidget(item, widget)  # Устанавливаем widget как виджет для элемента


        else:
            self.materials_list.clear()

    def closeEvent(self, event):
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    intro = IntroWindow()
    intro.show()
    '''а если тут, то откроется, но мне нужно id передать'''
    #window = TerrariaCraftingApp()
    #window.show()

    app.exec()
