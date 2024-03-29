# Shopping List App
The Shopping List App is a web application built with Flask, PostgreSQL, and Excel to manage a list of shopping items. Users can add, remove, and clear items from the list.

# Features(CRUD)

- Add Items: Users can add items to the shopping list along with their respective weights (in kilograms).
- Remove Items: Users can remove items from the shopping list.
- Clear List: Users can clear the entire shopping list.
- Data Persistence: Shopping list items are stored in a PostgreSQL database, ensuring that they persist across sessions.

# Database Structure
- The application uses a PostgreSQL database named lista_compras with a table named compras:

* id: Serial primary key for each item.
* item: Name of the item (VARCHAR).
* kg: Weight of the item in kilograms (FLOAT).

# Excel Integration

* In addition to the PostgreSQL database, the application also integrates with an Excel file to store files. However, this integration is not implemented in the provided code.

# Usage

- To use the Shopping List App:

- Run the Flask application (app.py) on your local machine.
- Open a web browser and navigate to http://localhost:5000.
- Use the interface to add, remove, or clear items from the shopping list.

# Dependencies

The application relies on the following dependencies:

- Flask: A micro web framework for Python.
- psycopg2: PostgreSQL adapter for Python.

# Setup

- Install Python, Flask, and psycopg2 on your system.
- Ensure that PostgreSQL is installed and running on your machine.
- Create a database named lista_compras in PostgreSQL.
- Update the database connection details (host, port, user, password) in the app.py file.
- Run the app.py file to start the Flask application.