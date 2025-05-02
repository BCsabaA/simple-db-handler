import sqlite3
import logging # TODO add logging



class Database():

    DATABASE = None
    TABLES = []
    def __init__(self, db_name):
        if Database.DATABASE:
            print('Database already exists')
            self.db_name = Database.DATABASE.db_name
            self.conn = Database.DATABASE.conn
            self.cursor = Database.DATABASE.cursor
            return
        self.db_name = db_name
        Database.DATABASE = self
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.close()

    def close(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def open(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def rollback(self):
        self.conn.rollback()

    def read_table(self, filters: dict=None, columns: list=None, foreign_columns: list=None, order_by: list=None):
            # TODO define table read
        pass

    def insert(self,obj):
        table = obj.__class__.TABLENAME
        if table not in Database.TABLES:
            obj.parse_object_to_table()
        if obj.__dict__.get('id') == None:
            obj.insert_instance_in_database()

    def update(self, obj):
        # TODO define objetc update
        pass

    def delete(self, obj):
        # TODO define objetc delete
        pass

    def __str__(self):
        return f'Database(name={self.db_name}, tables={self.TABLES} connection={self.conn}, cursor={self.cursor})'


class Table():

    type_map = {
        int: 'INTEGER',
        str: 'TEXT',
        float: 'REAL',
        bool: 'BOOLEAN'
    }

    def __init__(self):
        if not Database.DATABASE:
            print('No database')
            return
        if self.__class__.TABLENAME not in Database.TABLES:
            self.parse_object_to_table()
        print(self.__dict__.get('id'))
        print(self.__class__.TABLENAME)
        print(Database.TABLES)
        print(self.__class__.TABLENAME in Database.TABLES)
        # if self.__class__.TABLENAME in Database.TABLES:
        #     if self.__dict__.get('id') == None:
        #         self.insert_instance_in_database()
        
    def __str__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def insert_instance_in_database(self):
        print('insert_instance_in_database')
        columns = ', '.join(field for field in self.__dict__.keys() )
        values = tuple(self.__dict__.values())
        create_insert_query = f'INSERT INTO {self.__class__.TABLENAME}({columns}) VALUES({", ".join("?" for _ in values)})'
        print(create_insert_query)
        if not Database.DATABASE:
            print('No database')
            return
        Database.DATABASE.open()
        try:
            Database.DATABASE.cursor.execute(create_insert_query, values)
            Database.DATABASE.commit()
            self.id = Database.DATABASE.cursor.lastrowid
        except sqlite3.IntegrityError:
            Database.DATABASE.rollback()
            print('IntegrityError', f'{self} already exists, skipping')
        Database.DATABASE.close()

    def parse_object_to_table(self):
        fields = (field for field in self.__class__.__dict__.values() if isinstance(field, Field))
        create_table_query = f'CREATE TABLE IF NOT EXISTS {self.__class__.TABLENAME}('
        for field in fields:
            print(field)
            create_table_query += f'{field.name} {self.type_map[field.type]}'
            if field.primary_key:
                create_table_query += ' PRIMARY KEY'
            if field.autoincrement:
                create_table_query += ' AUTOINCREMENT'
            if field.unique:
                create_table_query += ' UNIQUE'
            if field.default is not None:
                create_table_query += f' DEFAULT {field.default}'
            if field.not_null:
                create_table_query += ' NOT NULL'
            if field.foreign_key_table is not None:
                create_table_query += f' REFERENCES {field.foreign_key_table}({field.foreign_key_column})'
            create_table_query += ', '
        create_table_query = create_table_query[:-2] + ')'
        print(create_table_query)
        if not Database.DATABASE:
            print('No database')
            return
        Database.DATABASE.open()
        Database.DATABASE.cursor.execute(create_table_query)
        Database.DATABASE.commit()
        Database.DATABASE.close()
        Database.TABLES.append(self.__class__.TABLENAME)


class Field():
    def __init__(self, name, type, default=None, primary_key=False, autoincrement=False, unique=False, not_null=False, foreign_key_table=None, foreign_key_column=None):
        self.name = name
        self.type = type
        self.default = default
        self.primary_key = primary_key
        self.autoincrement = autoincrement
        self.unique = unique
        self.not_null = not_null
        self.foreign_key_table = foreign_key_table
        self.foreign_key_column = foreign_key_column



class Person(Table):
    TABLENAME = 'persons'
    ID = Field('id', int, primary_key=True, autoincrement=True)
    NAME = Field('name', str)
    AGE = Field('age', int)
    PHONE = Field('phone', int, unique=True)
    DELETED = Field('deleted', bool, default=False)
    CARPLATE = Field('carplate', str, foreign_key_table='cars', foreign_key_column='plate')

    def __init__(self, name, age, phone, carplate=None):
        self.name = name
        self.age = age
        self.phone = phone
        self.carplate = carplate
        self.id = None
        super().__init__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f'Person(name={self.name}, age={self.age}, phone={self.phone})'
    
class Car(Table):
    TABLENAME = 'cars'
    ID = Field('id', int, primary_key=True, autoincrement=True)
    PLATE = Field('plate', str, unique=True)
    MODEL = Field('model', str)
    DELETED = Field('deleted', bool, default=False)

    def __init__(self, plate, model):
        self.plate = plate
        self.model = model
        self.id = None
        super().__init__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return f'Car(plate={self.plate}, model={self.model})'



def test():
    db =Database('test.db')

    # car1 = Car('ABC123', 'BMW')
    # car2 = Car('DEF456', 'Mercedes')
    # car3 = Car('GHI789', 'Volvo')

    # person1 = Person('Johnny Doe', 2, 1234567892, 'ABC123')
    # person2 = Person('Jane Doe', 24, 1234567891, 'DEF456')
    # person3 = Person('John Doe', 24, 1234567890)

    car4 = Car('HUH404', 'Opel')
    db.insert(car4)


if __name__ == '__main__':
    test()
