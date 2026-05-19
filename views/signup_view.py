from controllers.auth_controller import signup


def show_signup():
    print("\n=== MediTrack — Sign Up ===")
    username  = input("Username: ").strip()
    password  = input("Password: ").strip()
    full_name = input("Full name (optional): ").strip() or None
    email     = input("Email (optional): ").strip() or None

    success, result = signup(username, password, full_name, email)
    if success:
        print(f"\nAccount created! Your user ID is {result}. Please log in.")
        return True
    else:
        print(f"\n[ERROR] {result}")
        return False
