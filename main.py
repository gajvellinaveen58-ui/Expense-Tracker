from datetime import datetime
from abc import ABC, abstractmethod


# ==============================
# ABSTRACTION
# ==============================

class ExpenseBase(ABC):

    @abstractmethod
    def display(self):
        pass


# ==============================
# EXPENSE CLASS
# ==============================

class Expense(ExpenseBase):

    def __init__(self, amount, category, description, date=None):
        self.__amount = amount          # Encapsulation
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    # Getter method for private amount
    def get_amount(self):
        return self.__amount

    # Setter method
    def set_amount(self, amount):
        self.__amount = amount

    # Polymorphism
    def display(self):
        print(f"Amount      : ₹{self.__amount:.2f}")
        print(f"Category    : {self.category}")
        print(f"Description : {self.description}")
        print(f"Date        : {self.date}")


# ==============================
# INHERITANCE
# ==============================

class PersonalExpense(Expense):

    def display(self):
        print("[Personal Expense]")
        super().display()


class BusinessExpense(Expense):

    def display(self):
        print("[Business Expense]")
        super().display()


# ==============================
# EXPENSE TRACKER CLASS
# ==============================

class ExpenseTracker:

    def __init__(self):
        self.expenses = []

    # Add expense
    def add_expense(self):
        try:
            amount = float(input("Enter expense amount: "))

            if amount <= 0:
                print("Amount must be greater than zero.")
                return

        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()

        if not category or not description:
            print("Category and description cannot be empty.")
            return

        expense_type = input(
            "Enter type (1-Personal, 2-Business): "
        )

        if expense_type == "2":
            expense = BusinessExpense(
                amount,
                category,
                description
            )
        else:
            expense = PersonalExpense(
                amount,
                category,
                description
            )

        self.expenses.append(expense)
        self.save_expense(expense)

        print("Expense added successfully!")

    # Save expense to file
    def save_expense(self, expense):

        with open("expenses.txt", "a") as file:
            file.write(
                f"{expense.get_amount()}|"
                f"{expense.category}|"
                f"{expense.description}|"
                f"{expense.date}\n"
            )

    # Load expenses from file
    def load_expenses(self):

        try:
            with open("expenses.txt", "r") as file:

                for line in file:

                    data = line.strip().split("|")

                    if len(data) == 4:

                        amount, category, description, date = data

                        expense = Expense(
                            float(amount),
                            category,
                            description,
                            date
                        )

                        self.expenses.append(expense)

        except FileNotFoundError:
            pass

        except ValueError:
            print("Some data in the file could not be loaded.")

    # View all expenses
    def view_expenses(self):

        if not self.expenses:
            print("No expenses found.")
            return

        print("\n========== ALL EXPENSES ==========")

        for i, expense in enumerate(self.expenses, start=1):

            print(f"\nExpense {i}")
            print("--------------------")
            expense.display()

    # Calculate total
    def calculate_total(self):

        if not self.expenses:
            print("No expenses found.")
            return

        total = 0

        for expense in self.expenses:
            total += expense.get_amount()

        print(f"\nTotal Expenses: ₹{total:.2f}")

    # Category summary
    def category_summary(self):

        if not self.expenses:
            print("No expenses found.")
            return

        summary = {}

        for expense in self.expenses:

            category = expense.category
            amount = expense.get_amount()

            if category in summary:
                summary[category] += amount
            else:
                summary[category] = amount

        print("\n========== CATEGORY SUMMARY ==========")

        for category, amount in summary.items():
            print(f"{category}: ₹{amount:.2f}")

    # Search expenses
    def search_expenses(self):

        keyword = input(
            "Enter category or description to search: "
        ).strip().lower()

        found = False

        for expense in self.expenses:

            if (
                keyword in expense.category.lower()
                or keyword in expense.description.lower()
            ):

                if not found:
                    print("\n========== SEARCH RESULTS ==========")

                expense.display()
                print("--------------------")
                found = True

        if not found:
            print("No matching expenses found.")

    # Delete expense
    def delete_expense(self):

        if not self.expenses:
            print("No expenses found.")
            return

        self.view_expenses()

        try:
            number = int(
                input("\nEnter expense number to delete: ")
            )

            if number < 1 or number > len(self.expenses):
                print("Invalid expense number.")
                return

        except ValueError:
            print("Please enter a valid number.")
            return

        deleted_expense = self.expenses.pop(number - 1)

        self.rewrite_file()

        print(
            f"Expense of ₹{deleted_expense.get_amount():.2f} "
            "deleted successfully!"
        )

    # Rewrite file after deletion
    def rewrite_file(self):

        with open("expenses.txt", "w") as file:

            for expense in self.expenses:

                file.write(
                    f"{expense.get_amount()}|"
                    f"{expense.category}|"
                    f"{expense.description}|"
                    f"{expense.date}\n"
                )


# ==============================
# MAIN FUNCTION
# ==============================

def main():

    tracker = ExpenseTracker()

    tracker.load_expenses()

    while True:

        print("\n================================")
        print("       EXPENSE TRACKER")
        print("================================")

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Calculate Total")
        print("4. Category Summary")
        print("5. Search Expenses")
        print("6. Delete Expense")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            tracker.add_expense()

        elif choice == "2":
            tracker.view_expenses()

        elif choice == "3":
            tracker.calculate_total()

        elif choice == "4":
            tracker.category_summary()

        elif choice == "5":
            tracker.search_expenses()

        elif choice == "6":
            tracker.delete_expense()

        elif choice == "7":
            print("Thank you for using Expense Tracker!")
            break

        else:
            print("Invalid choice. Please select 1-7.")


# ==============================
# PROGRAM START
# ==============================

if __name__ == "__main__":
    main()