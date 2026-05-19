from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFrame, QComboBox,
    QDateEdit, QDoubleSpinBox, QSpinBox, QScrollArea,
    QSizePolicy, QMessageBox
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont, QCursor
from controllers.medicine_controller import MedicineController


class AddMedicineView(QWidget):
    def __init__(self, user_id=None, on_success=None):
        super().__init__()
        self.user_id = user_id
        self.on_success = on_success
        self._categories = []
        self._manufacturers = []
        self._units = []
        self._apply_styles()
        self._build_ui()
        self._load_lookups()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F3F4F8; }

            QFrame#FormCard {
                background-color: #FFFFFF;
                border-radius: 12px;
            }
            QLabel#PageTitle {
                font-size: 22px;
                font-weight: 700;
                color: #1A1A2E;
            }
            QFrame#CardTitleIcon {
                background-color: #4F46E5;
                border-radius: 8px;
            }
            QLabel#CardTitleIconLabel {
                color: #FFFFFF;
                font-size: 18px;
            }
            QLabel#CardTitle {
                font-size: 20px;
                font-weight: 700;
                color: #1A1A2E;
            }
            QLabel#FieldLabel {
                font-size: 13px;
                font-weight: 500;
                color: #374151;
            }
            QLineEdit#Input, QComboBox#Input,
            QDateEdit#Input, QDoubleSpinBox#Input,
            QSpinBox#Input {
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                color: #1F2937;
                background: #FFFFFF;
                min-height: 38px;
            }
            QLineEdit#Input:focus, QComboBox#Input:focus,
            QDateEdit#Input:focus, QDoubleSpinBox#Input:focus,
            QSpinBox#Input:focus {
                border: 1.5px solid #4F46E5;
            }
            QComboBox#Input::drop-down { border: none; }
            QDateEdit#Input::drop-down { border: none; }

            QPushButton#BtnAdd {
                background-color: #4F46E5;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: 600;
                padding: 12px;
                min-height: 46px;
            }
            QPushButton#BtnAdd:hover { background-color: #4338CA; }
            QPushButton#BtnAdd:pressed { background-color: #3730A3; }

            QPushButton#BtnReset {
                background-color: #FFFFFF;
                color: #374151;
                border: 1.5px solid #E5E7EB;
                border-radius: 8px;
                font-size: 15px;
                padding: 12px 28px;
                min-height: 46px;
            }
            QPushButton#BtnReset:hover { background-color: #F3F4F6; }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;}")

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.setSpacing(0)

        # Card
        card = QFrame()
        card.setObjectName("FormCard")
        card.setMaximumWidth(780)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(32, 28, 32, 32)
        card_layout.setSpacing(0)

        # Card title row
        title_row = QHBoxLayout()
        title_row.setSpacing(12)
        icon_frame = QFrame()
        icon_frame.setObjectName("CardTitleIcon")
        icon_frame.setFixedSize(40, 40)
        icon_inner = QVBoxLayout(icon_frame)
        icon_inner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl = QLabel("+")
        icon_lbl.setObjectName("CardTitleIconLabel")
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        icon_inner.addWidget(icon_lbl)
        card_title = QLabel("Add New Medicine")
        card_title.setObjectName("CardTitle")
        title_row.addWidget(icon_frame)
        title_row.addWidget(card_title)
        title_row.addStretch()
        card_layout.addLayout(title_row)
        card_layout.addSpacing(24)

        # Grid — 2 columns
        grid_row1 = QHBoxLayout(); grid_row1.setSpacing(16)
        grid_row2 = QHBoxLayout(); grid_row2.setSpacing(16)
        grid_row3 = QHBoxLayout(); grid_row3.setSpacing(16)
        grid_row4 = QHBoxLayout(); grid_row4.setSpacing(16)

        # Row 1: Name | Category
        self.input_name = self._make_input("Medicine Name *", "e.g., Paracetamol")
        self.combo_category = self._make_combo("Category *")
        grid_row1.addLayout(self.input_name[0])
        grid_row1.addLayout(self.combo_category[0])

        # Row 2: Quantity | Unit
        self.spin_qty = self._make_spinbox("Quantity *")
        self.combo_unit = self._make_combo("Unit *")
        grid_row2.addLayout(self.spin_qty[0])
        grid_row2.addLayout(self.combo_unit[0])

        # Row 3: Expiry Date | Price
        self.date_expiry = self._make_dateedit("Expiry Date *")
        self.spin_price = self._make_doublespinbox("Price (₱) *")
        grid_row3.addLayout(self.date_expiry[0])
        grid_row3.addLayout(self.spin_price[0])

        # Row 4: Manufacturer | Batch Number
        self.combo_manufacturer = self._make_combo("Manufacturer *")
        self.input_batch = self._make_input("Batch Number *", "e.g., BN2024-001")
        grid_row4.addLayout(self.combo_manufacturer[0])
        grid_row4.addLayout(self.input_batch[0])

        card_layout.addLayout(grid_row1)
        card_layout.addSpacing(16)
        card_layout.addLayout(grid_row2)
        card_layout.addSpacing(16)
        card_layout.addLayout(grid_row3)
        card_layout.addSpacing(16)
        card_layout.addLayout(grid_row4)
        card_layout.addSpacing(24)

        # Buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        btn_add = QPushButton("Add Medicine")
        btn_add.setObjectName("BtnAdd")
        btn_add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_add.clicked.connect(self._handle_add)
        btn_reset = QPushButton("Reset")
        btn_reset.setObjectName("BtnReset")
        btn_reset.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_reset.clicked.connect(self._reset_form)
        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_reset)
        card_layout.addLayout(btn_row)

        layout.addWidget(card)
        layout.addStretch()
        scroll.setWidget(content)
        root.addWidget(scroll)

    # ── FIELD FACTORIES ───────────────────────────────────────
    def _make_input(self, label, placeholder=""):
        wrap = QVBoxLayout(); wrap.setSpacing(6)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        inp = QLineEdit(); inp.setObjectName("Input")
        inp.setPlaceholderText(placeholder)
        wrap.addWidget(lbl); wrap.addWidget(inp)
        return wrap, inp

    def _make_combo(self, label):
        wrap = QVBoxLayout(); wrap.setSpacing(6)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        cb = QComboBox(); cb.setObjectName("Input")
        wrap.addWidget(lbl); wrap.addWidget(cb)
        return wrap, cb

    def _make_spinbox(self, label):
        wrap = QVBoxLayout(); wrap.setSpacing(6)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        sb = QSpinBox(); sb.setObjectName("Input")
        sb.setRange(0, 999999); sb.setValue(0)
        wrap.addWidget(lbl); wrap.addWidget(sb)
        return wrap, sb

    def _make_doublespinbox(self, label):
        wrap = QVBoxLayout(); wrap.setSpacing(6)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        sb = QDoubleSpinBox(); sb.setObjectName("Input")
        sb.setRange(0, 9999999); sb.setDecimals(2); sb.setValue(0)
        wrap.addWidget(lbl); wrap.addWidget(sb)
        return wrap, sb

    def _make_dateedit(self, label):
        wrap = QVBoxLayout(); wrap.setSpacing(6)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        de = QDateEdit(); de.setObjectName("Input")
        de.setCalendarPopup(True)
        de.setDate(QDate.currentDate().addYears(1))
        de.setDisplayFormat("MM/dd/yyyy")
        wrap.addWidget(lbl); wrap.addWidget(de)
        return wrap, de

    # ── LOAD LOOKUPS FROM DB ──────────────────────────────────
    def _load_lookups(self):
        self._categories = MedicineController.get_categories()
        self._manufacturers = MedicineController.get_manufacturers()
        self._units = MedicineController.get_units()

        cb_cat = self.combo_category[1]
        cb_cat.clear()
        cb_cat.addItem("Select category", None)
        for row in self._categories:
            cb_cat.addItem(row["name"], row["id"])

        cb_mfg = self.combo_manufacturer[1]
        cb_mfg.clear()
        cb_mfg.addItem("Select manufacturer", None)
        for row in self._manufacturers:
            cb_mfg.addItem(row["name"], row["id"])

        cb_unit = self.combo_unit[1]
        cb_unit.clear()
        cb_unit.addItem("Select unit", None)
        for row in self._units:
            cb_unit.addItem(row["name"], row["id"])

    # ── ADD HANDLER ───────────────────────────────────────────
    def _handle_add(self):
        name         = self.input_name[1].text().strip()
        category_id  = self.combo_category[1].currentData()
        mfg_id       = self.combo_manufacturer[1].currentData()
        unit_id      = self.combo_unit[1].currentData()
        quantity     = self.spin_qty[1].value()
        expiry_date  = self.date_expiry[1].date().toString("yyyy-MM-dd")
        price        = self.spin_price[1].value()
        batch        = self.input_batch[1].text().strip()

        if not name:
            return self._msg("Medicine name is required.", "warning")
        if not category_id:
            return self._msg("Please select a category.", "warning")
        if not mfg_id:
            return self._msg("Please select a manufacturer.", "warning")
        if not unit_id:
            return self._msg("Please select a unit.", "warning")
        if not batch:
            return self._msg("Batch number is required.", "warning")

        result = MedicineController.add_medicine(
            name=name,
            category_id=category_id,
            manufacturer_id=mfg_id,
            unit_id=unit_id,
            quantity=quantity,
            expiry_date=expiry_date,
            price=price,
            batch_number=batch,
            user_id=self.user_id
        )

        if result.get("success"):
            self._msg(f"'{name}' added successfully!", "info")
            self._reset_form()
            if self.on_success:
                self.on_success()
        else:
            self._msg(f"Error: {result.get('error')}", "critical")

    # ── RESET ─────────────────────────────────────────────────
    def _reset_form(self):
        self.input_name[1].clear()
        self.input_batch[1].clear()
        self.spin_qty[1].setValue(0)
        self.spin_price[1].setValue(0)
        self.date_expiry[1].setDate(QDate.currentDate().addYears(1))
        self.combo_category[1].setCurrentIndex(0)
        self.combo_manufacturer[1].setCurrentIndex(0)
        self.combo_unit[1].setCurrentIndex(0)

    # ── MESSAGE BOX ───────────────────────────────────────────
    def _msg(self, text, kind="info"):
        box = QMessageBox(self)
        box.setText(text)
        if kind == "info":
            box.setIcon(QMessageBox.Icon.Information)
            box.setWindowTitle("Success")
        elif kind == "warning":
            box.setIcon(QMessageBox.Icon.Warning)
            box.setWindowTitle("Validation")
        else:
            box.setIcon(QMessageBox.Icon.Critical)
            box.setWindowTitle("Error")
        box.exec()


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = AddMedicineView(user_id=1, on_success=lambda: print("Medicine added!"))
    win.setWindowTitle("Add Medicine")
    win.resize(900, 650)
    win.show()
    sys.exit(app.exec())