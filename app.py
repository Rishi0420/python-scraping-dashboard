from flask import Flask, jsonify, render_template
import sqlite3

# Initialize the Flask application
app = Flask(__name__)

# --- Configuration ---
# Path to the SQLite database file
DATABASE_PATH = 'laptops.db'


def get_db_connection():
    """
    Creates a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    # This allows us to access columns by name (like a dictionary)
    conn.row_factory = sqlite3.Row
    return conn

# --- API Endpoint ---


@app.route('/api/laptops')
def get_laptops_data():
    """
    API endpoint to fetch all laptop data from the database.
    Returns data in JSON format.
    """
    conn = get_db_connection()
    # Query the database to get all records from the 'laptops' table
    laptops = conn.execute('SELECT * FROM laptops').fetchall()
    conn.close()

    # Convert the list of database rows into a list of dictionaries
    # This makes it easy to convert to JSON
    laptops_list = [dict(row) for row in laptops]

    # Return the data as a JSON response
    return jsonify(laptops_list)

# --- Frontend Route ---


@app.route('/')
def index():
    """
    Serves the main HTML page for the dashboard.
    """
    # We will create this 'index.html' file in the next step
    return render_template('index.html')


# To run the Flask application
if __name__ == '__main__':
    # debug=True will auto-reload the server when you make changes
    app.run(debug=True)
