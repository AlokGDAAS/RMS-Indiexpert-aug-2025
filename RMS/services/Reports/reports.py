import os
import json
from datetime import datetime, timedelta
import csv

class Reports_Handler:
    DATE_FORMAT = "%d-%m-%Y %H:%M:%S"
    SIMPLE_DATE_FORMAT = "%d-%m-%Y"

    def __init__(self, bill_data_file,menu_data_file):
        self.bill_data_file = bill_data_file
        self.menu_data_file = menu_data_file
        self.bill_data = self.load_datalist(self.bill_data_file)
        self.menu_data = self.load_datalist(self.menu_data_file)

    def load_datalist(self, data_file):
        if not os.path.exists(data_file):
            print(f"{data_file} not found. Starting with empty data.")
            return []
        try:
            with open(data_file, "r") as file:
                data = json.load(file)
                return data if data else []
        except json.JSONDecodeError:
            print("Error reading JSON. Starting with empty data.")
            return []

    def check_date_range_data(self):
        if not self.bill_data:
            print("No bill data found.")
            return

        newest_date = datetime.strptime("01-01-1970", self.SIMPLE_DATE_FORMAT)
        oldest_date = datetime.now()

        for bill in self.bill_data:
            try:
                temp_date = datetime.strptime(bill["createddate"], self.SIMPLE_DATE_FORMAT)
                if temp_date > newest_date:
                    newest_date = temp_date
                if temp_date < oldest_date:
                    oldest_date = temp_date
            except (KeyError, ValueError):
                continue

        print(f" Newest Date in Data: {newest_date.strftime(self.SIMPLE_DATE_FORMAT)}")
        print(f" Oldest Date in Data: {oldest_date.strftime(self.SIMPLE_DATE_FORMAT)}")

    def _filter_orders_by_datetime_range(self, start_dt, end_dt):
        filtered = []
        for order in self.bill_data:
            try:
                order_dt = datetime.strptime(order['createddate'], self.SIMPLE_DATE_FORMAT)
                if start_dt <= order_dt <= end_dt:
                    filtered.append(order)
            except (ValueError, KeyError):
                continue
        return filtered

    def _filter_orders_by_days(self, days):
        end_dt = datetime.now()
        start_dt = end_dt - timedelta(days=days)
        return self._filter_orders_by_datetime_range(start_dt, end_dt)

    def _collect_stats(self, orders):
        total_revenue = 0
        total_quantity = 0
        item_stats = {}

        for order in orders:
            for item in order.get('item', []):
                name = item.get('name', 'unknown').lower()
                qty = int(item.get('quantity', 0))
                revenue = float(item.get('total+gst', 0))

                if name not in item_stats:
                    item_stats[name] = {"quantity": 0, "revenue": 0}

                item_stats[name]["quantity"] += qty
                item_stats[name]["revenue"] += revenue

                total_quantity += qty
                total_revenue += revenue

        return total_revenue, total_quantity, item_stats

    def _display_report(self, label, total_revenue, total_quantity, item_stats, to_file=None):
            
            
            print()
            lines = []
            lines.append(f"\n {label} Report")
            lines.append(f"Total Revenue: ₹{total_revenue:.2f}")
            lines.append(f"Total Quantity Sold: {total_quantity}")

            lines.append("\nItem Breakdown:")
            lines.append("{:<20} {:<10} {:<12} {:<15} {:<15}".format(
                "Item", "Quantity", "Revenue(₹)", "% of Qty", "% of Revenue"
            ))

            for name, stats in sorted(item_stats.items(), key=lambda x: x[1]['revenue'], reverse=True):
                qty_pct = (stats["quantity"] / total_quantity * 100) if total_quantity else 0
                rev_pct = (stats["revenue"] / total_revenue * 100) if total_revenue else 0
                lines.append("{:<20} {:<10} {:<12.2f} {:<15.2f} {:<15.2f}".format(
                    name, stats["quantity"], stats["revenue"], qty_pct, rev_pct
                ))

            lines.append("\n Top 5 by Revenue:")

            for i, (name, stats) in enumerate(sorted(item_stats.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5], 1):
                lines.append(f"{i}. {name.title()} - ₹{stats['revenue']:.2f}")

            lines.append("\n Top 5 by Quantity:")
            for i, (name, stats) in enumerate(sorted(item_stats.items(), key=lambda x: x[1]['quantity'], reverse=True)[:5], 1):
                lines.append(f"{i}. {name.title()} - {stats['quantity']} pcs")

            report_output = "\n".join(lines)
            if to_file:
                with open(to_file, "w", encoding="utf-8") as f:
                    f.write(report_output)
                print(f"\n Report saved to {to_file}")
            else:
                print(report_output)

            export = input("📁 Do you want to export the report to csv? (y/n): ").lower()
            if export == "y":
                    self.export_report_csv(label, total_revenue, total_quantity, item_stats)
     




    def export_report_csv(self, label, revenue, quantity, stats):
        filename = f"{label.replace(' ', '_')}_report.csv"
        with open(filename, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Item", "Quantity Sold", "Revenue"])
            for item, data in stats.items():
                writer.writerow([item, data['quantity'], data['revenue']])
        print(f"✅ CSV report saved to {filename}")     

    def generate_report(self, to_file=None):
        DATE_FORMAT = "%d-%m-%Y"  # fallback if self.SIMPLE_DATE_FORMAT isn't defined
        self.check_date_range_data()
        while True:
            print("\n Choose Report Type:")
            print("1. Weekly Report (Last 7 days)")
            print("2. Monthly Report (Last 30 days)")
            print("3. Custom Number of Days")
            print("4. Custom Date Range")
            print("5. Exit")

            choice = input("Enter your choice (1-5): ")

            if choice == "1":
                label = "Weekly"
                filtered = self._filter_orders_by_days(7)

            elif choice == "2":
                label = "Monthly"
                filtered = self._filter_orders_by_days(30)

            elif choice == "3":
                try:
                    d = int(input("Enter how many days old report you want: "))
                    label = f"Report for Last {d} Days"
                    filtered = self._filter_orders_by_days(d)
                except ValueError:
                    print("❌ Invalid number.")
                    continue

            elif choice == "4":
                try:
                    start_str = input("Enter start date (DD-MM-YYYY): ")
                    end_str = input("Enter end date (DD-MM-YYYY): ")
                    date_format = getattr(self, "SIMPLE_DATE_FORMAT", DATE_FORMAT)
                    start_dt = datetime.strptime(start_str, date_format)
                    end_dt = datetime.strptime(end_str, date_format) + timedelta(days=1) - timedelta(seconds=1)
                    label = f"Custom Report ({start_str} to {end_str})"
                    filtered = self._filter_orders_by_datetime_range(start_dt, end_dt)
                except ValueError:
                    print("❌ Invalid date format.")
                    continue

            elif choice == "5":
                print("👋 Exiting report generation.")
                return

            else:
                print("❌ Invalid choice. Please choose 1–5.")
                continue

            # Common logic for all valid reports
            total_revenue, total_quantity, item_stats = self._collect_stats(filtered)
            self._display_report(label, total_revenue, total_quantity, item_stats, to_file)

        




    def weekly_report(self, to_file=None):
        filtered = self._filter_orders_by_days(7)
        total_revenue, total_quantity, item_stats = self._collect_stats(filtered)
        self._display_report("Weekly", total_revenue, total_quantity, item_stats, to_file)

    def monthly_report(self, to_file=None):
        filtered = self._filter_orders_by_days(30)
        total_revenue, total_quantity, item_stats = self._collect_stats(filtered)
        self._display_report("Monthly", total_revenue, total_quantity, item_stats, to_file)

    def custom_report(self, start_date_str, end_date_str, to_file=None):
        try:
            start_dt = datetime.strptime(start_date_str, self.SIMPLE_DATE_FORMAT)
            end_dt = datetime.strptime(end_date_str, self.SIMPLE_DATE_FORMAT) + timedelta(days=1) - timedelta(seconds=1)
            filtered = self._filter_orders_by_datetime_range(start_dt, end_dt)
            label = f"Custom Report ({start_date_str} to {end_date_str})"
            total_revenue, total_quantity, item_stats = self._collect_stats(filtered)
            self._display_report(label, total_revenue, total_quantity, item_stats, to_file)
        except ValueError:
            print(" Invalid date format! Use DD-MM-YYYY")