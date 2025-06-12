import sys
from PyQt6.QtWidgets import QApplication
from gui.login_window import LoginWindow

if __name__ == "__main__":
    print(f"Python version: {sys.version}")
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())