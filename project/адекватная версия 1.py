import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,
    QComboBox, QMessageBox, QVBoxLayout, QListWidget, QListWidgetItem,
    QWidget, QLabel, QHBoxLayout, QMainWindow, QDialog,
    QPushButton, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

recipes = {
    "Wooden Sword": [["Wood x10"], "Image/Wooden_Sword.png"],
    "Copper Shortsword": [["Copper Bar x8", "Wood x10"], "Image/Copper_Shortsword.png"],
    "Iron Shortsword": [["Iron Bar x8"], "Image/Iron_Shortsword.png"],
    "Silver Shortsword": [["Silver Bar x8"], "Image/Silver_Shortsword.png"],
    "Gold Shortsword": [["Gold Bar x8"], "Image/Gold_Shortsword.png"],
    "Copper Axe": [["Copper Bar x8"], "Image/copper_bar.png"],
    "Iron Axe": [["Iron Bar x8"], "Image/iron_bar.png"],
    "Silver Axe": [["Silver Bar x8"], "Image/silver_bar.png"],
    "Gold Axe": [["Gold Bar x8"], "Image/gold_bar.png"],
    "Copper Pickaxe": [["Copper Bar x8"], "Image/copper_bar.png"],
    "Iron Pickaxe": [["Iron Bar x8"], "Image/iron_bar.png"],
    "Silver Pickaxe": [["Silver Bar x8"], "Image/silver_bar.png"],
    "Gold Pickaxe": [["Gold Bar x8"], "Image/gold_bar.png"],
}


class IntroWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to Terraria Crafting!")
        self.resize(400, 200)

        vbox = QVBoxLayout()

        label = QLabel(
            "Welcome to the Terraria Crafting app! \nThis app shows you the recipes for various Terraria items.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox.addWidget(label)

        button = QPushButton("Continue")
        button.clicked.connect(self.close)
        vbox.addWidget(button)

        self.setLayout(vbox)


class TerrariaCraftingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Terraria Crafting")

        # Крафт
        self.craft_label = QLabel("Item to Craft:")
        self.craft_input = QLineEdit("Wooden Sword")
        self.craft_input.setReadOnly(True)  # Делаем поле ввода только для чтения
        self.craft_button = QPushButton("Craft")
        self.craft_button.clicked.connect(self.show_recipe)
        self.craft_button.clicked.connect(self.update_materials_list)  # Добавили в сигнал

        self.recipe_label = QLabel("Recipe:")
        self.recipe_list = QComboBox()
        self.recipe_list.addItems(recipes.keys())
        self.recipe_list.currentTextChanged.connect(self.set_craft_input)
        self.recipe_list.currentTextChanged.connect(self.update_image)
        self.recipe_list.currentTextChanged.connect(self.update_materials_list)  # Добавили в сигнал

        self.recipe_image_label = QLabel()
        self.recipe_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Список материалов
        self.materials_label = QLabel("Materials:")
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
        selected_item = self.recipe_list.currentText()
        if selected_item in recipes:
            string = "\n".join(recipes[selected_item][0])
            QMessageBox.information(self, "Recipe", string)
        else:
            QMessageBox.warning(self, "Error", "Item not found!")

    def set_craft_input(self, text):
        self.craft_input.setText(text)

    def update_materials_list(self):
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
                hbox.setSpacing(10)  # Устанавливаем отступ в 5 пикселей

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    intro = IntroWindow()
    intro.exec()  # Отображаем вступительное окно

    window = TerrariaCraftingApp()
    window.show()
    sys.exit(app.exec())
