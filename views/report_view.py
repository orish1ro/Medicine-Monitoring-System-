from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar, QAbstractItemView,
    QFileDialog, QMessageBox, QSizePolicy
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor, QFont
from controllers.report_controller import (
    controller_get_report,
    controller_export_csv,
    controller_get_audit_log,
)
from utils.helpers import format_currency, format_date


class ReportView(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self._apply_styles()
        self._build_ui()
        self._load_report()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F3F4F8; }

            QFrame#SummaryCard, QFrame#BreakdownCard, QFrame#AuditCard {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QLabel#PageTitle {
                font-size: 22px;
                font-weight: 700;
                color: #1A1A2E;
            }
            QLabel#SectionTitle {
                font-size: 15px;
                font-weight: 600;
                color: #374151;
            }
            QLabel#StatKey {
                font-size: 13px;
                color: #6B7280;
            }
            QLabel#StatVal {
                font-size: 13px;
                font-weight: 600;
                color: #1F2937;
            }
            QLabel#StatValBig {
                font-size: 26px;
                font-weight: 700;
                color: #4F46E5;
            }
            QLabel#CatLabel {
                font-size: 13px;
                color: #374151;
            }
            QLabel#CatCount {
                font-size: 13px;
                font-weight: 600;
                color: #4F46E5;
                min-width: 30px;
            }

            QPushButton#BtnExport {
                background-color: #4F46E5;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 9px 22px;
                min-height: 40px;
            }
            QPushButton#BtnExport:hover { background-color: #4338CA; }
            QPushButton#BtnRefresh {
                background-color: #FFFFFF;
                color: #374151;
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                font-size: 14px;
                padding: 9px 18px;
                min-height: 40px;
            }
            QPushButton#BtnRefresh:hover { background-color: #F3F4F6; }

            QProgressBar {
                border: none;
                border-radius: 4px;
                background: #F3F4F6;
                height: 8px;
                text-align: right;
            }
            QProgressBar::chunk {
                background: #4F46E5;
                border-radius: 4px;
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
        from PyQt6.QtWidgets import QScrollArea
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;}")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(16)

        # Header row
        header_row = QHBoxLayout()
        title = QLabel("Generate Report")
        title.setObjectName("PageTitle")
        btn_refresh = QPushButton("⟳  Refresh")
        btn_refresh.setObjectName("BtnRefresh")
        btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_refresh.clicked.connect(self._load_report)
        btn_export = QPushButton("↓  Export CSV")
        btn_export.setObjectName("BtnExport")
        btn_export.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_export.clicked.connect(self._handle_export)
        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(btn_refresh)
        header_row.addSpacing(8)
        header_row.addWidget(btn_export)
        layout.addLayout(header_row)

        # Top row: Summary + Category Breakdown
        top_row = QHBoxLayout()
        top_row.setSpacing(16)

        # Summary card
        self.summary_card = QFrame()
        self.summary_card.setObjectName("SummaryCard")
        self.summary_card.setFixedWidth(300)
        self._summary_layout = QVBoxLayout(self.summary_card)
        self._summary_layout.setContentsMargins(24, 20, 24, 24)
        self._summary_layout.setSpacing(12)
        s_title = QLabel("Summary"); s_title.setObjectName("SectionTitle")
        self._summary_layout.addWidget(s_title)
        # placeholders filled by _populate_summary
        self._summary_rows = {}
        for key in ["Total Medicines", "Inventory Value", "Expired", "Expiring Soon", "Low Stock"]:
            row = QHBoxLayout()
            k_lbl = QLabel(key + ":"); k_lbl.setObjectName("StatKey")
            v_lbl = QLabel("—"); v_lbl.setObjectName("StatVal")
            row.addWidget(k_lbl); row.addStretch(); row.addWidget(v_lbl)
            self._summary_layout.addLayout(row)
            self._summary_rows[key] = v_lbl
        self._summary_layout.addStretch()
        top_row.addWidget(self.summary_card)

        # Category breakdown card
        breakdown_card = QFrame()
        breakdown_card.setObjectName("BreakdownCard")
        self._breakdown_layout = QVBoxLayout(breakdown_card)
        self._breakdown_layout.setContentsMargins(24, 20, 24, 24)
        self._breakdown_layout.setSpacing(10)
        b_title = QLabel("Category Breakdown"); b_title.setObjectName("SectionTitle")
        self._breakdown_layout.addWidget(b_title)
        # Breakdown rows added dynamically
        self._breakdown_content_layout = QVBoxLayout()
        self._breakdown_content_layout.setSpacing(8)
        self._breakdown_layout.addLayout(self._breakdown_content_layout)
        self._breakdown_layout.addStretch()
        top_row.addWidget(breakdown_card)

        layout.addLayout(top_row)

        # Audit log card
        audit_card = QFrame()
        audit_card.setObjectName("AuditCard")
        audit_layout = QVBoxLayout(audit_card)
        audit_layout.setContentsMargins(0, 0, 0, 0)
        audit_layout.setSpacing(0)

        audit_header = QHBoxLayout()
        audit_header.setContentsMargins(24, 20, 24, 12)
        a_title = QLabel("Recent Activity"); a_title.setObjectName("SectionTitle")
        self.audit_count_lbl = QLabel(""); self.audit_count_lbl.setObjectName("StatKey")
        audit_header.addWidget(a_title); audit_header.addStretch()
        audit_header.addWidget(self.audit_count_lbl)

        audit_layout.addLayout(audit_header)

        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(5)
        self.audit_table.setHorizontalHeaderLabels(["ID", "User", "Action", "Medicine", "When"])
        self.audit_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.audit_table.verticalHeader().setVisible(False)
        self.audit_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.audit_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.audit_table.setAlternatingRowColors(True)
        self.audit_table.setStyleSheet(
            self.audit_table.styleSheet() + "QTableWidget{alternate-background-color:#F9FAFB;}"
        )
        self.audit_table.setMinimumHeight(240)
        audit_layout.addWidget(self.audit_table)
        layout.addWidget(audit_card)
        layout.addStretch()

        scroll.setWidget(content)
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(scroll)

    # ── LOAD REPORT ───────────────────────────────────────────
    def _load_report(self):
        try:
            data = controller_get_report()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load report:\n{e}")
            return

        self._populate_summary(data["stats"])
        self._populate_breakdown(data.get("breakdown", []))
        self._populate_audit(data.get("audit_log", []))

    def _populate_summary(self, s):
        self._summary_rows["Total Medicines"].setText(str(s.get("total", 0)))
        self._summary_rows["Inventory Value"].setText(format_currency(s.get("inventory_value", 0)))
        self._summary_rows["Expired"].setText(str(s.get("expired", 0)))
        self._summary_rows["Expiring Soon"].setText(str(s.get("expiring_soon", 0)))
        self._summary_rows["Low Stock"].setText(str(s.get("low_stock", 0)))

        # Color coding
        self._summary_rows["Expired"].setStyleSheet("color:#EF4444;font-weight:600;")
        self._summary_rows["Expiring Soon"].setStyleSheet("color:#F97316;font-weight:600;")
        self._summary_rows["Low Stock"].setStyleSheet("color:#F59E0B;font-weight:600;")

    def _populate_breakdown(self, breakdown):
        # Clear old rows
        while self._breakdown_content_layout.count():
            item = self._breakdown_content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not breakdown:
            lbl = QLabel("No category data available.")
            lbl.setObjectName("StatKey")
            self._breakdown_content_layout.addWidget(lbl)
            return

        max_count = max((r["count"] for r in breakdown), default=1)
        for row in breakdown:
            row_widget = QWidget()
            row_layout = QVBoxLayout(row_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)
            row_layout.setSpacing(4)

            label_row = QHBoxLayout()
            cat_lbl = QLabel(str(row["category"])[:30])
            cat_lbl.setObjectName("CatLabel")
            count_lbl = QLabel(str(row["count"]))
            count_lbl.setObjectName("CatCount")
            count_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            label_row.addWidget(cat_lbl)
            label_row.addStretch()
            label_row.addWidget(count_lbl)

            bar = QProgressBar()
            bar.setRange(0, max_count)
            bar.setValue(row["count"])
            bar.setTextVisible(False)
            bar.setFixedHeight(8)

            row_layout.addLayout(label_row)
            row_layout.addWidget(bar)
            self._breakdown_content_layout.addWidget(row_widget)

    def _populate_audit(self, audit):
        self.audit_table.setRowCount(0)
        self.audit_count_lbl.setText(f"Last {len(audit)} entries")

        if not audit:
            self.audit_table.setRowCount(1)
            item = QTableWidgetItem("No activity recorded yet.")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QColor("#9CA3AF"))
            self.audit_table.setItem(0, 0, item)
            self.audit_table.setSpan(0, 0, 1, 5)
            return

        self.audit_table.setSpan(0, 0, 1, 1)
        ACTION_COLORS = {
            "add":    {"text": "#166534", "bg": "#DCFCE7"},
            "update": {"text": "#1E40AF", "bg": "#DBEAFE"},
            "delete": {"text": "#991B1B", "bg": "#FEE2E2"},
        }
        for i, log in enumerate(audit):
            self.audit_table.insertRow(i)
            self.audit_table.setItem(i, 0, QTableWidgetItem(str(log["id"])))
            self.audit_table.setItem(i, 1, QTableWidgetItem(str(log.get("username", ""))))

            action_str = str(log.get("action", "")).lower()
            action_item = QTableWidgetItem(action_str.capitalize())
            action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            colors = ACTION_COLORS.get(action_str, {"text": "#374151", "bg": "#F3F4F6"})
            action_item.setForeground(QColor(colors["text"]))
            action_item.setBackground(QColor(colors["bg"]))
            self.audit_table.setItem(i, 2, action_item)

            self.audit_table.setItem(i, 3, QTableWidgetItem(str(log.get("medicine_name", ""))))
            self.audit_table.setItem(i, 4, QTableWidgetItem(format_date(log.get("performed_at"))))
            self.audit_table.setRowHeight(i, 46)

    # ── EXPORT ────────────────────────────────────────────────
    def _handle_export(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export Inventory to CSV", "inventory_export.csv",
            "CSV Files (*.csv)"
        )
        if not filepath:
            return
        try:
            result = controller_export_csv(filepath)
            if result:
                QMessageBox.information(self, "Export Successful", f"File saved to:\n{result}")
            else:
                QMessageBox.warning(self, "Export Warning", "Export completed but no data was written.")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", str(e))


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = ReportView(user_id=1)
    win.setWindowTitle("Generate Report")
    win.resize(1100, 700)
    win.show()
    sys.exit(app.exec())