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


contacts = {}


@input_error
def add_contact(name, phone):
    contacts[name] = phone
    return "Contact added successfully"


@input_error
def change_contact(name, phone):
    contacts[name] = phone
    return "Contact updated successfully"


@input_error
def get_phone(name):
    return contacts[name]


def show_all_contacts():
    if not contacts:
        return "No contacts found"
    output = ""
    for name, phone in contacts.items():
        output += f"{name}: {phone}\n"
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

