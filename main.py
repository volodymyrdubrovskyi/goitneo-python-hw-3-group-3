from collections import UserDict
import re
import datetime
import pickle

# обработка ошибки количества символов в номере телефона
class LenPhoneError(Exception):
    pass

# обработка ошибки не числового номера телефона
class TypePhoneError(Exception):
    pass

# обработка ошибки не нахождения телефона
class PhoneNotFindError(Exception):
    pass

# обработка ошибки не нахождения записи
class RecordNotFindError(Exception):
    pass

# обработка неправильного формата даты
class DateFormatError(Exception):
    pass

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        self.value = value

class Birthday:
    def __init__(self, date=None):
            result = re.findall(r'\d\d.\d\d.\d\d\d\d', date)
            if result:
                self.bday = datetime.date(year=int(date[6:10]), month=int(date[3:5]), day=int(date[0:2]))
            else:
                raise DateFormatError

    def add_bday(self, date):
        result = re.findall(r"\d\d.\d\d.\d\d\d\d", date)
        if not result:
            raise DateFormatError
        else:
            self.bday = datetime.date(year=int(date[6:10]), month=int(date[3:5]), day=int(date[0:2]))

    def __str__(self) -> str:
        return 'No Data' if self.bday == None else self.bday.strftime('%d.%m.%Y')

class Phone(Field):
    MAX_PHONE_LEN = 10

    def __init__(self, value):
        self.value = value
    
class Record:
    def __init__(self, name, bday=None):
        self.name = Name(name)
        self.phones = []
        self.bday = bday

    # добавление обїекта телефон в запись
    def add_phone(self, phone):
        if len(phone) != Phone.MAX_PHONE_LEN:
            raise LenPhoneError
        elif not phone.isdigit():
            raise TypePhoneError
        else:
            new_phone = True
            for p in self.phones:
                if p.value == phone:
                    new_phone = False
            if new_phone:
                self.phones.append(Phone(phone))
        
    # удаление телефона из списка телефонов
    def remove_phone(self, phone):
        find_phone = False
        for p in self.phones:
            if p.value == phone:
                find_phone = True
                phone_to_remove = p
        if find_phone:
            self.phones.remove(phone_to_remove)
        else:
            raise PhoneNotFindError

    # изменение обїекта телефон в записи
    def edit_phone(self, phone_old, phone_new):
        if len(phone_new) != Phone.MAX_PHONE_LEN:
            raise LenPhoneError
        elif not phone.isdigit():
            raise TypePhoneError
        else:
            for phone in self.phones:
                if phone.value == phone_old:
                    phone.value = phone_new

    # поиск номера телефона в текущей записи
    def find_phone(self, phone):
        res = None
        for p in self.phones:
            if p.value == phone:
                res = phone
        return res

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def __init__(self):
        self.data = UserDict()
        self.filename = None
    
    # добавление записи в словарь адресной книги
    def add_record(self, record):
        self.data[record.name.value] = record

    # поиск записи в словаре адресной книги
    def find(self, name):
        rec = self.data.get(name)
        if rec == None:
            raise RecordNotFindError
        else:
            return rec

    # удаление записи в словаре адресной книги
    def delete(self, name):
        if self.data.get(name) == None:
            raise RecordNotFindError
        else:
            self.data.pop(name)
    
    def save_to_file(self):
        with open('addrbook.dat', 'wb') as fh:
            pickle.dump(self, fh)
    
    def read_from_file(self):
        with open('addrbook.dat', 'rb') as fh:
            return pickle.load(fh)

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    # try:
    #     bday = Birthday('22.12.2003')
    #     print(bday)
    # except DateFormatError:
    #     print('Wrong data format. Please use: DD.MM.YYYY')
    print("Welcome to the assistant bot!")
    
    # Загружаем адресную книгу, если находим. 
    # Если не находим: Делаем пустую AdressBook
    try:
        abook = AddressBook().read_from_file()
    except:
        abook = AddressBook()

    while True:
        user_input = input("Enter a command: ")
        if user_input:
            command, *args = parse_input(user_input)
            
            if command in ["close", "exit"]:
                # выход, тут сохраняем AdressBook
                abook.save_to_file()
                print("Good bye!")
                break
            
            elif command == "hello":
                print("How can I help you?")
            
            elif command == "add":
                if len(args) == 2 and len(args[0]) > 0:
                    try:
                        if args[0] in abook.data:
                            rec = abook.data[args[0]]
                            rec.add_phone(args[1])
                        else:
                            rec = Record(args[0])
                            rec.add_phone(args[1])
                            abook.add_record(rec)
                        print('Contact added sucessfully.')
                    except LenPhoneError:
                        print('Phone must be 10 symbols')
                else:
                    print('Invalid command format.')
            
            elif command == "all":
                for _, record in abook.data.items():
                    print(record)

            else:
                print('Invalid command.')

if __name__ == '__main__':
    main()