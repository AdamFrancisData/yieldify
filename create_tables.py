import psycopg2
from sql_queries import create_table_queries
import argparse


def create_database(db):
    '''Creates a connection to the yieldify database. End of function returns cursor with connection'''
    # connect to default database
    database_name = db
    conn = psycopg2.connect("host=127.0.0.1 dbname=yieldify")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create yieldify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS {}".format(db))
    cur.execute("CREATE DATABASE {} WITH ENCODING 'utf8' TEMPLATE template0".format(database_name))

    # close connection to default database
    conn.close()

    # connect to yieldify database
    conn = psycopg2.connect("host=127.0.0.1 dbname={}".format(database_name))
    cur = conn.cursor()

    return cur, conn


def create_tables(cur, conn):
    '''Creates tables specified in the create_table_queries object'''
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main(db):
    """ Function which drops and re-create yieldifydb database and all relevant tables.
        Usage: python create_tables.py
    """
    cur, conn = create_database(db)

    create_tables(cur, conn,)

    conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create table for live or testing')
    parser.add_argument("--table", default="yieldifydb", choices=["yieldifydb", "yieldifydb_test"], type=str,
                        help="Create either 'yieldifydb' or 'yieldifydb_test")
    args = parser.parse_args()
    db = args.table
    print(db)
    main(db)
