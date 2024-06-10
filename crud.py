from datetime import datetime

from connections import mongo_collection, mongo_client


# Assume mongo_collection is for books. We need to define collections for members and loans.
members_collection = mongo_client['library']['members']
loans_collection = mongo_client['library']['loans']

# Gestion des livres

# Fonction pour ajouter un livre
def add_book(book_id, title, author, year):
    book_doc = {
        "_id": book_id,
        "title": title,
        "author": author,
        "year": year
    }
    mongo_collection.insert_one(book_doc)

    # Neo4j's insertion
    # with neo4j_driver.session() as session:
    #     session.run(
    #         "CREATE (b:Book {id: $id, title: $title, author: $author, year: $year})",
    #         id=book_id, title=title, author=author, year=year
    #     )

# Fonction pour mettre à jour un livre
def update_book(book_id, title=None, author=None, year=None):
    update_fields = {}
    if title:
        update_fields["title"] = title
    if author:
        update_fields["author"] = author
    if year:
        update_fields["year"] = year

    if update_fields:
        mongo_collection.update_one({"_id": book_id}, {"$set": update_fields})

    # Neo4j update
    # with neo4j_driver.session() as session:
    #     if title:
    #         session.run("MATCH (b:Book {id: $id}) SET b.title = $title", id=book_id, title=title)
    #     if author:
    #         session.run("MATCH (b:Book {id: $id}) SET b.author = $author", id=book_id, author=author)
    #     if year:
    #         session.run("MATCH (b:Book {id: $id}) SET b.year = $year", id=book_id, year=year)

# Fonction pour récupérer un livre
def get_book(book_id):
    book_doc = mongo_collection.find_one({"_id": book_id})
    return book_doc

# Fonction pour supprimer un livre
def delete_book(book_id):
    mongo_collection.delete_one({"_id": book_id})

    # Neo4j deletion
    # with neo4j_driver.session() as session:
    #     session.run("MATCH (b:Book {id: $id}) DETACH DELETE b", id=book_id)

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




