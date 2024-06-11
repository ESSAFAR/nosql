from datetime import datetime, timedelta
from crud import add_book, update_book, get_book, delete_book, add_member, get_member, delete_member, add_loan, update_loan, get_loan, delete_loan, get_all_books_neo4j, get_all_books_mongo

# Add books
books = [
    {"book_id": 1, "title": "To Kill a Mockingbird", "authors": ["Harper Lee"], "year": 1960},
    {"book_id": 2, "title": "1984", "authors": ["George Orwell"], "year": 1949},
    {"book_id": 3, "title": "Pride and Prejudice", "authors": ["Jane Austen"], "year": 1813},
    {"book_id": 4, "title": "The Great Gatsby", "authors": ["F. Scott Fitzgerald"], "year": 1925},
    {"book_id": 5, "title": "Moby Dick", "authors": ["Herman Melville"], "year": 1851},
]

for book in books:
    add_book(book_id=book["book_id"], title=book["title"], authors=book["authors"], year=book["year"])

# Add members
members = [
    {"member_id": 101, "name": "John Doe", "email": "johndoe@example.com", "membership_date": datetime(2020, 1, 1)},
    {"member_id": 102, "name": "Jane Smith", "email": "janesmith@example.com", "membership_date": datetime(2021, 1, 1)},
    {"member_id": 103, "name": "Emily Johnson", "email": "emilyjohnson@example.com", "membership_date": datetime(2022, 1, 1)},
    {"member_id": 104, "name": "Michael Brown", "email": "michaelbrown@example.com", "membership_date": datetime(2023, 1, 1)},
    {"member_id": 105, "name": "Sarah Davis", "email": "sarahdavis@example.com", "membership_date": datetime(2024, 1, 1)},
]

for member in members:
    add_member(member_id=member["member_id"], name=member["name"], email=member["email"], membership_date=member["membership_date"])

# Add loans
loans = [
    {"loan_id": 1, "book_id": 1, "member_id": 101, "loan_date": datetime(2023, 1, 15), "return_date": datetime(2023, 2, 15)},
    {"loan_id": 12, "book_id": 1, "member_id": 101, "loan_date": datetime(2023, 1, 15), "return_date": datetime(2022, 2, 15)},
    {"loan_id": 13, "book_id": 1, "member_id": 101, "loan_date": datetime(2022, 1, 15), "return_date": datetime(2021, 2, 15)},
    {"loan_id": 14, "book_id": 1, "member_id": 101, "loan_date": datetime(2022, 1, 15), "return_date": datetime(2020, 2, 15)},
    {"loan_id": 15, "book_id": 1, "member_id": 101, "loan_date": datetime(2022, 1, 15), "return_date": datetime(2023, 2, 15)},
    {"loan_id": 16, "book_id": 1, "member_id": 101, "loan_date": datetime(2022, 1, 15), "return_date": datetime(2023, 2, 15)},
    {"loan_id": 17, "book_id": 1, "member_id": 101, "loan_date": datetime(2022, 1, 15), "return_date": datetime(2023, 2, 15)},
    {"loan_id": 18, "book_id": 1, "member_id": 101, "loan_date": datetime(2021, 1, 15), "return_date": datetime(2023, 2, 15)},
    {"loan_id": 19, "book_id": 1, "member_id": 101, "loan_date": datetime(2021, 1, 15), "return_date": datetime(2023, 2, 15)},
    {"loan_id": 2, "book_id": 2, "member_id": 102, "loan_date": datetime(2021, 3, 20), "return_date": datetime(2023, 4, 20)},
    {"loan_id": 3, "book_id": 3, "member_id": 103, "loan_date": datetime(2021, 5, 25), "return_date": datetime(2023, 6, 25)},
    {"loan_id": 4, "book_id": 4, "member_id": 104, "loan_date": datetime(2021, 7, 30), "return_date": datetime(2023, 8, 30)},
    {"loan_id": 5, "book_id": 5, "member_id": 105, "loan_date": datetime(2020, 9, 5), "return_date": datetime(2023, 10, 5)},
    {"loan_id": 6, "book_id": 1, "member_id": 102, "loan_date": datetime(2020, 11, 10), "return_date": datetime(2023, 12, 10)},
    {"loan_id": 7, "book_id": 2, "member_id": 103, "loan_date": datetime(2020, 1, 15), "return_date": datetime(2024, 2, 15)},
    {"loan_id": 8, "book_id": 3, "member_id": 104, "loan_date": datetime(2020, 3, 20), "return_date": datetime(2024, 4, 20)},
    {"loan_id": 9, "book_id": 4, "member_id": 105, "loan_date": datetime(2019, 5, 25), "return_date": datetime(2024, 6, 25)},
    {"loan_id": 10, "book_id": 5, "member_id": 101, "loan_date": datetime(2019, 7, 30), "return_date": datetime(2024, 8, 30)},
]

for loan in loans:
    add_loan(loan_id=loan["loan_id"], book_id=loan["book_id"], member_id=loan["member_id"], loan_date=loan["loan_date"], return_date=loan["return_date"])

# Optionally, we can retrieve and print out the added data to verify it
print("Books from MongoDB:")
books_mongo = get_all_books_mongo()
print(books_mongo)

print("Members:")
for member in members:
    print(get_member(member["member_id"]))

print("Loans:")
for loan in loans:
    print(get_loan(loan["loan_id"]))
