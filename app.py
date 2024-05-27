import tkinter as tk
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
