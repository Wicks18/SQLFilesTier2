import sqlite3

def connection(db):
    conn = sqlite3.connect(db)
    return conn
def Q1():
    cur = conn.cursor()
    query = """
        SELECT name
        FROM facilities
        WHERE membercost = '0'
        """
    cur.execute(query)
    num_fields = len(cur.description)
    field_names = [i[0] for i in cur.description]
    print(field_names)
    rows = cur.fetchall()
    print("Q1")
    for row in rows:
        print(row)

def Q2():
    cur = conn.cursor()
    query = """
        SELECT COUNT(name)
        FROM facilities
        WHERE membercost = '0';
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q2")
    for row in rows:
        print(row)

def Q3():
    cur = conn.cursor()
    query = """
        SELECT facid, name, membercost, monthlymaintenance
        FROM facilities
        WHERE membercost > '0' AND membercost < (monthlymaintenance * .2);
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q3")
    for row in rows:
        print(row)

def Q4():
    cur = conn.cursor()
    query = """
        SELECT *
        FROM facilities
        WHERE facid = '1' OR facid = '5';
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q4")
    for row in rows:
        print(row)

def Q5():
    cur = conn.cursor()
    query = """
        SELECT name, monthlymaintenance,
        CASE WHEN monthlymaintenance <= '100' THEN 'cheap'
             ELSE 'expensive' END AS 'label'
        FROM facilities;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q5")
    for row in rows:
        print(row)

def Q6():
    cur = conn.cursor()
    query = """
        SELECT firstname, surname
        FROM members
        WHERE joindate IN
            (SELECT MAX(joindate)
            FROM members);
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q6")
    for row in rows:
        print(row)

def Q7():
    cur = conn.cursor()
    query = """
        SELECT DISTINCT (m.firstname || ' ' || m.surname) AS name, f.name as court
        FROM bookings AS b
            JOIN facilities AS f
                ON (b.facid = f.facid)
            JOIN members AS m
                ON (b.memid = m.memid)
        WHERE f.name LIKE 'Tennis Court%'
        ORDER BY name;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q7")
    for row in rows:
        print(row)

def Q8():
    cur = conn.cursor()
    query = """
        SELECT (m.firstname || ' ' || m.surname) AS name, f.name as facility,
        CASE WHEN b.memid = 0 THEN (b.slots * f.guestcost)
             ELSE (b.slots * f.membercost) END AS cost
        FROM bookings AS b
            JOIN facilities AS f
                ON (b.facid = f.facid)
            JOIN members AS m
                ON (b.memid = m.memid)
        WHERE b.starttime LIKE '2012-09-14%' AND (
            (b.memid = 0 AND (b.slots * f.guestcost) > 30)
            OR
            (b.memid != 0 AND (b.slots * f.membercost) > 30)
            )
        ORDER BY cost DESC;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q8")
    for row in rows:
        print(row)

def Q9():
    cur = conn.cursor()
    query = """
        SELECT (m.firstname || ' ' || m.surname) AS name, f.name as facility,
        CASE WHEN b.memid = 0 THEN (b.slots * f.guestcost)
             ELSE (b.slots * f.membercost) END AS cost
        FROM bookings AS b
            JOIN facilities AS f
                ON (b.facid = f.facid)
            JOIN members AS m
                ON (b.memid = m.memid)
        WHERE b.bookid IN 
                (SELECT bookid
                 FROM bookings
                 WHERE starttime LIKE '2012-09-14%') 
            AND (
                (b.memid = 0 AND (b.slots * f.guestcost) > 30)
                OR
                (b.memid != 0 AND (b.slots * f.membercost) > 30)
                )
        ORDER BY cost DESC;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q9")
    for row in rows:
        print(row)

#['facid', 'name', 'membercost', 'guestcost', 'initialoutlay', 'monthlymaintenance']
#['memid', 'surname', 'firstname', 'address', 'zipcode', 'telephone', 'recommendedby', 'joindate']
#['bookid', 'facid', 'memid', 'starttime', 'slots']

def Q10():
    cur = conn.cursor()
    query = """
        SELECT f.name as court,
            SUM(
                CASE WHEN b.memid = 0 THEN (b.slots * f.guestcost)
                    ELSE (b.slots * f.membercost) END
            ) AS total_revenue
        FROM bookings AS b
            JOIN facilities AS f
                ON (b.facid = f.facid)
        GROUP BY court
        HAVING total_revenue < 1000
        ORDER BY total_revenue;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q10")
    for row in rows:
        print(row)

def Q11():
    cur = conn.cursor()
    query = """
        SELECT (m1.firstname || ' ' || m1.surname) AS member, (m2.firstname || ' ' || m2.surname) AS recommended_by
        FROM members AS m1
        LEFT JOIN members AS m2
            ON (m1.recommendedby = m2.memid)
        ORDER BY m1.surname
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q11")
    for row in rows:
        print(row)

def Q12():
    cur = conn.cursor()
    query = """
        SELECT f.name AS facility_name, COUNT(b.memid) AS member_usage
        FROM bookings AS b
            JOIN facilities AS f 
                ON (b.facid = f.facid)
        WHERE b.memid != 0
        GROUP BY f.name
        ORDER BY member_usage DESC;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q12")
    for row in rows:
        print(row)

def Q13():
    cur = conn.cursor()
    query = """
        SELECT f.name AS facility, COUNT(b.memid) AS member_usage,
            CASE WHEN strftime('%m', b.starttime) = '07' THEN 'july'
                 WHEN strftime('%m', b.starttime) = '08' THEN 'august'
                 ELSE 'september' END AS month
        FROM bookings AS b
            JOIN facilities AS f 
                ON (b.facid = f.facid)
        WHERE b.memid != 0
        GROUP BY facility, month
        ORDER BY facility, month;
        """
    cur.execute(query)
    rows = cur.fetchall()
    print("Q13")
    for row in rows:
        print(row)

db = "sqlite_db_pythonsqlite.db"
conn = connection(db)
Q1()
Q2()
Q3()
Q4()
Q5()
Q6()
Q7()
Q8()
Q9()
Q10()
Q11()
Q12()
Q13()