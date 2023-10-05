import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkinter import scrolledtext
from matplotlib import pyplot as plt

# Database Connection
conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

# Color Palettes
LightBlue = '#C2DEDC'
White = '#ECE5C7'
LightGrey = '#CDC2AE'
Purple = '#116A7B'
Yellow = '#F7E987'

# Size
window_x = 1000
window_y = 800


class ToastNotification(tk.Tk):
    def __init__(self, title, message):
        super().__init__()
        self.title(title)
        self.geometry("500x50")
        self.attributes('-topmost', True)
        self.configure(bg="white")

        self.label = tk.Label(self, text=message, bg="white", padx=10, pady=10)
        self.label.pack(fill=tk.BOTH, expand=True)

        self.after(1000, self.destroy)
class ExpenseTracker():
    def __init__(self):
        # Initialize the main application window
        self.root = tk.Tk()
        self.root.title("Expense Tracker")
        self.root.geometry('1000x800')
        self.root.config(bg=LightBlue)

        # Variable to hold the selected category from the ComboBox
        self.cat_name = tk.StringVar()

        # Create the GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Main Label
        self.main_label = tk.Label(self.root, text='Expense Tracker', font=('Cascadia Mono', 40, 'bold'),
                                   bg=LightBlue, fg=Purple)
        self.main_label.place(x=250, y=20, height=50, width=500)

        # Buttons for tracking and viewing expenses
        self.track_button = tk.Button(self.root, text='Track Expense', font=('Cascadia Mono Light', 20),
                                      command=self.trackExpense1, bg=Yellow, fg=Purple)
        self.track_button.place(x=100, y=100, height=60, width=210)

        self.summary_button = tk.Button(self.root, text='View Expense', font=('Cascadia Mono Light', 20),
                                        command=self.viewExpense, bg=Yellow, fg=Purple)
        self.summary_button.place(x=400, y=100, height=60, width=210)

        self.delete_button = tk.Button(self.root, text='Delete Expense', font=('Cascadia Mono Light', 20),
                                        command=self.deleteView, bg=Yellow, fg=Purple)
        self.delete_button.place(x=700, y=100, height=60, width=250)

        # TRACK EXPENSE

        # Labels and entry fields for tracking expenses
        self.date_label = tk.Label(self.root, text='Enter the date of the expense (YYYY-MM-DD): ',
                                   font=('HP Simplified Hans Light', 15), bg=LightBlue)
        self.date_entry = tk.Entry(self.root)

        self.desc_label = tk.Label(self.root, text='Enter the description: ',
                                   font=('HP Simplified Hans Light', 15), bg=LightBlue)
        self.desc_entry = tk.Entry(self.root, text="")

        self.cat_label = tk.Label(self.root, text='Enter the category: ',
                                  font=('HP Simplified Hans Light', 15), bg=LightBlue)
        self.cat_entry = tk.Entry(self.root, text="")

        # Fetch saved categories from the database
        cur.execute("SELECT DISTINCT category FROM Expenses")
        self.saved_categories = cur.fetchall()

        # ComboBox for selecting a saved category
        self.cat_combo = ttk.Combobox(self.root, text='saved categories', font=("Cascadia Mono", 20),
                                      values=self.saved_categories, textvariable=self.cat_name)

        # Button for adding a new category
        self.newcat_button = tk.Button(self.root, text='Add New Category', font=('Cascadia Mono Light', 15),
                                       command=self.addNewCategory, bg=Purple, fg=Yellow)

        # Button for selecting a category
        self.selectcat_button = tk.Button(self.root, text='Select Category', font=('Cascadia Mono Light', 15),
                                          command=self.selectCategory, bg=Purple, fg=Yellow)

        # Label and entry field for entering the price
        self.price_label = tk.Label(self.root, text='Enter the price: ',
                                    font=('HP Simplified Hans Light', 15), bg=LightBlue)
        self.price_entry = tk.Entry(self.root)

        # Button for tracking an expense
        self.track2_button = tk.Button(self.root, text='Track', font=('Cascadia Mono Light', 15),
                                       command=self.trackExpense2, bg=Purple, fg=Yellow)

        self.clear_button = tk.Button(self.root, text='Clear All', font=('Cascadia Mono Light', 15),
                                       command=self.clearAll, bg=Purple, fg=Yellow)

        # VIEW EXPENSE

        # Buttons for viewing all expenses and monthly expenses
        self.allexp_button = tk.Button(self.root, text='View All Expense', font=('Cascadia Mono Light', 15),
                                       command=self.viewAllExpense, bg=Purple, fg=Yellow)
        self.monthexp_button = tk.Button(self.root, text='View Monthly Expense', font=('Cascadia Mono Light', 15),
                                         command=self.viewMonthExpense, bg=Purple, fg=Yellow)

        # Label and entry field for entering the month for viewing monthly expenses
        self.viewdate_label = tk.Label(self.root, text='Enter the month (YYYY-MM):',
                                       font=('HP Simplified Hans Light', 15), bg=LightBlue)
        self.viewdate_entry = tk.Entry(self.root, text="")

        # ScrolledText widget for displaying expense details
        self.exp_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=('HP Simplified Hans Light', 15),
                                                  bg=LightGrey, fg=Purple)

        self.viewgraph_button = tk.Button(self.root, text='View Expense Chart', font=('Cascadia Mono Light', 15),
                                       command=self.viewExpenseChart, bg=Purple, fg=Yellow)


        #DELETE EXPENSE

        self.id_label = tk.Label(self.root, text='Enter the expense id to delete:',
                                   font=('HP Simplified Hans Light', 15), bg=LightBlue)
        self.id_entry = tk.Entry(self.root)
        self.delete_button = tk.Button(self.root, text='Delete', font=('Cascadia Mono Light', 15),
                                      command=self.deleteExpense, bg=Purple, fg=Yellow)



    def trackExpense1(self):
        # Show the tracking expense content
        self.hideDeleteExpense()
        self.hideSummaryContent()
        self.showExpenseContent()

    def trackExpense2(self):
        # Retrieve input values for tracking an expense
        date = self.date_entry.get()
        desc = self.desc_entry.get()
        cat = self.cat_entry.get()
        price = self.price_entry.get()

        # Insert expense into the database
        cur.execute("INSERT INTO expenses (Date, description, category, price) VALUES (?,?,?,?)",
                    (date, desc, cat, price))
        conn.commit()

    def showExpenseContent(self):
        # Show the tracking expense elements
        self.date_label.place(x=40, y=200, height=60, width=500)
        self.date_entry.place(x=500, y=210, height=40, width=300)
        self.desc_label.place(x=40, y=250, height=60, width=300)
        self.desc_entry.place(x=300, y=260, height=40, width=300)
        self.cat_label.place(x=30, y=300, height=60, width=300)
        self.cat_entry.place(x=300, y=310, height=40, width=300)
        self.cat_combo.place(x=630, y=310, height=40, width=200)
        self.newcat_button.place(x=60, y=380, height=40, width=300)
        self.selectcat_button.place(x=480, y=380, height=40, width=300)
        self.price_label.place(x=15, y=450, height=60, width=300)
        self.price_entry.place(x=300, y=460, height=40, width=300)
        self.track2_button.place(x=200, y=520, height=40, width=200)
        self.clear_button.place(x=500, y=520, height=40, width=200)


    def hideExpenseContent(self):
        # Hide the tracking expense elements
        self.date_label.place_forget()
        self.date_entry.place_forget()
        self.desc_label.place_forget()
        self.desc_entry.place_forget()
        self.cat_label.place_forget()
        self.cat_entry.place_forget()
        self.cat_combo.place_forget()
        self.newcat_button.place_forget()
        self.selectcat_button.place_forget()
        self.price_label.place_forget()
        self.price_entry.place_forget()
        self.track2_button.place_forget()
        self.clear_button.place_forget()


    def showSummaryContent(self):
        # Show the summary content elements
        self.allexp_button.place(x=80, y=200, height=40, width=300)
        self.monthexp_button.place(x=500, y=200, height=40, width=300)
        self.viewdate_label.place(x=20, y=250, height=60, width=300)
        self.viewdate_entry.place(x=300, y=255, height=40, width=300)
        self.exp_text.place(x=20, y=300, height=250, width=900)
        self.viewgraph_button.place(x=350,y=600,height=40, width=300)

    def hideSummaryContent(self):
        # Hide the summary content elements
        self.allexp_button.place_forget()
        self.monthexp_button.place_forget()
        self.viewdate_label.place_forget()
        self.viewdate_entry.place_forget()
        self.exp_text.place_forget()
        self.viewgraph_button.place_forget()

    def viewExpense(self):
        # Switch to the summary view
        self.hideDeleteExpense()
        self.hideExpenseContent()
        self.showSummaryContent()

    def viewAllExpense(self):
        # Display all expenses in the ScrolledText widget
        self.exp_text.config(state=tk.NORMAL)
        self.exp_text.delete('1.0', tk.END)
        cur.execute("SELECT * FROM Expenses")
        expenses = cur.fetchall()
        content = "Id \t\t| Date \t\t| Description \t\t| Category \t\t| Price \n"
        for expense in expenses:
            id, date, description, category, price = expense
            content += f"{id}\t\t|{date}\t\t|{description}\t\t|{category}\t\t|{price}\n"

        self.exp_text.insert(tk.INSERT, content)
        self.exp_text.config(state=tk.DISABLED)

    def viewMonthExpense(self):
        # Display monthly expenses in the ScrolledText widget
        self.exp_text.config(state=tk.NORMAL)
        self.exp_text.delete('1.0', tk.END)
        date = self.viewdate_entry.get()
        year, month = date.split('-')
        cur.execute("""SELECT id, date, description, category, price
                            FROM Expenses 
                            WHERE strftime('%Y%m', Date) = ?""", (year + month,))
        expenses = cur.fetchall()
        content = "Id \t\t| Date \t\t| Description \t\t| Category \t\t| Price \n"
        for expense in expenses:
            id, date, description, category, price = expense
            content += f"{id}\t\t|{date}\t\t|{description}\t\t|{category}\t\t|{price}\n"

        self.exp_text.insert(tk.INSERT, content)
        self.exp_text.config(state=tk.DISABLED)

    def addNewCategory(self):

        cat = self.cat_entry.get()

        if __name__ == "__main__":
           title = "Notification!"
           message = cat + " category added!"

        notification = ToastNotification(title, message)
        notification.mainloop()


    def selectCategory(self):
        # Select a category from the ComboBox and populate the cat_entry field
        selected_category = self.cat_combo.get()
        self.cat_entry.delete(0, tk.END)
        self.cat_entry.insert(0, selected_category)

    def clearAll(self):
        # Clear the values of all entry widgets
        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.cat_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def deleteView(self):
        self.showDeleteExpense()
        self.hideSummaryContent()
        self.hideExpenseContent()
        pass


    def showDeleteExpense(self):
        self.id_label.place(x=40, y=200, height=60, width=500)
        self.id_entry.place(x=450, y=210, height=40, width=300)
        self.delete_button.place(x=350, y=310, height=40, width=300)


    def hideDeleteExpense(self):
        self.id_label.place_forget()
        self.id_entry.place_forget()
        self.delete_button.place_forget()

    def deleteExpense(self):
        id = self.id_entry.get()
        cur.execute("Delete from Expenses where Id=?",id)
        conn.commit()

    def viewExpenseChart(self):
        #month_array= []
        expense_array = [0] * 12
        #year = 2023

        # Prepare data for the expense chart (modify this as needed)
        month_array = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        cur.execute("SELECT strftime('%m', Date) as month, SUM(price) FROM Expenses WHERE strftime('%Y', Date) = '2023' GROUP BY month")
        prices = cur.fetchall()
        for month, price in prices:
            month_idx = int(month) - 1  # Convert month (as a number) to index (0-11)
            expense_array[month_idx] = price

        # Create a bar chart
        plt.figure(figsize=(12, 6))
        plt.bar(month_array, expense_array, color=Purple)
        plt.xlabel('Month')
        plt.ylabel('Expense ($)')
        plt.title('Monthly Expense Chart')
        plt.grid(True)

        # Display the chart
        plt.show()



    def run(self):
        # Start the main application loop
        self.root.mainloop()


if __name__ == '__main__':
    app = ExpenseTracker()
    app.run()
