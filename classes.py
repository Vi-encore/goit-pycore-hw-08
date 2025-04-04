from collections import UserDict
from datetime import datetime, timedelta
from typing import Dict, List


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if not (len(value) == 10 and value.isnumeric()):
            raise ValueError(f"{value} should be numeric and 10 chars long")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}."

    def add_phone(self, phone: str) -> None:
        new_phone = Phone(phone)
        if new_phone.value in (p.value for p in self.phones):
            raise ValueError(f"Phone {phone} already exists.")
        self.phones.append(new_phone)

    def edit_phone(self, old_number: str, new_number: str) -> None:
        if Phone(new_number):
            for phone in self.phones:
                if phone.value == old_number:
                    phone.value = new_number
                else:
                    raise ValueError

    def remove_phone(self, phone_to_remove: str) -> None:
        self.phones = [phone for phone in self.phones if phone.value != phone_to_remove]

    def find_phone(self, phone_to_search: str) -> str | None:
        for phone in self.phones:
            if phone.value == phone_to_search:
                return phone_to_search
        return None

    def add_birthday(self, birthday: str) -> None:
        birthday = Birthday(birthday)
        if birthday.value == self.birthday:
            raise ValueError(f"Birthday has been added earlier.")
        self.birthday = birthday


class AddressBook(UserDict):

    def __init__(self) -> None:
        super().__init__()

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name, None)

    def delete(self, name: str) -> None:
        if name in self.data:
            self.data.pop(name)
        else:
            raise ValueError(f"Record {name} not found")

    def get_upcoming_birthdays(self) -> list | List[Dict[str, str]]:
        day_today = datetime.today().date()
        upcoming_birthdays = []

        for name, record in self.data.items():
            if record.birthday is not None:
                birthday_date = record.birthday.value
                birthday_this_year = birthday_date.replace(year=day_today.year)

                if birthday_this_year < day_today:
                    birthday_this_year = birthday_this_year.replace(
                        year=day_today.year + 1
                    )

                if 0 <= (birthday_this_year - day_today).days <= 7:
                    congrats_day = birthday_this_year

                    if birthday_this_year.weekday() in {5, 6}:
                        congrats_day += timedelta(days=(7 - congrats_day.weekday()))

                    upcoming_birthdays.append(
                        {
                            "name": name,
                            "birthday": birthday_date.strftime("%d.%m.%Y"),
                            "congratulation_date": congrats_day.strftime("%d.%m.%Y"),
                        }
                    )
        return upcoming_birthdays
