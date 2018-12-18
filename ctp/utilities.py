import psycopg2

def create_user_symbol(asset, base_ccy):
    """ Create the generic symbol that will be used in all price dictionaries as
    opposed to the specific symbols that are specific for each exchange
    """
    return (asset+base_ccy).upper()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = psycopg2.connect(host="localhost", database="tradereg", user="postgres", password="2727671")
        return conn
    except Error as e:
        print(e)

    return None

class Error(Exception):
    pass
