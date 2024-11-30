import os
import sqlite3
import sys

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QLineEdit, QGridLayout,
    QComboBox, QMessageBox, QListWidget, QListWidgetItem,
    QWidget, QHBoxLayout, QDialog,
    QPushButton, QVBoxLayout, QLabel, QTextEdit, QInputDialog
)

from insert_recipes import insert_recipes


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_database_path():
    #путь к файлу бд
    user_home = os.path.expanduser("~")
    database_dir = os.path.join(user_home, "TerrariaCraftingApp")
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)
    return os.path.join(database_dir, "TerrariaApp.db")


class IntroWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добро пожаловать в Terraria Crafting App!")

        self.conn = sqlite3.connect(get_database_path())
        self.cursor = self.conn.cursor()

        self.create_tables()
        insert_recipes(get_database_path())  # Вставка рецептов

        self.setup_ui()

    def create_tables(self):
        #создание таблиц
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_recipes (
                user_id INTEGER,
                recipe_name TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                name TEXT PRIMARY KEY,
                materials TEXT,
                image_path TEXT
            )
        """)
        self.conn.commit()

    def setup_ui(self):
        #интерфейс
        self.title_label = QLabel("Terraria Crafting App")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.info_label = QLabel("Приложение для поиска рецептов в игре Terraria")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.font = self.info_label.font()
        self.font.setPointSize(10)
        self.info_label.setFont(self.font)

        self.info_button = QPushButton("Информация об игре")
        self.info_button.clicked.connect(self.show_info)

        self.login_button = QPushButton("Вход")
        self.login_button.clicked.connect(self.show_login_dialog)

        self.register_button = QPushButton("Регистрация")
        self.register_button.clicked.connect(self.show_register_dialog)

        vbox = QVBoxLayout()
        vbox.addWidget(self.title_label)
        vbox.addWidget(self.info_label)
        vbox.addWidget(self.info_button)
        vbox.addWidget(self.login_button)
        vbox.addWidget(self.register_button)
        vbox.addStretch()

        self.setLayout(vbox)

    def show_login_dialog(self):
        #вход
        username, ok = QInputDialog.getText(self, "Вход", "Введите имя пользователя:")
        if ok and username:
            password, ok = QInputDialog.getText(self, "Вход", "Введите пароль:")
            if ok and password:
                self.authenticate_user(username, password)

    def show_register_dialog(self):
        #регистрация
        dialog = QDialog(self)
        dialog.setWindowTitle("Регистрация")

        username_label = QLabel("Имя пользователя:")
        password_label = QLabel("Пароль:")
        username_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.EchoMode.Password)
        register_button = QPushButton("Зарегистрироваться")

        grid = QGridLayout()
        grid.addWidget(username_label, 0, 0)
        grid.addWidget(username_input, 0, 1)
        grid.addWidget(password_label, 1, 0)
        grid.addWidget(password_input, 1, 1)
        grid.addWidget(register_button, 2, 0, 1, 2)

        dialog.setLayout(grid)

        register_button.clicked.connect(lambda: self.register_user(username_input.text(), password_input.text()))

        dialog.exec()

    def authenticate_user(self, username, password):
        #аутентификация пользователя
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = self.cursor.fetchone()
        if user:
            if password == user[2]:
                self.user_id = user[0]
                self.open_crafting_app(self.user_id)
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль!")
        else:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден!")

    def register_user(self, username, password):
        #регистрация пользователя
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if self.cursor.fetchone():
            QMessageBox.warning(self, "Ошибка", "Пользователь с таким именем уже существует!")
            return

        self.cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        QMessageBox.information(self, "Успешно", "Пользователь успешно зарегистрирован!")

    def show_info(self):
        #окно краткой информации об игре
        info_dialog = QDialog(self)
        info_dialog.setWindowTitle("О Terraria")

        text_edit = QTextEdit(info_dialog)
        text_edit.setText("Terraria - это инди игра в жанре песочницы с элементами экшена и приключений. \n"
                          "Игрок создает своего персонажа, исследует мир, строит дома, "
                          "создает оружие и сражается с разнообразными монстрами. \n"
                          "Игра отличается большой свободой действий, "
                          "возможностью крафта и исследования огромного мира. \n")
        text_edit.setReadOnly(True)

        close_button = QPushButton("Закрыть", info_dialog)
        close_button.clicked.connect(info_dialog.close)

        vbox = QVBoxLayout()
        vbox.addWidget(text_edit)
        vbox.addWidget(close_button)

        info_dialog.setLayout(vbox)
        info_dialog.exec()

    def open_crafting_app(self, user_id):
        #открывает основное приложение, закрываем интро
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

        self.conn = sqlite3.connect(get_database_path())
        self.cursor = self.conn.cursor()

        self.setWindowTitle("Terraria Crafting")

        self.user_id = user_id

        self.favorite_button = QPushButton("Избранное")
        self.favorite_button.clicked.connect(self.toggle_favorite)

        self.craft_label = QLabel("Выбранный предмет:")
        self.craft_input = QLineEdit()
        self.craft_input.setReadOnly(True)
        self.craft_button = QPushButton("Крафт")
        self.craft_button.clicked.connect(self.show_recipe)
        self.craft_button.clicked.connect(self.export_materials_to_txt)  # Добавлено для экспорта материалов
        self.craft_button.clicked.connect(self.update_materials_list)

        self.recipe_label = QLabel("Рецепт:")
        self.recipe_list = QComboBox()

        self.load_recipes()
        self.recipe_list.currentTextChanged.connect(self.set_craft_input)
        self.recipe_list.currentTextChanged.connect(self.update_image)
        self.recipe_list.currentTextChanged.connect(self.update_materials_list)

        self.recipe_image_label = QLabel()
        self.recipe_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.favorite_recipes_list = QListWidget(self)
        for recipe_name in self.load_favorite_recipes():
            self.favorite_recipes_list.addItem(recipe_name)
        self.favorite_recipes_list.currentTextChanged.connect(self.set_craft_input)
        self.favorite_recipes_list.currentTextChanged.connect(self.update_image)
        self.favorite_recipes_list.currentTextChanged.connect(self.update_materials_list)

        self.materials_label = QLabel("Материалы:")
        self.materials_list = QListWidget()
        self.update_materials_list()

        grid = QGridLayout()

        grid.addWidget(self.craft_label, 0, 0)
        grid.addWidget(self.craft_input, 0, 1)
        grid.addWidget(self.craft_button, 1, 0, 1, 3)
        grid.addWidget(self.recipe_label, 2, 0)
        grid.addWidget(self.recipe_list, 2, 1, 1, 3)
        grid.addWidget(self.recipe_image_label, 3, 0, 1, 3)
        grid.addWidget(self.favorite_button, 0, 2)
        grid.addWidget(QLabel("Избранные рецепты:"), 5, 0)
        grid.addWidget(self.favorite_recipes_list, 0, 4, 0, 2)
        grid.addWidget(self.materials_label, 4, 0)
        grid.addWidget(self.materials_list, 5, 0, 1, 3)
        self.setLayout(grid)

        self.update_image()

    def load_recipes(self):
        #загрузка рецептов из бд
        self.cursor.execute("SELECT name FROM recipes")
        recipes = [row[0] for row in self.cursor.fetchall()]
        self.recipe_list.addItems(recipes)

    def load_favorite_recipes(self):
        #загрузка избранных рецептов
        self.cursor.execute("SELECT recipe_name FROM favorite_recipes WHERE user_id = ?", (self.user_id,))
        self.favorite_recipes = [row[0] for row in self.cursor.fetchall()]
        self.update_favorite_button()
        return self.favorite_recipes

    def toggle_favorite(self):
        #проверка на избранное
        selected_item = self.recipe_list.currentText()
        item = QListWidgetItem(selected_item)

        if selected_item in self.favorite_recipes:
            #убрать рецепт из избранного
            list_items = self.favorite_recipes_list.findItems(selected_item, Qt.MatchFlag.MatchExactly)
            for item in list_items:
                self.favorite_recipes_list.takeItem(self.favorite_recipes_list.row(item))
            self.favorite_recipes.remove(selected_item)
            self.cursor.execute("DELETE FROM favorite_recipes WHERE user_id = ? AND recipe_name = ?",
                                (self.user_id, selected_item))
        else:
            # добавить рецепт
            self.favorite_recipes.append(selected_item)
            self.favorite_recipes_list.addItem(item)
            self.cursor.execute("INSERT INTO favorite_recipes (user_id, recipe_name) VALUES (?, ?)",
                                (self.user_id, selected_item))

        self.conn.commit()
        self.update_favorite_button()

    def update_favorite_button(self):
        #обновить текст кнопки избранное
        selected_item = self.recipe_list.currentText()
        if selected_item in self.favorite_recipes:
            self.favorite_button.setText("Избранное (✔)")
        else:
            self.favorite_button.setText("Избранное")

    def update_image(self):
        #обновить изображение
        selected_item = self.recipe_list.currentText()
        self.update_favorite_button()
        if selected_item:
            self.cursor.execute("SELECT image_path FROM recipes WHERE name = ?", (selected_item,))
            image_path = resource_path(self.cursor.fetchone()[0])
            try:
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(100, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.recipe_image_label.setPixmap(pixmap)
            except FileNotFoundError:
                print(f"Image not found for {selected_item} at {image_path}")
                self.recipe_image_label.clear()

    def show_recipe(self):
        #показать детали рецепта
        selected_item = self.recipe_list.currentText()
        if selected_item:
            self.cursor.execute("SELECT materials FROM recipes WHERE name = ?", (selected_item,))
            materials = self.cursor.fetchone()[0]
            QMessageBox.information(self, "Recipe", materials)
        else:
            QMessageBox.warning(self, "Error", "Item not found!")

    def set_craft_input(self, text):
        #взять название выбранного рецепта
        self.recipe_list.setCurrentText(text)
        self.craft_input.setText(text)

    def update_materials_list(self):
        #обновления списка материалов
        selected_item = self.recipe_list.currentText()
        if selected_item:
            self.materials_list.clear()
            self.cursor.execute("SELECT materials FROM recipes WHERE name = ?", (selected_item,))
            materials = self.cursor.fetchone()[0].split(", ")
            for material in materials:
                material_name, material_count = material.split(" x")

                image_path = resource_path(f"Image/Materials/{material_name}.png")
                image_label = QLabel()
                try:
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
                    image_label.setPixmap(pixmap)
                except FileNotFoundError:
                    image_label.setText("")

                hbox = QHBoxLayout()
                hbox.setSpacing(10)

                hbox.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignLeft)

                text_label = QLabel(f"{material_name} x {material_count}")
                text_label.setFixedSize(200, 20)
                text_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                hbox.addWidget(text_label)

                widget = QWidget()
                widget.setLayout(hbox)

                item = QListWidgetItem()
                item.setSizeHint(QSize(150, 50))
                self.materials_list.addItem(item)
                self.materials_list.setItemWidget(item, widget)

        else:
            self.materials_list.clear()

    def export_materials_to_txt(self):
        #вывод рецепта в txt файл
        selected_item = self.recipe_list.currentText()
        if selected_item:
            self.cursor.execute("SELECT materials FROM recipes WHERE name = ?", (selected_item,))
            materials = self.cursor.fetchone()[0]
            file_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "recipes.txt")
            with open(file_path, 'a', encoding='utf-8') as file:
                file.write(f"\nМатериалы для {selected_item}:\n")
                file.write(materials + "\n")
            QMessageBox.information(self, "Успешно", f"Материалы для {selected_item} добавлены в {file_path}")

    def closeEvent(self, event):
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    intro = IntroWindow()
    intro.show()

    app.exec()
