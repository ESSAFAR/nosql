from connections import mongo_client
from crud import add_book, update_book, get_book, delete_book

if __name__ == "__main__":
    # Adding a book
    add_book("2", "1984", "George Orwell", 1949)

    # Updating a book
    update_book("2", author="Orwell, George")

    # Retrieving a book
    book = get_book("2")
    print(book)

    # Deleting a book
    delete_book("2")

    # Closing connections
    mongo_client.close()
