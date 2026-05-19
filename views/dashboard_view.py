from controllers.dashboard_controller import controller_get_dashboard
from utils.helpers import format_currency


def show_dashboard():
    data = controller_get_dashboard()
    s = data['stats']
    print(f"\n{'='*45}")
    print(f"  MediTrack Dashboard — {data['date']}")
    print(f"  Logged in as: {data['user']['username']}")
    print(f"{'='*45}")
    print(f"  Total Medicines  : {s['total']}")
    print(f"  Expired          : {s['expired']}")
    print(f"  Expiring Soon    : {s['expiring_soon']}")
    print(f"  Low Stock        : {s['low_stock']}")
    print(f"  Inventory Value  : {format_currency(s['inventory_value'])}")
    if data['alerts_created']:
        print(f"\n  ⚠  {data['alerts_created']} new alert(s) generated.")
    print(f"{'='*45}")
