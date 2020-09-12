import atexit
import sqlite3
from pathlib import Path
import sys
import inspect


# Data Transfer Objects:
class Employee(object):
    def __init__(self, id, name, salary, coffee_stand):
        self.id = id
        self.name = name
        self.salary = salary
        self.coffee_stand = coffee_stand

    def __str__(self):
        return tuple([self.id, self.name, self.salary, self.coffee_stand]).__str__()


class Supplier(object):
    def __init__(self, id, name, contact_information):
        self.id = id
        self.name = name
        self.contact_information = contact_information

    def __str__(self):
        return tuple([self.id, self.name, self.contact_information]).__str__()


class Product(object):
    def __init__(self, id, description, price, quantity):
        self.id = id
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return tuple([self.id, self.description, self.price, self.quantity]).__str__()

class Coffee_stand(object):
    def __init__(self, id, location, number_of_employees):
        self.id = id
        self.location = location
        self.number_of_employees = number_of_employees

    def __str__(self):
        return tuple([self.id, self.location, self.number_of_employees]).__str__()


class Activitie(object):
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date

    def __str__(self):
        return tuple([self.product_id, self.quantity, self.activator_id, self.date]).__str__()


class activities_report(object):
    def __init__(self, date, name, quantity, seller, supplier):
        self.date = date
        self.name = name
        self.quantity = quantity
        self.seller = seller
        self.supplier = supplier

    def __str__(self):
        return tuple([self.date, self.name, self.quantity, self.seller, self.supplier]).__str__()


class Employees_report(object):
    def __init__(self, name, salary, working_location, total):
        self.name = name
        self.salary = salary
        self.working_location = working_location
        self.total = total

    def __str__(self):
        return tuple([self.name, self.salary, self.working_location, self.total]).__str__()

# Data Access Objects:
# All of these are meant to be singletons
class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, employee):
        self._conn.execute("""
               INSERT INTO employees (id, name, salary, coffee_stand) VALUES (?, ?, ?, ?)
           """, [employee.id, employee.name, employee.salary, employee.coffee_stand])

    def find(self, employee_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, salary, coffee_stand FROM employees WHERE id = ?
        """, [employee_id])
        return Employee(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        employee = c.execute(""" SELECT * FROM employees ORDER BY id """).fetchall()
        return [Employee(*row) for row in employee]


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, contact_information) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.contact_information])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, contact_information FROM suppliers WHERE id = ?
        """, [supplier_id])

        return Supplier(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        suppliers = c.execute(""" SELECT * FROM suppliers ORDER BY id """).fetchall()
        return [Supplier(*row) for row in suppliers]

class _Products:

    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
               INSERT INTO products (id, description, price, quantity) VALUES (?, ?, ?, ?)
           """, [product.id, product.description, product.price, product.quantity])

    def find(self, product_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, description, price, quantity FROM products WHERE id = ?
        """, [product_id])

        return Product(*c.fetchone())

    def update(self, quantity, product_id):
        self._conn.execute("""
            UPDATE products SET quantity=(?) WHERE id=(?)
            """, [quantity, product_id])
        self._conn.commit()

    def find_all(self):
        c = self._conn.cursor()
        products = c.execute(""" SELECT * FROM products ORDER BY id """).fetchall()
        return [Product(*row) for row in products]


class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
               INSERT INTO coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
           """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def find(self, coffee_stand_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, number_of_employees FROM coffee_stands WHERE id = ?
        """, [coffee_stand_id])

        return Coffee_stand(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        coffee_stand = c.execute(""" SELECT * FROM coffee_stands ORDER BY id """).fetchall()
        return [Coffee_stand(*row) for row in coffee_stand]

class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activitie):
        self._conn.execute("""
               INSERT INTO activities (product_id, quantity, activator_id, date) VALUES (?, ?, ?, ?)
           """, [activitie.product_id, activitie.quantity, activitie.activator_id, activitie.date])

    def find(self, activitie_product_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT product_id, quantity, activator_id, date FROM activities WHERE id = ?
        """, [activitie_product_id])
        return Activitie(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        activities = c.execute(""" SELECT * FROM activities ORDER BY date """).fetchall()
        return [Activitie(*row) for row in activities]


