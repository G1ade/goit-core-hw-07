from collections import UserDict

class Field:
    """Base class for record fields."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """Class for storing contact name. Required field."""
    pass

class Phone(Field):
    """Class for storing phone number with validation (10 digits)."""
    def __init__(self, value):
        if not (isinstance(value, str) and value.isdigit() and len(value) == 10):
             raise ValueError("Phone number must be 10 digits")
        super().__init__(value)

class Record:
    """
    Class for storing contact information including name and list of phones.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number: str):
        """Add phone to the record."""
        phone = Phone(phone_number)
        self.phones.append(phone)
    
    def remove_phone(self, phone_number: str):
        """Remove phone from the record."""
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return
        raise ValueError("Phone number not found")

    def edit_phone(self, old_phone: str, new_phone: str):
        """Edit phone number in the record."""
        for phone in self.phones:
            if phone.value == old_phone:
                # Validate new phone before replacing
                Phone(new_phone)  # This will raise ValueError if invalid
                phone.value = new_phone
                return
        raise ValueError("Old phone number not found")

    def find_phone(self, phone_number: str):
        """Find phone object by number."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    """
    Class for storing and managing records.
    Inherits from UserDict.
    """
    def add_record(self, record: Record):
        """Add record to address book."""
        self.data[record.name.value] = record

    def find(self, name: str):
        """Find record by name."""
        return self.data.get(name)
    
    def delete(self, name: str):
        """Delete record by name."""
        del self.data[name]

    def __str__(self):
        """Pretty print for AddressBook."""
        if not self.data:
            return "Address book is empty"
        
        lines = ["Contacts Book:", "-" * 40]
        for record in self.data.values():
            lines.append(str(record))
        lines.append("-" * 40)
        return "\n".join(lines)


book = AddressBook()

john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

book.add_record(john_record)

jane_record = Record("Jane")
jane_record.add_phone("9876543210")

book.add_record(jane_record)

found = book.find("John")
print(found)
print(book)