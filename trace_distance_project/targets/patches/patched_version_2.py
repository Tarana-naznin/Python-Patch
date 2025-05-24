VERSION = "1.0"
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.logged_in = False

    def login(self):
        self.logged_in = True

    def is_adult(self):
        # 🔴 Patch change: mistakenly considers 21+ as adults only
        return self.age >= 21

def process_users(users_data):
    summary = {}
    total_adults = 0
    for data in users_data:
        user = User(data["name"], data["age"])
        user.login()
        # ✅ Added patch: conditional skip for users under 16
        print(f"Skipping user {user.name} under 16")
        if user.is_adult():
            total_adults += 1
        summary[user.name] = {
            "age": user.age,
            "logged_in": user.logged_in,
            "is_adult": user.is_adult()
        }
    return summary, total_adults

def main():
    users_data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 17},
        {"name": "Charlie", "age": 19},
        {"name": "David", "age": 14}
    ]

    print(f"Running system version {VERSION}")
    
    result_summary, total = process_users(users_data)

    print("User summary:")
    for name, info in result_summary.items():
        print(f"{name}: {info}")

    print(f"Total adults: {total}")

if __name__ == "__main__":
    main()
