from controllers.medicine_controller import (
    controller_get_all_medicines, controller_update_medicine, controller_delete_medicine
)
from controllers.inventory_controller import (
    controller_get_categories, controller_get_units, controller_get_manufacturers
)
from utils.helpers import format_currency, format_date, get_medicine_status


def show_inventory():
    medicines = controller_get_all_medicines()
    print(f"\n=== Inventory ({len(medicines)} items) ===")

    if not medicines:
        print("No medicines in inventory.")
        return

    print(f"\n{'ID':<5} {'Name':<25} {'Category':<15} {'Qty':<6} {'Unit':<10} {'Expiry':<12} {'Price':<10} {'Status'}")
    print("-" * 100)
    for m in medicines:
        status = get_medicine_status(m)
        print(
            f"{m['id']:<5} {m['name']:<25} {m['category_name']:<15} "
            f"{m['quantity']:<6} {m['unit_name']:<10} "
            f"{format_date(m['expiry_date']):<12} "
            f"{format_currency(m['price']):<10} {status}"
        )


def show_edit_medicine():
    print("\n=== Edit Medicine ===")
    med_id = input("Enter medicine ID to edit: ").strip()
    if not med_id.isdigit():
        print("[ERROR] Invalid ID.")
        return

    from controllers.medicine_controller import controller_get_medicine
    med = controller_get_medicine(int(med_id))
    if not med:
        print("[ERROR] Medicine not found.")
        return

    categories    = controller_get_categories()
    units         = controller_get_units()
    manufacturers = controller_get_manufacturers()

    print(f"\nEditing: {med['name']} (press Enter to keep current value)\n")

    def prompt(label, current):
        val = input(f"{label} [{current}]: ").strip()
        return val if val else str(current)

    data = {
        'name':            prompt("Name",              med['name']),
        'category_id':     prompt("Category ID",       med['category_id']),
        'manufacturer_id': prompt("Manufacturer ID",   med['manufacturer_id']),
        'unit_id':         prompt("Unit ID",           med['unit_id']),
        'quantity':        prompt("Quantity",          med['quantity']),
        'expiry_date':     prompt("Expiry date",       format_date(med['expiry_date'])),
        'price':           prompt("Price",             med['price']),
        'batch_number':    prompt("Batch number",      med['batch_number']),
        'low_stock_threshold': prompt("Low stock threshold", med.get('low_stock_threshold', 10)),
    }

    success, error = controller_update_medicine(int(med_id), data)
    if success:
        print("\n[OK] Medicine updated.")
    else:
        print(f"\n[ERROR] {error}")


def show_delete_medicine():
    print("\n=== Delete Medicine ===")
    med_id = input("Enter medicine ID to delete: ").strip()
    if not med_id.isdigit():
        print("[ERROR] Invalid ID.")
        return

    confirm = input(f"Are you sure you want to delete medicine #{med_id}? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return

    success, error = controller_delete_medicine(int(med_id))
    if success:
        print("\n[OK] Medicine deleted.")
    else:
        print(f"\n[ERROR] {error}")
