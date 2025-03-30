from flask import Blueprint, request, jsonify, session
import pymysql
from database import get_db_connection

auth_bp = Blueprint('auth', __name__)

# 🔹 User Registration (Stores plain text password)
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', 
                           (username, password))
            connection.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except pymysql.IntegrityError:
        return jsonify({"error": "Username already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection:
            connection.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        print("Received login request:", data)

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        connection = get_db_connection()
        if not connection:
            return jsonify({"error": "Database connection failed"}), 500
        
        print("Database connection successful!")

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # ✅ Ensures we get a dictionary
            cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
            user = cursor.fetchone()
        
        print("User fetched from DB:", user)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        stored_password = user["password"]  # ✅ Access by key instead of index
        print(f"Stored Password: {stored_password}, Entered Password: {password}")

        if password == stored_password:  # No hashing used
            session['loggedin'] = True
            session['username'] = username
            print("Login successful!")
            return jsonify({"message": "Login successful!"})
        else:
            print("Invalid password!")
            return jsonify({"error": "Invalid password"}), 401
    except Exception as e:
        print("Exception occurred:", str(e))
        return jsonify({"error": str(e)}), 500
    finally:
        if 'connection' in locals():
            connection.close()
            print("Database connection closed.")


# 🔹 User Logout
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully!"}), 200
