from controllers.report_controller import (
    controller_get_report, controller_export_csv
)
from utils.helpers import format_currency, format_date


def show_report():
    data = controller_get_report()
    s    = data['stats']

    print(f"\n{'='*45}")
    print("  Inventory Report")
    print(f"{'='*45}")
    print(f"  Total Medicines  : {s['total']}")
    print(f"  Inventory Value  : {format_currency(s['inventory_value'])}")
    print(f"  Low Stock Items  : {s['low_stock']}")
    print(f"  Expiring Soon    : {s['expiring_soon']}")

    print("\n  Category Breakdown:")
    for row in data['breakdown']:
        bar = '#' * row['count']
        print(f"    {row['category']:<20} {bar} ({row['count']})")

    print(f"\n  Recent Activity (last 50):")
    print(f"  {'ID':<5} {'User':<15} {'Action':<10} {'Medicine':<25} {'When'}")
    print("  " + "-" * 75)
    for log in data['audit_log']:
        print(
            f"  {log['id']:<5} {log['username']:<15} {log['action']:<10} "
            f"{log['medicine_name']:<25} {format_date(log['performed_at'])}"
        )


def show_export():
    print("\n=== Export Inventory to CSV ===")
    filepath = input("Filename (blank = auto): ").strip() or None
    result = controller_export_csv(filepath)
    if result:
        print(f"[OK] Exported to: {result}")
    else:
        print("[ERROR] Export failed or no data.")
