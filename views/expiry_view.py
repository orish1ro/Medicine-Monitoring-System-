from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpinBox, QTabWidget, QAbstractItemView,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from controllers.expiry_controller import (
    controller_get_expired,
    controller_get_expiring_soon,
    controller_get_alerts,
    controller_resolve_alert,
)
from utils.helpers import format_date, days_until_expiry


class ExpiryView(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self._apply_styles()
        self._build_ui()
        self._load_data()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F3F4F8; }

            QFrame#ControlCard {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QLabel#PageTitle {
                font-size: 22px;
                font-weight: 700;
                color: #1A1A2E;
            }
            QLabel#FieldLabel {
                font-size: 13px;
                font-weight: 500;
                color: #374151;
            }
            QLabel#CountLabel {
                font-size: 13px;
                color: #6B7280;
            }
            QSpinBox#Input {
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1F2937;
                background: #FFFFFF;
                min-height: 38px;
            }
            QSpinBox#Input:focus { border: 1.5px solid #4F46E5; }

            QPushButton#BtnCheck {
                background-color: #4F46E5;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 22px;
                min-height: 40px;
            }
            QPushButton#BtnCheck:hover { background-color: #4338CA; }

            QPushButton#BtnResolve {
                background-color: #DCFCE7;
                color: #166534;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 500;
                padding: 5px 12px;
            }
            QPushButton#BtnResolve:hover { background-color: #BBF7D0; }

            QTabWidget::pane {
                background: #FFFFFF;
                border: none;
                border-radius: 12px;
            }
            QTabBar::tab {
                background: #F3F4F6;
                color: #6B7280;
                border: none;
                border-radius: 8px;
                padding: 9px 20px;
                font-size: 13px;
                font-weight: 500;
                margin-right: 6px;
            }
            QTabBar::tab:selected {
                background: #4F46E5;
                color: #FFFFFF;
                font-weight: 600;
            }

            QTableWidget {
                background: #FFFFFF;
                border: none;
                font-size: 13px;
                gridline-color: #F3F4F6;
            }
            QTableWidget::item { padding: 8px 12px; color: #374151; }
            QTableWidget::item:selected {
                background-color: #EEF2FF;
                color: #1F2937;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                color: #6B7280;
                font-size: 12px;
                font-weight: 600;
                padding: 10px 12px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
            }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(16)

        # Page title
        title = QLabel("Check Expiry")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        # Control card
        ctrl_card = QFrame()
        ctrl_card.setObjectName("ControlCard")
        ctrl_layout = QHBoxLayout(ctrl_card)
        ctrl_layout.setContentsMargins(24, 16, 24, 16)
        ctrl_layout.setSpacing(12)

        lbl = QLabel("Show medicines expiring within")
        lbl.setObjectName("FieldLabel")
        self.spin_days = QSpinBox()
        self.spin_days.setObjectName("Input")
        self.spin_days.setRange(1, 365)
        self.spin_days.setValue(30)
        self.spin_days.setFixedWidth(90)
        lbl2 = QLabel("days")
        lbl2.setObjectName("FieldLabel")

        btn_check = QPushButton("◷  Refresh")
        btn_check.setObjectName("BtnCheck")
        btn_check.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_check.clicked.connect(self._load_data)

        ctrl_layout.addWidget(lbl)
        ctrl_layout.addWidget(self.spin_days)
        ctrl_layout.addWidget(lbl2)
        ctrl_layout.addStretch()
        ctrl_layout.addWidget(btn_check)
        root.addWidget(ctrl_card)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Tab 1: Expired
        self.table_expired = self._make_table(["Name", "Category", "Qty", "Unit", "Expiry Date", "Days Overdue"])
        self.tabs.addTab(self._wrap_table(self.table_expired), "⚠  Expired")

        # Tab 2: Expiring Soon
        self.table_expiring = self._make_table(["Name", "Category", "Qty", "Unit", "Expiry Date", "Days Left"])
        self.tabs.addTab(self._wrap_table(self.table_expiring), "◷  Expiring Soon")

        # Tab 3: Alerts
        self.table_alerts = self._make_table(["ID", "Type", "Medicine", "Message", "Action"])
        self.table_alerts.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table_alerts.setColumnWidth(4, 110)
        self.tabs.addTab(self._wrap_table(self.table_alerts), "🔔  Alerts")

        root.addWidget(self.tabs)

    def _make_table(self, headers):
        t = QTableWidget()
        t.setColumnCount(len(headers))
        t.setHorizontalHeaderLabels(headers)
        t.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        t.verticalHeader().setVisible(False)
        t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        t.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        t.setAlternatingRowColors(True)
        t.setStyleSheet(t.styleSheet() + "QTableWidget{alternate-background-color:#F9FAFB;}")
        return t

    def _wrap_table(self, table):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.addWidget(table)
        return w

    # ── LOAD DATA ─────────────────────────────────────────────
    def _load_data(self):
        days = self.spin_days.value()
        try:
            expired  = controller_get_expired()
            expiring = controller_get_expiring_soon(days)
            alerts   = controller_get_alerts()
        except Exception as e:
            return

        self._populate_expired(expired)
        self._populate_expiring(expiring)
        self._populate_alerts(alerts)

        # Update tab labels with counts
        self.tabs.setTabText(0, f"⚠  Expired  ({len(expired)})")
        self.tabs.setTabText(1, f"◷  Expiring Soon  ({len(expiring)})")
        self.tabs.setTabText(2, f"🔔  Alerts  ({len(alerts)})")

    def _populate_expired(self, medicines):
        self.table_expired.setRowCount(0)
        if not medicines:
            self._set_empty(self.table_expired, "No expired medicines — great!", 6)
            return
        for i, m in enumerate(medicines):
            self.table_expired.insertRow(i)
            days_over = abs(days_until_expiry(m["expiry_date"]))
            self._set_row(self.table_expired, i, [
                m["name"], m.get("category_name", ""), str(m["quantity"]),
                m.get("unit_name", ""), format_date(m["expiry_date"]), str(days_over)
            ], bold_col=0)
            # Highlight row red
            for col in range(6):
                item = self.table_expired.item(i, col)
                if item:
                    item.setForeground(QColor("#991B1B"))
                    item.setBackground(QColor("#FEF2F2"))
            self.table_expired.setRowHeight(i, 46)

    def _populate_expiring(self, medicines):
        self.table_expiring.setRowCount(0)
        if not medicines:
            self._set_empty(self.table_expiring, "No medicines expiring in this window.", 6)
            return
        for i, m in enumerate(medicines):
            self.table_expiring.insertRow(i)
            days_left = days_until_expiry(m["expiry_date"])
            self._set_row(self.table_expiring, i, [
                m["name"], m.get("category_name", ""), str(m["quantity"]),
                m.get("unit_name", ""), format_date(m["expiry_date"]), str(days_left)
            ], bold_col=0)
            for col in range(6):
                item = self.table_expiring.item(i, col)
                if item:
                    item.setForeground(QColor("#92400E"))
                    item.setBackground(QColor("#FFFBEB"))
            self.table_expiring.setRowHeight(i, 46)

    def _populate_alerts(self, alerts):
        self.table_alerts.setRowCount(0)
        if not alerts:
            self._set_empty(self.table_alerts, "No unresolved alerts.", 5)
            return
        for i, a in enumerate(alerts):
            self.table_alerts.insertRow(i)
            self._set_row(self.table_alerts, i, [
                str(a["id"]), str(a.get("alert_type", "")),
                str(a.get("medicine_name", "")), str(a.get("message", ""))
            ])
            # Resolve button
            from PyQt6.QtWidgets import QWidget as _W, QHBoxLayout as _H
            btn_wrap = _W()
            btn_layout = _H(btn_wrap)
            btn_layout.setContentsMargins(6, 2, 6, 2)
            btn = QPushButton("Resolve")
            btn.setObjectName("BtnResolve")
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn.clicked.connect(lambda _, aid=a["id"]: self._resolve_alert(aid))
            btn_layout.addWidget(btn)
            self.table_alerts.setCellWidget(i, 4, btn_wrap)
            self.table_alerts.setRowHeight(i, 46)

    # ── HELPERS ───────────────────────────────────────────────
    def _set_row(self, table, row_idx, values, bold_col=None):
        for col, val in enumerate(values):
            item = QTableWidgetItem(str(val))
            if col == bold_col:
                f = item.font(); f.setBold(True); item.setFont(f)
            table.setItem(row_idx, col, item)

    def _set_empty(self, table, msg, col_span):
        table.setRowCount(1)
        item = QTableWidgetItem(msg)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        item.setForeground(QColor("#9CA3AF"))
        table.setItem(0, 0, item)
        table.setSpan(0, 0, 1, col_span)

    def _resolve_alert(self, alert_id):
        try:
            success = controller_resolve_alert(alert_id)
            if success:
                QMessageBox.information(self, "Resolved", f"Alert #{alert_id} has been resolved.")
                self._load_data()
            else:
                QMessageBox.warning(self, "Error", f"Could not resolve alert #{alert_id}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = ExpiryView(user_id=1)
    win.setWindowTitle("Check Expiry")
    win.resize(1100, 650)
    win.show()
    sys.exit(app.exec())