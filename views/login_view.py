from controllers.auth_controller import login


def show_login():
    print("\n=== MediTrack — Login ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    success, result = login(username, password)
    if success:
        print(f"\nWelcome, {result['username']}!")
        return True
    else:
        print(f"\n[ERROR] {result}")
        return False
