import datetime


class RestaurantPOS:
    def __init__(self):
        # Menu with nested dictionaries
        self.menu = {
            "Drinks": {
                1: {"name": "Coffee", "price": 80, "stock": 50},
                2: {"name": "Fresh Lime", "price": 60, "stock": 30}
            },
            "Main Course": {
                3: {"name": "Veg Burger", "price": 150, "stock": 20},
                4: {"name": "Pasta", "price": 220, "stock": 15}
            },
            "Dessert": {
                5: {"name": "Brownie", "price": 120, "stock": 10},
                6: {"name": "Ice Cream", "price": 90, "stock": 25}
            }
        }
        self.daily_sales = []  # Store per-order summaries
        self.gst_rate = 0.05
        self.service_charge_rate = 0.10

    def display_menu(self):
        """Displays the menu"""
        print("\n--- RESTAURANT MENU ---")
        for category, items in self.menu.items():
            print(f"\n[{category}]")
            for item_id, details in items.items():
                print(f"ID {item_id}: {details['name']} - ₹{details['price']} (Stock: {details['stock']})")

    def export_bill_to_file(self, bill_text):
        """Export bill to a text file"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"bill_{timestamp}.txt"

        # FIX: Added encoding='utf-8' to handle the ₹ symbol
        with open(filename, "w", encoding='utf-8') as f:
            f.write(bill_text)
        print(f"\n[Success] Bill exported to {filename}")

    def take_order(self):
        """Order taking with stock validation"""
        current_order = []
        while True:
            self.display_menu()
            try:
                choice = int(input("\nEnter Item ID to order (or 0 to finish): "))
                if choice == 0: break

                found = False
                for category, items in self.menu.items():
                    if choice in items:
                        item = items[choice]
                        qty = int(input(f"Enter quantity for {item['name']}: "))

                        if qty <= item['stock']:
                            current_order.append({"name": item['name'], "price": item['price'], "qty": qty})
                            item['stock'] -= qty  # Auto-update inventory
                            print(f"Added {qty} {item['name']} to order.")
                            found = True
                        else:
                            print(f"Error: Only {item['stock']} items available.")
                            found = True
                        break

                if not found:
                    print("Invalid Item ID.")
            except ValueError:
                print("Invalid input.")

        if current_order:
            self.generate_bill(current_order)

    def generate_bill(self, order_items):
        """Calculate totals and generate bill text"""
        subtotal = sum(item['price'] * item['qty'] for item in order_items)
        gst = subtotal * self.gst_rate
        service_charge = subtotal * self.service_charge_rate
        total = subtotal + gst + service_charge

        bill_lines = [
            "==============================",
            "       RESTAURANT BILL        ",
            "==============================",
        ]
        for item in order_items:
            bill_lines.append(f"{item['name']} x{item['qty']}: ₹{item['price'] * item['qty']}")
        bill_lines.append("-" * 30)
        bill_lines.append(f"Subtotal:       ₹{subtotal:.2f}")
        bill_lines.append(f"GST (5%):       ₹{gst:.2f}")
        bill_lines.append(f"Srv Charge (10%): ₹{service_charge:.2f}")
        bill_lines.append("-" * 30)
        bill_lines.append(f"TOTAL AMOUNT:   ₹{total:.2f}")
        bill_lines.append("==============================")

        bill_text = "\n".join(bill_lines)
        print(bill_text)

        self.daily_sales.append({"total": total, "items": order_items})

        save_choice = input("\nDo you want to export this bill to a file? (y/n): ")
        if save_choice.lower() == 'y':
            self.export_bill_to_file(bill_text)

    def show_sales_summary(self):
        """Daily sales summary"""
        total_revenue = sum(sale['total'] for sale in self.daily_sales)
        print("\n--- DAILY SALES SUMMARY ---")
        print(f"Total Revenue: ₹{total_revenue:.2f}")
        print(f"Total Orders:  {len(self.daily_sales)}")

    def run(self):
        """Main system loop"""
        while True:
            print("\n--- POS SYSTEM ---")
            print("1. New Order\n2. View Menu\n3. Daily Sales\n4. Exit")
            choice = input("Select: ")
            if choice == '1':
                self.take_order()
            elif choice == '2':
                self.display_menu()
            elif choice == '3':
                self.show_sales_summary()
            elif choice == '4':
                break
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    pos = RestaurantPOS()
    pos.run()