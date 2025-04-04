from classes import Record, AddressBook
from typing import Callable, Dict, List
import pickle


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


# Function for handling errors during processing input commands (decorator)
def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Invalid command format."
        except IndexError:
            return "Invalid command format."
        except KeyError:
            return "That user is not found"

    return inner


@input_error  # handle if no command was typed
# Function for handling input commands from a terminal
def parse_input(user_input: str) -> tuple:
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
# Add new contact to contacts dictionary
def add_contact(args, book: AddressBook) -> str:
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


# Show all existing contacts in dictionary
def show_all(book: AddressBook) -> str:
    if not book:
        return "Contact list is empty"

    result = [f"{name}: {phone}" for name, phone in book.items()]
    return "\n".join(result)


@input_error
# Change existing contact in contacts dictionary
def change_contact(args: list, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return record


@input_error
# Show phone number fpr selected user
def phone_user(args: list, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError
    return record


@input_error
# add birthday for selected user
def add_birthday(args: list, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        return f"There is no contact with name {name}"
    record.add_birthday(birthday)
    return f"Birthday added."


@input_error
# show birthday for selected user
def show_birthday(args: list, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"There is no contact with name {name}"
    if record.birthday is None:
        return f"There is no birthday added for {name}"
    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
# show upcoming birthdays for next 7 days
def birthdays(book: AddressBook) -> str | list | List[Dict[str, str]]:
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        return "There is no upcoming birthdays"
    return birthdays


# Main function for handling input commands
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            save_data(book) 
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone_user(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))
            pass

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
