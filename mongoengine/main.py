from functools import wraps
from models import Quote, Author
import redis
import re

from redis_lru import RedisLRU

#Initialize the connection to Redis
client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def input_error(func):
    """
    Wrapper for handling input errors.
    Args:
        func (callable): The function to wrap.
    Returns:
        callable: A wrapper for the function with input error handling.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except IndexError as e:
            print('Not enough data.', str(e))
        except ValueError as e:
            print('Wrong value.', str(e))
        except KeyError as e:
            print('Wrong key.', str(e))
    return wrapper


def parser(user_input: str) -> tuple:
    """
    Parses user input and returns the function and arguments.
    Args:
        user_input (str): User input.
    Returns:
        tuple: A tuple containing the function and arguments.
    """
    if not user_input:
        raise IndexError("Nothing was entered ...")
    parts = user_input.split(":")
    func = parts[0]
    args = parts[1] if len(parts) > 1 else ''
    return func, args



def all(argument: str) -> None:
    """
    Prints all quotes of authors with tags.
    Args:
        argument (str): Not used.
    Returns:
        None
    """
    [print(f'{quote.author.fullname}: {", ".join(quote.tags)}') for quote in Quote.objects] or print('Not Found')



def name(author_name: str) -> None:
    """
    Prints quotes for the specified author.
    Args:
        author_name (str): Author's name.
    Returns:
        None
    """
    matching_authors = []
    author_query = {"fullname": {"$regex": f"^{author_name}", "$options": "i"}}
    authors = Author.objects(__raw__=author_query)

    for author in authors:
        matching_authors.append(author.fullname)
    if len(matching_authors) > 0 and len(author_name) >=2:
        [print(quote.quote) for quote in Quote.objects if quote.author.fullname in matching_authors]
    else:
        print('Not Found')


def tag(tag_to_find: str) -> None:
    """
    Prints quotes with the specified tag.
    Args:
        tag_to_find (str): Tag to search for.
    Returns:
        None
    """
    tag_regex = re.escape(tag_to_find)  # Екрануємо спеціальні символи
    tag_query = {"tags": {"$regex": f"^{tag_regex}", "$options": "i"}}
    quotes = Quote.objects(__raw__=tag_query)

    [print(quote.quote) for quote in quotes if len(tag_to_find) >= 2] or print(
        'Not Found')



def tags(tags_to_find: str) -> None:
    """
    Prints quotes with the specified tags.
    Args:
        tags_to_find (str): Tags to search for (comma-separated).
    Returns:
        None
    """
    tags = tags_to_find.split(',')
    [print(quote["quote"]) for quote in Quote.objects if any(tag in quote["tags"] for tag in tags)] or print(
        'Not Found')


def exit(argument: str) -> str:
    """
    Exits the program.
    Args:
        argument (str): Not used.
    Returns:
        str: A message indicating program termination.
    """
    return 'Goodbye!'


@input_error
def main_cycle() -> bool:
    """
    Main program loop.
    Returns:
        bool: True if the program has completed.
    """
    user_input = input('>>> ').strip().lower()
    func_name, argument = parser(user_input)
    func = globals().get(func_name)
    if func:
        result = func(argument)
        if result:
            return result.endswith('Goodbye!')
        else:
            return False
    else:
        print(f"Function '{func_name}' not found.")
        return False


def main() -> None:
    """
    Main program function.
    """
    while True:
        if main_cycle():
            break


if __name__ == "__main__":
    try:
        client.ping()
        print("Connected to Redis")
    except redis.ConnectionError:
        print("Failed to connect to Redis")
    main()


