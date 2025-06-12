from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QMenu, QMessageBox, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor, QAction
from PyQt6.QtCore import QTimer, QDateTime

from gui.tabs.sales_tab import SalesTab
from gui.tabs.dashboard import DashboardTab
from gui.tabs.purchases_tab import PurchasesTab
from gui.tabs.stocks_tab import StocksTab
from gui.tabs.reports_tab import ReportsTab
from gui.tabs.software_tab import SoftwareTab
from gui.tabs.tools_tab import ToolsTab
from gui.tabs.user_management_tab import UserManagementTab

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedWidth(250)
        self.setStyleSheet("background: #2D3035;")
        self.layout = QVBoxLayout(self)

        self.user_label = QLabel(f"👤 {self.parent.username} ({self.parent.role})")
        self.user_label.setFont(QFont("Helvetica", 14, QFont.Weight.Bold))
        self.user_label.setStyleSheet("color: #F5F7FA; padding: 10px; background: #495057;")
        self.user_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.layout.addWidget(self.user_label)

        nav_items = [
            ("Dashboard", self.parent.open_dashboard),
            ("Sales", self.parent.open_sales),
            ("Purchases", self.parent.open_purchases),
            ("Stocks", self.parent.open_stocks),
            ("Reports", self.parent.open_reports),
            ("Software", self.parent.open_software),
            ("Tools", self.parent.open_tools),
            ("Exit", self.parent.quit)
        ]

        if self.parent.role == "Admin":
            nav_items.insert(-1, ("Admin Users", self.parent.open_user_management))

        for name, callback in nav_items:
            btn = QPushButton(f"📋 {name}")
            btn.setFont(QFont("Helvetica", 12))
            btn.setStyleSheet("""
                QPushButton {
                    background: transparent;
                    color: #F5F7FA;
                    text-align: left;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background: #495057;
                    color: #00C4B4;
                }
            """)
            btn.clicked.connect(callback)
            self.layout.addWidget(btn)

        self.layout.addStretch()
        footer = QLabel("SSMS v1.0")
        footer.setFont(QFont("Helvetica", 10))
        footer.setStyleSheet("color: #ADB5BD; padding: 10px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(footer)

class Header(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(70)
        self.setStyleSheet("background: #1E2A44;")
        self.layout = QHBoxLayout(self)

        title = QLabel("Sale & Stock Management System")
        title.setFont(QFont("Helvetica", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #F5F7FA;")
        self.layout.addWidget(title)

        self.datetime_label = QLabel("2025-04-25 12:00:00")
        self.datetime_label.setFont(QFont("Helvetica", 12))
        self.datetime_label.setStyleSheet("color: #ADB5BD;")
        self.layout.addWidget(self.datetime_label)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)  # 1000ms = 1 second
        self.update_datetime()  # Immediately set current datetime

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setFixedWidth(200)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background: #2D3035;
                color: #F5F7FA;
                border: 1px solid #495057;
                border-radius: 15px;
                padding: 5px 10px;
            }
            QLineEdit:focus {
                border: 1px solid #00C4B4;
            }
        """)
        self.layout.addWidget(self.search_bar)

        self.layout.addStretch()

        user_btn = QPushButton(f"👤 {parent.username} ({parent.role})")
        user_btn.setFont(QFont("Helvetica", 12))
        user_btn.setStyleSheet("""
            QPushButton {
                background: #2D3035;
                color: #F5F7FA;
                border-radius: 15px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background: #495057;
            }
        """)
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background: #2D3035;
                color: #F5F7FA;
                border: 1px solid #495057;
            }
            QMenu::item:selected {
                background: #495057;
            }
        """)
        menu.addAction(QAction("Profile", self))
        menu.addAction(QAction("Settings", self))
        menu.addAction(QAction("Logout", self, triggered=parent.quit))
        user_btn.setMenu(menu)
        self.layout.addWidget(user_btn)

    def update_datetime(self):
        now = QDateTime.currentDateTime()
        formatted = now.toString("yyyy-MM-dd HH:mm:ss")
        self.datetime_label.setText(formatted)


class MainWindow(QMainWindow):
    def __init__(self, user=None):
        super().__init__()
        self.user = user or {"username": "Guest", "role": "Viewer", "email": "guest@example.com"}
        self.username = self.user["username"]
        self.role = self.user["role"]
        self.email = self.user.get("email", "N/A")

        self.setWindowTitle("Sale & Stock Management System")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet("background: #1E2A44;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.header = Header(self)
        layout.addWidget(self.header)

        content = QWidget()
        content_layout = QHBoxLayout(content)
        self.sidebar = Sidebar(self)
        content_layout.addWidget(self.sidebar)

        self.stacked_widget = QStackedWidget()
        self.dashboard_tab = DashboardTab(self, user=self.user)
        self.sales_tab = SalesTab(user=self.user)
        self.purchases_tab = PurchasesTab(user=self.user)
        self.stocks_tab = StocksTab(user=self.user)
        self.reports_tab = ReportsTab(self)
        self.software_tab = SoftwareTab(user=self.user)
        self.tools_tab = ToolsTab(self)
        if self.role == "Admin":
            self.user_management_tab = UserManagementTab(self)
            self.stacked_widget.addWidget(self.user_management_tab)

        self.stacked_widget.addWidget(self.dashboard_tab)
        self.stacked_widget.addWidget(self.sales_tab)
        self.stacked_widget.addWidget(self.purchases_tab)
        self.stacked_widget.addWidget(self.stocks_tab)
        self.stacked_widget.addWidget(self.reports_tab)
        self.stacked_widget.addWidget(self.software_tab)
        self.stacked_widget.addWidget(self.tools_tab)

        content_layout.addWidget(self.stacked_widget)
        layout.addWidget(content)

        footer = QWidget()
        footer.setFixedHeight(40)
        footer.setStyleSheet("background: #2D3035;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.addWidget(QLabel("Powered by xAI"))
        footer_layout.addStretch()
        help_btn = QPushButton("Help & Support")
        help_btn.clicked.connect(self.show_help)
        footer_layout.addWidget(help_btn)
        layout.addWidget(footer)

        self.stacked_widget.setCurrentWidget(self.dashboard_tab)

    def open_dashboard(self): self.stacked_widget.setCurrentWidget(self.dashboard_tab)
    def open_sales(self): self.stacked_widget.setCurrentWidget(self.sales_tab)
    def open_purchases(self): self.stacked_widget.setCurrentWidget(self.purchases_tab)
    def open_stocks(self): self.stacked_widget.setCurrentWidget(self.stocks_tab)
    def open_reports(self): self.stacked_widget.setCurrentWidget(self.reports_tab)
    def open_software(self): self.stacked_widget.setCurrentWidget(self.software_tab)
    def open_tools(self): self.stacked_widget.setCurrentWidget(self.tools_tab)

    def open_user_management(self):
        print("Switching to User Management Tab...")
        self.stacked_widget.setCurrentWidget(self.user_management_tab)

    def show_help(self): QMessageBox.information(self, "Help", "Contact support@xai.com")
    def quit(self): self.close()
