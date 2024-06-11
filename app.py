import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import requests
from io import BytesIO
from crud import add_book, update_book, get_book, delete_book, members_collection, loans_collection, \
    get_all_books_mongo, delete_member, update_loan, delete_loan

import tkinter as tk
from tkinter import ttk, messagebox

class LibraryManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Manager")
        self.geometry("800x400")

        tab_control = ttk.Notebook(self)
        tab_control.pack(expand=1, fill="both")

        self.create_books_tab(tab_control)
        self.create_members_tab(tab_control)
        self.create_loans_tab(tab_control)

    def create_books_tab(self, tab_control):
        books_tab = ttk.Frame(tab_control)
        tab_control.add(books_tab, text="Books")

        self.books_tree = ttk.Treeview(books_tab, columns=("Title", "Authors", "Year"))
        self.books_tree.heading("#0", text="Book ID")
        self.books_tree.heading("Title", text="Title")
        self.books_tree.heading("Authors", text="Authors")
        self.books_tree.heading("Year", text="Year")
        self.books_tree.pack(fill="both", expand=True)

        self.retrieve_all_books()

        books_buttons_frame = ttk.Frame(books_tab)
        books_buttons_frame.pack(pady=10)

        ttk.Button(books_buttons_frame, text="Refresh", command=self.retrieve_all_books).grid(row=0, column=0, padx=5)
        ttk.Button(books_buttons_frame, text="Update", command=self.update_book).grid(row=0, column=1, padx=5)
        ttk.Button(books_buttons_frame, text="Delete", command=self.delete_book).grid(row=0, column=2, padx=5)

    def retrieve_all_books(self):
        for item in self.books_tree.get_children():
            self.books_tree.delete(item)
        books = get_all_books_mongo()
        for book in books:
            self.books_tree.insert("", "end", text=book["_id"], values=(book["title"], ", ".join(book["authors"]), book["year"]))

    def update_book(self):
        selected_item = self.books_tree.selection()
        if selected_item:
            book_id = self.books_tree.item(selected_item, "text")
            title = self.books_tree.item(selected_item, "values")[0]
            authors = self.books_tree.item(selected_item, "values")[1].split(", ")
            year = self.books_tree.item(selected_item, "values")[2]

            # Open a new window or dialog for updating the book details
            update_dialog = tk.Toplevel(self)
            update_dialog.title("Update Book")

            ttk.Label(update_dialog, text="Title:").grid(row=0, column=0, padx=5, pady=5)
            title_entry = ttk.Entry(update_dialog)
            title_entry.insert(0, title)
            title_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(update_dialog, text="Authors:").grid(row=1, column=0, padx=5, pady=5)
            authors_entry = ttk.Entry(update_dialog)
            authors_entry.insert(0, ", ".join(authors))
            authors_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(update_dialog, text="Year:").grid(row=2, column=0, padx=5, pady=5)
            year_entry = ttk.Entry(update_dialog)
            year_entry.insert(0, year)
            year_entry.grid(row=2, column=1, padx=5, pady=5)

            # Update book function
            def perform_update():
                updated_title = title_entry.get()
                updated_authors = authors_entry.get().split(", ")
                updated_year = year_entry.get()

                # Perform validation if needed

                # Update the book
                update_book(book_id, updated_title, updated_authors, updated_year)

                # Close the dialog
                update_dialog.destroy()

                # Show success message
                messagebox.showinfo("Update Book", "Book updated successfully")

                # Refresh the books tab
                self.retrieve_all_books()

            ttk.Button(update_dialog, text="Update", command=perform_update).grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        else:
            messagebox.showwarning("Selection Error", "Please select a book to update")
    def delete_book(self):
        selected_item = self.books_tree.selection()
        if selected_item:
            book_id = self.books_tree.item(selected_item, "text")
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete book with ID: {book_id}?")
            if confirmation:
                delete_book(book_id)
                self.retrieve_all_books()
        else:
            messagebox.showwarning("Selection Error", "Please select a book to delete")

    def create_members_tab(self, tab_control):
        members_tab = ttk.Frame(tab_control)
        tab_control.add(members_tab, text="Members")

        self.members_tree = ttk.Treeview(members_tab, columns=("Name", "Email", "Membership Date"))
        self.members_tree.heading("#0", text="Member ID")
        self.members_tree.heading("Name", text="Name")
        self.members_tree.heading("Email", text="Email")
        self.members_tree.heading("Membership Date", text="Membership Date")
        self.members_tree.pack(fill="both", expand=True)

        self.retrieve_all_members()

        members_buttons_frame = ttk.Frame(members_tab)
        members_buttons_frame.pack(pady=10)

        ttk.Button(members_buttons_frame, text="Refresh", command=self.retrieve_all_members).grid(row=0, column=0, padx=5)
        ttk.Button(members_buttons_frame, text="Update", command=self.update_member).grid(row=0, column=1, padx=5)
        ttk.Button(members_buttons_frame, text="Delete", command=self.delete_member).grid(row=0, column=2, padx=5)

    def retrieve_all_members(self):
        for item in self.members_tree.get_children():
            self.members_tree.delete(item)
        members = members_collection.find()
        for member in members:
            self.members_tree.insert("", "end", text=member["_id"], values=(member["name"], member["email"], member["membership_date"]))

    def update_member(self):
        selected_item = self.members_tree.selection()
        if selected_item:
            member_id = self.members_tree.item(selected_item, "text")
            name = self.members_tree.item(selected_item, "values")[0]
            email = self.members_tree.item(selected_item, "values")[1]
            membership_date = self.members_tree.item(selected_item, "values")[2]
            # Open a new window or dialog for updating the member details
            # You can implement the update functionality here
            messagebox.showinfo("Update Member", f"Updating member with ID: {member_id}")
        else:
            messagebox.showwarning("Selection Error", "Please select a member to update")

    def delete_member(self):
        selected_item = self.members_tree.selection()
        if selected_item:
            member_id = self.members_tree.item(selected_item, "text")
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete member with ID: {member_id}?")
            if confirmation:
                delete_member(member_id)
                self.retrieve_all_members()
        else:
            messagebox.showwarning("Selection Error", "Please select a member to delete")

    def create_loans_tab(self, tab_control):
        loans_tab = ttk.Frame(tab_control)
        tab_control.add(loans_tab, text="Loans")

        self.loans_tree = ttk.Treeview(loans_tab, columns=("Book ID", "Member ID", "Return Date", "Loan Date"))
        self.loans_tree.heading("#0", text="Loan ID")
        self.loans_tree.heading("Book ID", text="Book ID")
        self.loans_tree.heading("Member ID", text="Member ID")
        self.loans_tree.heading("Loan Date", text="Loan Date")
        self.loans_tree.heading("Return Date", text="Return Date")
        self.loans_tree.pack(fill="both", expand=True)

        self.retrieve_all_loans()

        loans_buttons_frame = ttk.Frame(loans_tab)
        loans_buttons_frame.pack(pady=10)

        ttk.Button(loans_buttons_frame, text="Refresh", command=self.retrieve_all_loans).grid(row=0, column=0, padx=5)
        ttk.Button(loans_buttons_frame, text="Update", command=self.update_loan).grid(row=0, column=1, padx=5)
        ttk.Button(loans_buttons_frame, text="Delete", command=self.delete_loan).grid(row=0, column=2, padx=5)

    def retrieve_all_loans(self):
        for item in self.loans_tree.get_children():
            self.loans_tree.delete(item)
        loans = loans_collection.find()
        for loan in loans :
             self.loans_tree.insert("", "end", text=loan["_id"], values=(loan["book_id"], loan["member_id"], loan["loan_date"], loan.get("return_date", "")))

    def update_loan(self):
        selected_item = self.loans_tree.selection()
        if selected_item:
            loan_id = self.loans_tree.item(selected_item, "text")
            book_id = self.loans_tree.item(selected_item, "values")[0]
            member_id = self.loans_tree.item(selected_item, "values")[1]
            loan_date = self.loans_tree.item(selected_item, "values")[2]
            return_date = self.loans_tree.item(selected_item, "values")[3]

            # Create a new dialog window
            update_dialog = tk.Toplevel(self)
            update_dialog.title("Update Loan")


            ttk.Label(update_dialog, text="Return Date:").grid(row=4, column=0, padx=5, pady=5)
            return_date_entry = ttk.Entry(update_dialog)
            return_date_entry.insert(0, return_date)
            return_date_entry.grid(row=4, column=1, padx=5, pady=5)

            # Update loan function
            def perform_update():
                updated_return_date = return_date_entry.get()
                # Perform validation if needed
                # Update the loan
                update_loan(loan_id, updated_return_date)
                # Close the dialog
                # Refresh the loans tab
                update_dialog.destroy()
                messagebox.showinfo("Update Loan", "Loan updated successfully")
                self.retrieve_all_loans()

            ttk.Button(update_dialog, text="Update", command=perform_update).grid(row=5, column=0, columnspan=2, padx=5,
                                                                                  pady=10)

        else:
            messagebox.showwarning("Selection Error", "Please select a loan to update")

    def delete_loan(self):
        selected_item = self.loans_tree.selection()
        if selected_item:
            loan_id = self.loans_tree.item(selected_item, "text")
            confirmation = messagebox.askyesno("Confirmation", f"Are you sure you want to delete loan with ID: {loan_id}?")
            if confirmation:
                delete_loan(loan_id)
                self.retrieve_all_loans()
        else:
            messagebox.showwarning("Selection Error", "Please select a loan to delete")

if __name__ == "__main__":
    app = LibraryManagerApp()
    app.mainloop()