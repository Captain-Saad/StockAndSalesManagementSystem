import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from db_connection import DatabaseConnection

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("Initializing LoginWindow...")
        self.setWindowTitle("SSMS - Login")
        self.setGeometry(100, 100, 400, 500)
        self.setStyleSheet("background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1E2A44, stop:1 #2A3444);")

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Login Card
        card = QWidget()
        card.setFixedSize(300, 350)
        card.setStyleSheet("""
            QWidget {
                background: #2D3035;
                border-radius: 15px;
                border: 1px solid #495057;
            }
        """)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("SSMS Login")
        title.setFont(QFont("Helvetica", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: #F5F7FA;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)

        # Spacer
        card_layout.addSpacing(20)

        # Username Field
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: #3A3F4A;
                color: #F5F7FA;
                border: 1px solid #495057;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00C4B4;
            }
        """)
        card_layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background: #3A3F4A;
                color: #F5F7FA;
                border: 1px solid #495057;
                border-radius: 10px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00C4B4;
            }
        """)
        card_layout.addWidget(self.password_input)

        # Login Button
        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(40)
        login_btn.setFont(QFont("Helvetica", 12, QFont.Weight.Bold))
        login_btn.setStyleSheet("""
            QPushButton {
                background: #00C4B4;
                color: #FFFFFF;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:hover {
                background: #00E0C6;
            }
        """)
        login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(login_btn)

        # Forgot Password Link
        forgot_password = QPushButton("Forgot Password?")
        forgot_password.setFont(QFont("Helvetica", 10))
        forgot_password.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #ADB5BD;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                color: #00C4B4;
            }
        """)
        forgot_password.clicked.connect(self.show_forgot_password)
        card_layout.addWidget(forgot_password)

        layout.addWidget(card)
        print("LoginWindow initialized successfully.")

    def handle_login(self):
        print("Attempting login...")
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return

        # Authenticate against the database
        try:
            with DatabaseConnection() as conn:
                if conn is None:
                    QMessageBox.critical(self, "Database Error", "Failed to connect to the database.")
                    return

                try:
                    cursor = conn.cursor()
                    query = "SELECT username, role, email FROM users WHERE username = %s AND password = %s"
                    cursor.execute(query, (username, password))
                    user = cursor.fetchone()

                    if user:
                        print("Login successful, creating MainWindow...")
                        from gui.main_window import MainWindow
                        self.main_window = MainWindow(user=user)
                        print("MainWindow created, showing MainWindow...")
                        self.main_window.show()
                        print("MainWindow shown, closing LoginWindow...")
                        self.close()
                        print("LoginWindow closed.")
                    else:
                        QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Authentication failed: {e}")
                finally:
                    cursor.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error during login: {e}")

    def show_forgot_password(self):
        QMessageBox.information(self, "Forgot Password", "Please contact support@xai.com to reset your password.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())