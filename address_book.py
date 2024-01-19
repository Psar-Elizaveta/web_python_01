from contact import Name, Phone, Record, Address, Birthday, Email
from collections import UserDict
from abc import ABC, abstractmethod
import re
import json
from datetime import datetime, date, timedelta



class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name] = record

    def __str__(self):
        result = []
        for account in self.data:
            if account['birthday']:
                birth = account['birthday'].strftime("%d/%m/%Y")
            else:
                birth = ''
            if account['phones']:
                new_value = []
                for phone in account['phones']:
                    print(phone)
                    if phone:
                        new_value.append(phone)
                phone = ', '.join(new_value)
            else:
                phone = ''
            result.append(
                "_" * 50 + "\n" + f"Name: {account['name']} \nPhones: {phone} \nBirthday: {birth} \nEmail: {account['email']} \nStatus: {account['status']} \nNote: {account['note']}\n" + "_" * 50 + '\n')
        return '\n'.join(result)

    def __next__(self):
        phones = []
        self.counter += 1
        if self.data[self.counter]['birthday']:
            birth = self.data[self.counter]['birthday'].strftime("%d/%m/%Y")
        if self.counter == len(self.data):
            self.counter = -1
            raise StopIteration
        for number in self.data[self.counter]['phones']:
            if number:
                phones.append(number)
        result = "_" * 50 + "\n" + f"Name: {self.data[self.counter]['name']} \nPhones: {', '.join(phones)} \nBirthday: {birth} \nEmail: {self.data[self.counter]['email']} \nStatus: {self.data[self.counter]['status']} \nNote: {self.data[self.counter]['note']}\n" + "_" * 50
        return result

    def __iter__(self):
        return self

    def __setitem__(self, index, contact):
        self.data[index] = {'name': contact.name,
                            'phones': contact.phones,
                            'birthday': contact.birthday}
                            # 'email': contact.email,
                            # 'address': contact.address}

    def __getitem__(self, index):
        return self.data[index]

    def log(self, action):
        current_time = dt.strftime(dt.now(), '%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')

    def add(self, record):
        account = {'name': Pecord.name,
                'phones': Pecord.phones,
                'birthday': Pecord.birthday,
                'email': Pecord.email,
                'status': Pecord.status,
                'note': Pecord.note}
        self.data.append(account)
        self.log(f"Contact {Pecord.name} has been added.")


    def dump(self, file_name='addressbook.bin'):
        with open(file_name, 'wb') as file:
            json.dump(self.data, file)
        self.log("Addressbook has been saved!")

    # def load(self, file_name='addressbook.bin'):
    #     with open(file_name, 'rb') as file:
    #         self.data = json.load(file)
    #     self.log("Addressbook has been loaded!")

    def load(self, file_name='addressbook.bin'):
        if file_name:
            with open(file_name, 'rb') as file:
                self.data = json.load(file)
            self.log("Addressbook has been loaded!")
        else:
            self.log('Adressbook has been created!')
        return self.data

    def search(self, pattern, category):
        result = []
        category_new = category.strip().lower().replace(' ', '')
        pattern_new = pattern.strip().lower().replace(' ', '')

        for account in self.data:
            if category_new == 'phones':

                for phone in account['phones']:

                    if phone.lower().startswith(pattern_new):
                        result.append(account)
            elif account[category_new].lower().replace(' ', '') == pattern_new:
                result.append(account)
        if not result:
            print('There is no such contact in address book!')
        return result

    def edit(self, contact_name, parameter, new_value):
        names = []
        try:
            for account in self.data:
                names.append(account['name'])
                if account['name'] == contact_name:
                    if parameter == 'birthday':
                        new_value = Birthday(new_value).value
                    elif parameter == 'email':
                        new_value = Email(new_value).value
                    # elif parameter == 'status':
                    #     new_value = Status(new_value).value
                    elif parameter == 'phones':
                        new_contact = new_value.split(' ')
                        new_value = []
                        for number in new_contact:
                            new_value.append(Phone(number).value)
                    if parameter in account.keys():
                        account[parameter] = new_value
                    else:
                        raise ValueError
            if contact_name not in names:
                raise NameError
        except ValueError:
            print('Incorrect parameter! Please provide correct parameter')
        except NameError:
            print('There is no such contact in address book!')
        else:
            self.log(f"Contact {contact_name} has been edited!")
            return True
        return False

    def remove(self, pattern):
        flag = False
        for account in self.data:
            if account['name'] == pattern:
                self.data.remove(account)
                self.log(f"Contact {account['name']} has been removed!")
                flag = True
            '''if pattern in account['phones']:
                        account['phones'].remove(pattern)
                        self.log.log(f"Phone number of {account['name']} has been removed!")'''
        return flag

    def __get_current_week(self):
        now = dt.now()
        current_weekday = now.weekday()
        if current_weekday < 5:
            week_start = now - timedelta(days=2 + current_weekday)
        else:
            week_start = now - timedelta(days=current_weekday - 5)
        return [week_start.date(), week_start.date() + timedelta(days=7)]

    def congratulate(self):
        result = []
        WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_year = dt.now().year
        congratulate = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
        for account in self.data:
            if account['birthday']:
                new_birthday = account['birthday'].replace(year=current_year)
                birthday_weekday = new_birthday.weekday()
                if self.__get_current_week()[0] <= new_birthday.date() < self.__get_current_week()[1]:
                    if birthday_weekday < 5:
                        congratulate[WEEKDAYS[birthday_weekday]].append(account['name'])
                    else:
                        congratulate['Monday'].append(account['name'])
        for key, value in congratulate.items():
            if len(value):
                result.append(f"{key}: {' '.join(value)}")
        return '_' * 50 + '\n' + '\n'.join(result) + '\n' + '_' * 50


    def add_record(self, contact):
        self.data[contact.name] = contact

    def remove_contact(self, contact):
        self.data.pop(contact.name, None)

    def iterator(self, item_number):
        counter = 0
        result = ''
        for item, record in self.data.items():
            result += f'{item}: {record}'
            counter += 1
            if counter >= item_number:
                yield result
                counter = 0
                result = ''
            return counter

    def find_information_by_name(self, search_name):
        users_search = []
        for user, info in self.data.items():
            if search_name.lower() in info.search_name.value.lower():
                users_search.append(self.data[user])
        if users_search:
            return users_search
        else:
            return "Nothing found"

    def find_information_by_phone(self, search_phone):
        users_search = []
        for user, info in self.data.items():
            if info.phones and info.phones[0].value != None:
                for phone in info.phones:
                    if str(search_phone) in phone.value:
                        users_search.append(self.data[user])
        if users_search:
            return users_search
        else:
            return "Nothing found"

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # def dump(self, file_name='addressbook.json'):
    #     with open(file_name, 'wb') as file:
    #         json.dump(self.data, file)
    #
    # def load(self, file_name='addressbook.json'):
    #     with open(file_name, 'rb') as file:
    #         self.data = json.load(file)
    #
    # def search_contact(self, search_item):
    #     results = [contact for contact in self.data if
    #                search_item in contact['name'] or search_item in contact['phone']]
    #     return results