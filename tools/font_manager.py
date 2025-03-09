import os
import sys
from PyQt6.QtGui import QFont, QFontDatabase

class FontManager:
    def __init__(self):
        self.font_files = [
            "Gilroy-Regular.ttf",
            "Gilroy-Bold.ttf",
            "Gilroy-Light.ttf",
            "Gilroy-Thin.ttf"
        ]

        # Détecter si l'application est compilée
        if getattr(sys, 'frozen', False):
            assets_path = os.path.join(os.path.dirname(sys.executable), "..", "Resources", "assets", "font")
        else:
            assets_path = os.path.abspath("assets/font/")

        self.font_families = set()
        self.load_fonts(assets_path)

        # Vérifier la famille de police trouvée
        if self.font_families:
            self.main_font_family = list(self.font_families)[0]  # 🔹 On prend la première famille
        else:
            self.main_font_family = "Arial"  # 🔹 Police de secours

    def load_fonts(self, font_path):
        """Charge les polices à partir du répertoire spécifié"""
        for font_file in self.font_files:
            font_file_path = os.path.join(font_path, font_file)
            font_id = QFontDatabase.addApplicationFont(font_file_path)

            if font_id == -1:
                print(f"Erreur : Impossible de charger {font_file}")
            else:
                family = QFontDatabase.applicationFontFamilies(font_id)[0]
                self.font_families.add(family)

    def get_font(self, weight="regular", size=12):
        """Renvoie une police selon le poids et la taille demandés"""
        weight_map = {
            "regular": QFont.Weight.Normal,
            "bold": QFont.Weight.Bold,
            "light": QFont.Weight.Light,
            "thin": QFont.Weight.Thin
        }

        font = QFont(self.main_font_family, size, weight_map.get(weight, QFont.Weight.Normal))
        return font