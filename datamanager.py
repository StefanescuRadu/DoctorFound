import database_common
import util


@database_common.connection_handler
def add_user(cursor, email):
    query = """
        INSERT INTO users VALUES(
        %(email)s, %(expiration_date)s)
        """
    details = {
        'email': email,
        'expiration_date': '2002-12-27'
    }
    cursor.execute(query, details)


@database_common.connection_handler
def check_if_user_exists(cursor, email):
    query = """
        SELECT email FROM users
        WHERE email = %(email)s
        """
    email = {'email': email}
    cursor.execute(query, email)
    return cursor.fetchall()


@database_common.connection_handler
def check_if_premium(cursor, email):
    query = """
        SELECT premium_expiration FROM users
        WHERE email = %(email)s
        """
    email = {'email': email}
    cursor.execute(query, email)
    return cursor.fetchall()