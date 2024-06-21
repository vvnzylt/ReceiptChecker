import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

def round_num(value):
    num = Decimal(str(value))
    rounded_num = num.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return float(rounded_num)

class ReceiptEntry:
    item_name: str
    quantity: str
    unit_price: float
    total_price: float

class ReceiptEntryNode:
    def __init__(self, item_name, quantity, unit_price):
        self.entry = ReceiptEntry()
        self.entry.item_name = item_name
        self.entry.quantity = quantity
        self.entry.unit_price = round_num(unit_price)
        self.entry.total_price = self.compute_total_price(quantity, self.entry.unit_price)
        self.previous_node = None
        self.next_node = None

    def compute_total_price(self, quantity, unit_price):
        # Since quantities with units are treated 1, they must be checked using RegEx 
        filtered_quantity = re.search(r"^(?!0+(?:\.0+)?(?:g|kg|mL|L)?$)([1-9]\d*)?(([1-9]\d*|0)\.\d+)?(g|kg|mL|L)$", quantity)
        if filtered_quantity:
            quantity = 1
        else:
            pass
        # Returns a computed total_price value to the self.entry.total_price above at the ReceiptEntryNode constructor
        return int(quantity) * unit_price

class ReceiptEntryList:
    def __init__(self):
        self.receipt_number = None
        self.date = None
        self.time = None
        self.head = None
        self.tail = None

    def swap(self, node_1, node_2):
        node_1.item_name, node_2.item_name = node_2.item_name, node_1.item_name
        node_1.quantity, node_2.quantity = node_2.quantity, node_1.quantity
        node_1.unit_price, node_2.unit_price = node_2.unit_price, node_1.unit_price
        node_1.total_price, node_2.total_price = node_2.total_price, node_1.total_price

    def sort_list(self):
        current = self.head

        while current is not None:
            next_value = current.next_node
            while next_value is not None:
                # Swapping will happen if the current node has less value than its next node. However, if there are items that have same values,
                # string comparison will happen in which letters will be arranged from Z to A.
                if (current.entry.total_price < next_value.entry.total_price) or (current.entry.total_price == next_value.entry.total_price and current.entry.item_name < next_value.entry.item_name):
                    self.swap(current.entry, next_value.entry)
                next_value = next_value.next_node
            current = current.next_node

    def change_receipt_header(self):
        def change_receipt_code(self):
            new_name = str(input("Enter new receipt code:\n>>>"))
            print(f"\"{self.receipt_number}\" will be changed into \"{new_name}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        self.receipt_number = new_name
                        break
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")

        def change_date(self):
            current_date = datetime.strptime(self.date, "%m/%d/%Y") if self.date else None

            print("\nEnter new date in YYYY/MM/DD format (e.g., 12/29/2000):")
            while True:
                new_date = str(input(">>>"))
                try:
                    filtered_date = datetime.strptime(new_date, "%m/%d/%Y")
                    break
                except ValueError:
                    print("\nERROR: Invalid date. Please ensure that date is in proper format YYYY/MM/DD format (e.g., 12/29/2000)")

            if current_date is not None:
                print(f"\"{current_date.strftime("%m/%d/%Y")}\" will be changed into \"{filtered_date.strftime("%m/%d/%Y")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")
            else:
                print(f"New date will be \"{filtered_date.strftime("%m/%d/%Y")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        self.date = str(filtered_date.strftime("%m/%d/%Y"))
                        break
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")
            
        def change_time(self):
            current_time = datetime.strptime(self.time, "%H:%M:%S") if self.time else None

            print("\nEnter new time in HH:MM:SS format (e.g., 20:01:59):")
            while True:
                new_time = str(input(">>>"))
                try:
                    filtered_time = datetime.strptime(new_time, "%H:%M:%S")
                    break
                except ValueError:
                    print("\nERROR: Invalid time. Please ensure that time is in proper HH:MM:SS format (e.g., 20:01:59)")

            if current_time is not None:
                print(f"\"{current_time.strftime("%H:%M:%S")}\" will be changed into \"{filtered_time.strftime("%H:%M:%S")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")
            else:
                print(f"New time will be \"{filtered_time.strftime("%H:%M:%S")}\". Confirm change?\n1 = Yes\n2 = No\n\nEnter option: ")

            while True:
                try:
                    option = int(input(">>> "))
                    if option == 1:
                        self.time = str(filtered_time.strftime("%H:%M:%S"))
                        break
                    elif option == 2:
                        return
                    else:
                        print("\nInvalid option. Please enter a number between 1 and 2.")
                except ValueError:
                    print("\nInvalid value. Please enter a correct number.")
            
        print(f"\nReceipt code: {self.receipt_number}")
        print(f"Date/time: {self.date} {self.time}")

        print("1 = Change receipt code\n2 = Change date\n3 = Change time\n4 = Go back\n\nEnter option: ")
        while True:
            try:
                option = int(input(">>> "))

                if option == 1:
                    change_receipt_code(self)
                    break
                elif option == 2:
                    change_date(self)
                    break
                elif option == 3:
                    change_time(self)
                    break
                elif option == 4:
                    break
                else:
                    print("\nInvalid option. Please enter a number between 1 and 4.")
            except ValueError:
                print("\nInvalid value. Please enter a correct number.")
