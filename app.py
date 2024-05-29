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
        self.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, fill=fill_color, outline=outline_color)
        self.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, fill=fill_color, outline=outline_color)
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
        style.configure("TNotebook.Tab", background="bisque", foreground="brown", font=("Arial", 10, "bold"),
                        padding=[10, 5])
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

        ttk.Button(inner_frame, text="Delete Book", command=self.delete_book).grid(column=0, row=1, columnspan=2,
                                                                                   pady=10)

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

        ttk.Button(parent, text="Submit",
                   command=lambda: command(entry_book_id, entry_title, entry_author, entry_year)).grid(column=0, row=4,
                                                                                                       columnspan=2,
                                                                                                       pady=10)

    def add_book(self, book_id, title, author, year):
        book_id = book_id.get()
        title = title.get()
        author = author.get()
        year = year.get()

        if book_id and title and author and year:
            add_book(book_id, title, author, year)
            messagebox.showinfo("Success", "Book added successfully")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def update_book(self, book_id, title, author, year):
        book_id = book_id.get()
        title = title.get()
        author = author.get()
        year = year.get()

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
 

