from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QComboBox, QAbstractItemView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from controllers.search_controller import controller_search, controller_get_search_filters
from utils.helpers import format_currency, format_date, get_medicine_status


class SearchView(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self._apply_styles()
        self._build_ui()
        self._load_categories()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F3F4F8; }

            QFrame#SearchCard {
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
            QLineEdit#Input {
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 14px;
                color: #1F2937;
                background: #FFFFFF;
                min-height: 38px;
            }
            QLineEdit#Input:focus {
                border: 1.5px solid #4F46E5;
            }
            QComboBox#Input {
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1F2937;
                background: #FFFFFF;
                min-height: 38px;
            }
            QComboBox#Input:focus {
                border: 1.5px solid #4F46E5;
            }
            QComboBox#Input::drop-down { border: none; }

            QPushButton#BtnSearch {
                background-color: #4F46E5;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 22px;
                min-height: 40px;
            }
            QPushButton#BtnSearch:hover { background-color: #4338CA; }
            QPushButton#BtnSearch:pressed { background-color: #3730A3; }

            QPushButton#BtnClear {
                background-color: #FFFFFF;
                color: #374151;
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                font-size: 14px;
                padding: 8px 18px;
                min-height: 40px;
            }
            QPushButton#BtnClear:hover { background-color: #F3F4F6; }

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
            QFrame#TableCard {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(16)

        # Page title
        title = QLabel("Search Medicine")
        title.setObjectName("PageTitle")
        root.addWidget(title)

        # Search bar card
        search_card = QFrame()
        search_card.setObjectName("SearchCard")
        search_layout = QVBoxLayout(search_card)
        search_layout.setContentsMargins(24, 20, 24, 20)
        search_layout.setSpacing(14)

        # Row 1: keyword + category
        filter_row = QHBoxLayout()
        filter_row.setSpacing(12)

        kw_wrap = QVBoxLayout(); kw_wrap.setSpacing(5)
        kw_lbl = QLabel("Keyword"); kw_lbl.setObjectName("FieldLabel")
        self.input_keyword = QLineEdit()
        self.input_keyword.setObjectName("Input")
        self.input_keyword.setPlaceholderText("Name, manufacturer, or batch number...")
        self.input_keyword.returnPressed.connect(self._handle_search)
        kw_wrap.addWidget(kw_lbl)
        kw_wrap.addWidget(self.input_keyword)

        cat_wrap = QVBoxLayout(); cat_wrap.setSpacing(5)
        cat_lbl = QLabel("Category"); cat_lbl.setObjectName("FieldLabel")
        self.combo_category = QComboBox()
        self.combo_category.setObjectName("Input")
        self.combo_category.setFixedWidth(220)
        cat_wrap.addWidget(cat_lbl)
        cat_wrap.addWidget(self.combo_category)

        filter_row.addLayout(kw_wrap)
        filter_row.addLayout(cat_wrap)
        search_layout.addLayout(filter_row)

        # Row 2: buttons
        btn_row = QHBoxLayout()
        btn_search = QPushButton("⌕  Search")
        btn_search.setObjectName("BtnSearch")
        btn_search.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_search.clicked.connect(self._handle_search)

        btn_clear = QPushButton("Clear")
        btn_clear.setObjectName("BtnClear")
        btn_clear.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_clear.clicked.connect(self._handle_clear)

        self.count_label = QLabel("")
        self.count_label.setObjectName("CountLabel")

        btn_row.addWidget(btn_search)
        btn_row.addWidget(btn_clear)
        btn_row.addStretch()
        btn_row.addWidget(self.count_label)
        search_layout.addLayout(btn_row)

        root.addWidget(search_card)

        # Results table card
        table_card = QFrame()
        table_card.setObjectName("TableCard")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Name", "Category", "Qty", "Unit",
            "Expiry Date", "Price", "Batch No.", "Status"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(
            self.table.styleSheet() + "QTableWidget{alternate-background-color:#F9FAFB;}"
        )

        table_layout.addWidget(self.table)
        root.addWidget(table_card)

    # ── LOAD CATEGORIES ───────────────────────────────────────
    def _load_categories(self):
        try:
            categories = controller_get_search_filters()
        except Exception:
            categories = []
        self.combo_category.clear()
        self.combo_category.addItem("All Categories", None)
        for c in categories:
            self.combo_category.addItem(c["name"], c["id"])

    # ── SEARCH ────────────────────────────────────────────────
    def _handle_search(self):
        keyword     = self.input_keyword.text().strip()
        category_id = self.combo_category.currentData()

        try:
            results = controller_search(keyword, category_id)
        except Exception as e:
            self.count_label.setText(f"Error: {e}")
            return

        self._populate_table(results)

    def _handle_clear(self):
        self.input_keyword.clear()
        self.combo_category.setCurrentIndex(0)
        self.table.setRowCount(0)
        self.count_label.setText("")

    # ── POPULATE TABLE ────────────────────────────────────────
    def _populate_table(self, results):
        self.table.setRowCount(0)

        if not results:
            self.count_label.setText("No results found.")
            self.table.setRowCount(1)
            empty = QTableWidgetItem("No medicines matched your search.")
            empty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setForeground(QColor("#9CA3AF"))
            self.table.setItem(0, 0, empty)
            self.table.setSpan(0, 0, 1, 8)
            return

        self.table.setSpan(0, 0, 1, 1)
        self.count_label.setText(f"{len(results)} result{'s' if len(results) != 1 else ''} found.")

        STATUS_COLORS = {
            "expired":       {"text": "#991B1B", "bg": "#FEE2E2"},
            "expiring_soon": {"text": "#92400E", "bg": "#FEF3C7"},
            "low_stock":     {"text": "#92400E", "bg": "#FEF3C7"},
            "ok":            {"text": "#166534", "bg": "#DCFCE7"},
        }
        STATUS_LABELS = {
            "expired":       "Expired",
            "expiring_soon": "Expiring Soon",
            "low_stock":     "Low Stock",
            "ok":            "Good",
        }

        for row_idx, m in enumerate(results):
            self.table.insertRow(row_idx)
            status_key = get_medicine_status(m)
            colors     = STATUS_COLORS.get(status_key, STATUS_COLORS["ok"])
            status_lbl = STATUS_LABELS.get(status_key, status_key)

            def _item(text, bold=False):
                it = QTableWidgetItem(str(text))
                if bold:
                    f = it.font(); f.setBold(True); it.setFont(f)
                return it

            self.table.setItem(row_idx, 0, _item(m["name"], bold=True))
            self.table.setItem(row_idx, 1, _item(m.get("category", "")))
            self.table.setItem(row_idx, 2, _item(m["quantity"]))
            self.table.setItem(row_idx, 3, _item(m.get("unit", "")))
            self.table.setItem(row_idx, 4, _item(format_date(m["expiry_date"])))
            self.table.setItem(row_idx, 5, _item(format_currency(m["price"])))
            self.table.setItem(row_idx, 6, _item(m.get("batch_number", "")))

            status_item = QTableWidgetItem(status_lbl)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(QColor(colors["text"]))
            status_item.setBackground(QColor(colors["bg"]))
            self.table.setItem(row_idx, 7, status_item)

            self.table.setRowHeight(row_idx, 46)


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = SearchView(user_id=1)
    win.setWindowTitle("Search Medicine")
    win.resize(1100, 650)
    win.show()
    sys.exit(app.exec())