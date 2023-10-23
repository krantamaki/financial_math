"""
Module for handling the SQL database
"""
import sqlite3 as sql
from config import *


# Global variable that holds the connection to the database
# Should only be access via the get_connection function
_connection = None


# Lists containing the table names and column names as tuples
TABLES = [("STOCK", "TICKER TEXT, PRICE REAL, VOL REAL, DRIFT REAL, DESC TEXT")]


def get_connection():
    """
    Function for accessing the global variable holding the connection to the database
    :return: Connection object
    """
    global _connection
    if _connection is None:
        _connection = sql.connect(DATABASE)

    return _connection


def get_cursor():
    """
    Function for accessing a cursor via the global variable holding the connection
    :return: Cursor object
    """
    con = get_connection()

    return con.cursor()


def check_database():
    """
    Function that checks if the required tables exists
    :return: True if tables exists False otherwise
    """
    valid = True
    cur = get_cursor()

    res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [tup[0] for tup in res.fetchall()]

    for table in TABLES:
        table_name = table[0]
        if table_name not in table_names:
            valid = False

    return valid


def init_database():
    """
    Function that initializes the database with required tables
    Won't do anything if the tables exists
    :return: Void
    """
    if check_database():
        return

    cur = get_cursor()

    for tup in TABLES:
        cur.execute(f"CREATE TABLE IF NOT EXISTS {tup[0]}({tup[1]})")


def reset_database():
    """
    Function that resets the database i.e. removes the existing tables and adds them
    back as empty
    :return: Void
    """
    cur = get_cursor()

    for tup in TABLES:
        cur.execute(f"DROP TABLE IF EXISTS {tup[0]}")
        cur.execute(f"CREATE TABLE IF NOT EXISTS {tup[0]}({tup[1]})")


# List the functions and variables accessible in other modules
__all__ = ["get_connection", "get_cursor", "check_database", "init_database", "reset_database"]

