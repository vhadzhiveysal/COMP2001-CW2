# COMP2001-CW2

<ins>**Introduction**</ins>  
The Trail Application Micro-Service exposes a set of API endpoints that allow clients (e.g., web or mobile applications) to retrieve hiking trail data stored in a SQL Server database. The micro-service provides an endpoint to fetch trail information and return it in a JSON format.

<ins>**Features**</ins>  
Access to detailed trail information, including name, length, estimated time, and elevation gain.
RESTful architecture that allows for easy integration with other components of the Trail Application.
Simple error handling and response structures.

<ins>**Technologies**</ins>  
This micro-service is built using the following technologies:

**Python**: The primary programming language for building the micro-service.  
**Flask**: A micro web framework in python for building the REST API.  
**SQL Server**: The database used to store trail data.  
**PyODBC**: A Python library for connecting to SQL Server databases.  
**Postman**: API platform software.  
**Microsoft ODBC Driver 18 for SQL Server**: DLL which connects to SQL Server.  
**Docker**: Platform that delivers software in containers.  

You will need these technologies to be able to run the solution.

<ins>**Running the solution**</ins>

Open `app.py` using Python, copy the url in cmd, specifically the 'Running on ...' line to Postman. Then in app.py, copy and paste the parameters for each function listed to the URL on Postman, and match the api method as well to run each command.  
For example, running `[GET] http://127.0.0.1:5000/api/route` on Postman would run the `get_routes()` function on app.py.  

When adding a new route/trail, be sure to set the 'Content-Type' header to 'application/json' first.  
*(On Postman, head to the Headers tab, add this key-value pair:  
Key: `Content-Type`  
Value: `application/json`)*  
Then navigate to the Body tab, and follow a template like this to add a new route:  

```
{
  "Name": "Test Trail",
  "Length": 3.4,
  "EstTime": "01:00:00",
  "ElevationGain": 100
}
```  
***Note: The `name` acts as a primary key in the routes table, therefore duplicates of names cannot exist in the table, and any effort to make it so will result in an error.***

When deleting a route/trail, navigate to the Body tab, and follow a template like this to delete a route:  
```
{
  "Name": "Test Trail"
}
```  

When updating a route/trail, follow the same template as you would with adding a new route, but make sure the `Name` is the same as an existing route/trail.
