from datetime import datetime

from crud import add_book, update_book, get_book, delete_book, add_member, get_member, delete_member, add_loan, \
    update_loan, get_loan, delete_loan, get_all_books_neo4j, get_all_books_mongo

# Test the functions

add_book(
    book_id=1,
    title="Sample Book",
    authors=["Author 1", "Author 2"],
    year=2022
)

# Update the book
update_book(book_id=1, title="Updated Sample Book", authors=["Author 3", "Author 4"], year=2023)

# Retrieve the book
book = get_book(book_id=1)
print("Retrieved Book:", book)


# Retrieve all books
books_neo4j = get_all_books_neo4j()
print("Books from Neo4j:", books_neo4j)

books_mongo = get_all_books_mongo()
print("Books from Mongo:", books_mongo)

# Delete the book
delete_book(book_id=1)

# Add a member
add_member(member_id=11, name="Essafar", email="anwar@mail.com", membership_date=datetime.now())

# Retrieve the member
member = get_member(member_id=11)
print("Retrieved Member:", member)

# Delete the member
delete_member(member_id=11)

# Add a loan
add_loan(loan_id=12, book_id=13, member_id=11, loan_date=datetime.now())

# # Update the loan
update_loan(loan_id=12, return_date=datetime.now())

# Retrieve the loan
loan = get_loan(loan_id=12)
print("Retrieved Loan:", loan)


#Delete the loan
delete_loan(loan_id=12)



# Retrieve all books from MongoDB
books_mongo = get_all_books_mongo()
print("Books from MongoDB:", books_mongo)


