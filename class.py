from collections import UserDict
from datetime import datetime, timedelta, date
import re

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

class Birthday(Field):
    def __init__(self, value):
        just_dig_date = re.sub(r'\D', '', value)
        try:
            formatted_date = datetime.strptime(just_dig_date, '%d%m%Y').date()
            super().__init__(formatted_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """
    Class for storing contact information including name and list of phones.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone_number: str):
        """Add phone to the record."""
        phone = Phone(phone_number)
        self.phones.append(phone)

    def add_birthday(self, date: str):
        """Add birthday to the record."""
        self.birthday = Birthday(date)
    
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
        return f"Birthday: {self.birthday.value}, Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

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

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        def find_next_weekday(start_date, weekday):
            days_ahead = weekday - start_date.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return start_date + timedelta(days=days_ahead)

        def adjust_for_weekend(birthday):
            # Если суббота (5) или воскресенье (6) — переносим на понедельник (0)
            if birthday.weekday() >= 5:
                return find_next_weekday(birthday, 0)  # 0 = Monday
            return birthday

        for record in self.data.values():
            # Пропускаем записи без даты рождения
            if record.birthday is None:
                continue
                
            birthday_date = record.birthday.value  # Получаем date объект
            
            # День рождения в этом году
            birthday_this_year = birthday_date.replace(year=today.year)
            
            # Если день рождения уже прошёл в этом году — смотрим на следующий год
            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)
            
            # Проверяем, попадает ли в окно days
            days_until = (birthday_this_year - today).days
            
            if 0 <= days_until <= days:
                # Корректируем на выходные
                congratulation_date = adjust_for_weekend(birthday_this_year)
                
                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime('%d.%m.%Y')
                })
        
        return upcoming_birthdays


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