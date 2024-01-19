from abc import ABC, abstractmethod
import re
from datetime import datetime, date
from collections import UserDict
from pathlib import Path
import os
import pickle

WORK_DIR = Path(os.path.abspath(__file__)).parent 
BOOK_NAME = str(WORK_DIR) + '//my_book.bin' 


class ValidPhoneException(Exception):
    pass


class ValidNameException(Exception):
    pass


class ContactFormatterInfo(ABC):
    @abstractmethod
    def value_of(self):
        raise NotImplementedError


class Name(ContactFormatterInfo):
    def __init__(self, name: str):
        if len(name) < 2:
            raise ValidNameException('Invalid name! Please enter a name with at least 2 symbols')
        self.name = name

    def value_of(self):
        return self.name


class Phone(ContactFormatterInfo):
    def __init__(self, phone: str):
        self.phone = phone

    def value_of(self):
        return self.validate_phone()

    def validate_phone(self):
        phone_number = (self.phone.strip()
                        .replace('(', '')
                        .replace(')', '')
                        .replace('-', '')
                        .replace(' ', '')
                        .replace('+', ''))
        if len(phone_number) == 13:
            if re.match('^\\+38\d{10}$', phone_number):
                return f'{phone_number}'
        elif len(phone_number) == 12:
            if re.match('^\d{12}$', phone_number):
                return '+' + phone_number
        elif len(phone_number) == 10:
            if re.match('^\d{10}$', phone_number):
                return '+38' + phone_number
        else:
            raise ValidPhoneException('Invalid phone number! Please enter correct number phone!')


class Address(ContactFormatterInfo):
    def __init__(self, country: str, city: str, street: str, house: int):
        self.country = country
        self.city = city
        self.street = street
        self.house = house

    def value_of(self):
        return f'{self.country}, {self.city}, {self.street}, {self.house}'


class Birthday(ContactFormatterInfo):
    def __init__(self, birthday):
        self.birthday = birthday

    def value_of(self):
        return self.check_birthday()

    def check_birthday(self):
        if self.birthday == None:
            return None

        try:
            datetime.strptime(self.birthday, '%Y-%m-%d')
            return self.birthday

        except ValueError:
            return None


class Email(ContactFormatterInfo):
    def __init__(self, email):
        self.email = email

    def value_of(self):
        return self.validate_email()

    def validate_email(self):
        if re.match(r'^[\w]{1,}([\w.+-]{0,1}[\w]{1,}){0,}@[\w]{1,}([\w-]{0,1}[\w]{1,}){0,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$',
                self.email):
            return self.email
        else:
            raise ValueError('Invalid email address! Please enter correct email')
        
        
class Record:
    def __init__(self, name: ContactFormatterInfo, phone: ContactFormatterInfo, address: ContactFormatterInfo,
                birthday: ContactFormatterInfo):
        self.name = name
        self.phone = phone
        self.address = address
        self.birthday = birthday
        self.emails = []
        self.phones = []

    def __str__(self):
        # return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, e-mails: {'; '.join(p.value for p in self.emails)}, address: {self.home}"
        return f"Contact name: {self.name}, phones: {'; '.join(p for p in self.phones)}, e-mails: {'; '.join(p for p in self.emails)}, address: {self.address}, birthday: {self.birthday}"

    # def get_phone_number(self):
    #     return f'{self.name.value_of()} : {self.phone.value_of()}'
    #
    # def get_address(self):
    #     return f'{self.name.value_of()} : {self.address.value_of()}'
    #
    # def get_birthday(self):
    #     return f'{self.name.value_of()} : {self.birthday.value_of()}'

    # def __str__(self) -> str:
    #     return f'Contact name: {self.name}, phones: {";".join(str(p) for p in self.phones)}'

    def add_phone(self, phone: Phone):
        new_phone = phone.value_of()
        if new_phone not in self.phones:
            self.phones.append(new_phone)

    def remove_phone(self, phone):
        for ph in self.phones:
            if ph == phone:
                self.phones.remove(phone)

    def find_phone(self, phone):
        for phone_number in self.phones:
            if phone_number == phone:
                return phone_number
        return None

    #def __str__(self):
        #return f"Contact name: {self.name}, phones: {'; '.join(p for p in self.phones)}"

    def edit_phone(self, old_phone, new_phone):
        old_phone = Phone.value_of(old_phone)
        for phone_number in self.phones:
            if old_phone == phone_number:
                self.phones.remove(phone_number)
                self.phones.append(Phone.value_of(new_phone))
                return
        raise ValueError

    def show_contact(self):
        return {"name": self.name,
                "phone": [self.phone for self.phone in self.phones] if self.phones else [],
                "birthday": self.birthday if self.birthday else self.birthday}

    def find_phone(self, phone_number: str):
        phone_number = Phone.value_of(phone_number)

        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_email(self, email: str):
        tmp = Email.value_of(self.email)
        if tmp:
            self.emails.append(Email(email))
        else:
            print(f'E-mail {email} is not valid.')

    def find_email(self, email: str):
        for email in self.emails:
            if email.value == email:
                return email
        return None

    def edit_email(self, old_email, new_email):
        email_obj = self.find_email(old_email)

        if email_obj:
            if Email.validate_email(new_email):
                email_obj.value = new_email
            return True
        else:
            print(f'E-mail {old_email} not found.')
            return False

    def days_to_birthday(self):
        if self.birthday is None:
            return 'No contact with this birthday'
        else:
            today = date.today()
            next_birthday = date(today.year, self.birthday.month, self.birthday.day)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_to_birthday = (next_birthday - today).days
            return days_to_birthday

class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    
    def find(self, name: str):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    
    def find_record(self, part: str):
        result = {}

        for item, record in self.items():
            # пошук в phones
            for p in record.phones:
                if part in str(p):
                    result[item] = self.data[item]

            # пошук в name
            if part.lower() in item.lower():
                result[item] = self.data[item]
            
            # пошук в emails
            for e in record.emails:
                if part in str(e):
                    result[item] = self.data[item]

        return result
    
    # сериалізація адресної книги та запису її у файл
    def dump(self):
         with open(BOOK_NAME, 'wb') as file:   #'my_book.bin'
            if len(self.data) > 0:
                pickle.dump(self, file)
                return True


    def load(self):
        with open(BOOK_NAME, 'rb') as file: #'my_book.bin'
            self.data = pickle.load(file)

    def exit(self):
        result = self.dump()
        return result
        

# ----------------------------------------------------------------------------------------------------------


def assistant():

    my_book = None
    my_book = AddressBook()
    my_book.load()

    print ('*' * 50)
    print (['Welcome to Assistant-bot'])
    print (f'Workdir [{WORK_DIR.parent}]')
    print ('-' * 50)

    while True:
        
        result = False
        
        command = input('Input command or "?" for help: > ').lower().strip()
        
        print('*' * 20, f'{command}', '*' * (28 - len(command)))

        if command == "end" or command == "exit":
            my_book.exit()
            print ('Bye-Bye!')
            break
        
        elif command == 'add_contact':
            name = input('Input name for contact: ').strip()
            if name != '':
                birthday = input('Input bithday in format [yyyy-mm-dd]: ').strip()
                record = Record(name, birthday)

                my_book.add_record(record)
                
                result = True

            else:
                print("Name can't be empty. Try again.")
        
        elif command == 'del_contact':
            name = input('Input name for contact: ').strip()
            if name != '':
                my_book.delete(name)
                result = True

        elif command == 'add_address':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    home = input('Input address: ').strip()
                    record.home = home
                    result = True
                else:
                    print('Name not found.')

        elif command == 'add_birthday':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    birthday = input('Input birthday in format yyyy-mm-dd: ').strip()
                    record.birthday.value = birthday
                    result = True
                else:
                    print('Name not found.')

        elif command == 'add_email':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    email = input('Input email: ').strip()
                    record.add_email(email)
                    result = True
                else:
                    print('Name not found.')
        
        elif command == 'edit_email':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    old_email = input('Input old email: ').strip()
                    new_email = input('Input new email: ').strip()
                    record.edit_email(old_email, new_email)
                    result = True
                else:
                    print('Name not found.')
        
        elif command == 'add_phone':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    phone = input('Input phone number: ').strip()
                    record.add_phone(phone)
                    result = True
                else:
                    print('Name not found.')
        
        elif command == 'edit_phone':
            name = input('Input contact name: ').strip()
            if name != '':
                record = my_book.find(name)
                if record:
                    old_phone = input('Input old phone number: ').strip()
                    new_phone = input('Input new phone number: ').strip()
                    record.edit_phone(old_phone, new_phone)
                    result = True
                else:
                    print('Name not found.')

        elif command == 'find_record':
            find = input('Input symbols to search: ').strip()
            if find != '':
                print(f'-----Search by [{find}]--------')
                records = my_book.find_record(find)
                if len(records):
                    
                    for name, record in records.items():
                        print(record)
                    print('*' * 0)
                    result = True
                else:
                    print('No match found.')

        
        elif command.startswith('show_birthdays'):
            days = input('Input max days to birthdays: ')
            if days.isdigit():
                days = int(days)
                if my_book:
                    for name, record in my_book.data.items():
                        delta_days = record.days_to_birthday()
                        if delta_days:
                            if int(delta_days) < days:
                                print(record.show_birthday())
                    result = True
            else:
                print('Incorect value of days count')


        elif command == 'show_book':
            if my_book:
                for name, record in my_book.data.items():
                    print(record)
                    result = True
        
        elif command == 'scan_folder':
        
            folder = input('Input folder name for scaning: ') 

            if os.path.exists(folder):
                folder = Path(folder)
                scan.scan(folder)
                scan.scan_result()
                result = True
            else:
                print ('Folder not found')

        elif command == 'sort_folder':
            
            folder = input('Input folder name for sorting: ') 

            if os.path.exists(folder):
                folder = Path(folder)
                sort.main(folder)
                result = True
            else:
                print('Error sorting files')

        elif command == 'notes':
            notes.main()

        elif command == "?":
            commands = []
            
            commands.append('- [end] or [exit]  - quit program')
            
            commands.append('- [add_contact]    - adding contact to book')
            commands.append('- [del_contact]    - remove contact from book')
            commands.append('- [add_address]    - adding address to contact')
            commands.append('- [add_birthday]   - adding birthday to contact')
            commands.append('- [add_email]      - adding email to contact')
            commands.append('- [edit_email]     - edit email')
            commands.append('- [add_phone]      - adding phone number to contact')
            commands.append('- [edit_phone]     - edit phone number')
            commands.append('- [find_record]    - search contact by symbols')

            commands.append('- [show_birthdays] - show all birtdays in book')
            commands.append('- [show_book]      - show all contacts in book')
            
            commands.append('- [scan_folder]    - scan folder')
            commands.append('- [sort_folder]    - sort folder')
            commands.append('- [notes]          - case of notes')

            
            for c in commands:
                print(f'{c}')
        
        print('*' * 50)
        if result:
            print('Result: OK')
        


if __name__ == "__main__":
    
    assistant()
# name = Name('Liza')
# phone = Phone('0608475176')
# birthday = Birthday('12.01.2006')
# address = Address('UA', 'Poltava', 'Privet Drive', 8)
# contact = Contact(name, phone, address, birthday)
# print(contact.get_phone_number())
# print(contact.get_address())
# print(contact.get_birthday())
# print(contact.add_phone('0956745532'))
# print(contact.get_birthday())
