from functools import wraps


def input_error(func):
    """
    A decorator that wraps a function and catches common exceptions,
    returning a string message for each exception type.

    Args:
        * func (callable): The function to be decorated.

    Returns:
        * callable: The wrapped function which handles the following exceptions:
            - KeyError: Raised when a dictionary key is not found.
            - ValueError: Raised when a function receives an argument of the correct
                type but an inappropriate value.
            - IndexError: Raised when a sequence subscript is out of range.
            - Exception: Catches any other unexpected exceptions.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"ValueError: {str(e)}"
        except KeyError as e:
            return f"KeyError: {str(e)}"
        except IndexError as e:
            return f"IndexError: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    return inner


@input_error
def parse_input(user_input: str):
    """
    A function that receives the row, breaks it into words,
    the first word leads to lower case and removes extra characters.

    Args:
        * user_input (str): The user input.
    Returns:
        * cmd (str): the first word of the string without spaces in lower case
        * args (list): the rest of the words in the string
    """
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args: list, contacts: dict):
    """
    A function that adds a new contact to the contacts dictionary.

    Args:
        * args (list): the list of words after the command
        * contacts (dict): the dictionary of contacts
    Returns:
    * str: "Contact added."
    """
    if len(args) < 2:
        raise ValueError("Name or number are missing. usage: add <name> <number>")
    name, phone = args
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args: list, contacts: dict):
    """
    A function that changes the phone number of an existing contact.

    Args:
        * args (list): the list of words after the command
        * contacts (dict): the dictionary of contacts

    Returns:
        * str: "Contact changed." if success and "No such name '{name}' was found" if
            failed.
    """
    if len(args) < 2:
        raise ValueError("Name or number are missing. usage: change <name> <number>")
    name, phone = args
    if name not in contacts:
        raise KeyError(f"No such name '{name}' was found")
    contacts[name] = phone
    return "Contact changed."


@input_error
def show_phone(args: list, contacts: dict):
    """
    A function that shows the phone number of a contact.
    
    Args:
        * args (list): the list of words after the command
        * contacts (dict): the dictionary of contacts
    
    Returns:
        * str: the phone number if found and "Contact not found." if failed.
    """
    if len(args) == 0:
        raise IndexError("Name is missing. usage: phone <name>")
    name = args[0]
    if name not in contacts:
        raise KeyError(f"Contact {name} not found.")
    return contacts[name]


@input_error
def list_all(contacts: dict):
    """
    A function that lists all contacts and their phone numbers.
    
    Args:
        * contacts (dict): the dictionary of contacts
    
    Returns:
        * str: the list of contacts and their phone numbers.
    """
    all_contacts = "\n".join([
        f"{name}: {phone}" for name, phone in contacts.items()
    ])
    if not all_contacts:
        raise IndexError("The phone list is empty.")
    return all_contacts


def main():
    """
        This is a simple phonebook application.
    """
    contacts = {}
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(list_all(contacts))
        else:
            print("Invalid command. ",
                "Acceptable commands: <add | change | phone | all | close | exit>")


if __name__ == "__main__":
    main()
