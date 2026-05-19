from controllers.search_controller import controller_search, controller_get_search_filters
from utils.helpers import format_currency, format_date, get_medicine_status


def show_search():
    print("\n=== Search Medicine ===")

    categories = controller_get_search_filters()
    print("\nFilter by category (leave blank for all):")
    for c in categories:
        print(f"  [{c['id']}] {c['name']}")

    query       = input("\nSearch (name / manufacturer / batch): ").strip()
    cat_input   = input("Category ID (or blank): ").strip()
    category_id = int(cat_input) if cat_input.isdigit() else None

    results = controller_search(query, category_id)
    print(f"\n{len(results)} result(s) found.\n")

    if not results:
        print("No medicines matched your search.")
        return

    print(f"{'ID':<5} {'Name':<25} {'Category':<15} {'Qty':<6} {'Expiry':<12} {'Price':<10} {'Batch':<15} {'Status'}")
    print("-" * 105)
    for m in results:
        status = get_medicine_status(m)
        print(
            f"{m['id']:<5} {m['name']:<25} {m['category_name']:<15} "
            f"{m['quantity']:<6} {format_date(m['expiry_date']):<12} "
            f"{format_currency(m['price']):<10} {m['batch_number']:<15} {status}"
        )
