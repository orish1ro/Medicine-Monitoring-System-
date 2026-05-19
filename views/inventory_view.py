from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDialog, QComboBox,
    QLineEdit, QDateEdit, QDoubleSpinBox, QSpinBox,
    QAbstractItemView, QButtonGroup, QRadioButton,
    QSizePolicy, QTextEdit
)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QFont, QCursor
from controllers.medicine_controller import MedicineController


class InventoryView(QWidget):
    def __init__(self, user_id=None):
        super().__init__()
        self.user_id = user_id
        self._apply_styles()
        self._build_ui()
        self.load_data()

    # ── STYLES ────────────────────────────────────────────────
    def _apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F3F4F8; }

            QTableWidget {
                background: #FFFFFF;
                border: none;
                font-size: 13px;
                gridline-color: #F3F4F6;
            }
            QTableWidget::item { padding: 8px 10px; color: #374151; }
            QTableWidget::item:selected {
                background-color: #EEF2FF;
                color: #1F2937;
            }
            QHeaderView::section {
                background-color: #F9FAFB;
                color: #6B7280;
                font-size: 12px;
                font-weight: 600;
                padding: 10px 10px;
                border: none;
                border-bottom: 1px solid #E5E7EB;
            }
            QFrame#TableCard { background-color: #FFFFFF; border-radius: 12px; }
            QLabel#PageTitle { font-size: 22px; font-weight: 700; color: #1A1A2E; }
            QLabel#CountLabel { font-size: 13px; color: #6B7280; }

            QPushButton#BtnStock {
                background-color: #D1FAE5;
                color: #065F46;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: 600;
                padding: 5px 8px;
            }
            QPushButton#BtnStock:hover { background-color: #A7F3D0; }

            QPushButton#BtnDispense {
                background-color: #FEF3C7;
                color: #92400E;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: 600;
                padding: 5px 8px;
            }
            QPushButton#BtnDispense:hover { background-color: #FDE68A; }

            QPushButton#BtnEdit {
                background-color: #EDE9FE;
                color: #4F46E5;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: 500;
                padding: 5px 8px;
            }
            QPushButton#BtnEdit:hover { background-color: #DDD6FE; }

            QPushButton#BtnDelete {
                background-color: #FEE2E2;
                color: #EF4444;
                border: none; border-radius: 6px;
                font-size: 11px; font-weight: 500;
                padding: 5px 8px;
            }
            QPushButton#BtnDelete:hover { background-color: #FECACA; }

            QPushButton#BtnRefresh {
                background-color: #4F46E5; color: #FFFFFF;
                border: none; border-radius: 8px;
                font-size: 13px; font-weight: 500;
                padding: 8px 18px;
            }
            QPushButton#BtnRefresh:hover { background-color: #4338CA; }

            QLabel#LowStockWarning {
                background-color: #FEF3C7;
                color: #92400E;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                font-weight: 500;
            }
        """)

    # ── UI BUILD ──────────────────────────────────────────────
    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(28, 28, 28, 28)
        root.setSpacing(12)

        # Header row
        header_row = QHBoxLayout()
        title = QLabel("View Inventory")
        title.setObjectName("PageTitle")
        self.count_label = QLabel("0 medicines")
        self.count_label.setObjectName("CountLabel")
        btn_refresh = QPushButton("⟳  Refresh")
        btn_refresh.setObjectName("BtnRefresh")
        btn_refresh.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_refresh.clicked.connect(self.load_data)
        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(self.count_label)
        header_row.addSpacing(12)
        header_row.addWidget(btn_refresh)
        root.addLayout(header_row)

        # Low stock warning banner (hidden by default)
        self.low_stock_banner = QLabel("⚠  Some medicines are low on stock! Please restock soon.")
        self.low_stock_banner.setObjectName("LowStockWarning")
        self.low_stock_banner.setVisible(False)
        root.addWidget(self.low_stock_banner)

        # Table card
        card = QFrame()
        card.setObjectName("TableCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)

        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "Name", "Category", "Qty", "Unit",
            "Expiry Date", "Price", "Manufacturer", "Batch", "Status", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(9, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(9, 220)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(False)

        card_layout.addWidget(self.table)
        root.addWidget(card)

    # ── LOAD DATA ─────────────────────────────────────────────
    def load_data(self):
        medicines = MedicineController.get_all_medicines()
        self.table.setRowCount(0)
        self.count_label.setText(f"{len(medicines)} medicine{'s' if len(medicines)!=1 else ''}")

        # Check low stock for banner
        low_count = sum(1 for m in medicines
                        if m["quantity"] <= m.get("low_stock_threshold", 10))
        self.low_stock_banner.setVisible(low_count > 0)
        if low_count > 0:
            self.low_stock_banner.setText(
                f"⚠  {low_count} medicine{'s' if low_count>1 else ''} "
                f"{'are' if low_count>1 else 'is'} low on stock! Please restock soon."
            )

        if not medicines:
            self.table.setRowCount(1)
            empty = QTableWidgetItem("No medicines in inventory. Add your first medicine.")
            empty.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setForeground(QColor("#9CA3AF"))
            self.table.setItem(0, 0, empty)
            self.table.setSpan(0, 0, 1, 10)
            return

        self.table.setSpan(0, 0, 1, 1)

        for row_idx, med in enumerate(medicines):
            self.table.insertRow(row_idx)
            expiry     = med["expiry_date"]
            qty        = med["quantity"]
            threshold  = med.get("low_stock_threshold", 10)
            status, color = self._get_status(expiry, qty, threshold)
            is_low     = (status == "Low Stock")
            is_expired = (status == "Expired")

            # ── Row background highlight ──────────────────────
            row_bg = None
            if is_expired:
                row_bg = QColor("#FFF5F5")
            elif is_low:
                row_bg = QColor("#FFFBEB")

            self._set_item(row_idx, 0, med["name"],         bold=True,  row_bg=row_bg)
            self._set_item(row_idx, 1, med["category"],                  row_bg=row_bg)
            self._set_item(row_idx, 2, str(qty),                         row_bg=row_bg,
                           fg="#EF4444" if is_low else None)
            self._set_item(row_idx, 3, med["unit"],                      row_bg=row_bg)
            self._set_item(row_idx, 4, str(expiry),                      row_bg=row_bg)
            self._set_item(row_idx, 5, f"₱{float(med['price']):.2f}",   row_bg=row_bg)
            self._set_item(row_idx, 6, med["manufacturer"],              row_bg=row_bg)
            self._set_item(row_idx, 7, med["batch_number"],              row_bg=row_bg)

            # Status badge
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            status_item.setForeground(QColor(color["text"]))
            status_item.setBackground(QColor(color["bg"]))
            self.table.setItem(row_idx, 8, status_item)

            # ── Action buttons ────────────────────────────────
            action_widget = QWidget()
            if row_bg:
                action_widget.setStyleSheet(f"background:{row_bg.name()};")
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(4)

            # ± Stock
            btn_stock = QPushButton("± Stock")
            btn_stock.setObjectName("BtnStock")
            btn_stock.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn_stock.clicked.connect(lambda _, m=med: self._open_stock_adjust(m))

            # Dispense
            btn_dispense = QPushButton("Dispense")
            btn_dispense.setObjectName("BtnDispense")
            btn_dispense.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn_dispense.clicked.connect(lambda _, m=med: self._open_dispense(m))

            # Edit
            btn_edit = QPushButton("Edit")
            btn_edit.setObjectName("BtnEdit")
            btn_edit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn_edit.clicked.connect(lambda _, m=med: self._open_edit(m))

            # Delete
            btn_del = QPushButton("Del")
            btn_del.setObjectName("BtnDelete")
            btn_del.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            btn_del.clicked.connect(lambda _, m=med: self._confirm_delete(m))

            action_layout.addWidget(btn_stock)
            action_layout.addWidget(btn_dispense)
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_del)
            self.table.setCellWidget(row_idx, 9, action_widget)
            self.table.setRowHeight(row_idx, 50)

    # ── HELPERS ───────────────────────────────────────────────
    def _set_item(self, row, col, text, bold=False, row_bg=None, fg=None):
        item = QTableWidgetItem(text)
        if bold:
            f = item.font(); f.setBold(True); item.setFont(f)
        if row_bg:
            item.setBackground(row_bg)
        if fg:
            item.setForeground(QColor(fg))
        self.table.setItem(row, col, item)

    def _get_status(self, expiry_date, qty, threshold=10):
        from datetime import date
        today = date.today()
        expiry = expiry_date if not hasattr(expiry_date, 'toPyDate') else expiry_date.toPyDate()
        if expiry < today:
            return "Expired",       {"text": "#991B1B", "bg": "#FEE2E2"}
        if (expiry - today).days <= 30:
            return "Expiring Soon", {"text": "#9A3412", "bg": "#FFEDD5"}
        if qty <= threshold:
            return "Low Stock",     {"text": "#92400E", "bg": "#FEF3C7"}
        return "Good",              {"text": "#166534", "bg": "#DCFCE7"}

    # ── 1. STOCK ADJUSTMENT DIALOG ────────────────────────────
    def _open_stock_adjust(self, med):
        dialog = StockAdjustDialog(med, user_id=self.user_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    # ── 2. DISPENSE DIALOG ────────────────────────────────────
    def _open_dispense(self, med):
        dialog = DispenseDialog(med, user_id=self.user_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    # ── 3. EDIT DIALOG ────────────────────────────────────────
    def _open_edit(self, med):
        dialog = EditMedicineDialog(med, user_id=self.user_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_data()

    # ── DELETE ────────────────────────────────────────────────
    def _confirm_delete(self, med):
        reply = QMessageBox.question(
            self, "Delete Medicine",
            f"Are you sure you want to delete '{med['name']}'?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            result = MedicineController.delete_medicine(med["id"], user_id=self.user_id)
            if result.get("success"):
                QMessageBox.information(self, "Deleted", f"'{med['name']}' deleted.")
                self.load_data()
            else:
                QMessageBox.critical(self, "Error", result.get("error", "Delete failed."))


# ══════════════════════════════════════════════════════════════
# 1. STOCK ADJUSTMENT DIALOG
# ══════════════════════════════════════════════════════════════
class StockAdjustDialog(QDialog):
    def __init__(self, medicine, user_id=None, parent=None):
        super().__init__(parent)
        self.medicine = medicine
        self.user_id  = user_id
        self.setWindowTitle(f"Adjust Stock — {medicine['name']}")
        self.setFixedWidth(380)
        self._apply_styles()
        self._build_ui()

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog { background: #FFFFFF; }
            QLabel#DlgTitle { font-size: 17px; font-weight: 700; color: #1A1A2E; }
            QLabel#CurrentStock {
                font-size: 28px; font-weight: 700; color: #4F46E5;
                qproperty-alignment: AlignCenter;
            }
            QLabel#StockSub { font-size: 12px; color: #6B7280; qproperty-alignment: AlignCenter; }
            QLabel#FieldLabel { font-size: 13px; font-weight: 500; color: #374151; }
            QSpinBox#Input {
                border: 1.5px solid #E5E7EB; border-radius: 8px;
                padding: 10px 14px; font-size: 16px; font-weight: 600;
                color: #1F2937; background: #FFFFFF; min-height: 44px;
            }
            QSpinBox#Input:focus { border-color: #4F46E5; }
            QRadioButton { font-size: 14px; color: #374151; padding: 6px; }
            QPushButton#BtnAdd {
                background: #D1FAE5; color: #065F46;
                border: none; border-radius: 8px;
                font-size: 14px; font-weight: 600; padding: 10px;
            }
            QPushButton#BtnAdd:hover { background: #A7F3D0; }
            QPushButton#BtnDeduct {
                background: #FEE2E2; color: #991B1B;
                border: none; border-radius: 8px;
                font-size: 14px; font-weight: 600; padding: 10px;
            }
            QPushButton#BtnDeduct:hover { background: #FECACA; }
            QPushButton#BtnCancel {
                background: #F3F4F6; color: #374151;
                border: none; border-radius: 8px;
                font-size: 14px; padding: 10px;
            }
            QPushButton#BtnCancel:hover { background: #E5E7EB; }
        """)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Title
        title = QLabel(f"± Stock Adjustment")
        title.setObjectName("DlgTitle")
        layout.addWidget(title)

        # Medicine name
        name_lbl = QLabel(self.medicine["name"])
        name_lbl.setStyleSheet("font-size:14px;color:#6B7280;")
        layout.addWidget(name_lbl)

        # Current stock display
        stock_frame = QFrame()
        stock_frame.setStyleSheet("background:#F5F3FF;border-radius:10px;")
        sf_layout = QVBoxLayout(stock_frame)
        sf_layout.setContentsMargins(16, 16, 16, 16)
        sf_layout.setSpacing(4)
        stock_num = QLabel(str(self.medicine["quantity"]))
        stock_num.setObjectName("CurrentStock")
        stock_sub = QLabel(f"Current stock ({self.medicine['unit']})")
        stock_sub.setObjectName("StockSub")
        sf_layout.addWidget(stock_num)
        sf_layout.addWidget(stock_sub)
        layout.addWidget(stock_frame)

        # Amount input
        amt_lbl = QLabel("Amount to Add / Deduct")
        amt_lbl.setObjectName("FieldLabel")
        layout.addWidget(amt_lbl)
        self.spin_amount = QSpinBox()
        self.spin_amount.setObjectName("Input")
        self.spin_amount.setRange(1, 999999)
        self.spin_amount.setValue(1)
        layout.addWidget(self.spin_amount)

        # Reason
        reason_lbl = QLabel("Reason (optional)")
        reason_lbl.setObjectName("FieldLabel")
        layout.addWidget(reason_lbl)
        self.input_reason = QLineEdit()
        self.input_reason.setPlaceholderText("e.g., Restock, Damaged, Return...")
        self.input_reason.setStyleSheet(
            "border:1.5px solid #E5E7EB;border-radius:8px;"
            "padding:8px 12px;font-size:13px;background:#FFFFFF;"
        )
        layout.addWidget(self.input_reason)

        # Buttons
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        btn_add = QPushButton("+ Add Stock")
        btn_add.setObjectName("BtnAdd")
        btn_add.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_add.clicked.connect(lambda: self._adjust("add"))

        btn_deduct = QPushButton("- Deduct Stock")
        btn_deduct.setObjectName("BtnDeduct")
        btn_deduct.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_deduct.clicked.connect(lambda: self._adjust("deduct"))

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("BtnCancel")
        btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_row.addWidget(btn_add)
        btn_row.addWidget(btn_deduct)
        layout.addLayout(btn_row)
        layout.addWidget(btn_cancel)

    def _adjust(self, mode):
        amount  = self.spin_amount.value()
        reason  = self.input_reason.text().strip() or ("Restock" if mode == "add" else "Stock deduction")
        current = self.medicine["quantity"]

        if mode == "deduct" and amount > current:
            QMessageBox.warning(self, "Invalid",
                f"Cannot deduct {amount}. Only {current} in stock.")
            return

        new_qty = current + amount if mode == "add" else current - amount

        result = MedicineController.update_medicine(
            medicine_id     = self.medicine["id"],
            name            = self.medicine["name"],
            category_id     = self.medicine["category_id"],
            manufacturer_id = self.medicine["manufacturer_id"],
            unit_id         = self.medicine["unit_id"],
            quantity        = new_qty,
            expiry_date     = str(self.medicine["expiry_date"]),
            price           = float(self.medicine["price"]),
            batch_number    = self.medicine["batch_number"],
            low_stock_threshold = self.medicine.get("low_stock_threshold", 10),
            user_id         = self.user_id
        )

        if result.get("success"):
            action = "Added" if mode == "add" else "Deducted"
            QMessageBox.information(self, "Success",
                f"✅ {action} {amount} {self.medicine['unit']}.\n"
                f"New stock: {new_qty} {self.medicine['unit']}\n"
                f"Reason: {reason}")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", result.get("error", "Update failed."))


# ══════════════════════════════════════════════════════════════
# 2. DISPENSE DIALOG
# ══════════════════════════════════════════════════════════════
class DispenseDialog(QDialog):
    def __init__(self, medicine, user_id=None, parent=None):
        super().__init__(parent)
        self.medicine = medicine
        self.user_id  = user_id
        self.setWindowTitle(f"Dispense — {medicine['name']}")
        self.setFixedWidth(400)
        self._apply_styles()
        self._build_ui()

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog { background: #FFFFFF; }
            QLabel#DlgTitle { font-size: 17px; font-weight: 700; color: #1A1A2E; }
            QLabel#FieldLabel { font-size: 13px; font-weight: 500; color: #374151; }
            QLabel#StockInfo {
                font-size: 13px; color: #6B7280;
                background: #F9FAFB; border-radius: 8px; padding: 8px 12px;
            }
            QLineEdit#Input, QSpinBox#Input {
                border: 1.5px solid #E5E7EB; border-radius: 8px;
                padding: 9px 12px; font-size: 14px;
                color: #1F2937; background: #FFFFFF; min-height: 40px;
            }
            QLineEdit#Input:focus, QSpinBox#Input:focus { border-color: #F59E0B; }
            QPushButton#BtnDispense {
                background: #F59E0B; color: #FFFFFF;
                border: none; border-radius: 8px;
                font-size: 14px; font-weight: 600; padding: 12px;
            }
            QPushButton#BtnDispense:hover { background: #D97706; }
            QPushButton#BtnCancel {
                background: #F3F4F6; color: #374151;
                border: none; border-radius: 8px;
                font-size: 14px; padding: 12px;
            }
            QPushButton#BtnCancel:hover { background: #E5E7EB; }
        """)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        # Title
        title = QLabel("💊 Dispense Medicine")
        title.setObjectName("DlgTitle")
        layout.addWidget(title)

        # Medicine info
        info = QLabel(
            f"Medicine:  {self.medicine['name']}\n"
            f"Category:  {self.medicine['category']}\n"
            f"Available: {self.medicine['quantity']} {self.medicine['unit']}"
        )
        info.setObjectName("StockInfo")
        layout.addWidget(info)

        # Patient / Customer name
        pt_lbl = QLabel("Patient / Customer Name *")
        pt_lbl.setObjectName("FieldLabel")
        layout.addWidget(pt_lbl)
        self.input_patient = QLineEdit()
        self.input_patient.setObjectName("Input")
        self.input_patient.setPlaceholderText("e.g., Juan Dela Cruz")
        layout.addWidget(self.input_patient)

        # Quantity to dispense
        qty_lbl = QLabel("Quantity to Dispense *")
        qty_lbl.setObjectName("FieldLabel")
        layout.addWidget(qty_lbl)
        self.spin_qty = QSpinBox()
        self.spin_qty.setObjectName("Input")
        self.spin_qty.setRange(1, self.medicine["quantity"] or 1)
        self.spin_qty.setValue(1)
        layout.addWidget(self.spin_qty)

        # Total price display
        self.total_label = QLabel("Total: ₱0.00")
        self.total_label.setStyleSheet(
            "font-size:15px;font-weight:700;color:#4F46E5;"
        )
        self.spin_qty.valueChanged.connect(self._update_total)
        self._update_total(1)
        layout.addWidget(self.total_label)

        # Notes
        notes_lbl = QLabel("Notes (optional)")
        notes_lbl.setObjectName("FieldLabel")
        layout.addWidget(notes_lbl)
        self.input_notes = QLineEdit()
        self.input_notes.setObjectName("Input")
        self.input_notes.setPlaceholderText("e.g., Prescription #12345")
        layout.addWidget(self.input_notes)

        # Buttons
        btn_row = QHBoxLayout(); btn_row.setSpacing(10)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.setObjectName("BtnCancel")
        btn_cancel.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_cancel.clicked.connect(self.reject)

        btn_dispense = QPushButton("✔  Confirm Dispense")
        btn_dispense.setObjectName("BtnDispense")
        btn_dispense.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn_dispense.clicked.connect(self._handle_dispense)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_dispense)
        layout.addLayout(btn_row)

    def _update_total(self, qty):
        total = qty * float(self.medicine["price"])
        self.total_label.setText(f"Total: ₱{total:.2f}")

    def _handle_dispense(self):
        patient = self.input_patient.text().strip()
        qty     = self.spin_qty.value()
        notes   = self.input_notes.text().strip()

        if not patient:
            QMessageBox.warning(self, "Required", "Please enter patient/customer name.")
            return

        if qty > self.medicine["quantity"]:
            QMessageBox.warning(self, "Insufficient Stock",
                f"Only {self.medicine['quantity']} {self.medicine['unit']} available.")
            return

        new_qty = self.medicine["quantity"] - qty
        total   = qty * float(self.medicine["price"])
        changes = (f"Dispensed {qty} {self.medicine['unit']} to {patient}. "
                   f"Total: ₱{total:.2f}. Notes: {notes or 'None'}")

        result = MedicineController.update_medicine(
            medicine_id     = self.medicine["id"],
            name            = self.medicine["name"],
            category_id     = self.medicine["category_id"],
            manufacturer_id = self.medicine["manufacturer_id"],
            unit_id         = self.medicine["unit_id"],
            quantity        = new_qty,
            expiry_date     = str(self.medicine["expiry_date"]),
            price           = float(self.medicine["price"]),
            batch_number    = self.medicine["batch_number"],
            low_stock_threshold = self.medicine.get("low_stock_threshold", 10),
            user_id         = self.user_id
        )

        if result.get("success"):
            # Log to audit
            from database.db_connection import get_connection, close_connection
            conn = get_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO audit_log (user_id, medicine_id, action, changes)
                        VALUES (%s, %s, %s, %s)
                    """, (self.user_id, self.medicine["id"], "DISPENSE", changes))
                    conn.commit()
                    cur.close()
                except Exception as e:
                    print(f"[Dispense] audit log error: {e}")
                finally:
                    close_connection(conn)

            QMessageBox.information(self, "Dispensed",
                f"✅ Successfully dispensed!\n\n"
                f"Patient:   {patient}\n"
                f"Medicine:  {self.medicine['name']}\n"
                f"Quantity:  {qty} {self.medicine['unit']}\n"
                f"Total:     ₱{total:.2f}\n"
                f"Remaining: {new_qty} {self.medicine['unit']}")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", result.get("error", "Dispense failed."))


# ══════════════════════════════════════════════════════════════
# 3. EDIT DIALOG (unchanged, kept here)
# ══════════════════════════════════════════════════════════════
class EditMedicineDialog(QDialog):
    def __init__(self, medicine, user_id=None, parent=None):
        super().__init__(parent)
        self.medicine = medicine
        self.user_id  = user_id
        self.setWindowTitle(f"Edit — {medicine['name']}")
        self.setMinimumWidth(560)
        self._categories    = MedicineController.get_categories()
        self._manufacturers = MedicineController.get_manufacturers()
        self._units         = MedicineController.get_units()
        self._apply_styles()
        self._build_ui()
        self._fill_data()

    def _apply_styles(self):
        self.setStyleSheet("""
            QDialog { background-color: #FFFFFF; border-radius: 12px; }
            QLabel#DlgTitle { font-size: 18px; font-weight: 700; color: #1A1A2E; }
            QLabel#FieldLabel { font-size: 13px; font-weight: 500; color: #374151; }
            QLineEdit#Input, QComboBox#Input, QDateEdit#Input,
            QDoubleSpinBox#Input, QSpinBox#Input {
                border: 1.5px solid #E5E7EB; border-radius: 8px;
                padding: 8px 12px; font-size: 14px; color: #1F2937;
                background: #FFFFFF; min-height: 36px;
            }
            QLineEdit#Input:focus, QComboBox#Input:focus,
            QDateEdit#Input:focus, QDoubleSpinBox#Input:focus,
            QSpinBox#Input:focus { border-color: #4F46E5; }
            QPushButton#BtnSave {
                background-color: #4F46E5; color: #FFFFFF;
                border: none; border-radius: 8px;
                font-size: 14px; font-weight: 600; padding: 10px 24px;
            }
            QPushButton#BtnSave:hover { background-color: #4338CA; }
            QPushButton#BtnCancel {
                background-color: #FFFFFF; color: #374151;
                border: 1.5px solid #E5E7EB; border-radius: 8px;
                font-size: 14px; padding: 10px 24px;
            }
            QPushButton#BtnCancel:hover { background-color: #F3F4F6; }
        """)

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 24, 28, 24)
        layout.setSpacing(16)

        title = QLabel("Edit Medicine")
        title.setObjectName("DlgTitle")
        layout.addWidget(title)

        g1 = QHBoxLayout(); g1.setSpacing(14)
        g2 = QHBoxLayout(); g2.setSpacing(14)
        g3 = QHBoxLayout(); g3.setSpacing(14)
        g4 = QHBoxLayout(); g4.setSpacing(14)

        self.e_name         = self._field(g1, "Medicine Name *", QLineEdit)
        self.e_category     = self._combo_field(g1, "Category *",     self._categories)
        self.e_qty          = self._spin_field(g2, "Quantity *",      QSpinBox,       0, 999999)
        self.e_unit         = self._combo_field(g2, "Unit *",         self._units)
        self.e_expiry       = self._date_field(g3, "Expiry Date *")
        self.e_price        = self._spin_field(g3, "Price (₱) *",    QDoubleSpinBox, 0, 9999999, decimals=2)
        self.e_manufacturer = self._combo_field(g4, "Manufacturer *", self._manufacturers)
        self.e_batch        = self._field(g4, "Batch Number *",       QLineEdit)

        layout.addLayout(g1); layout.addLayout(g2)
        layout.addLayout(g3); layout.addLayout(g4)

        btn_row = QHBoxLayout(); btn_row.addStretch()
        btn_cancel = QPushButton("Cancel"); btn_cancel.setObjectName("BtnCancel")
        btn_cancel.clicked.connect(self.reject)
        btn_save = QPushButton("Save Changes"); btn_save.setObjectName("BtnSave")
        btn_save.clicked.connect(self._handle_save)
        btn_row.addWidget(btn_cancel); btn_row.addSpacing(8); btn_row.addWidget(btn_save)
        layout.addLayout(btn_row)

    def _field(self, grid, label, widget_cls):
        wrap = QVBoxLayout(); wrap.setSpacing(5)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        w = widget_cls(); w.setObjectName("Input")
        wrap.addWidget(lbl); wrap.addWidget(w)
        grid.addLayout(wrap); return w

    def _combo_field(self, grid, label, items):
        wrap = QVBoxLayout(); wrap.setSpacing(5)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        cb = QComboBox(); cb.setObjectName("Input")
        for row in items: cb.addItem(row["name"], row["id"])
        wrap.addWidget(lbl); wrap.addWidget(cb)
        grid.addLayout(wrap); return cb

    def _spin_field(self, grid, label, cls, min_v, max_v, decimals=None):
        wrap = QVBoxLayout(); wrap.setSpacing(5)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        sb = cls(); sb.setObjectName("Input"); sb.setRange(min_v, max_v)
        if decimals is not None: sb.setDecimals(decimals)
        wrap.addWidget(lbl); wrap.addWidget(sb)
        grid.addLayout(wrap); return sb

    def _date_field(self, grid, label):
        wrap = QVBoxLayout(); wrap.setSpacing(5)
        lbl = QLabel(label); lbl.setObjectName("FieldLabel")
        de = QDateEdit(); de.setObjectName("Input")
        de.setCalendarPopup(True); de.setDisplayFormat("MM/dd/yyyy")
        wrap.addWidget(lbl); wrap.addWidget(de)
        grid.addLayout(wrap); return de

    def _fill_data(self):
        m = self.medicine
        self.e_name.setText(m["name"])
        self.e_batch.setText(m["batch_number"])
        self.e_qty.setValue(int(m["quantity"]))
        self.e_price.setValue(float(m["price"]))
        expiry = m["expiry_date"]
        if hasattr(expiry, 'toPyDate'): expiry = expiry.toPyDate()
        self.e_expiry.setDate(QDate(expiry.year, expiry.month, expiry.day))
        self._set_combo(self.e_category,     m["category_id"])
        self._set_combo(self.e_manufacturer, m["manufacturer_id"])
        self._set_combo(self.e_unit,         m["unit_id"])

    def _set_combo(self, combo, value):
        for i in range(combo.count()):
            if combo.itemData(i) == value:
                combo.setCurrentIndex(i); return

    def _handle_save(self):
        result = MedicineController.update_medicine(
            medicine_id     = self.medicine["id"],
            name            = self.e_name.text().strip(),
            category_id     = self.e_category.currentData(),
            manufacturer_id = self.e_manufacturer.currentData(),
            unit_id         = self.e_unit.currentData(),
            quantity        = self.e_qty.value(),
            expiry_date     = self.e_expiry.date().toString("yyyy-MM-dd"),
            price           = self.e_price.value(),
            batch_number    = self.e_batch.text().strip(),
            user_id         = self.user_id
        )
        if result.get("success"):
            QMessageBox.information(self, "Updated", "Medicine updated successfully!")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", result.get("error", "Update failed."))


# ── Standalone preview ────────────────────────────────────────
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    win = InventoryView(user_id=1)
    win.setWindowTitle("View Inventory")
    win.resize(1200, 700)
    win.show()
    sys.exit(app.exec())