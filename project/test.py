import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,
    QComboBox, QMessageBox, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
# Список рецептов (замените на свои данные) и изображения
recipes = {
    "Деревянный меч": ["Дерево x10", "Image/wood.jpg"],
    "Медный короткий меч": ["Медная руда x8", "Image/copper.png"],
    "Железный короткий меч": ["Железная руда x8", "Image/iron.png"],
    "Серебряный короткий меч": ["Серебряная руда x8", "Image/silver.png"],
    "Золотой короткий меч": ["Золотая руда x8", "Image/gold.png"],
    "Каменная кирка": ["Камень x20", "Image/stone.png"],
}


class TerrariaCraftingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terraria Crafting")

        # Крафт
        self.craft_label = QLabel("Item to Craft:")
        self.craft_input = QLineEdit()
        self.craft_input.setReadOnly(True) # Делаем поле ввода только для чтения
        self.craft_button = QPushButton("Craft")
        self.craft_button.clicked.connect(self.show_recipe)

        self.recipe_label = QLabel("Recipe:")
        self.recipe_list = QComboBox()
        self.recipe_list.addItems(recipes.keys())
        self.recipe_list.currentTextChanged.connect(self.set_craft_input)
        # Убираем update_image из currentTextChanged, т.к. изображения показывать не нужно
        # self.recipe_list.currentTextChanged.connect(self.update_image)

        self.recipe_image_label = QLabel()
        self.recipe_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Макет
        grid = QGridLayout()
        grid.addWidget(self.craft_label, 0, 0)
        grid.addWidget(self.craft_input, 0, 1)
        grid.addWidget(self.craft_button, 1, 0, 1, 2)
        grid.addWidget(self.recipe_label, 2, 0)
        grid.addWidget(self.recipe_list, 2, 1)
        grid.addWidget(self.recipe_image_label, 3, 0, 1, 2)
        self.setLayout(grid)

        # Начальное обновление изображения
        self.update_image()

    def update_image(self):
        # Удаляем этот метод, т.к. изображения показывать не нужно
        # selected_item = self.recipe_list.currentText()
        # if selected_item in recipes:
        #     image_path = recipes[selected_item][1]
        #     try:
        #         pixmap = QPixmap(image_path)
        #         pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        #         self.recipe_image_label.setPixmap(pixmap)
        #     except FileNotFoundError:
        #         print(f"Image not found for {selected_item} at {image_path}")
        #         self.recipe_image_label.clear()
        pass # Оставляем пустой, чтобы ничего не делать

    def show_recipe(self):
        item_name = self.craft_input.text()
        if item_name in recipes:
            recipe = recipes[item_name]
            materials = recipe[0].split(" x")

            # Создаем QMessageBox с вертикальным макетом
            message_box = QMessageBox()
            message_box.setWindowTitle("Recipe")
            vbox = QVBoxLayout()

            # Добавляем текст рецепта
            text_label = QLabel(recipe[0])
            vbox.addWidget(text_label)

            # Добавляем изображения ресурсов
            for material in materials:
                material_name = material.split(" ")[0]
                material_count = int(material.split(" ")[1])

                # Проверяем, есть ли изображение для этого материала
                if f"Image/{material_name.lower()}.png" in recipes:
                    image_path = f"Image/{material_name.lower()}.png"
                    try:
                        pixmap = QPixmap(image_path)
                        pixmap = pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio)
                        image_label = QLabel()
                        image_label.setPixmap(pixmap)

                        # Добавляем изображение в горизонтальный макет
                        hbox = QHBoxLayout()
                        hbox.addWidget(image_label)
                        hbox.addWidget(QLabel(f"x{material_count}"))
                        vbox.addLayout(hbox)
                    except FileNotFoundError:
                        print(f"Image not found for {material_name} at {image_path}")

            message_box.setLayout(vbox)
            message_box.exec()
        else:
            QMessageBox.warning(self, "Error", "Item not found!")

    def set_craft_input(self, text):
        self.craft_input.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TerrariaCraftingApp()
    window.show()
    sys.exit(app.exec())

