from database.db_setup import setup_database
from views.login_view import show_login
from views.signup_view import show_signup
from views.dashboard_view import show_dashboard
from views.inventory_view import show_inventory, show_edit_medicine, show_delete_medicine
from views.add_medicine_view import show_add_medicine
from views.search_view import show_search
from views.expiry_view import show_expiry, show_alerts
from views.report_view import show_report, show_export
from controllers.auth_controller import logout, get_current_user


def auth_menu():
    while True:
        print("\n=== MediTrack ===")
        print("1. Login")
        print("2. Sign Up")
        print("0. Exit")
        choice = input("\nChoice: ").strip()
        if choice == '1':
            if show_login():
                return True
        elif choice == '2':
            show_signup()
        elif choice == '0':
            print("Goodbye.")
            return False
        else:
            print("Invalid choice.")


def main_menu():
    while True:
        user = get_current_user()
        print(f"\n=== Main Menu [{user['username']}] ===")
        print("1. Dashboard")
        print("2. View Inventory")
        print("3. Add Medicine")
        print("4. Edit Medicine")
        print("5. Delete Medicine")
        print("6. Search Medicine")
        print("7. Check Expiry")
        print("8. Alerts")
        print("9. Generate Report")
        print("10. Export CSV")
        print("0. Logout")

        choice = input("\nChoice: ").strip()
        if   choice == '1':  show_dashboard()
        elif choice == '2':  show_inventory()
        elif choice == '3':  show_add_medicine()
        elif choice == '4':  show_edit_medicine()
        elif choice == '5':  show_delete_medicine()
        elif choice == '6':  show_search()
        elif choice == '7':  show_expiry()
        elif choice == '8':  show_alerts()
        elif choice == '9':  show_report()
        elif choice == '10': show_export()
        elif choice == '0':
            logout()
            print("Logged out.")
            break
        else:
            print("Invalid choice.")


def main():
    print("Initialising database...")
    setup_database()

    while True:
        logged_in = auth_menu()
        if not logged_in:
            break
        main_menu()


if __name__ == "__main__":
    main()
