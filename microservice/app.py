from flask import Flask, request, jsonify
from models.db import execute_query
from models.db import get_db_connection
from dotenv import load_dotenv
from datetime import time
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# API Endpoints

# Get all routes
@app.route('/api/route', methods=['GET'])
def get_routes():
    try:
        print("Attempting to connect to the database...")  # Debug log
        conn = get_db_connection()
        if not conn:
            print("Database connection failed")
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        print("Database connection successful")  # Debug log

        # Test query
        cursor.execute("SELECT 1")
        print("Test query executed successfully")  # Debug log

        # Fetch routes
        cursor.execute("SELECT * FROM CW1.Route")  # Update schema if necessary
        print("Executed query: SELECT * FROM CW1.Route")  # Debug log

        routes = []
        for row in cursor.fetchall():
            routes.append({
                "Name": row[0],
                "Length": row[1],
                    "EstTime": row[2].strftime("%H:%M:%S") if isinstance(row[2], time) else row[2],  # Convert time to string
                "ElevationGain": row[3]
            })

        cursor.close()
        conn.close()

        if not routes:
            return jsonify({"message": "No routes found"}), 404

        return jsonify(routes), 200
    except Exception as e:
        print("Error fetching routes:", str(e))  # Debug log
        return jsonify({"error": str(e)}), 500


# Add a new route
@app.route('/api/route', methods=['POST'])
def add_route():
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415
    
    try:
        data = request.get_json()
        print(f"Received data: {data}")  # Debug log

        query = """
            INSERT INTO CW1.Route (Name, Length, EstTime, ElevationGain)
            VALUES (?, ?, ?, ?)
        """
        params = (data['Name'], data['Length'], data['EstTime'], data.get('ElevationGain'))
        print(f"Executing query: {query} with params: {params}")  # Debug log
        
        result = execute_query(query, params, fetch_all=False)
        print(f"Query execution result: {result}")  # Debug log
        
        if result is not None:
            return jsonify({"message": "Route added successfully"}), 201
        return jsonify({"error": "Failed to add route"}), 500
    except Exception as e:
        print(f"Error adding route: {e}")  # Debug log
        return jsonify({"error": "Failed to add route"}), 500

# Delete a route by name
@app.route('/api/route', methods=['DELETE'])
def delete_route():
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415

    try:
        data = request.get_json()
        route_name = data.get('Name')

        if not route_name:
            return jsonify({"error": "Route name is required"}), 400

        # Query to delete the route by name
        query = "DELETE FROM CW1.Route WHERE Name = ?"
        params = (route_name,)

        result = execute_query(query, params, fetch_all=False)

        if result is not None:
            return jsonify({"message": f"Route '{route_name}' deleted successfully"}), 200
        return jsonify({"error": "Failed to delete route"}), 500
    except Exception as e:
        print(f"Error deleting route: {e}")  # Debug log
        return jsonify({"error": "Failed to delete route"}), 500

@app.route('/api/route', methods=['PUT'])
def update_route():
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type. Expected application/json"}), 415

    try:
        data = request.get_json()
        route_name = data.get('Name')

        if not route_name:
            return jsonify({"error": "Route name is required"}), 400
        
        # Prepare fields to be updated
        updates = []
        params = []

        # Check which fields are provided and build the update query dynamically
        if 'Length' in data:
            updates.append("Length = ?")
            params.append(data['Length'])
        
        if 'EstTime' in data:
            updates.append("EstTime = ?")
            params.append(data['EstTime'])
        
        if 'ElevationGain' in data:
            updates.append("ElevationGain = ?")
            params.append(data['ElevationGain'])
        
        if not updates:
            return jsonify({"error": "No fields to update provided"}), 400
        
        # Add the route name as the final parameter for the WHERE clause
        update_query = f"UPDATE CW1.Route SET {', '.join(updates)} WHERE Name = ?"
        params.append(route_name)  # This should be the last parameter

        # Execute the query
        result = execute_query(update_query, tuple(params), fetch_all=False)

        if result is not None:
            return jsonify({"message": f"Route '{route_name}' updated successfully"}), 200
        return jsonify({"error": "Failed to update route"}), 500
    except Exception as e:
        print(f"Error updating route: {e}")  # Debug log
        return jsonify({"error": "Failed to update route"}), 500




# Get all classifications
@app.route('/api/classification', methods=['GET'])
def get_classifications():
    try:
        print("Executing query to fetch classifications...")  # Debug log
        query = "SELECT * FROM CW1.Classification"  # Adjust schema if necessary
        classifications = execute_query(query)

        if classifications:
            print(f"Fetched classifications: {classifications}")  # Debug log
            return jsonify([
                {"Name": c[0], "RouteType": c[1], "Difficulty": c[2]}
                for c in classifications
            ]), 200

        print("No classifications found or query failed.")  # Debug log
        return jsonify({"error": "No classifications found"}), 404
    except Exception as e:
        print(f"Error fetching classifications: {e}")  # Debug log
        return jsonify({"error": "Failed to fetch classifications"}), 500


# Get all trail logs
@app.route('/api/traillog', methods=['GET'])
def get_trail_logs():
    query = "SELECT * FROM CW1.TrailLog"
    logs = execute_query(query)
    if logs:
        return jsonify([{"LogID": l[0], "TrailName": l[1], "AddedBy": l[2], "AddedAt": str(l[3])} for l in logs])
    return jsonify({"error": "Failed to fetch trail logs"}), 500

if __name__ == '__main__':
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)