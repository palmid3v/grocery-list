from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='grocery_shopping',
    user='postgres',
    password='Paaccaal96#!.'
)

# you should create first=database then tabble

def check_database():
    cursor = conn.cursor()
    cursor.execute("SELECT item, kg FROM groceries")
    existing_items = cursor.fetchall()
    cursor.close()
    if existing_items:
        return existing_items
    else:
        return []


def clear_database():
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groceries")
    conn.commit()
    cursor.close()


def insert_item(item, kg):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groceries (item, kg) VALUES (%s, %s)", (item, kg))
    conn.commit()
    cursor.close()


def remove_item(item):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM groceries WHERE item = %s", (item,))
    conn.commit()
    cursor.close()


@app.route('/')
def index():
    existing_items = check_database()
    return render_template('index.html', items=existing_items, message=request.args.get('message'))  # Updated this line



@app.route('/add', methods=['POST'])
def add_item():
    item_compra = request.form.get('item')
    kg_compra = request.form.get('kg')

    existing_items = check_database()

    if item_compra in [item[0] for item in existing_items]:
        return redirect(url_for('index', message='Item already exists in the list.'))  # Updated this line

    try:
        kg_compra = float(kg_compra)
    except ValueError:
        kg_compra = 0

    insert_item(item_compra, kg_compra)
    return redirect(url_for('index'))




@app.route('/remove', methods=['POST'])
def remove():
    item = request.form.get('item')
    remove_item(item)
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
    clear_database()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)