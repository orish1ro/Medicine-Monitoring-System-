from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSizePolicy, QScrollArea, QStackedWidget
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QCursor


class DashboardView(QWidget):
    def __init__(self, username="User", on_navigate=None, on_logout=None):
        super().__init__()
        self.username    = username
        self.on_navigate = on_navigate
        self.on_logout   = on_logout
        self.setWindowTitle("Medicine Management System")
        self.setMinimumSize(1100, 650)
        self._apply_styles()
        self._build_ui()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget#DashRoot { background-color: #F3F4F8; }

            QFrame#Sidebar { background-color: #2D2D8E; }
            QLabel#BrandLabel { color:#FFFFFF; font-size:20px; font-weight:700; }

            QPushButton#NavBtn {
                color: rgba(255,255,255,0.75);
                background: transparent;
                border: none;
                border-left: 3px solid transparent;
                text-align: left;
                padding: 12px 18px;
                font-size: 14px;
            }
            QPushButton#NavBtn:hover {
                background-color: rgba(255,255,255,0.1);
                color: #FFFFFF;
            }
            QPushButton#NavBtnActive {
                color: #FFFFFF;
                background-color: #4F46E5;
                border: none;
                border-left: 3px solid #FFFFFF;
                text-align: left;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 600;
            }

            QFrame#Topbar {
                background-color: #FFFFFF;
                border-bottom: 1px solid #E5E7EB;
            }
            QLabel#TopTitle   { font-size:15px; font-weight:500; color:#374151; }
            QLabel#WelcomeLabel { font-size:13px; color:#6B7280; }

            QPushButton#LogoutBtn {
                color: #EF4444;
                border: 1.5px solid #EF4444;
                border-radius: 8px;
                padding: 6px 14px;
                font-size: 13px;
                font-weight: 500;
                background: transparent;
            }
            QPushButton#LogoutBtn:hover { background-color: #FEF2F2; }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        self.setObjectName("DashRoot")
        main = QHBoxLayout(self)
        main.setContentsMargins(0, 0, 0, 0)
        main.setSpacing(0)

        # ── Sidebar ──────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(230)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(0, 0, 0, 0)
        sb_layout.setSpacing(0)

        brand = QLabel("  MediTrack")
        brand.setObjectName("BrandLabel")
        brand.setContentsMargins(20, 22, 20, 18)
        sb_layout.addWidget(brand)

        self._nav_buttons = {}
        nav_items = [
            ("dashboard", "⊞  Dashboard"),
            ("inventory",  "⬡  View Inventory"),
            ("add",        "⊕  Add Medicine"),
            ("search",     "⌕  Search Medicine"),
            ("expiry",     "◷  Check Expiry"),
            ("report",     "☰  Generate Report"),
        ]
        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setObjectName("NavBtnActive" if key == "dashboard" else "NavBtn")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(lambda _, k=key: self._navigate(k))
            sb_layout.addWidget(btn)
            self._nav_buttons[key] = btn

        sb_layout.addStretch()
        main.addWidget(sidebar)

        # ── Right side ───────────────────────────────────────
        right = QWidget()
        right.setObjectName("DashRoot")
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)

        # Topbar
        topbar = QFrame()
        topbar.setObjectName("Topbar")
        topbar.setFixedHeight(56)
        tb = QHBoxLayout(topbar)
        tb.setContentsMargins(20, 0, 20, 0)

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setStyleSheet("border:none;background:transparent;color:#6B7280;font-size:14px;")
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.clicked.connect(self._handle_logout)

        top_title = QLabel("Medicine Management System")
        top_title.setObjectName("TopTitle")

        self.welcome_label = QLabel(f"Welcome, {self.username}")
        self.welcome_label.setObjectName("WelcomeLabel")

        logout_btn = QPushButton("⇥  Logout")
        logout_btn.setObjectName("LogoutBtn")
        logout_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        logout_btn.clicked.connect(self._handle_logout)

        tb.addWidget(close_btn)
        tb.addSpacing(8)
        tb.addWidget(top_title)
        tb.addStretch()
        tb.addWidget(self.welcome_label)
        tb.addSpacing(16)
        tb.addWidget(logout_btn)
        right_layout.addWidget(topbar)

        # ── Content area (swap views here) ───────────────────
        self.content_area = QScrollArea()
        self.content_area.setWidgetResizable(True)
        self.content_area.setStyleSheet("QScrollArea{border:none;background:#F3F4F8;}")
        right_layout.addWidget(self.content_area)

        main.addWidget(right)

        # Load default dashboard content
        self.show_dashboard_content()

    # ── SWAP CONTENT ─────────────────────────────────────────
    def set_content(self, widget: QWidget):
        """Replace the content area with any widget."""
        self.content_area.setWidget(widget)

    def show_dashboard_content(self, stats=None):
        """Build and show the dashboard overview with given stats."""
        if stats is None:
            stats = {"total": 0, "expired": 0, "expiring": 0, "low_stock": 0}

        content = QWidget()
        content.setObjectName("DashRoot")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(0)

        # Title
        title = QLabel("Dashboard Overview")
        title.setStyleSheet("font-size:22px;font-weight:700;color:#1A1A2E;")
        layout.addWidget(title)
        layout.addSpacing(20)

        # Stat cards
        stat_row = QHBoxLayout()
        stat_row.setSpacing(16)
        for icon, color, val, lbl in [
            ("⬡", "#3B82F6", stats["total"],     "Total Medicines"),
            ("⚠", "#EF4444", stats["expired"],   "Expired"),
            ("▦", "#F97316", stats["expiring"],  "Expiring Soon"),
            ("↘", "#F59E0B", stats["low_stock"], "Low Stock"),
        ]:
            card = QFrame()
            card.setStyleSheet("QFrame{background:#FFFFFF;border-radius:12px;}")
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            card.setMinimumHeight(110)
            cl = QVBoxLayout(card)
            cl.setContentsMargins(20, 16, 20, 16)
            cl.setSpacing(6)

            ic = QFrame()
            ic.setFixedSize(44, 44)
            ic.setStyleSheet(f"background:{color};border-radius:10px;")
            il = QVBoxLayout(ic)
            il.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ilbl = QLabel(icon)
            ilbl.setStyleSheet(f"color:#FFFFFF;font-size:18px;")
            ilbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            il.addWidget(ilbl)
            cl.addWidget(ic)

            vl = QLabel(str(val))
            vl.setStyleSheet(f"color:{color};font-size:28px;font-weight:700;")
            ll = QLabel(lbl)
            ll.setStyleSheet(f"color:{color};font-size:13px;")
            cl.addWidget(vl)
            cl.addWidget(ll)
            stat_row.addWidget(card)

        layout.addLayout(stat_row)
        layout.addSpacing(20)

        # Bottom row
        bottom = QHBoxLayout()
        bottom.setSpacing(16)

        # Quick Actions
        qc = QFrame()
        qc.setStyleSheet("QFrame{background:#FFFFFF;border-radius:12px;}")
        ql = QVBoxLayout(qc)
        ql.setContentsMargins(24, 20, 24, 24)
        ql.setSpacing(10)
        qt = QLabel("Quick Actions")
        qt.setStyleSheet("font-size:15px;font-weight:600;color:#374151;")
        ql.addWidget(qt)
        for label, key in [("Add New Medicine","add"),("Search Medicine","search"),("Generate Report","report")]:
            b = QPushButton(label)
            b.setMinimumHeight(46)
            b.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            b.setStyleSheet(
                "background:#4F46E5;color:#fff;border:none;border-radius:8px;font-size:14px;font-weight:600;"
                if key == "add" else
                "background:#F3F4F6;color:#374151;border:none;border-radius:8px;font-size:14px;"
            )
            b.clicked.connect(lambda _, k=key: self._navigate(k))
            ql.addWidget(b)
        ql.addStretch()
        bottom.addWidget(qc)

        # System Info
        sc = QFrame()
        sc.setFixedWidth(360)
        sc.setStyleSheet("QFrame{background:#FFFFFF;border-radius:12px;}")
        sl = QVBoxLayout(sc)
        sl.setContentsMargins(24, 20, 24, 24)
        sl.setSpacing(14)
        st = QLabel("System Information")
        st.setStyleSheet("font-size:15px;font-weight:600;color:#374151;")
        sl.addWidget(st)
        today = QDate.currentDate().toString("dd/MM/yyyy")
        for k, v, green in [
            ("Last Updated:", today, False),
            ("Storage:", "MySQL Database", False),
            ("Status:", "Active", True),
        ]:
            row = QHBoxLayout()
            kl = QLabel(k); kl.setStyleSheet("color:#6B7280;font-size:13px;")
            vl = QLabel(v); vl.setStyleSheet(
                f"color:{'#22C55E' if green else '#374151'};font-size:13px;font-weight:500;"
            )
            row.addWidget(kl); row.addStretch(); row.addWidget(vl)
            sl.addLayout(row)
        sl.addStretch()
        bottom.addWidget(sc)

        layout.addLayout(bottom)
        layout.addStretch()

        self.content_area.setWidget(content)

    # ── NAV ACTIVE STATE ─────────────────────────────────────
    def set_active_nav(self, key: str):
        for k, btn in self._nav_buttons.items():
            btn.setObjectName("NavBtnActive" if k == key else "NavBtn")
            btn.setStyle(btn.style())

    def set_username(self, username: str):
        self.username = username
        self.welcome_label.setText(f"Welcome, {username}")

    # ── HANDLERS ─────────────────────────────────────────────
    def _navigate(self, key: str):
        self.set_active_nav(key)
        if self.on_navigate:
            self.on_navigate(key)

    def _handle_logout(self):
        if self.on_logout:
            self.on_logout()


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = DashboardView(
        username="admin",
        on_navigate=lambda k: print(f"Navigate: {k}"),
        on_logout=lambda: print("Logout")
    )
    win.show_dashboard_content({
        "total": 24, "expired": 2, "expiring": 5, "low_stock": 3
    })
    win.show()
    sys.exit(app.exec())