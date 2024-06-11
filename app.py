import random
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from io import BytesIO
from crud import add_book, update_book, get_book, delete_book, members_collection, loans_collection, \
    get_all_books_mongo, delete_member, update_loan, delete_loan

import tkinter as tk
from tkinter import ttk, messagebox

import tkinter as tk
from tkinter import ttk, messagebox
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

        ttk.Button(books_buttons_frame, text="Add", command=self.add_book).grid(row=0, column=0, padx=5)
        ttk.Button(books_buttons_frame, text="Refresh", command=self.retrieve_all_books).grid(row=0, column=1, padx=5)
        ttk.Button(books_buttons_frame, text="Update", command=self.update_book).grid(row=0, column=2, padx=5)
        ttk.Button(books_buttons_frame, text="Delete", command=self.delete_book).grid(row=0, column=3, padx=5)

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

    def add_book(self):

            # Open a new window or dialog for updating the book details
            add_dialog = tk.Toplevel(self)
            add_dialog.title("Add Book")

            ttk.Label(add_dialog, text="Id:").grid(row=0, column=0, padx=5, pady=5)
            id_entry = ttk.Entry(add_dialog)
            id_entry.insert(0, "")
            id_entry.grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(add_dialog, text="Title:").grid(row=1, column=0, padx=5, pady=5)
            title_entry = ttk.Entry(add_dialog)
            title_entry.insert(0, "")
            title_entry.grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(add_dialog, text="Authors:").grid(row=2, column=0, padx=5, pady=5)
            authors_entry = ttk.Entry(add_dialog)
            authors_entry.insert(0, ", ".join(""))
            authors_entry.grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(add_dialog, text="Year:").grid(row=3, column=0, padx=5, pady=5)
            year_entry = ttk.Entry(add_dialog)
            year_entry.insert(0, "")
            year_entry.grid(row=3, column=1, padx=5, pady=5)

            def perform_add():
                 updated_title = title_entry.get()
                 updated_authors = authors_entry.get().split(", ")
                 updated_year = year_entry.get()

                 # Perform validation if needed

                 # Update the book
                 add_book(77779, updated_title, updated_authors, updated_year)

                 # Close the dialog
                 add_book().destroy()

                 # Show success message
                 messagebox.showinfo("Update Book", "Book updated successfully")
                 self.retrieve_all_books()

            ttk.Button(add_dialog, text="Add", command=perform_add).grid(row=4, column=0, columnspan=2, padx=5, pady=10)






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



""" import tkinter as tk
from tkinter import ttk, messagebox
from crud import add_book, update_book, get_book, delete_book


class BookManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Manager")
        self.geometry("400x300")

        tab_control = ttk.Notebook(self)

        # Create Tabs
        self.create_add_book_tab(tab_control)
        self.create_update_book_tab(tab_control)
        self.create_get_book_tab(tab_control)
        self.create_delete_book_tab(tab_control)

        tab_control.pack(expand=1, fill='both')

    def create_add_book_tab(self, tab_control):
        add_book_tab = ttk.Frame(tab_control)
        tab_control.add(add_book_tab, text='Add Book')

        # Add Book Form
        ttk.Label(add_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.add_book_id = ttk.Entry(add_book_tab)
        self.add_book_id.grid(column=1, row=0)

        ttk.Label(add_book_tab, text="Title").grid(column=0, row=1, padx=10, pady=10)
        self.add_book_title = ttk.Entry(add_book_tab)
        self.add_book_title.grid(column=1, row=1)

        ttk.Label(add_book_tab, text="Author").grid(column=0, row=2, padx=10, pady=10)
        self.add_book_author = ttk.Entry(add_book_tab)
        self.add_book_author.grid(column=1, row=2)

        ttk.Label(add_book_tab, text="Year").grid(column=0, row=3, padx=10, pady=10)
        self.add_book_year = ttk.Entry(add_book_tab)
        self.add_book_year.grid(column=1, row=3)

        ttk.Button(add_book_tab, text="Add Book", command=self.add_book).grid(column=0, row=4, columnspan=2, pady=10)

    def create_update_book_tab(self, tab_control):
        update_book_tab = ttk.Frame(tab_control)
        tab_control.add(update_book_tab, text='Update Book')

        # Update Book Form
        ttk.Label(update_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.update_book_id = ttk.Entry(update_book_tab)
        self.update_book_id.grid(column=1, row=0)

        ttk.Label(update_book_tab, text="Title").grid(column=0, row=1, padx=10, pady=10)
        self.update_book_title = ttk.Entry(update_book_tab)
        self.update_book_title.grid(column=1, row=1)

        ttk.Label(update_book_tab, text="Author").grid(column=0, row=2, padx=10, pady=10)
        self.update_book_author = ttk.Entry(update_book_tab)
        self.update_book_author.grid(column=1, row=2)

        ttk.Label(update_book_tab, text="Year").grid(column=0, row=3, padx=10, pady=10)
        self.update_book_year = ttk.Entry(update_book_tab)
        self.update_book_year.grid(column=1, row=3)

        ttk.Button(update_book_tab, text="Update Book", command=self.update_book).grid(column=0, row=4, columnspan=2,
                                                                                       pady=10)

    def create_get_book_tab(self, tab_control):
        get_book_tab = ttk.Frame(tab_control)
        tab_control.add(get_book_tab, text='Get Book')

        # Get Book Form
        ttk.Label(get_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.get_book_id = ttk.Entry(get_book_tab)
        self.get_book_id.grid(column=1, row=0)

        ttk.Button(get_book_tab, text="Get Book", command=self.get_book).grid(column=0, row=1, columnspan=2, pady=10)

        self.get_book_result = ttk.Label(get_book_tab, text="")
        self.get_book_result.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    def create_delete_book_tab(self, tab_control):
        delete_book_tab = ttk.Frame(tab_control)
        tab_control.add(delete_book_tab, text='Delete Book')

        # Delete Book Form
        ttk.Label(delete_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.delete_book_id = ttk.Entry(delete_book_tab)
        self.delete_book_id.grid(column=1, row=0)

        ttk.Button(delete_book_tab, text="Delete Book", command=self.delete_book).grid(column=0, row=1, columnspan=2,
                                                                                       pady=10)

    def add_book(self):
        book_id = self.add_book_id.get()
        title = self.add_book_title.get()
        author = self.add_book_author.get()
        year = self.add_book_year.get()

        if book_id and title and author and year:
            add_book(book_id, title, author, year)
            messagebox.showinfo("Success", "Book added successfully")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def update_book(self):
        book_id = self.update_book_id.get()
        title = self.update_book_title.get()
        author = self.update_book_author.get()
        year = self.update_book_year.get()

        if book_id:
            update_book(book_id, title, author, year)
            messagebox.showinfo("Success", "Book updated successfully")
        else:
            messagebox.showwarning("Input Error", "Please provide a Book ID")
`
    def get_book(self):
        book_id = self.get_book_id.get()

        if book_id:
            book = get_book(book_id)
            if book:
                book_info = f"Title: {book['title']}\nAuthor: {book['author']}\nYear: {book['year']}"
                self.get_book_result.config(text=book_info)
            else:
                messagebox.showinfo("Not Found", "Book not found")
        else:
            messagebox.showwarning("Input Error", "Please provide a Book ID")

    def delete_book(self):
        book_id = self.delete_book_id.get()

        if book_id:
            delete_book(book_id)
            messagebox.showinfo("Success", "Book deleted successfully")
        else:
            messagebox.showwarning("Input Error", "Please provide a Book ID")


if __name__ == "__main__":
    app = BookManagerApp()
    app.mainloop()
 """




""" import tkinter as tk
from tkinter import ttk, messagebox
from crud import add_book, update_book, get_book, delete_book


class BookManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Manager")
        self.geometry("400x300")

        tab_control = ttk.Notebook(self)

        # Create Tabs
        self.create_add_book_tab(tab_control)
        self.create_update_book_tab(tab_control)
        self.create_get_book_tab(tab_control)
        self.create_delete_book_tab(tab_control)

        tab_control.pack(expand=1, fill='both')

    def create_add_book_tab(self, tab_control):
        add_book_tab = ttk.Frame(tab_control)
        tab_control.add(add_book_tab, text='Add Book')

        # Add Book Form
        ttk.Label(add_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.add_book_id = ttk.Entry(add_book_tab)
        self.add_book_id.grid(column=1, row=0)

        ttk.Label(add_book_tab, text="Title").grid(column=0, row=1, padx=10, pady=10)
        self.add_book_title = ttk.Entry(add_book_tab)
        self.add_book_title.grid(column=1, row=1)

        ttk.Label(add_book_tab, text="Author").grid(column=0, row=2, padx=10, pady=10)
        self.add_book_author = ttk.Entry(add_book_tab)
        self.add_book_author.grid(column=1, row=2)

        ttk.Label(add_book_tab, text="Year").grid(column=0, row=3, padx=10, pady=10)
        self.add_book_year = ttk.Entry(add_book_tab)
        self.add_book_year.grid(column=1, row=3)

        ttk.Button(add_book_tab, text="Add Book", command=self.add_book).grid(column=0, row=4, columnspan=2, pady=10)

    def create_update_book_tab(self, tab_control):
        update_book_tab = ttk.Frame(tab_control)
        tab_control.add(update_book_tab, text='Update Book')

        # Update Book Form
        ttk.Label(update_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.update_book_id = ttk.Entry(update_book_tab)
        self.update_book_id.grid(column=1, row=0)

        ttk.Label(update_book_tab, text="Title").grid(column=0, row=1, padx=10, pady=10)
        self.update_book_title = ttk.Entry(update_book_tab)
        self.update_book_title.grid(column=1, row=1)

        ttk.Label(update_book_tab, text="Author").grid(column=0, row=2, padx=10, pady=10)
        self.update_book_author = ttk.Entry(update_book_tab)
        self.update_book_author.grid(column=1, row=2)

        ttk.Label(update_book_tab, text="Year").grid(column=0, row=3, padx=10, pady=10)
        self.update_book_year = ttk.Entry(update_book_tab)
        self.update_book_year.grid(column=1, row=3)

        ttk.Button(update_book_tab, text="Update Book", command=self.update_book).grid(column=0, row=4, columnspan=2,
                                                                                       pady=10)

    def create_get_book_tab(self, tab_control):
        get_book_tab = ttk.Frame(tab_control)
        tab_control.add(get_book_tab, text='Get Book')

        # Get Book Form
        ttk.Label(get_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.get_book_id = ttk.Entry(get_book_tab)
        self.get_book_id.grid(column=1, row=0)

        ttk.Button(get_book_tab, text="Get Book", command=self.get_book).grid(column=0, row=1, columnspan=2, pady=10)

        self.get_book_result = ttk.Label(get_book_tab, text="")
        self.get_book_result.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    def create_delete_book_tab(self, tab_control):
        delete_book_tab = ttk.Frame(tab_control)
        tab_control.add(delete_book_tab, text='Delete Book')

        # Delete Book Form
        ttk.Label(delete_book_tab, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.delete_book_id = ttk.Entry(delete_book_tab)
        self.delete_book_id.grid(column=1, row=0)

        ttk.Button(delete_book_tab, text="Delete Book", command=self.delete_book).grid(column=0, row=1, columnspan=2,
                                                                                       pady=10)

    def add_book(self):
        book_id = self.add_book_id.get()
        title = self.add_book_title.get()
        author = self.add_book_author.get()
        year = self.add_book_year.get()

        if book_id and title and author and year:
            add_book(book_id, title, author, year)
            messagebox.showinfo("Success", "Book added successfully")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def update_book(self):
        book_id = self.update_book_id.get()
        title = self.update_book_title.get()
        author = self.update_book_author.get()
        year = self.update_book_year.get()

        if book_id:
            update_book(book_id, title, author, year)
            messagebox.showinfo("Success", "Book updated successfully")
        else:
            messagebox.showwarning("Input Error", "Please provide a Book ID")
`
    def get_book(self):
        book_id = self.get_book_id.get()

        if book_id:
            book = get_book(book_id)
            if book:
                book_info = f"Title: {book['title']}\nAuthor: {book['author']}\nYear: {book['year']}"
                self.get_book_result.config(text=book_info)
            else:
                messagebox.showinfo("Not Found", "Book not found")
        else:
            messagebox.showwarning("Input Error", "Please provide a Book ID")

    def delete_book(self):
        book_id = self.delete_book_id.get()

        if book_id:
            delete_book(book_id)
            messagebox.showinfo("Success", "Book deleted successfully")
        else:
            messagebox.showwarning("Input Error", "Please provide a Book ID")


if __name__ == "__main__":
    app = BookManagerApp()
    app.mainloop()
 """


"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import requests
from io import BytesIO
from crud import add_book, update_book, get_book, delete_book

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, bg_color, border_color, radius=25, **kwargs):
        super().__init__(parent, **kwargs)
        self.radius = radius
        self.bg_color = bg_color
        self.border_color = border_color

        self.bind("<Configure>", self._on_resize)
        self._draw_rounded_rect()

    def _on_resize(self, event):
        self._draw_rounded_rect()

    def _draw_rounded_rect(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        self.create_rounded_rect(0, 0, width, height, self.radius, self.bg_color, self.border_color)

    def create_rounded_rect(self, x1, y1, x2, y2, r, fill_color, outline_color):
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=fill_color, outline=outline_color)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill_color, outline=outline_color)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill_color, outline=outline_color)

class BookManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Manager")
        self.geometry("600x600")

        # Download the background image
        image_url = 'https://www.iee-ulb.eu/content/uploads/2018/01/alfons-morales-410757-480x650.jpg'
        response = requests.get(image_url)
        image_data = response.content
        self.background_image = Image.open(BytesIO(image_data))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Create a rounded frame with a transparent color
        self.rounded_frame = RoundedFrame(self, bg_color="bisque", border_color="darkred", radius=25)
        self.rounded_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.6)

        # Create a container frame inside the rounded frame
        self.container = ttk.Frame(self.rounded_frame, style="Transparent.TFrame")
        self.container.place(relwidth=1, relheight=1)

        # Style configuration
        style = ttk.Style(self)
        style.configure("TLabel", background="bisque", foreground="brown", font=("Arial", 14, "bold"))
        style.configure("TEntry", font=("Arial", 14))
        style.configure("TButton", background="darkred", color="bisque", foreground="brown", font=("Arial", 14, "bold"))

        # Style for Notebook and Tabs
        style.configure("TNotebook", background="bisque", foreground="brown")
        style.configure("TNotebook.Tab", background="bisque", foreground="brown", font=("Arial", 10, "bold"), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "beige")], foreground=[("selected", "darkred")])

        tab_control = ttk.Notebook(self.container)

        # Create Tabs
        self.create_add_book_tab(tab_control)
        self.create_update_book_tab(tab_control)
        self.create_get_book_tab(tab_control)
        self.create_delete_book_tab(tab_control)

        tab_control.pack(expand=1, fill='both')

    def create_transparent_frame(self, frame):
        # Create a transparent image
        transparent_image = self.background_image.copy()
        enhancer = ImageEnhance.Brightness(transparent_image)
        transparent_image = enhancer.enhance(0.5)  # Adjust the transparency level (0.5 for 50% transparency)
        transparent_photo = ImageTk.PhotoImage(transparent_image)

        # Create a label to hold the transparent image
        transparent_label = tk.Label(frame, image=transparent_photo)
        transparent_label.image = transparent_photo
        transparent_label.place(relwidth=1, relheight=1)

    def create_add_book_tab(self, tab_control):
        add_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(add_book_tab, text='Add Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(add_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        # Add Book Form
        self.create_form(inner_frame, self.add_book)

    def create_update_book_tab(self, tab_control):
        update_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(update_book_tab, text='Update Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(update_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        # Update Book Form
        self.create_form(inner_frame, self.update_book)

    def create_get_book_tab(self, tab_control):
        get_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(get_book_tab, text='Get Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(get_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        ttk.Label(inner_frame, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.get_book_id = ttk.Entry(inner_frame)
        self.get_book_id.grid(column=1, row=0, padx=10, pady=10)

        ttk.Button(inner_frame, text="Get Book", command=self.get_book).grid(column=0, row=1, columnspan=2, pady=10)

        self.get_book_result = ttk.Label(inner_frame, text="", style="TLabel")
        self.get_book_result.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    def create_delete_book_tab(self, tab_control):
        delete_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(delete_book_tab, text='Delete Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(delete_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        ttk.Label(inner_frame, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.delete_book_id = ttk.Entry(inner_frame)
        self.delete_book_id.grid(column=1, row=0, padx=10, pady=10)

        ttk.Button(inner_frame, text="Delete Book", command=self.delete_book).grid(column=0, row=1, columnspan=2, pady=10)

    def create_form(self, parent, command):
        ttk.Label(parent, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        entry_book_id = ttk.Entry(parent)
        entry_book_id.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(parent, text="Title").grid(column=0, row=1, padx=10, pady=10)
        entry_title = ttk.Entry(parent)
        entry_title.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(parent, text="Author").grid(column=0, row=2, padx=10, pady=10)
        entry_author = ttk.Entry(parent)
        entry_author.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(parent, text="Year").grid(column=0, row=3, padx=10, pady=10)
        entry_year = ttk.Entry(parent)
        entry_year.grid(column=1, row=3, padx=10, pady=10)

        ttk.Button(parent, text="Submit", command=lambda: command(entry_book_id.get(), entry_title.get(), entry_author.get(), entry_year.get())).grid(column=0, row=4, columnspan=2, pady=10)

    def add_book(self, book_id, title, author, year):
        result = add_book(book_id, title, author, year)
        messagebox.showinfo("Add Book", result)

    def update_book(self, book_id, title, author, year):
        result = update_book(book_id, title, author, year)
        messagebox.showinfo("Update Book", result)

    def get_book(self):
        book_id = self.get_book_id.get()
        result = get_book(book_id)
        self.get_book_result.config(text=result)

    def delete_book(self):
        book_id = self.delete_book_id.get()
        result = delete_book(book_id)
        messagebox.showinfo("Delete Book", result)

if __name__ == "__main__":
    app = BookManagerApp()
    app.mainloop()


"""
"""
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageEnhance
import requests
from io import BytesIO
from crud import add_book, update_book, get_book, delete_book

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, bg_color, border_color, radius=25, **kwargs):
        super().__init__(parent, **kwargs)
        self.radius = radius
        self.bg_color = bg_color
        self.border_color = border_color

        self.bind("<Configure>", self._on_resize)
        self._draw_rounded_rect()

    def _on_resize(self, event):
        self._draw_rounded_rect()

    def _draw_rounded_rect(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()
        self.create_rounded_rect(0, 0, width, height, self.radius, self.bg_color, self.border_color)

    def create_rounded_rect(self, x1, y1, x2, y2, r, fill_color, outline_color):
        self.create_arc(x1, y1, x1 + 2*r, y1 + 2*r, start=90, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x2 - 2*r, y1, x2, y1 + 2*r, start=0, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x1, y2 - 2*r, x1 + 2*r, y2, start=180, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x2 - 2*r, y2 - 2*r, x2, y2, start=270, extent=90, fill=fill_color, outline=outline_color)
        self.create_rectangle(x1 + r, y1, x2 - r, y2, fill=fill_color, outline=outline_color)
        self.create_rectangle(x1, y1 + r, x2, y2 - r, fill=fill_color, outline=outline_color)

class BookManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Manager")
        self.geometry("600x600")

        # Download the background image
        image_url = 'https://www.iee-ulb.eu/content/uploads/2018/01/alfons-morales-410757-480x650.jpg'
        response = requests.get(image_url)
        image_data = response.content
        self.background_image = Image.open(BytesIO(image_data))
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a label to hold the background image
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Create a rounded frame with a transparent color
        self.rounded_frame = RoundedFrame(self, bg_color="bisque", border_color="darkred", radius=25)
        self.rounded_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.7, relheight=0.6)

        # Create a container frame inside the rounded frame
        self.container = ttk.Frame(self.rounded_frame, style="Transparent.TFrame")
        self.container.place(relwidth=1, relheight=1)

        # Style configuration
        style = ttk.Style(self)
        style.configure("TLabel", background="bisque", foreground="brown", font=("Arial", 14, "bold"))
        style.configure("TEntry", font=("Arial", 14))
        style.configure("TButton", background="darkred", color="bisque", foreground="brown", font=("Arial", 14, "bold"))

        # Style for Notebook and Tabs
        style.configure("TNotebook", background="bisque", foreground="brown")
        style.configure("TNotebook.Tab", background="bisque", foreground="brown", font=("Arial", 10, "bold"), padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", "beige")], foreground=[("selected", "darkred")])

        tab_control = ttk.Notebook(self.container)

        # Create Tabs
        self.create_add_book_tab(tab_control)
        self.create_update_book_tab(tab_control)
        self.create_get_book_tab(tab_control)
        self.create_delete_book_tab(tab_control)

        tab_control.pack(expand=1, fill='both')

    def create_transparent_frame(self, frame):
        # Create a transparent image
        transparent_image = self.background_image.copy()
        enhancer = ImageEnhance.Brightness(transparent_image)
        transparent_image = enhancer.enhance(0.5)  # Adjust the transparency level (0.5 for 50% transparency)
        transparent_photo = ImageTk.PhotoImage(transparent_image)

        # Create a label to hold the transparent image
        transparent_label = tk.Label(frame, image=transparent_photo)
        transparent_label.image = transparent_photo
        transparent_label.place(relwidth=1, relheight=1)

    def create_add_book_tab(self, tab_control):
        add_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(add_book_tab, text='Add Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(add_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        # Add Book Form
        self.create_form(inner_frame, self.add_book)

    def create_update_book_tab(self, tab_control):
        update_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(update_book_tab, text='Update Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(update_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        # Update Book Form
        self.create_form(inner_frame, self.update_book)

    def create_get_book_tab(self, tab_control):
        get_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(get_book_tab, text='Get Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(get_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        ttk.Label(inner_frame, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.get_book_id = ttk.Entry(inner_frame)
        self.get_book_id.grid(column=1, row=0, padx=10, pady=10)

        ttk.Button(inner_frame, text="Get Book", command=self.get_book).grid(column=0, row=1, columnspan=2, pady=10)

        self.get_book_result = ttk.Label(inner_frame, text="", style="TLabel")
        self.get_book_result.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    def create_delete_book_tab(self, tab_control):
        delete_book_tab = ttk.Frame(tab_control, style="Transparent.TFrame")
        tab_control.add(delete_book_tab, text='Delete Book')

        # Center the form inside the tab
        inner_frame = ttk.Frame(delete_book_tab, style="Transparent.TFrame")
        inner_frame.pack(expand=True, padx=20, pady=20)

        ttk.Label(inner_frame, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        self.delete_book_id = ttk.Entry(inner_frame)
        self.delete_book_id.grid(column=1, row=0, padx=10, pady=10)

        ttk.Button(inner_frame, text="Delete Book", command=self.delete_book).grid(column=0, row=1, columnspan=2, pady=10)

    def create_form(self, parent, command):
        ttk.Label(parent, text="Book ID").grid(column=0, row=0, padx=10, pady=10)
        entry_book_id = ttk.Entry(parent)
        entry_book_id.grid(column=1, row=0, padx=10, pady=10)

        ttk.Label(parent, text="Title").grid(column=0, row=1, padx=10, pady=10)
        entry_title = ttk.Entry(parent)
        entry_title.grid(column=1, row=1, padx=10, pady=10)

        ttk.Label(parent, text="Author").grid(column=0, row=2, padx=10, pady=10)
        entry_author = ttk.Entry(parent)
        entry_author.grid(column=1, row=2, padx=10, pady=10)

        ttk.Label(parent, text="Year").grid(column=0, row=3, padx=10, pady=10)
        entry_year = ttk.Entry(parent)
        entry_year.grid(column=1, row=3, padx=10, pady=10)

        ttk.Button(parent, text="Submit", command=lambda: command(entry_book_id.get(), entry_title.get(), entry_author.get(), entry_year.get())).grid(column=0, row=4, columnspan=2, pady=10)

    def add_book(self, book_id, title, author, year):
        # if not all([book_id, title, author, year]):
        #     messagebox.showerror("Add Book", "Please fill in all fields.")
        #     return

        result = add_book(book_id, title, author, year)
        messagebox.showinfo("Add Book", "The book has been successfully added.")


    def update_book(self, book_id, title, author, year):
        result = update_book(book_id, title, author, year)
        messagebox.showinfo("Update Book", "The book has been successfully updated")

    def get_book(self):
        book_id = self.get_book_id.get()
        result = get_book(book_id)
        self.get_book_result.config(text=result)

    def delete_book(self):
        book_id = self.delete_book_id.get()
        result = delete_book(book_id)
        messagebox.showinfo("Delete Book", "The book has been deleted")

if __name__ == "__main__":
    app = BookManagerApp()
    app.mainloop()
"""
