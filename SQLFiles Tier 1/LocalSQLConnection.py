import sqlite3
from sqlite3 import Error

 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
 
    return conn

 
def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query1 = """
        SELECT *
        FROM FACILITIES
        """
    cur.execute(query1)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def Query2(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query = """
    WITH sub AS (
    SELECT *,
        CASE 
            WHEN m.memid = 0 THEN f.guestcost * b.slots
            ELSE f.membercost * b.slots 
        END AS booking_cost
    FROM Bookings AS b
    JOIN Facilities AS f
    ON b.facid = f.facid
    JOIN Members AS m
    ON b.memid = m.memid
    ) 
    SELECT name, SUM(booking_cost) AS revenue
    FROM sub
    GROUP BY name 
    HAVING revenue < 1000
    ORDER BY revenue DESC
    """
    cur.execute(query)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def Query3(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query = """
    SELECT  m1.surname || ', ' || m1.firstname AS recommended, m2.surname || ', ' || m2.firstname AS recommender
    FROM Members AS m1
    JOIN Members AS m2
    ON m1.recommendedby = m2.memid
    ORDER BY m1.surname, m1.firstname
    """
    cur.execute(query)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def Query4(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query = """
    SELECT f.name, 
    ROUND(100.0 * SUM(slots)/
    (
        SELECT SUM(slots)
        FROM Bookings
        WHERE memid != 0
    ), 2) AS percentage_of_usage_by_members
    FROM Bookings as b
    LEFT JOIN Facilities as f
    ON b.facid = f.facid
    WHERE memid != 0
    GROUP BY f.name
    """
    cur.execute(query)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)

def Query5(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    
    query = """
    SELECT strftime('%m',b.starttime) AS month, f.name,
    ROUND(100.0 * SUM(slots)/
    (
        SELECT SUM(slots)
        FROM Bookings
        
    ), 2) AS percentage_of_usage_by_members
    FROM Bookings as b
    LEFT JOIN Facilities as f
    ON b.facid = f.facid
    WHERE memid != 0
    GROUP BY month, f.name
    """
    cur.execute(query)
 
    rows = cur.fetchall()
 
    for row in rows:
        print(row)


def main():
    database = "sqlite_db_pythonsqlite.db"
 
    # create a database connection
    conn = create_connection(database)
    with conn: 
        print("2. Query all tasks")
        #select_all_tasks(conn)
        Query5(conn)
 
 
if __name__ == '__main__':
    main()