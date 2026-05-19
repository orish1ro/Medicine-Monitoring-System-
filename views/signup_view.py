from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QCursor


class SignupView(QWidget):
    def __init__(self, on_signup=None, on_go_login=None):
        super().__init__()
        self.on_signup = on_signup
        self.on_go_login = on_go_login
        self.setWindowTitle("Medicine Management System — Create Account")
        self.setMinimumSize(900, 680)
        self._apply_styles()
        self._build_ui()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget#SignupRoot {
                background-color: #DDE1F0;
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollArea > QWidget > QWidget {
                background: transparent;
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
            QLabel#SuccessLabel {
                color: #16A34A;
                font-size: 12px;
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
                font-size: 20px;
            }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        self.setObjectName("SignupRoot")

        root_layout = QVBoxLayout(self)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root_layout.setContentsMargins(0, 20, 0, 20)

        # Scroll area for smaller screens
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scroll_content = QWidget()
        scroll_content.setObjectName("SignupRoot")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scroll_layout.setContentsMargins(0, 20, 0, 20)

        # Card
        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(460)
        card.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(0)

        # Icon circle
        icon_wrap = QHBoxLayout()
        icon_wrap.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_circle = QFrame()
        icon_circle.setObjectName("IconCircle")
        icon_circle.setFixedSize(64, 64)
        icon_inner = QVBoxLayout(icon_circle)
        icon_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl = QLabel("✚")
        icon_lbl.setObjectName("IconLabel")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        icon_inner.addWidget(icon_lbl)
        icon_wrap.addWidget(icon_circle)
        card_layout.addLayout(icon_wrap)
        card_layout.addSpacing(18)

        # Title
        title = QLabel("Create Account")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addSpacing(6)

        subtitle = QLabel("Register to access Medicine Management System")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setWordWrap(True)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(28)

        # Full Name
        self._add_field(card_layout, "Full Name", "full_name", "Enter your full name")
        card_layout.addSpacing(14)

        # Username
        self._add_field(card_layout, "Username", "username", "Choose a username")
        card_layout.addSpacing(14)

        # Email
        self._add_field(card_layout, "Email", "email", "Enter your email")
        card_layout.addSpacing(14)

        # Password
        self._add_field(card_layout, "Password", "password", "Create a password", password=True)
        card_layout.addSpacing(14)

        # Confirm Password
        self._add_field(card_layout, "Confirm Password", "confirm", "Repeat your password", password=True, enter_action=self._handle_signup)
        card_layout.addSpacing(22)

        # Create Account button
        btn = QPushButton("Create Account")
        btn.setObjectName("BtnPrimary")
        btn.setMinimumHeight(48)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.clicked.connect(self._handle_signup)
        card_layout.addWidget(btn)
        card_layout.addSpacing(8)

        # Error / success labels
        self.error_label = QLabel("")
        self.error_label.setObjectName("ErrorLabel")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setVisible(False)
        card_layout.addWidget(self.error_label)

        self.success_label = QLabel("")
        self.success_label.setObjectName("SuccessLabel")
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setVisible(False)
        card_layout.addWidget(self.success_label)

        card_layout.addSpacing(14)

        # Switch to login
        switch_row = QHBoxLayout()
        switch_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        switch_lbl = QLabel("Already have an account?")
        switch_lbl.setObjectName("SwitchLabel")
        btn_login = QPushButton("Sign in")
        btn_login.setObjectName("LinkBtn")
        btn_login.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_login.clicked.connect(self._go_login)
        switch_row.addWidget(switch_lbl)
        switch_row.addSpacing(4)
        switch_row.addWidget(btn_login)
        card_layout.addLayout(switch_row)

        scroll_layout.addWidget(card)
        scroll.setWidget(scroll_content)
        root_layout.addWidget(scroll)

    def _add_field(self, layout, label_text, attr_name, placeholder, password=False, enter_action=None):
        lbl = QLabel(label_text)
        lbl.setObjectName("FieldLabel")
        layout.addWidget(lbl)
        layout.addSpacing(6)
        inp = QLineEdit()
        inp.setObjectName("Input")
        inp.setPlaceholderText(placeholder)
        inp.setMinimumHeight(44)
        if password:
            inp.setEchoMode(QLineEdit.EchoMode.Password)
        if enter_action:
            inp.returnPressed.connect(enter_action)
        setattr(self, f"input_{attr_name}", inp)
        layout.addWidget(inp)

    # ── HANDLERS ──────────────────────────────────────────────
    def _handle_signup(self):
        full_name = self.input_full_name.text().strip()
        username  = self.input_username.text().strip()
        email     = self.input_email.text().strip()
        password  = self.input_password.text()
        confirm   = self.input_confirm.text()

        self.error_label.setVisible(False)
        self.success_label.setVisible(False)

        if not full_name:
            return self._show_error("Full name is required.")
        if len(username) < 3:
            return self._show_error("Username must be at least 3 characters.")
        if "@" not in email:
            return self._show_error("Please enter a valid email.")
        if len(password) < 4:
            return self._show_error("Password must be at least 4 characters.")
        if password != confirm:
            return self._show_error("Passwords do not match.")

        if self.on_signup:
            result = self.on_signup(full_name, username, email, password)
            if result and result.get("error"):
                self._show_error(result["error"])
            else:
                self._show_success("Account created! Redirecting to login...")
                QTimer.singleShot(1800, self._go_login)

    def _go_login(self):
        if self.on_go_login:
            self.on_go_login()

    def _show_error(self, msg: str):
        self.error_label.setText(msg)
        self.error_label.setVisible(True)

    def _show_success(self, msg: str):
        self.success_label.setText(msg)
        self.success_label.setVisible(True)

    def show_error(self, message: str):
        self._show_error(message)

    def clear(self):
        for attr in ["full_name", "username", "email", "password", "confirm"]:
            getattr(self, f"input_{attr}").clear()
        self.error_label.setVisible(False)
        self.success_label.setVisible(False)


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = SignupView(
        on_signup=lambda fn, u, e, p: print(f"Signup: {fn}, {u}, {e}"),
        on_go_login=lambda: print("Go to login")
    )
    win.show()
    sys.exit(app.exec())