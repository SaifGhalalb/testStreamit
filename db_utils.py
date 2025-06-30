
import sqlite3
import pandas as pd

def get_connection():
    return sqlite3.connect('umrah.db', check_same_thread=False)

# ------------------ PACKAGES ------------------ #
def get_all_packages():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM packages', conn)
    conn.close()
    return df

def add_package(name, price, hotel, duration, transport):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO packages (name, price, hotel, duration_days, transport) VALUES (?, ?, ?, ?, ?)',
              (name, price, hotel, duration, transport))
    conn.commit()
    conn.close()

# ------------------ TRAVELLERS (Users List) ------------------ #
def add_traveller(data):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
        INSERT INTO travellers (user_id, name, passport_number, nationality, dob, phone, email, emergency_contact, handled_by)
        VALUES (:user_id, :name, :passport_number, :nationality, :dob, :phone, :email, :emergency_contact, :handled_by)
    ''', data)
    conn.commit()
    conn.close()

def get_travellers():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM travellers', conn)
    conn.close()
    return df

# ------------------ HOTELS ------------------ #
def add_hotel(name, city, rating):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO hotels (name, city, rating) VALUES (?, ?, ?)', (name, city, rating))
    conn.commit()
    conn.close()

def get_hotels():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM hotels', conn)
    conn.close()
    return df

# ------------------ GUIDES ------------------ #
def add_guide(name, phone, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO guides (name, phone, email) VALUES (?, ?, ?)', (name, phone, email))
    conn.commit()
    conn.close()

def get_guides():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM guides', conn)
    conn.close()
    return df

# ------------------ TRIPS & BUSES ------------------ #
def add_trip(package_id, trip_date, price, hotel_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO trips (package_id, trip_date, price, hotel_id) VALUES (?, ?, ?, ?)',
              (package_id, trip_date, price, hotel_id))
    conn.commit()
    conn.close()

def get_trips():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT t.*, p.name as package_name, h.name as hotel_name
        FROM trips t
        JOIN packages p ON t.package_id = p.id
        LEFT JOIN hotels h ON t.hotel_id = h.id
    """, conn)
    conn.close()
    return df

def add_bus(trip_id, bus_number, capacity, guide_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO buses (trip_id, bus_number, capacity, guide_id) VALUES (?, ?, ?, ?)',
              (trip_id, bus_number, capacity, guide_id))
    conn.commit()
    conn.close()

def get_buses():
    conn = get_connection()
    df = pd.read_sql_query('''
        SELECT b.*, g.name as guide_name, t.trip_date
        FROM buses b
        LEFT JOIN guides g ON b.guide_id = g.id
        JOIN trips t ON b.trip_id = t.id
    ''', conn)
    conn.close()
    return df

# ------------------ BOOKINGS ------------------ #
def create_booking(user_id, package_id, travel_date, payment_method, bus_id=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO bookings (user_id, package_id, travel_date, payment_method, bus_id) VALUES (?, ?, ?, ?, ?)',
              (user_id, package_id, travel_date, payment_method, bus_id))
    booking_id = c.lastrowid
    conn.commit()
    conn.close()
    return booking_id

def save_booking_file(booking_id, file_path):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO booking_files (booking_id, file_path) VALUES (?, ?)', (booking_id, file_path))
    conn.commit()
    conn.close()

def get_user_bookings(user_id):
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT b.id, p.name AS package, b.travel_date, b.status, b.payment_method, bu.bus_number
        FROM bookings b
        JOIN packages p ON b.package_id = p.id
        LEFT JOIN buses bu ON b.bus_id = bu.id
        WHERE b.user_id = ?
    """, conn, params=(user_id,))
    conn.close()
    return df

def get_all_bookings():
    conn = get_connection()
    df = pd.read_sql_query(
        """
        SELECT b.id,
               u.name   AS user_name,
               p.name   AS package_name,
               t.id     AS trip_id,          -- <-- add!
               t.trip_date,
               b.payment_method,
               b.status,
               bu.bus_number,
               g.name   AS guide_name
        FROM bookings b
        JOIN users   u  ON b.user_id   = u.id
        JOIN packages p ON b.package_id = p.id
        LEFT JOIN buses  bu ON b.bus_id = bu.id
        LEFT JOIN trips  t  ON bu.trip_id = t.id
        LEFT JOIN guides g  ON bu.guide_id = g.id
        """,
        conn,
    )
    conn.close()
    return df


def update_booking_status(booking_id, new_status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE bookings SET status=? WHERE id=?', (new_status, booking_id))
    conn.commit()
    conn.close()

# ------------------ SUPPORT ------------------ #
def create_support_request(user_id, issue):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO support_requests (user_id, issue) VALUES (?, ?)', (user_id, issue))
    conn.commit()
    conn.close()

def get_user_support(user_id):
    conn = get_connection()
    df = pd.read_sql_query('SELECT id, issue, status, created_at FROM support_requests WHERE user_id=?',
                           conn, params=(user_id,))
    conn.close()
    return df

def get_all_support():
    conn = get_connection()
    df = pd.read_sql_query('SELECT * FROM support_requests', conn)
    conn.close()
    return df

def update_support_status(ticket_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute('UPDATE support_requests SET status=? WHERE id=?', (status, ticket_id))
    conn.commit()
    conn.close()

# ------------------ LOGGING ------------------ #
def log_activity(user_id, action):
    conn = get_connection()
    c = conn.cursor()
    c.execute('INSERT INTO activity_log (user_id, action) VALUES (?, ?)', (user_id, action))
    conn.commit()
    conn.close()
def update_row(table, row_id: int, fields: dict):
    conn = get_connection(); c = conn.cursor()
    cols = ", ".join([f"{k}=?" for k in fields.keys()])
    c.execute(f"UPDATE {table} SET {cols} WHERE id=?", (*fields.values(), row_id))
    conn.commit(); conn.close()

def delete_row(table, row_id: int):
    conn = get_connection(); conn.execute(f"DELETE FROM {table} WHERE id=?", (row_id,))
    conn.commit(); conn.close()

def get_connection():  # keep as-is, just reminder
    return sqlite3.connect("umrah.db", check_same_thread=False)
