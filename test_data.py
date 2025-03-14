import sqlite3
import SQL

def insert_test_data():
    connect_db = sqlite3.connect('database.db')
    cursor = connect_db.cursor()
    
    # Insert admin user
    admin_user = ('admin1', 'admin1', 'admin@example.com', 'Admin', 'User', 'Admin Org', 'Admin', '00000')
    try:
        cursor.execute("""
            INSERT INTO user_details 
            (username, password, e_mail, fname, sname, org_school_name, account_type, id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, admin_user)
    except sqlite3.IntegrityError:
        print(f"Admin user {admin_user[0]} already exists")
    
    # Insert test users
    test_users = [
        ('testuser1', 'password123', 'test1@example.com', 'John', 'Doe', 'Test School 1', 'Student', '12345'),
        ('testuser2', 'password456', 'test2@example.com', 'Jane', 'Smith', 'Test School 2', 'Teacher', '67890')
    ]
    
    for user in test_users:
        try:
            cursor.execute("""
                INSERT INTO user_details 
                (username, password, e_mail, fname, sname, org_school_name, account_type, id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, user)
        except sqlite3.IntegrityError:
            print(f"User {user[0]} already exists")
    
    # Insert test organizations
    test_orgs = [
        ('testorg1', 'orgpass123', 'org1@example.com', 'Test Organization 1', 'Admin'),
        ('testorg2', 'orgpass456', 'org2@example.com', 'Test Organization 2', 'Admin')
    ]
    
    for org in test_orgs:
        try:
            cursor.execute("""
                INSERT INTO org_details 
                (username, password, e_mail, org_school_name, account_type)
                VALUES (?, ?, ?, ?, ?)
            """, org)
        except sqlite3.IntegrityError:
            print(f"Organization {org[0]} already exists")
    
    connect_db.commit()
    connect_db.close()
    print("Test data inserted successfully!")

if __name__ == "__main__":
    SQL.check_db()  # Ensure database exists
    insert_test_data() 