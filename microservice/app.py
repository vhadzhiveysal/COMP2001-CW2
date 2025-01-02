from flask import Flask, request, jsonify
from models.db import execute_query
from models.db import get_db_connection
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API Endpoints

# Get all routes
@app.route('/api/route', methods=['GET'])
def get_routes():
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CW1.Route")  # Update schema if necessary
        routes = [
            {
                "Name": row[0],
                "Length": row[1],
                "EstTime": row[2],
                "ElevationGain": row[3]
            }
            for row in cursor.fetchall()
        ]
        cursor.close()
        conn.close()

        if not routes:
            return jsonify({"message": "No routes found"}), 404

        return jsonify(routes), 200
    except Exception as e:
        print("Error fetching routes:", str(e))  # Debug log
        return jsonify({"error": "Failed to fetch routes"}), 500

# Add a new route
@app.route('/api/route', methods=['POST'])
def add_route():
    data = request.get_json()
    query = """
        INSERT INTO Route (Name, Length, EstTime, ElevationGain)
        VALUES (?, ?, ?, ?)
    """
    params = (data['Name'], data['Length'], data['EstTime'], data.get('ElevationGain'))
    result = execute_query(query, params, fetch_all=False)
    if result is not None:
        return jsonify({"message": "Route added successfully"}), 201
    return jsonify({"error": "Failed to add route"}), 500

# Get all classifications
@app.route('/api/classification', methods=['GET'])
def get_classifications():
    query = "SELECT * FROM Classification"
    classifications = execute_query(query)
    if classifications:
        return jsonify([{"Name": c[0], "RouteType": c[1], "Difficulty": c[2]} for c in classifications])
    return jsonify({"error": "Failed to fetch classifications"}), 500

# Get all trail logs
@app.route('/api/traillog', methods=['GET'])
def get_trail_logs():
    query = "SELECT * FROM TrailLog"
    logs = execute_query(query)
    if logs:
        return jsonify([{"LogID": l[0], "TrailName": l[1], "AddedBy": l[2], "AddedAt": str(l[3])} for l in logs])
    return jsonify({"error": "Failed to fetch trail logs"}), 500

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)