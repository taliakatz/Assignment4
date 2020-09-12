import atexit
import sqlite3

from persistence import _Employees, _Suppliers, _Products, _Coffee_stands, _Activities, Employees_report, \
    activities_report


class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('moncafe.db')
        self.employees = _Employees(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.products = _Products(self._conn)
        self.coffee_stands = _Coffee_stands(self._conn)
        self.activities = _Activities(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
                CREATE TABLE Employees (
                    id           INTEGER PRIMARY KEY,
                    name         TEXT NOT NULL,
                    salary       REAL NOT NULL,
                    coffee_stand INTEGER, 

                    FOREIGN KEY(coffee_stand) REFERENCES coffee_stands(id)
                );

                CREATE TABLE Suppliers (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    contact_information TEXT 
                );

                CREATE TABLE Products (
                    id INTEGER PRIMARY KEY,
                    description TEXT NOT NULL,
                    price REAL NOT NULL,
                    quantity INTEGER NOT NULL

                );
                CREATE TABLE Coffee_stands (
                    id INTEGER PRIMARY KEY,  
                    location TEXT NOT NULL,
                    number_of_employees INTEGER

                );
                CREATE TABLE Activities (
                    product_id  INTEGER, 
                    quantity INTEGER NOT NULL,
                    activator_id INTEGER NOT NULL,
                    date DATE NOT NULL,

                    FOREIGN KEY(product_id) REFERENCES Product(id),
                    FOREIGN KEY(activator_id) REFERENCES Supplier(id)
                );
        """)


    def get_employees_reports(self):
        c = self._conn.cursor()
        all = c.execute("""
                    SELECT name, salary, working_location, COALESCE(sum(total), 0)
                    FROM(
                    SELECT Employees.id, Employees.name as name, Employees.salary as salary,
                    Activities.quantity as quantity, Activities.product_id, Coffee_stands.location as working_location,
                    Products.price, abs(Products.price*Activities.quantity) as total 
                    FROM(
                    Employees LEFT JOIN Coffee_stands ON Employees.coffee_stand = Coffee_stands.id
                    LEFT JOIN Activities ON Activities.activator_id = Employees.id
                    LEFT JOIN Products ON Activities.product_id = Products.id))
                    GROUP BY name 
                    ORDER BY name
                """).fetchall()
        return [Employees_report(*row) for row in all]

    def get_activities_report(self):
        c = self._conn.cursor()
        all = c.execute("""SELECT date, description, quantity, COALESCE(employee_name,NULL),COALESCE(Suppliers.name,NULL)
                    FROM(
                    SELECT product_id, quantity, activator_id, date, description, Employees.name as employee_name
                    FROM(
                    SELECT Activities.product_id, Activities.quantity, Activities.activator_id, Activities.date, 
                    Products.description
                    FROM
                    Activities LEFT JOIN Products ON Activities.product_id = Products.id
                    ) as tbl1 LEFT JOIN Employees ON Employees.id = tbl1.activator_id
                    ) as tbl2 LEFT JOIN Suppliers ON Suppliers.id = tbl2.activator_id 
                    ORDER BY date
                """).fetchall()
        return [activities_report(*row) for row in all]

# the repository singleton
rep = _Repository()
atexit.register(rep._close)