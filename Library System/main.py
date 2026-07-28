import json
import datetime
import os


class LibrarySystem:
    def __init__(self, filename="library_data.json"):
        self.filename = filename
        # Initialize databases as per architecture
        self.books = {}  # Book Inventory
        self.members = {}  # Member Management
        self.fine_rate = 10  #
        self.load_data()

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.books = data.get("books", {})
                self.members = data.get("members", {})
        print("System Initialized.")

    def save_data(self):
        # Saves data manually to file
        with open(self.filename, 'w') as f:
            json.dump({"books": self.books, "members": self.members}, f, indent=4)
        print("Data saved successfully.")

    # --- Book Management ---
    def add_or_update_book(self, book_id, title, author, category):
        self.books[book_id] = {
            "title": title, "author": author,
            "category": category, "is_issued": False
        }
        self.save_data()
        print(f"Book '{title}' saved.")

    # --- Member Management ---
    def register_member(self, member_id, name):
        self.members[member_id] = {
            "name": name, "issued_books": {}, "total_fines": 0
        }
        self.save_data()
        print(f"Member '{name}' registered.")

    # --- Search Engine ---
    def search(self, query):
        query = query.lower()
        results = [b for bid, b in self.books.items() if query in b['title'].lower() or query in b['author'].lower()]
        results += [m for mid, m in self.members.items() if query == mid]
        return results

    # --- Issue Module ---
    def issue_book(self, member_id, book_id):
        if member_id not in self.members: return "Member not found."
        if book_id not in self.books or self.books[book_id]['is_issued']: return "Book unavailable."

        due_date = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
        self.books[book_id]['is_issued'] = True
        self.members[member_id]['issued_books'][book_id] = due_date
        self.save_data()
        return f"Book issued. Due: {due_date}"

    # --- Return & Fine Calculation ---
    def return_book(self, member_id, book_id):
        if book_id not in self.members[member_id]['issued_books']: return "Transaction not found."

        due_date = datetime.date.fromisoformat(self.members[member_id]['issued_books'].pop(book_id))
        today = datetime.date.today()

        fine = 0
        if today > due_date:
            fine = (today - due_date).days * self.fine_rate
            self.members[member_id]['total_fines'] += fine

        self.books[book_id]['is_issued'] = False
        self.save_data()
        return f"Returned. Fine: {fine}. Total Fines: {self.members[member_id]['total_fines']}"

    # --- Reports ---
    def generate_report(self):
        print("\n--- Library Usage Report ---")
        for mid, m in self.members.items():
            print(f"Member: {m['name']} | Fines: {m['total_fines']}")
            print(f"  Issued: {list(m['issued_books'].keys())}")


# --- User Interface for Manual Entry ---
if __name__ == "__main__":
    lib = LibrarySystem()
    while True:
        print("\n1. Add Book | 2. Register Member | 3. Issue | 4. Return | 5. Report | 6. Exit")
        choice = input("Select option: ")
        if choice == '1':
            bid = input("Book ID: ")
            t = input("Title: ")
            a = input("Author: ")
            c = input("Category: ")
            lib.add_or_update_book(bid, t, a, c)
        elif choice == '2':
            mid = input("Member ID: ")
            n = input("Name: ")
            lib.register_member(mid, n)
        elif choice == '3':
            mid = input("Member ID: ")
            bid = input("Book ID: ")
            print(lib.issue_book(mid, bid))
        elif choice == '4':
            mid = input("Member ID: ")
            bid = input("Book ID: ")
            print(lib.return_book(mid, bid))
        elif choice == '5':
            lib.generate_report()
        else:
            break