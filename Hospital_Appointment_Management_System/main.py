"""
Project: Hospital Appointment & Queue Management System
Developer: Sameer Waybhase
Reference: Hospital_Appointment_Management_System.pdf
"""

import datetime
import os
from collections import deque


class HospitalOPDSystem:
    def __init__(self):
        self.developer = "Sameer Waybhase"
        # 1. Define doctor and appointment data structures
        self.departments = {
            "General Medicine": "Dr. Smith",
            "Pediatrics": "Dr. Khanna",
            "Cardiology": "Dr. Mehta",
            "Orthopedics": "Dr. Wilson"
        }
        self.doctor_queues = {dept: deque() for dept in self.departments}
        self.all_patients = []
        self.token_counter = 1000
        self.data_file = "Patient_Registration_List.txt"
        self.report_file = "OPD_Summary_Report.txt"

        self.print_architecture()

    def print_architecture(self):
        print("\n" + "=" * 60)
        print("SYSTEM ARCHITECTURE")
        print("Patient → Registration → Token Generator → Doctor Queue → Consultation Tracker → Search System")
        print("=" * 60)

    # 2. Build the patient registration module
    # 3. Generate doctor-specific tokens automatically
    def register_patient(self, name, age, dept_input, is_emergency=False):
        matched_dept = next((d for d in self.departments if d.lower() == dept_input.lower()), None)

        if not matched_dept:
            print(f"\n[!] Error: Department '{dept_input}' not found.")
            return

        self.token_counter += 1
        # Token assignment (doctor-wise format)
        token = f"{matched_dept[:3].upper()}-{self.token_counter}"

        # 4. Premium: Automatic next-available-time calculation
        # Each patient in queue adds 15 minutes of wait time
        wait_minutes = len(self.doctor_queues[matched_dept]) * 15
        est_time = (datetime.datetime.now() + datetime.timedelta(minutes=wait_minutes)).strftime("%H:%M")

        patient_entry = {
            "token": token,
            "name": name,
            "age": age,
            "dept": matched_dept,
            "doctor": self.departments[matched_dept],
            "status": "Waiting",
            "time": est_time,
            "is_emergency": is_emergency
        }

        # 4. Create queue management / Emergency priority
        if is_emergency:
            self.doctor_queues[matched_dept].appendleft(patient_entry)
            patient_entry["status"] = "EMERGENCY"
        else:
            self.doctor_queues[matched_dept].append(patient_entry)

        self.all_patients.append(patient_entry)
        self.save_to_permanent_file()

        print(f"\n[✔] REGISTRATION COMPLETE")
        print(f"Token: {token} | Doctor: {self.departments[matched_dept]} | Est. Time: {est_time}")

    # 5. Implement search functionality using keywords/token
    def search_system(self, query):
        print(f"\n--- Searching Records for: {query} ---")
        found = False
        for p in self.all_patients:
            if query.lower() in p['name'].lower() or query.upper() in p['token']:
                print(f"Match: {p['token']} | {p['name']} | Dept: {p['dept']} | Status: {p['status']}")
                found = True
        if not found:
            print("No matches found in the system.")

    # 6. Add consultation-complete status update
    def track_consultation(self, dept_input):
        matched_dept = next((d for d in self.departments if d.lower() == dept_input.lower()), None)
        if matched_dept and self.doctor_queues[matched_dept]:
            patient = self.doctor_queues[matched_dept].popleft()
            # Update historical status
            for p in self.all_patients:
                if p['token'] == patient['token']:
                    p['status'] = "Consulted"
            print(f"\n[✔] Consultation marked 'Complete' for {patient['name']} ({patient['token']})")
            self.save_to_permanent_file()
        else:
            print(f"\n[!] Queue is already empty for {dept_input}.")

    # 7. Display doctor-wise queue details
    def display_queues(self):
        print(f"\n--- LIVE DOCTOR QUEUES (Dev: {self.developer}) ---")
        for dept, queue in self.doctor_queues.items():
            print(f"\n[{dept}] - Doctor: {self.departments[dept]}")
            if not queue:
                print("  > No patients waiting.")
            else:
                for idx, p in enumerate(queue):
                    prio = " [PRIORITY]" if p['is_emergency'] else ""
                    print(f"  {idx + 1}. {p['token']} - {p['name']}{prio}")

    # Premium: Export patient list and Daily summary
    def save_to_permanent_file(self):
        with open(self.data_file, "w") as f:
            f.write(f"HOSPITAL PATIENT RECORD - MASTER LIST\n")
            f.write(f"Lead Developer: {self.developer}\n")
            f.write("=" * 70 + "\n")
            f.write(f"{'Token':<10} | {'Name':<15} | {'Dept':<15} | {'Status':<12}\n")
            f.write("-" * 70 + "\n")
            for p in self.all_patients:
                f.write(f"{p['token']:<10} | {p['name']:<15} | {p['dept']:<15} | {p['status']:<12}\n")

    # Premium: Department-wise workload analytics
    def generate_workload_analytics(self):
        print(f"\n--- GENERATING WORKLOAD ANALYTICS ---")
        with open(self.report_file, "w") as f:
            f.write(f"OPD WORKLOAD SUMMARY - {datetime.date.today()}\n")
            f.write(f"Prepared by: {self.developer}\n\n")
            for dept in self.departments:
                total = len([p for p in self.all_patients if p['dept'] == dept])
                consulted = len([p for p in self.all_patients if p['dept'] == dept and p['status'] == "Consulted"])
                line = f"Dept: {dept:<15} | Total Reg: {total:<3} | Completed: {consulted:<3}"
                print(line)
                f.write(line + "\n")
        print(f"\n[✔] Full Daily Summary exported to: {self.report_file}")


# --- MANUAL USER CONTROL PANEL ---

def main():
    opd = HospitalOPDSystem()

    while True:
        print(f"\n--- OPD MANAGEMENT SYSTEM MENU ---")
        print("1. Patient Registration")
        print("2. Search Patient (Name/Token)")
        print("3. View Live Doctor Queues")
        print("4. Mark Consultation Done")
        print("5. View Master Record (File Data)")
        print("6. Export Analytics Report")
        print("7. Exit System")

        cmd = input("\nEnter Option: ")

        if cmd == '1':
            n = input("Patient Name: ")
            a = input("Patient Age: ")
            print("Available Depts:", list(opd.departments.keys()))
            d = input("Enter Dept: ")
            e = input("Is Emergency? (y/n): ").lower() == 'y'
            opd.register_patient(n, a, d, e)

        elif cmd == '2':
            q = input("Search Name or Token: ")
            opd.search_system(q)

        elif cmd == '3':
            opd.display_queues()

        elif cmd == '4':
            d = input("Enter Department: ")
            opd.track_consultation(d)

        elif cmd == '5':
            if os.path.exists(opd.data_file):
                with open(opd.data_file, "r") as f:
                    print("\n" + f.read())
            else:
                print("No records found.")

        elif cmd == '6':
            opd.generate_workload_analytics()

        elif cmd == '7':
            print("\n" + "*" * 50)
            print(f"SHUTTING DOWN... SYSTEM CLOSED MANUALLY")
            print(f"PROJECT BY: {opd.developer.upper()}")
            print("*" * 50)
            break
        else:
            print("Invalid input.")


if __name__ == "__main__":
    main()