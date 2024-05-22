from connections import mongo_client, neo4j_driver
from crud import add_book, update_book, get_book, delete_book

if __name__ == "__main__":
    # Adding a book
    add_book("1", "1984", "George Orwell", 1949)

    # Updating a book
    update_book("1", author="Orwell, George")

    # Retrieving a book
    book = get_book("1")
    print(book)

    # Deleting a book
    delete_book("1")

    # Closing connections
    mongo_client.close()
    neo4j_driver.close()
