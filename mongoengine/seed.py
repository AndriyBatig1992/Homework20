import json
from models import Author, Quote

def import_data_from_json() -> None:
    """
    Import data from JSON files and store them in the database.
    Reads data about authors and quotes from JSON files and adds them to the database.
    Args:
        None
    Returns:
        None
    """
    with open('data/authors.json', encoding="utf-8") as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author = Author(**author_data)
            author.save()

    with open("data/quotes.json", encoding="utf-8") as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data["author"]
            author = Author.objects(fullname=author_name).first()
            quote_data["author"] = author
            quote = Quote(**quote_data)
            quote.save()

if __name__ == '__main__':
    import_data_from_json()
