from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QColor, QPalette, QCursor


class LoginView(QWidget):
    def __init__(self, on_login=None, on_go_signup=None):
        super().__init__()
        self.on_login = on_login
        self.on_go_signup = on_go_signup
        self.setWindowTitle("Medicine Management System")
        self.setMinimumSize(900, 600)
        self._apply_styles()
        self._build_ui()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget#LoginRoot {
                background-color: #DDE1F0;
            }
            QFrame#Card {
                background-color: #FFFFFF;
                border-radius: 16px;
            }
            QLabel#Title {
                font-size: 22px;
                font-weight: 700;
                color: #1A1A2E;
            }
            QLabel#Subtitle {
                font-size: 13px;
                color: #6B7280;
            }
            QLabel#FieldLabel {
                font-size: 13px;
                font-weight: 500;
                color: #374151;
            }
            QLineEdit#Input {
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                padding: 10px 14px;
                font-size: 14px;
                color: #1F2937;
                background: #FFFFFF;
            }
            QLineEdit#Input:focus {
                border: 1.5px solid #4F46E5;
            }
            QPushButton#BtnPrimary {
                background-color: #4F46E5;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px;
            }
            QPushButton#BtnPrimary:hover {
                background-color: #4338CA;
            }
            QPushButton#BtnPrimary:pressed {
                background-color: #3730A3;
            }
            QLabel#ErrorLabel {
                color: #DC2626;
                font-size: 12px;
            }
            QLabel#DemoLabel {
                color: #9CA3AF;
                font-size: 11px;
            }
            QPushButton#LinkBtn {
                color: #4F46E5;
                font-size: 13px;
                font-weight: 600;
                border: none;
                background: transparent;
                padding: 0;
            }
            QPushButton#LinkBtn:hover {
                color: #4338CA;
                text-decoration: underline;
            }
            QLabel#SwitchLabel {
                color: #6B7280;
                font-size: 13px;
            }
            QFrame#IconCircle {
                background-color: #4F46E5;
                border-radius: 32px;
            }
            QLabel#IconLabel {
                color: #FFFFFF;
                font-size: 24px;
            }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        self.setObjectName("LoginRoot")

        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.setContentsMargins(0, 0, 0, 0)

        # Card
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(440)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 44, 40, 40)
        card_layout.setSpacing(0)

        # Icon circle
        icon_wrap = QHBoxLayout()
        icon_wrap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_circle = QFrame()
        icon_circle.setObjectName("IconCircle")
        icon_circle.setFixedSize(64, 64)
        icon_inner = QVBoxLayout(icon_circle)
        icon_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl = QLabel("→")
        icon_lbl.setObjectName("IconLabel")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        icon_inner.addWidget(icon_lbl)
        icon_wrap.addWidget(icon_circle)
        card_layout.addLayout(icon_wrap)
        card_layout.addSpacing(18)

        # Title
        title = QLabel("Medicine Management System")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addSpacing(6)

        subtitle = QLabel("Sign in to manage inventory")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(28)

        # Username
        lbl_user = QLabel("Username")
        lbl_user.setObjectName("FieldLabel")
        card_layout.addWidget(lbl_user)
        card_layout.addSpacing(6)
        self.input_user = QLineEdit()
        self.input_user.setObjectName("Input")
        self.input_user.setPlaceholderText("Enter username")
        self.input_user.setMinimumHeight(44)
        card_layout.addWidget(self.input_user)
        card_layout.addSpacing(16)

        # Password
        lbl_pass = QLabel("Password")
        lbl_pass.setObjectName("FieldLabel")
        card_layout.addWidget(lbl_pass)
        card_layout.addSpacing(6)
        self.input_pass = QLineEdit()
        self.input_pass.setObjectName("Input")
        self.input_pass.setPlaceholderText("Enter password")
        self.input_pass.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_pass.setMinimumHeight(44)
        self.input_pass.returnPressed.connect(self._handle_login)
        card_layout.addWidget(self.input_pass)
        card_layout.addSpacing(22)

        # Sign In button
        btn_login = QPushButton("Sign In")
        btn_login.setObjectName("BtnPrimary")
        btn_login.setMinimumHeight(48)
        btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_login.clicked.connect(self._handle_login)
        card_layout.addWidget(btn_login)
        card_layout.addSpacing(8)

        # Error label
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)

        # Demo hint
        demo = QLabel("Demo: Use any username (3+ chars) and password (4+ chars)")
        demo.setObjectName("DemoLabel")
        demo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(4)
        card_layout.addWidget(demo)
        card_layout.addSpacing(14)

        # Switch to signup
        switch_row = QHBoxLayout()
        switch_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        switch_lbl = QLabel("Don't have an account?")
        switch_lbl.setObjectName("SwitchLabel")
        btn_signup = QPushButton("Sign up")
        btn_signup.setObjectName("LinkBtn")
        btn_signup.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_signup.clicked.connect(self._go_signup)
        switch_row.addWidget(switch_lbl)
        switch_row.addSpacing(4)
        switch_row.addWidget(btn_signup)
        card_layout.addLayout(switch_row)

        root_layout.addWidget(card)

    # ── HANDLERS ──────────────────────────────────────────────
    def _handle_login(self):
        username = self.input_user.text().strip()
        password = self.input_pass.text().strip()
        if len(username) < 3 or len(password) < 4:
            self.error_label.setText("Invalid username or password.")
            self.error_label.setVisible(True)
            return
        self.error_label.setVisible(False)
        if self.on_login:
            self.on_login(username, password)

    def _go_signup(self):
        if self.on_go_signup:
            self.on_go_signup()

    def show_error(self, message: str):
        self.error_label.setText(message)
        self.error_label.setVisible(True)

    def clear(self):
        self.input_user.clear()
        self.input_pass.clear()
        self.error_label.setVisible(False)


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = LoginView(
        on_login=lambda u, p: print(f"Login: {u} / {p}"),
        on_go_signup=lambda: print("Go to signup")
    )
    win.show()
    sys.exit(app.exec())