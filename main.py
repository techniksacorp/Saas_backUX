import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from ui import MainWindow
from tools.font_manager import FontManager

if __name__ == "__main__":

    
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("IconeMACOS.icns"))
    font_manager = FontManager()
    font = font_manager.get_font("regular", 12)
    app.setFont(font)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

# app = QApplication(sys.argv)
# app.setWindowIcon(QIcon("IconeMACOS.icns"))

# window = MainWindow()
# window.show()
# sys.exit(app.exec())