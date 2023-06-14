from collections import UserDict


class Field:
    def __init__(self):
        self.value = None

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, name):
        super().__init__()
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        super().__init__()
        self.value = phone


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def __str__(self):
        phones = ", ".join(str(phone) for phone in self.phones)
        return f"{self.name}: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter user name"
    return wrapper


address_book = AddressBook()


@input_error
def add_contact(name, phone):
    if name not in address_book.data:
        record = Record(name)
        address_book.add_record(record)
    else:
        record = address_book.data[name]
    record.add_phone(phone)
    return "Contact added successfully"


@input_error
def change_contact(name, phone):
    if name in address_book.data:
        record = address_book.data[name]
        record.add_phone(phone)
        return "Contact updated successfully"
    raise KeyError


@input_error
def get_phone(name):
    if name in address_book.data:
        record = address_book.data[name]
        return str(record)
    raise KeyError


def show_all_contacts():
    if not address_book.data:
        return "No contacts found"
    output = ""
    for record in address_book.values():
        output += str(record) + "\n"
    return output.strip()


def main():
    while True:
        command = input("Enter a command: ").lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone = command.split()
            print(add_contact(name, phone))
        elif command.startswith("change"):
            _, name, phone = command.split()
            print(change_contact(name, phone))
        elif command.startswith("phone"):
            _, name = command.split()
            print(get_phone(name))
        elif command == "show all":
            print(show_all_contacts())
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
