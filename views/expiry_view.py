from controllers.expiry_controller import (
    controller_get_expired, controller_get_expiring_soon, controller_get_alerts
)
from utils.helpers import format_date, days_until_expiry


def show_expiry():
    print("\n=== Expiry Checker ===")
    days_input = input("Check expiring within how many days? [30]: ").strip()
    days = int(days_input) if days_input.isdigit() else 30

    expired     = controller_get_expired()
    expiring    = controller_get_expiring_soon(days)

    print(f"\n--- Expired ({len(expired)}) ---")
    if expired:
        print(f"{'ID':<5} {'Name':<25} {'Qty':<6} {'Expiry':<12} {'Days'}")
        print("-" * 65)
        for m in expired:
            d = days_until_expiry(m['expiry_date'])
            print(f"{m['id']:<5} {m['name']:<25} {m['quantity']:<6} {format_date(m['expiry_date']):<12} {d}")
    else:
        print("None.")

    print(f"\n--- Expiring within {days} days ({len(expiring)}) ---")
    if expiring:
        print(f"{'ID':<5} {'Name':<25} {'Qty':<6} {'Expiry':<12} {'Days Left'}")
        print("-" * 65)
        for m in expiring:
            d = days_until_expiry(m['expiry_date'])
            print(f"{m['id']:<5} {m['name']:<25} {m['quantity']:<6} {format_date(m['expiry_date']):<12} {d}")
    else:
        print("None.")


def show_alerts():
    print("\n=== Unresolved Alerts ===")
    alerts = controller_get_alerts()
    if not alerts:
        print("No unresolved alerts.")
        return
    print(f"\n{'ID':<5} {'Type':<15} {'Medicine':<25} {'Message'}")
    print("-" * 80)
    for a in alerts:
        print(f"{a['id']:<5} {a['alert_type']:<15} {a['medicine_name']:<25} {a['message'] or ''}")
