from controllers.medicine_controller import controller_add_medicine
from controllers.inventory_controller import (
    controller_get_categories, controller_get_units, controller_get_manufacturers
)


def show_add_medicine():
    print("\n=== Add New Medicine ===")

    categories    = controller_get_categories()
    units         = controller_get_units()
    manufacturers = controller_get_manufacturers()

    print("\nCategories:")
    for c in categories:
        print(f"  [{c['id']}] {c['name']}")

    print("\nManufacturers:")
    for m in manufacturers:
        print(f"  [{m['id']}] {m['name']}")

    print("\nUnits:")
    for u in units:
        print(f"  [{u['id']}] {u['name']}")

    print()
    data = {
        'name':            input("Medicine name: ").strip(),
        'category_id':     input("Category ID: ").strip(),
        'manufacturer_id': input("Manufacturer ID: ").strip(),
        'unit_id':         input("Unit ID: ").strip(),
        'quantity':        input("Quantity: ").strip(),
        'expiry_date':     input("Expiry date (YYYY-MM-DD): ").strip(),
        'price':           input("Price: ").strip(),
        'batch_number':    input("Batch number: ").strip(),
        'low_stock_threshold': input("Low stock threshold [10]: ").strip() or '10',
    }

    success, result = controller_add_medicine(data)
    if success:
        print(f"\n[OK] Medicine added. ID: {result}")
    else:
        print(f"\n[ERROR] {result}")
