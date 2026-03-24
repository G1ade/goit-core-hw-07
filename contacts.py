from pathlib import Path
from collections import UserDict
from datetime import datetime, timedelta, date
import pickle



class Field:
    """Base class for record fields."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for storing contact name."""
    pass

class Phone(Field):
    """Class for storing phone number with validation (10 digits)."""
    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
             raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Birthday(Field):
    """Class for storing birthday with validation."""
    def __init__(self, value):
        try:
            if datetime.strptime(value, '%d.%m.%Y').date():
                super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Class for storing contact information including name and list of phones."""
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str):
        """Add phone to the record."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def add_birthday(self, birthday_date: str):
        """Add birthday to the record."""
        self.birthday = Birthday(birthday_date)
    
    def remove_phone(self, phone_number: str):
        """Remove phone from the record."""
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone: str, new_phone: str):
        """Edit phone number in the record."""
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Old phone number not found")

    def find_phone(self, phone_number: str):
        """Find phone object by number."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones) if self.phones else "No phones"
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday_str}"


class AddressBook(UserDict):
    """Class for storing and managing records."""
    
    def add_record(self, record: Record):
        """Add record to address book."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Find record by name."""
        return self.data.get(name)
    
    def delete(self, name: str):
        """Delete record by name."""
        if name not in self.data:
            raise KeyError(f"Contact '{name}' not found")
        del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        """
        We'll return a contact list showing the days when people have seizures.
        Go forward 7 days, including the exact day.
        """
        upcoming_birthdays = []
        today = date.today()

        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        def adjust_for_weekend(birthday):
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)
            return birthday

        for record in self.data.values():
            if record.birthday is None:
                continue
                
            birthday_date = datetime.strptime(record.birthday.value, '%d.%m.%Y').date()
            birthday_this_year = birthday_date.replace(year=today.year)
            
            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)
            
            days_until = (birthday_this_year - today).days
            
            if 0 <= days_until <= days:
                congratulation_date = adjust_for_weekend(birthday_this_year)
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "birthday": congratulation_date.strftime('%d.%m.%Y')
                })
        
        return upcoming_birthdays

    def __str__(self):
        if not self.data:
            return "Address book is empty"
        lines = ["Contacts Book:", "-" * 50]
        for record in self.data.values():
            lines.append(str(record))
        lines.append("-" * 50)
        return "\n".join(lines)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Missing contact information, please use the 'help' command if you have any difficulties."
        except KeyError as e:
            return str(e)
        except AttributeError:
            return "The contact is missing or the name is entered incorrectly"
    return inner


def parse_input(user_input: str) -> tuple:
    """Parse user input into command and arguments."""
    parts = user_input.split()
    cmd = parts[0].strip().lower() if parts else ""
    args = parts[1:]
    return cmd, args


def save_data(book: AddressBook, path: Path):
    """Save address book to file using pickle."""
    with open(path, 'wb') as f:
        pickle.dump(book, f)


def load_data(path: Path) -> AddressBook:
    """Load address book from file."""
    if path.exists():
        with open(path, 'rb') as f:
            return pickle.load(f)
    return AddressBook()


@input_error
def add_contact(args: list, book: AddressBook) -> str:
    """Add new contact or phone to existing contact."""
       
    name, phone = args[0], args[1]
    record = book.find(name)
    
    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return f"Contact {name} added with phone {phone}."
    else:
        record.add_phone(phone)
        return f"Phone {phone} added to contact {name}."


@input_error
def add_birthday(args: list, book: AddressBook) -> str:
    """Add birthday to contact."""

    name, birthday = args[0], args[1]
    record = book.find(name)   
    record.add_birthday(birthday)
    return f"Birthday {birthday} added to contact {name}."


@input_error
def show_birthday(args: list, book: AddressBook) -> str:
    """Show birthday of contact."""
        
    name = args[0]
    record = book.find(name)
        
    if record.birthday is None:
        return f"Contact {name} has no birthday set."
    
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args: list, book: AddressBook) -> str:
    """Show upcoming birthdays for next week."""

    days = int(args[0]) if args else 7
    upcoming = book.get_upcoming_birthdays(days)
    
    if not upcoming:
        return f"No upcoming birthdays in the next {days} days."
    
    lines = [f"Upcoming birthdays (next {days} days):", "-" * 40]
    for item in upcoming:
        lines.append(f"{item['name']}: {item['birthday']}")
    return "\n".join(lines)


@input_error
def change_contact(args: list, book: AddressBook) -> str:
    """Change phone number for contact."""
    
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)
    
    record.edit_phone(old_phone, new_phone)
    return f"Phone changed from {old_phone} to {new_phone} for {name}."


@input_error
def phone_username(args: list, book: AddressBook) -> str:
    """Show all phones for contact."""
    
    name = args[0]
    record = book.find(name)
        
    phones = '; '.join(p.value for p in record.phones)
    return f"{name}: {phones}"


@input_error
def remove_phone(args: list, book: AddressBook) -> str:
    """Remove phone from contact."""

    name, phone = args[0], args[1]
    record = book.find(name)  
    record.remove_phone(phone)
    return f"Phone {phone} removed from {name}."


@input_error
def delete_contact(args: list, book: AddressBook) -> str:
    """Delete contact from address book."""
    
    name = args[0]
    book.delete(name)
    return f"Contact {name} deleted."


def all_contacts(book: AddressBook) -> str:
    """Show all contacts."""

    return str(book) if book.data else "Address book is empty."


def show_help() -> str:
    """Show available commands."""

    return """Available commands:
  hello                             - Greeting
  add [name] [phone]                - Add contact or phone
  change [name] [old] [new]         - Change phone
  phone [name]                      - Show contact phones
  remove [name] [phone]             - Remove phone from contact
  delete [name]                     - Delete contact
  add-birthday [name] [DD.MM.YYYY]  - Add birthday
  show-birthday [name]              - Show birthday
  birthdays [days]                  - Upcoming birthdays (default 7 days)
  all                               - Show all contacts
  save                              - Save to file
  close/exit                        - Exit
"""