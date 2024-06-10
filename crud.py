from datetime import datetime

from neo4j.exceptions import ServiceUnavailable

from connections import mongo_collection, mongo_client, neo4j_driver


# Assume mongo_collection is for books. We need to define collections for members and loans.
members_collection = mongo_client['library']['members']
loans_collection = mongo_client['library']['loans']

# Gestion des livres

# Fonction pour ajouter un livre
def add_book(book_id, title, authors, year):
    book_doc = {
        "_id": book_id,
        "title": title,
        "authors": authors,
        "year": year
    }
    # Insert into MongoDB
    mongo_collection.insert_one(book_doc)

    # Insert into Neo4j
    with neo4j_driver.session() as session:
        try:
            session.run(
                """
                CREATE (b:Book {id: $book_id, title: $title, year: $year})
                WITH b
                UNWIND $authors AS author
                MERGE (a:Author {name: author})
                MERGE (a)-[:AUTHORED]->(b)
                """,
                book_id=book_id, title=title, year=year, authors=authors
            )
        except ServiceUnavailable as e:
            print(f"Neo4j service is unavailable: {e}")


# Fonction pour mettre à jour un livre
def update_book(book_id, title=None, authors=None, year=None):
    update_fields = {}
    if title:
        update_fields["title"] = title
    if year:
        update_fields["year"] = year

    if update_fields:
        mongo_collection.update_one({"_id": book_id}, {"$set": update_fields})

    # Neo4j update
    with neo4j_driver.session() as session:
        if authors:
            session.run(
                """
                MATCH (b:Book {id: $book_id})<-[r:AUTHORED]-(a:Author)
                DELETE r
                WITH b
                UNWIND $authors AS author
                MERGE (a:Author {name: author})
                MERGE (a)-[:AUTHORED]->(b)
                """,
                book_id=book_id, authors=authors
            )

# Fonction pour récupérer un livre
def get_book(book_id):
    book_doc = mongo_collection.find_one({"_id": book_id})
    return book_doc

# Fonction pour supprimer un livre
def delete_book(book_id):
    mongo_collection.delete_one({"_id": book_id})
    # Neo4j deletion
    with neo4j_driver.session() as session:
        session.run("MATCH (b:Book {id: $id}) DETACH DELETE b", id=book_id)

# Gestion des adhérents
# Fonction pour ajouter un adhérent
def add_member(member_id, name, email, membership_date):
    member_doc = {
        "_id": member_id,
        "name": name,
        "email": email,
        "membership_date": membership_date
    }
    members_collection.insert_one(member_doc)

# Fonction pour mettre à jour un adhérent
def update_member(member_id, name=None, email=None, membership_date=None):
    update_fields = {}
    if name:
        update_fields["name"] = name
    if email:
        update_fields["email"] = email
    if membership_date:
        update_fields["membership_date"] = membership_date

    if update_fields:
        members_collection.update_one({"_id": member_id}, {"$set": update_fields})

# Fonction pour récupérer un adhérent
def get_member(member_id):
    member_doc = members_collection.find_one({"_id": member_id})
    return member_doc

# Fonction pour supprimer un adhérent
def delete_member(member_id):
    members_collection.delete_one({"_id": member_id})

# Gestion des prêts

# Fonction pour enregistrer un prêt
def add_loan(loan_id, book_id, member_id, loan_date, return_date=None):
    loan_doc = {
        "_id": loan_id,
        "book_id": book_id,
        "member_id": member_id,
        "loan_date": loan_date,
        "return_date": return_date
    }
    loans_collection.insert_one(loan_doc)

# Fonction pour mettre à jour un prêt
def update_loan(loan_id, return_date=None):
    update_fields = {}
    if return_date:
        update_fields["return_date"] = return_date

    if update_fields:
        loans_collection.update_one({"_id": loan_id}, {"$set": update_fields})

# Fonction pour récupérer un prêt
def get_loan(loan_id):
    loan_doc = loans_collection.find_one({"_id": loan_id})
    return loan_doc

# Fonction pour supprimer un prêt
def delete_loan(loan_id):
    loans_collection.delete_one({"_id": loan_id})

# Fonction pour récupérer tous les livres depuis Neo4j
def get_all_books_neo4j():
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (b:Book)-[:AUTHORED]-(a:Author)
            RETURN b.id AS id, b.title AS title, b.year AS year, collect(a) AS authors;
            """
        )
        books = []
        for record in result:
            books.append({
                "id": record["id"],
                "title": record["title"],
                "authors": record["authors"],
                "year": record["year"]
            })
        return books

# Fonction pour récupérer tous les livres depuis MongoDB
def get_all_books_mongo():
    books = mongo_collection.find()
    return list(books)


# Fonction pour récupérer tous les livres depuis Neo4j
def get_all_books_neo4j2():
    with neo4j_driver.session() as session:
        result = session.run(
            """
            MATCH (b:Book)-[:AUTHORED]->(a:Author)
            RETURN b.id AS id, b.title AS title, COLLECT(a.name) AS authors, b.year AS year
            """
        )
        books = []
        for record in result:
            books.append({
                "id": record["id"],
                "title": record["title"],
                "authors": record["authors"],
                "year": record["year"]
            })
        return books
