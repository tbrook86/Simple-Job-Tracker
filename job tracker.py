import pandas as pd
import matplotlib.pyplot as plt
import os

CSV_FILE = "tracker_data.csv"  #This is the name of the excel document you are using as storage it should be in the same folder as the code.
print("Saving and loading CSV from:", os.path.abspath(CSV_FILE))

def display_menu():
    print("\nJob Application Tracker")
    print("1. Add New Application")
    print("2. View All Applications")
    print("3. Filter Applications by Status")
    print("4. Show Status Breakdown")
    print("5. Edit an Application")
    print("6. Delete an Application")
    print("7. Exit")
    return input("Choose an option: ")

def statistics(xyz):
    if xyz.empty:
        print("No data to visualize.")
        return
    status_counts = xyz["Status"].value_counts()
    status_counts.plot(kind='pie', autopct='%1.1f%%', title='Application Status Distribution')
    plt.ylabel('')
    plt.show()

def loading_data():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Job Title", "Company", "Status", "Date Applied", "Comments"])

def saved_data(xyz):
    xyz.to_csv(CSV_FILE, index=False)

def add_entry(xyz):
    job = input("Job Title: ")
    company = input("Company: ")
    status = input("Status (Applied/Interview/Offer/Rejected): ")
    date = input("Date Applied (MM/DD/YY): ")
    comments = input("Notes: ")
    xyz.loc[len(xyz)] = [job, company, status, date, comments]
    saved_data(xyz)
    print("Entry added.")

def view_entries(xyz):
    print(xyz)

def filter_entries(xyz):
    if xyz.empty:
        print("No applications to filter.")
        return
    status = input("Enter a status keyword to filter by (e.g., applied, interview, offer): ").strip().lower()
    if status == "":
        print("You must enter a valid option.")
        return
    filtered = xyz[xyz["Status"].str.lower().str.contains(status)]
    if filtered.empty:
        print(f"No applications found matching the keyword: '{status}'")
    else:
        print(f"\nApplications matching '{status}':\n")
        print(filtered)

def edit_entry(xyz):
    if xyz.empty:
        print("No applications to edit.")
        return

    try:
        print(xyz.reset_index())
        idx = int(input("Enter the index number of the application to edit: "))
        if idx not in xyz.index:
            print("Invalid index number.")
            return

        print("\nLeave field blank to keep current value.")
        for column in ["Job Title", "Company", "Status", "Date Applied", "Comments"]:
            current_value = xyz.at[idx, column]
            new_value = input(f"{column} (current: {current_value}): ").strip()
            if new_value:
                xyz.at[idx, column] = new_value

        saved_data(xyz)
        print("Application updated successfully.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def delete_entry(xyz):
    if xyz.empty:
        print("No applications to delete.")
        return

    try:
        print(xyz.reset_index())
        idx = int(input("Enter the index number of the application to delete: "))
        if idx not in xyz.index:
            print("Invalid index number.")
            return

        confirm = input(f"Are you sure you want to delete '{xyz.at[idx, 'Job Title']}' at '{xyz.at[idx, 'Company']}'? (yes/no): ").strip().lower()
        if confirm in ["yes", "y"]:
            xyz.drop(index=idx, inplace=True)
            xyz.reset_index(drop=True, inplace=True)
            saved_data(xyz)
            print("Application deleted successfully.")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    xyz = loading_data()
    extra_mapping = {  #Added extra mapping for convienence the code is not case sensitive
        "1": "add", "add": "add",
        "2": "view", "view": "view",
        "3": "filter", "filter": "filter",
        "4": "stats", "stats": "stats",
        "5": "edit", "edit": "edit",
        "6": "delete", "delete": "delete",
        "7": "exit", "exit": "exit", "quit": "exit"
    }

    while True:
        choice = display_menu().strip().lower()
        action = extra_mapping.get(choice)
        if action == "add":
            add_entry(xyz)
        elif action == "view":
            view_entries(xyz)
        elif action == "filter":
            filter_entries(xyz)
        elif action == "stats":
            statistics(xyz)
        elif action == "edit":
            edit_entry(xyz)
        elif action == "delete":
            delete_entry(xyz)
        elif action == "exit":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
