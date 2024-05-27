from connections import mongo_collection, mongo_client


# Function to add a book
def add_book(book_id, title, author, year):
    # MongoDB insertion
    book_doc = {
        "_id": book_id,
        "title": title,
        "author": author,
        "year": year
    }
    mongo_collection.insert_one(book_doc)

    # Neo4j insertion
    # with neo4j_driver.session() as session:
    #     session.run(
    #         "CREATE (b:Book {id: $id, title: $title, author: $author, year: $year})",
    #         id=book_id, title=title, author=author, year=year
    #     )


# Function to update a book
def update_book(book_id, title=None, author=None, year=None):
    # MongoDB update
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


# Function to retrieve a book
def get_book(book_id):
    # MongoDB retrieval
    book_doc = mongo_collection.find_one({"_id": book_id})
    if book_doc:
        return book_doc
    else:
        return None


# Function to delete a book
def delete_book(book_id):
    # MongoDB deletion
    mongo_collection.delete_one({"_id": book_id})

    # Neo4j deletion
    # with neo4j_driver.session() as session:
    #     session.run("MATCH (b:Book {id: $id}) DETACH DELETE b", id=book_id)
