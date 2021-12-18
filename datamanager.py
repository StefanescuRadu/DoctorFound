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


@database_common.connection_handler
def give_premium(cursor, email):
    query = """
        UPDATE users
        SET premium_expiration = %(future_date)s
        WHERE email = %(email)s;
        """
    details = {'email': email,
               'future_date': util.get_future_datetime()}
    cursor.execute(query, details)


@database_common.connection_handler
def check_if_cabinet_exists(cursor, place_id):
    query = """
        SELECT place_id FROM cabinets
        WHERE place_id = %(place_id)s
        """
    place_id = {
        'place_id': place_id
    }
    cursor.execute(query, place_id)
    return cursor.fetchall()


@database_common.connection_handler
def add_cabinet(cursor, location):
    query = """
        INSERT INTO cabinets(
        formatted_address, place_id, name, rating, geometry, temp_distance)
        VALUES (%(formatted_address)s, %(place_id)s, %(name)s, %(rating)s, %(geometry)s, %(temp_distance)s
        )
        """
    values = {
        'formatted_address': location['formatted_address'],
        'place_id': location['place_id'],
        'name': location['name'],
        'rating': location['rating'],
        'geometry': location['geometry'],
        'temp_distance': location['temp_distance']
    }
    cursor.execute(query, values)