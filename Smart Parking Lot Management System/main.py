import datetime
import os


# Color-coded CLI UI for improved readability
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


class SmartParkingSystem:
    def __init__(self, total_slots=5, vip_slots=1):
        self.slots = {f"S{i + 1}": None for i in range(total_slots)}
        self.vip_slots = [f"S{i + 1}" for i in range(vip_slots)]
        self.rates = {'BIKE': 10, 'CAR': 20, 'EV': 15, 'HEAVY': 50}
        self.revenue_log = []
        self.total_vehicles_served = 0

    def display_status(self):
        print(f"\n{Colors.HEADER}--- Current Parking Status ---{Colors.END}")
        for slot, data in self.slots.items():
            status = f"{data['vehicle_no']} ({data['type']})" if data else "Empty"
            print(f"{slot}: {status}")

    def vehicle_entry(self):
        vehicle_no = input("Enter Vehicle Number: ")
        print("Types: BIKE, CAR, EV, HEAVY")
        v_type = input("Enter Vehicle Type: ").upper()

        if v_type not in self.rates:
            print(f"{Colors.RED}Invalid Type!{Colors.END}")
            return

        is_vip = input("Is this a VIP vehicle? (y/n): ").lower() == 'y'

        # Slot Allocation Logic
        slot = None
        if is_vip:
            for s in self.vip_slots:
                if self.slots[s] is None: slot = s; break
        if not slot:
            for s, d in self.slots.items():
                if d is None: slot = s; break

        if not slot:
            print(f"{Colors.RED}Error: No slots available!{Colors.END}")
            return

        self.slots[slot] = {
            'vehicle_no': vehicle_no,
            'type': v_type,
            'entry_time': datetime.datetime.now()
        }
        self.total_vehicles_served += 1
        print(f"{Colors.GREEN}Success! Parked in {slot}.{Colors.END}")

    def vehicle_exit(self):
        slot_id = input("Enter Slot ID to Exit (e.g., S1): ").upper()
        if slot_id not in self.slots or self.slots[slot_id] is None:
            print(f"{Colors.YELLOW}Error: Invalid slot or slot is empty!{Colors.END}")
            return

        data = self.slots[slot_id]
        duration = (datetime.datetime.now() - data['entry_time']).total_seconds() / 3600
        hours = max(1, round(duration))
        base = self.rates.get(data['type'], 20)
        fee = base if hours <= 2 else base + ((hours - 2) * (base * 0.5))

        self.revenue_log.append({'vehicle': data['vehicle_no'], 'fee': fee})
        self.slots[slot_id] = None
        print(f"{Colors.BLUE}Vehicle {data['vehicle_no']} exited. Fee: ${fee:.2f}{Colors.END}")

    def export_report(self):
        filename = "Daily_Revenue_Report.txt"
        with open(filename, "w") as f:
            f.write("--- PARKING REVENUE REPORT ---\n")
            f.write(f"Date: {datetime.date.today()}\n\n")
            for entry in self.revenue_log:
                f.write(f"Vehicle: {entry['vehicle']} | Fee: ${entry['fee']:.2f}\n")
            f.write(f"\nTotal Revenue: ${sum(e['fee'] for e in self.revenue_log):.2f}")
        print(f"{Colors.GREEN}Report exported to {filename}{Colors.END}")


# --- Interactive Main Loop ---
def main():
    system = SmartParkingSystem()
    while True:
        print(f"\n{Colors.BOLD}--- SMART PARKING MENU ---{Colors.END}")
        print("1. View Status\n2. Park Vehicle\n3. Vehicle Exit\n4. Export Report\n5. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            system.display_status()
        elif choice == '2':
            system.vehicle_entry()
        elif choice == '3':
            system.vehicle_exit()
        elif choice == '4':
            system.export_report()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()