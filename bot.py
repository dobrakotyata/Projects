import pickle
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    def __init__(self):
        self._value = None

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __init__(self, name):
        super().__init__()
        self.value = name


class Phone(Field):
    def __init__(self, phone):
        super().__init__()
        self.value = phone

    @Field.value.setter
    def value(self, new_value):
        if not self.is_valid_phone(new_value):
            raise ValueError("Invalid phone number")
        self._value = new_value

    @staticmethod
    def is_valid_phone(phone):
        # Implement phone number validation logic here
        return True


class Birthday(Field):
    def __init__(self, birthday):
        super().__init__()
        self.value = birthday

    @Field.value.setter
    def value(self, new_value):
        if not self.is_valid_birthday(new_value):
            raise ValueError("Invalid birthday")
        self._value = new_value

    @staticmethod
    def is_valid_birthday(birthday):
        # Implement birthday validation logic here
        return True


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        next_birthday = datetime(today.year, self.birthday.value.month, self.birthday.value.day).date()
        if next_birthday < today:
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
        return (next_birthday - today).days

    def __str__(self):
        phones = ", ".join(str(phone) for phone in self.phones)
        return f"{self.name}: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def __iter__(self):
        return iter(self.data.values())

    def __next__(self):
        raise StopIteration

    def save(self, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)

    def load(self, file_path):
        with open(file_path, 'rb') as file:
            self.data = pickle.load(file)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter user name"

    return wrapper


address_book = AddressBook()


@input_error
def add_contact(name, phone, birthday=None):
    if name not in address_book.data:
        record = Record(name, birthday)
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
    for record in address_book:
        output += str(record) + "\n"
    return output.strip()


def search_contacts(query):
    matching_contacts = []
    for record in address_book:
        if query in record.name.value or any(query in phone.value for phone in record.phones):
            matching_contacts.append(str(record))
    if matching_contacts:
        return "\n".join(matching_contacts)
    else:
        return "No matching contacts found"


def main():
    while True:
        command = input("Enter a command: ").lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            _, name, phone, *birthday = command.split()
            birthday = datetime.strptime(' '.join(birthday), '%d-%m-%Y').date() if birthday else None
            print(add_contact(name, phone, birthday))
        elif command.startswith("change"):
            _, name, phone = command.split()
            print(change_contact(name, phone))
        elif command.startswith("phone"):
            _, name = command.split()
            print(get_phone(name))
        elif command == "show all":
            print(show_all_contacts())
        elif command.startswith("search"):
            _, query = command.split()
            print(search_contacts(query))
        elif command.startswith("save"):
            _, file_path = command.split()
            address_book.save(file_path)
            print(f"Address book saved to {file_path}")
        elif command.startswith("load"):
            _, file_path = command.split()
            address_book.load(file_path)
            print(f"Address book loaded from {file_path}")
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()

