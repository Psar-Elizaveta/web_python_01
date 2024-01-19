from abc import ABC, abstractmethod
from pathlib import Path
import os
from rich import print
from collections import UserDict
import json
import copy



WORK_DIR = Path(os.path.abspath(__file__)).parent
NOTEBOOK = str(WORK_DIR) + '//notebook.bin'

class Note(ABC):
    @abstractmethod
    def value_of(self):
        raise NotImplementedError


class NoteName(Note):

    def __init__(self, value):
        if len(value) < 30:
            self.value = value
        else:
            self.value = value[:30]

    def value_of(self):
        return f'{self.value}'


class Status(Note):

    def __init__(self, value="in progress"):
        self.value = "in progress"

    def value_of(self):
        return f'{self.value}'


class Notes(Note):

    def __init__(self, value):
        if len(value) < 250:
            self.value = value
        else:
            self.value = value[:250]

    def value_of(self):
        return f'{self.value}'

class Tags(Note):
    def __init__(self, value):
        self.value = value

    def value_of(self):
        return f'{self.value}'


class RecordNote:
    def __init__(self, name, note: Notes, tag: Tags = None, status="in progress"):
        self.name = name
        self.note = note
        self.tags = []
        if tag:
            self.tags.append(tag)
        self.status = Status(status)

    def __str__(self):
        return f"Name: {self.name.value} Note: {self.note.value} Tags: {self.tags} Status: {self.status.value}"

    def value_of(self):
        return f"Name: {self.name.value} Note: {self.note.value} Tags: {self.tags} Status: {self.status.value}"


class NoteBook(UserDict):
    def __init__(self):
        self.data = {}

    def value_of(self):
        return f'{self.data}'

    def add_note(self, record):
        self.data[record.name.value] = record

    def change_name(self, old_name, new_name):
        self.data[new_name] = copy.deepcopy(self.data[old_name])
        self.data[new_name].name.value = new_name
        self.data.pop(old_name)

    def change_tag(self, name, tags):
        new_tag = Tags(tags)
        for k, v in self.data.items():
            if k == name:
                self.data[k].tags = []
                self.data[k].tags.append(new_tag)

    def change_note(self, name, new_note):
        new_note = Notes(new_note)
        for k in self.data:
            if k == name:
                self.data[k].note = new_note

    def change_status(self, name, new_status):
        if new_status.lower() in ["in progress", "done"]:
            self.data[name].status.value = new_status.lower()

    def show_record(self, name):
        if name in self.data.keys():
            return self.data[name]

    def show_note(self, name):
        for k in self.data:
            if k == name:
                return self.data[k]

    def delete_note(self, rec: RecordNote):
        for a, v in self.data.items():
            if v.note == rec.note:
                deleted_note = a.note
                self.data.pop(a)
                return deleted_note

    def delete_notes_by_status(self, status):
        result = {}
        for name, record in self.data.items():
            if record.status.value != status:
                result[name] = record
        self.data = result

    def delete_tag(self, name, del_tag):
        old_tags = self.data[name].tags
        new_tags = [tag for tag in old_tags if tag.value != del_tag]
        self.data[name].tags = new_tags

    def add_tag(self, name, new_tag):
        if new_tag.value not in [i.value for i in self.data[name].tags]:
            self.data[name].tags.append(new_tag)

    def find_info_by_name(self, keyword):
        result = []
        for name, record in self.data.items():
            if keyword.lower() == name.lower():
                result.append(self.data[name])
                break
        return result

    def find_info_by_tag(self, keyword):
        result = []
        for name, record in self.data.items():
            for tag in record.tags:
                if keyword.lower() == tag.value.lower():
                    result.append(self.data[name])
                    break
        return result

    def find_info_by_status(self, keyword):
        result = []
        for name, record in self.data.items():
            if keyword.lower() == record.status.value.lower():
                result.append(self.data[name])
        return result

    def get_tags(self, name):
        return self.data[name].tags

    def change_tag(self, name, old_tag, new_tag):
        for i in range(len(self.data[name].tags)):
            if old_tag.value == self.data[name].tags[i].value:
                self.data[name].tags[i].value = new_tag.value

    def serialize(self):
        with open(NOTEBOOK, 'wb') as file:
            if len(self.data) > 0:
                json.dumps(self, file)

    def deserialize(self):
        try:
            with open(NOTEBOOK, 'rb') as file:
                self.data = json.load(file)
        except:
            pass

    def show_records(self):
        return self.data
NOTES_BOOK = NoteBook()


def hello():
    return "How can I help you?"


def help():
    print(f'To start working with the assistant, write one of the commands[bold magenta].\nYou can use these commands[/bold magenta]\U0001F60A\n', "-" * 90)
    print(f'[bold blue]add:[/bold blue]    Adds a note to the notebook.\n', '-' * 90)
    print(f'[bold blue]search:[/bold blue]  Searches for notes in the notebook by the following fields: name / tag / status.\n', '-' * 90)
    print(f'[bold blue]change:[/bold blue]  Changes the information in the note: name / note / tag / status.\n', '-' * 90)
    print(f'[bold blue]shownote:[/bold blue]  Show note which the user want to see.\n', '-' * 90)
    print(f'[bold blue]show:[/bold blue]    Show all notes.\n', '-' * 90)
    print(f'[bold blue]del:[/bold blue]     Deleting a note, or deleting completed notes.\n', '-' * 90)
    print(f'[bold blue]cancel:[/bold blue]  An undo command anywhere in the assistant.\n', '-' * 90)
    print(f'[bold blue]good bye, close, exit:[/bold blue] Exit the program.\n', '-' * 90)
    command = input("Press any key to return. ")
    if command.lower() == "cancel":
        return "Exit from the help menu. "
    else:

        main()


# def add():
#     name = input("Enter a name to your record: ")
#     while name == "":
#         print("Note name cannot be empty!")
#         name = input("What do you want to record?: ")
#         if name.lower() == "cancel":
#             return "Adding a new record has been canceled"
#         elif name == classes.NoteName(name):
#             while True:
#                 answer = input(
#                     "You have already such note, do you want to rewrite it? (y/n) ")
#                 if answer.lower() == "y":
#                     name = classes.NoteName(name)
#                     break
#                 elif answer.lower() == "cancel":
#                     return "Adding a new note has been canceled"
#                 elif answer.lower() == "n":
#                     break
#             if answer.lower() == "y":
#                 break
#             else:
#                 continue
#         else:
#             name = classes.NoteName(name)
#             break
#     if name == "cancel":
#         return "Adding a new note has been canceled"
#     name = classes.NoteName(name)
#     note = input(f"Type {name.value}'s note: ")
#     if note.lower() == "cancel":
#         return "Adding a new note has been canceled"
#     else:
#         note = classes.Notes(note)
#     tag = input(f"Type {name.value}'s tag: ")
#     if tag.lower() == "cancel":
#         return "Adding a new tag has been canceled"
#     else:
#         tag = classes.Tags(tag)
#     record = classes.RecordNote(name, note, tag)
#     NOTES_BOOK.add_note(record)
#     return f"Note {name.value} has been saved"
class NoteManager:
    def add(self):
        name = self.get_valid_name()
        if name == "cancel":
            return "Adding a new note has been canceled"
        note = self.get_valid_note(name)
        if note == "cancel":
            return "Adding a new note has been canceled"
        tag = self.get_valid_tag(name)
        if tag == "cancel":
            return "Adding a new tag has been canceled"
        record = self.create_record(name, note, tag)
        NOTES_BOOK.add_note(record)
        return f"Note {name.value} has been saved"

    def get_valid_name(self):
        while True:
            name = input("Enter a name to your record: ")
            if name == "":
                print("Note name cannot be empty!")
            elif name.lower() == "cancel":
                return "cancel"
            elif any(note.name == name for note in NOTES_BOOK):
                rewrite = input("You have already such note, do you want to rewrite it? (y/n) ")
                if rewrite.lower() == "y":
                    return NoteName(name)
            else:
                return NoteName(name)

    def get_valid_note(self, name):
        note = input(f"Type {name.value}'s note: ")
        return Notes(note) if note.lower() != "cancel" else "cancel"

    def get_valid_tag(self, name):
        tag = input(f"Type {name.value}'s tag: ")
        return Tags(tag) if tag.lower() != "cancel" else "cancel"

    def create_record(self, name, note, tag):
        return RecordNote(name, note, tag)


# def search():
#     while True:
#         result = input("Choose what you want to find (name / tag / status): ")
#         if result.lower() == "name":
#             result = input("What you want to find: ")
#             if result == "cancel":
#                 print("Searching has been canceled")
#             if NOTES_BOOK.find_info_by_name(result):
#                 showing_func(NOTES_BOOK.find_info_by_name(result))
#             else:
#                 print("Nothing match to result")
#         elif result.lower() == "tag":
#             result = input("What you want to find: ")
#             if result == "cancel":
#                 print("Searching has been canceled")
#             if NOTES_BOOK.find_info_by_tag(result.lower()):
#                 showing_func(NOTES_BOOK.find_info_by_tag(result.lower()))
#             else:
#                 print("Nothing match to result")
#         elif result.lower() == "status":
#             result = input("What you want to find: ")
#             if result == "cancel":
#                 print("Searching has been canceled")
#             if NOTES_BOOK.find_info_by_status(result):
#                 showing_func(NOTES_BOOK.find_info_by_status(result))
#             else:
#                 print("Nothing match to result")
#         elif result.lower() == "cancel":
#             print("Serching has been canceled")
#             break
#         else:
#             print("Wrong command")

class SearchContext:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def execute_search(self, query):
        return self.strategy.search(query)


class NameSearchStrategy:
    def search(self, query, notes_book):
        return notes_book.find_info_by_name(query)


class TagSearchStrategy:
    def search(self, query, notes_book):
        return notes_book.find_info_by_tag(query.lower())


class StatusSearchStrategy:
    def search(self, query, notes_book):
        return notes_book.find_info_by_status(query)


def search():
    strategies = {
        "name": NameSearchStrategy(),
        "tag": TagSearchStrategy(),
        "status": StatusSearchStrategy()
    }
    context = SearchContext(strategies["name"])

    while True:
        search_type = input("Choose what you want to find (name / tag / status / cancel): ").lower()
        if search_type == "cancel":
            print("Searching has been canceled")
            break

        if search_type in strategies:
            query = input("What you want to find: ")
            if query == "cancel":
                print("Searching has been canceled")
                break

            context.set_strategy(strategies[search_type])
            results = context.execute_search(query, NOTES_BOOK)
            if results:
                showing_func(results)
            else:
                print("Nothing matches the result")
        else:
            print("Wrong command")
def change():
    name = input("Which note do you want to change? ")
    if name.lower() == "cancel":
        return "Changing has been canceled"
    if NOTES_BOOK.show_record(name):
        while True:
            item = input(
                f"What do you want to change at {name}'s records: (name / note / tag / status)? ")
            if item.lower() == "name":
                new_name = input(f"Type a new name for note {name}: ")
                NOTES_BOOK.change_name(name, new_name)
                return f"Name for note {name} changed to {new_name}"
            elif item.lower() == "note":
                new_note = input(
                    f"Type a new text for note {name}: ")
                if new_note.lower() == "cancel":
                    return "Changing has been canceled"
                NOTES_BOOK.change_note(name, new_note)
                return f"Text for note {name} changed."
            elif item.lower() == "tag":
                command = input(
                    "Choose option: add (add one more tag) / change (replace tag to another) / dell (dell tag): ")
                if command.lower() == "add":
                    while True:
                        new_tag = input(
                            f"Type a new tag for note {name}: ")
                        if new_tag.lower() == "cancel":
                            return "Changing has been canceled"
                        else:
                            new_tag = Tags(new_tag)
                        if new_tag.value:
                            NOTES_BOOK.add_tag(name, new_tag)
                            return f"Tag {new_tag.value} has been added"
                        else:
                            answer = input(
                                "Please, type the tag. Would you like to try one more time? (y/n): ")
                            if answer.lower() == "n":
                                break
                            elif answer.lower() == "y":
                                continue
                            elif answer.lower() == "cancel":
                                return "Changing has been canceled"
                            else:
                                break
                elif command.lower() == "change":
                    while True:
                        old_tag = input(
                            "Type tag you want to change: ")
                        if old_tag.lower() == "cancel":
                            return "Changing has been canceled"
                        if old_tag in [tag.value for tag in NOTES_BOOK.get_tags(name)]:
                            while True:
                                new_tag = input("Type a new tag: ")
                                if new_tag.lower() == "cancel":
                                    return "Changing has been canceled"
                                new_tag = Tags(new_tag)
                                if new_tag.value == None:
                                    while True:
                                        answer = input(
                                            "Would you like try one more time? (y/n) ")
                                        if answer.lower() == "y":
                                            break
                                        elif answer.lower() in ["cancel", "n"]:
                                            return "Changing has been canceled"
                                        else:
                                            print("Wrong command")
                                else:
                                    old_tag = Tags(old_tag)
                                    NOTES_BOOK.change_tag(
                                        name, old_tag, new_tag)
                                    return f"Tag {old_tag.value} has been changed to {new_tag.value}"
                elif command.lower() == "dell":
                    while True:
                        tag = input("Please type a tag you want to delete ")
                        if tag == "cancel":
                            return f"You canceled changing contact {name}"
                        if NOTES_BOOK.find_info_by_tag(tag):
                            NOTES_BOOK.delete_tag(name, tag)
                            return f"Tag {tag} has been deleted"
                        else:
                            while True:
                                answer = input(
                                    "Such tag didn't exist, would you like to try one more time? (y/n)")
                                if answer.lower() in ["cancel", "n"]:
                                    return "Deleting has been canceled"
                                if answer.lower() == "y":
                                    break
                                else:
                                    print("Wrong command")
                else:
                    answer = input(
                        "Please, type the tag. Would you like to try one more time? (write y - it's means yes, or n - no): ")
                    if answer.lower() == "n":
                        break
                    elif answer.lower() == "y":
                        continue
                    elif answer.lower() == "cancel":
                        return "Changing has been canceled"
                    else:
                        continue
            elif item.lower() == "status":
                while True:
                    new_status = input(
                        f"Type a new status for note {name}: (Done / In progress)? ")
                    if new_status.lower() == "cancel":
                        return "Changing has been canceled"
                    NOTES_BOOK.change_status(name, new_status)
                    return f"Status for note {name} changed to {new_status}"
            elif item.lower() == "cancel":
                return "Changing has been canceled"
            else:
                answer = input(
                    "You have such options: (name / note / tag / status). Would you like to try one more time? (y/n)")
                if answer.lower() == "y":
                    continue
                else:
                    break
    else:
        return f"{name} didn't exist"


def delete_note():
    while True:
        command = input("Do you want to delete one note? (write n or y) ")
        if command.lower() == "cancel":
            return "You have canceled deleting"
        if command.lower() == "y":
            note = input("Which note do you want to delete? ")
            if note in NOTES_BOOK.data.keys():
                NOTES_BOOK.data.pop(note)
                return f"Note {note} has been deleted"
            else:
                while True:
                    answer = input(
                        "No such note, do you want to try one more time? (y/n) ")
                    if answer.lower() == "y":
                        break
                    elif answer.lower() in ["n", "cancel"]:
                        return "You have canceled deleting"
                    else:
                        print("Wrong command")
        elif command.lower() == "n":
            while True:
                answer = input(
                    "Do you want to delete all completed notes? (y/n) ")
                if answer.lower() in ["cancel"]:
                    return "You have canceled deleting"
                if answer.lower() == "y":
                    NOTES_BOOK.delete_notes_by_status("done")
                    return f"Notes with status 'done' has been deleted"
                elif command.lower() == "cancel":
                    return "You have canceled deleting"
                else:
                    while True:
                        answer = input(
                            "No such note, do you want to try one more time? (y/n) ")
                        if answer.lower() == "y":
                            break
                        elif answer.lower() == "n":
                            return "You have canceled deleting"
                        else:
                            print("Wrong command")
        else:
            print("Wrong command")


def show_note():
    name = input("Which note do you want to see? ")
    if name.lower() == "cancel":
        return "Showing has been canceled"
    if NOTES_BOOK.show_record(name):
        return NOTES_BOOK.show_record(name)
    else:
        return "Nothing match"


# def show_note():
#     name = input("Which note do you want to see? ")
#     if name.lower() == "cancel":
#         return "Showing has been canceled"
#     if NOTES_BOOK.show_record(name):
#         return NOTES_BOOK.show_record(name)
#     else:
#         return "Nothing match"


def show_all():
    counter = 1
    print(
        f"{'№':^2} | {'Name':^31} | {'Note':^67} | {'Tags':^26} | {'Status':^11} |\n", "-" * 150)
    for info in NOTES_BOOK.show_records().values():
        name = info.name.value
        if len(info.tags) == 1:
            tags = info.tags[0].value
        elif len(info.tags) > 1:
            tags_l = []
            for tag in [tag.value for tag in info.tags]:
                tags_l.append(tag)
            tags = ", ".join(tags_l)
        tags = tags if len(tags) < 26 else tags[:23] + "..."
        note = info.note.value
        note = note if len(note) < 67 else note[:63] + "..."
        status = info.status.value
        print(
            f"{counter:<2} | {name:<31} | {note:<67} | {tags:<26} | {status:<11} |\n", "-" * 150)
        counter += 1


def showing_func(lst):
    counter = 1
    print(
        f"{'№':^2} | {'Name':^31} | {'Note':^67} | {'Tags':^26} | {'Status':^11} |\n", "-" * 150)
    for info in lst:
        name = info.name.value
        if len(info.tags) == 1:
            tags = info.tags[0].value
        elif len(info.tags) > 1:
            tags_l = []
            for tag in [tag.value for tag in info.tags]:
                tags_l.append(tag)
            tags = ", ".join(tags_l)
        tags = tags if len(tags) < 26 else tags[:23] + "..."
        note = info.note.value
        note = note if len(note) < 67 else note[:63] + "..."
        status = info.status.value
        print(
            f"{counter:<2} | {name:<31} | {note:<67} | {tags:<26} | {status:<11} |\n", "-" * 150)
        counter += 1


def end_work():
    return "Good bye"


COMMANDS = {"hello": hello,
            "help": help,
            "add": lambda: note_manager.add(),
            "search": search,
            "change": change,
            "show": show_all,
            "shownote": show_note,
            "del": delete_note,
            "end_work": end_work}


def parser(command):
    if command.lower() == "hello":
        return "hello"
    if command.lower() in ["good bye", "close", "exit"]:
        return "end_work"
    if command.lower() == "help":
        return "help"
    if command.split()[0].lower() == "add":
        return "add"
    if command.split()[0].lower() == "search":
        return "search"
    if command.split()[0].lower() == "change":
        return "change"
    if command.split()[0].lower() == "show":
        return "show"
    if command.split()[0].lower() == "shownote":
        return "shownote"
    if command.split()[0].lower() == "del":
        return "del"
    else:
        return "wrong_command"


def main():
    print(WORK_DIR)
    print("Hello. If you need help, write 'help'")

    NOTES_BOOK.deserialize()

    while True:
        user_command = input(">>> ")
        command = parser(user_command)
        if command == "end_work":
            print(COMMANDS["end_work"]())
            NOTES_BOOK.serialize()
            break
        if command == "hello":
            print(COMMANDS["hello"]())
            continue
        if command == "help":
            print(COMMANDS["help"]())
            continue
        if command == "add":
            print(COMMANDS["add"]())
            continue
        if command == "shownote":
            print(COMMANDS["shownote"]())
            continue
        if command == "show":
            COMMANDS["show"]()
            continue
        if command == "wrong_command":
            print("Wrong command")
            continue
        if command == "search":
            COMMANDS[command]()
            continue
        print(COMMANDS[command]())


if __name__ == "__main__":
    note_manager = NoteManager()
    main()