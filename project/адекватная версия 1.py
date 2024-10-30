import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,
    QComboBox, QMessageBox, QVBoxLayout, QListWidget, QListWidgetItem,
    QWidget, QLabel, QHBoxLayout, QMainWindow, QDialog,
    QPushButton, QVBoxLayout, QLabel
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

# Список рецептов (замените на свои данные) и изображения
recipes = {
    "Wooden Sword": ["Wood x10", "Image/Wooden_Sword.png"],
    "Copper Shortsword": ["Copper Bar x8", "Image/Copper_Shortsword.png"],
    "Iron Shortsword": ["Iron Bar x8", "Image/Iron_Shortsword.png"],
    "Silver Shortsword": ["Silver Bar x8", "Image/Silver_Shortsword.png"],
    "Gold Shortsword": ["Gold Bar x8", "Image/Gold_Shortsword.png"],
    "Stone Pickaxe": ["Stone x20", "Image/stone.png"],
    "Wooden Axe": ["Wood x10", "Image/Wood.png"],
    "Stone Axe": ["Stone x20", "Image/stone.png"],
    "Copper Axe": ["Copper Bar x8", "Image/copper_bar.png"],
    "Iron Axe": ["Iron Bar x8", "Image/iron_bar.png"],
    "Silver Axe": ["Silver Bar x8", "Image/silver_bar.png"],
    "Gold Axe": ["Gold Bar x8", "Image/gold_bar.png"],
    "Wooden Hammer": ["Wood x10", "Image/Wood.png"],
    "Stone Hammer": ["Stone x20", "Image/stone.png"],
    "Copper Hammer": ["Copper Bar x8", "Image/copper_bar.png"],
    "Iron Hammer": ["Iron Bar x8", "Image/iron_bar.png"],
    "Silver Hammer": ["Silver Bar x8", "Image/silver_bar.png"],
    "Gold Hammer": ["Gold Bar x8", "Image/gold_bar.png"],
    "Wooden Pickaxe": ["Wood x10", "Image/Wood.png"],
    "Copper Pickaxe": ["Copper Bar x8", "Image/copper_bar.png"],
    "Iron Pickaxe": ["Iron Bar x8", "Image/iron_bar.png"],
    "Silver Pickaxe": ["Silver Bar x8", "Image/silver_bar.png"],
    "Gold Pickaxe": ["Gold Bar x8", "Image/gold_bar.png"],
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
        self.craft_input = QLineEdit()
        self.craft_input.setReadOnly(True)  # Делаем поле ввода только для чтения
        self.craft_button = QPushButton("Craft")
        self.craft_button.clicked.connect(self.show_recipe)

        self.recipe_label = QLabel("Recipe:")
        self.recipe_list = QComboBox()
        self.recipe_list.addItems(recipes.keys())
        self.recipe_list.currentTextChanged.connect(self.set_craft_input)
        self.recipe_list.currentTextChanged.connect(self.update_image)  # Вернули строчку

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
        selected_item = self.recipe_list.currentText()
        if selected_item in recipes:
            image_path = recipes[selected_item][1]
            try:
                pixmap = QPixmap(image_path)
                pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
                self.recipe_image_label.setPixmap(pixmap)
            except FileNotFoundError:
                print(f"Image not found for {selected_item} at {image_path}")
                self.recipe_image_label.clear()

    def show_recipe(self):
        item_name = self.craft_input.text()
        if item_name in recipes:
            recipe = recipes[item_name]
            QMessageBox.information(self, "Recipe", recipe[0])
        else:
            QMessageBox.warning(self, "Error", "Item not found!")

    def set_craft_input(self, text):
        self.craft_input.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    intro = IntroWindow()
    intro.exec() # Отображаем вступительное окно

    window = TerrariaCraftingApp()
    window.show()
    sys.exit(app.exec())