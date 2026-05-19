import csv
import os
from datetime import datetime
from models.medicine_model import get_all_medicines


def export_inventory_csv(filepath=None):
    """
    Export all medicines to a CSV file.
    Returns the filepath on success, None on failure.
    """
    if not filepath:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = f"medicine_inventory_{timestamp}.csv"

    medicines = get_all_medicines()
    if not medicines:
        print("[EXPORT] No medicines to export.")
        return None

    fieldnames = [
        'id', 'name', 'category_name', 'quantity', 'unit_name',
        'expiry_date', 'price', 'manufacturer_name', 'batch_number',
        'low_stock_threshold', 'created_at'
    ]

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(medicines)
        print(f"[EXPORT] Saved to {os.path.abspath(filepath)}")
        return filepath
    except Exception as e:
        print(f"[EXPORT ERROR] {e}")
        return None
