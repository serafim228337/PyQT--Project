import sqlite3

def insert_recipes(db_path='terrariaapp.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    recipes_no = {
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
        "Terra Blade": [["Broken_Hero_Sword x1", "True_Excalibur x1", "True_Nights_Edge x1", ],
                        "Image/item/Terra_Blade.png"],
    }

    for name, (materials, image_path) in recipes_no.items():
        cursor.execute("INSERT OR IGNORE INTO recipes (name, materials, image_path) VALUES (?, ?, ?)",
                       (name, ", ".join(materials), image_path))
    conn.commit()
    conn.close()
