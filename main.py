import sqlite3
import datetime

conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

while True:
    print("Select an option:")
    print("1. Enter a new expense")
    print("2. View expense summary")

    choice = int(input())

    if choice ==1:
        date = input("Enter the date of the expense(YYYY-MM-DD): ")
        desc = input("Enter the description of the expense:" )

        cur.execute("SELECT DISTINCT category FROM Expenses")
        categories = cur.fetchall()

        print('Select a category by number - ')
        for index, category in enumerate(categories):
            print(f"{index +1}. {category[0]}")
        print(f"{len(categories) +1 }. Create a new category")

        category_choice = int(input())
        if category_choice == len(categories) + 1:
            category = input("Enter the new category name: ")
        else:
            category = categories[category_choice - 1][0]

        price = input('Enter the price of expense:')

        cur.execute("INSERT INTO expenses (Date,description,category,price) VALUES (?,?,?,?) ", (date,desc,category,price))
        conn.commit()
    elif choice ==2:
        print("Select an option: ")
        print("1. View all expenses ")
        print("2. View Monthly expenses by category")

        view_choice = int(input())

        if view_choice == 1:
            cur.execute("SELECT * FROM Expenses")
            expenses = cur.fetchall()
            for expense in expenses:
                print(expense)

        elif view_choice ==2 :
            month = input("Enter the month(MM): ")
            year = input("Enter the year (YYYY): ")
            cur.execute("""SELECT category, SUM(price) FROM Expenses 
                        WHERE strftime('%m',Date) =? AND strftime('%Y',Date) =? 
                         GROUP BY category""" , (month,year))

            expenses = cur.fetchall()
            for expense in expenses:
                print(f"Category: {expense[0]} , Total: {expense[1]}")

        else:
            exit()




    else:
        exit()
