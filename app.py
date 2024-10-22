from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import barcode
from barcode.writer import ImageWriter
import os
# import qrcode
# import os

app = Flask(__name__)

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='grocery_shopping',
    user='postgres',
    password='newpassword'  # Update the password here
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

# BARCODE GENERATOR
def insert_item(item, kg):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO groceries (item, kg) VALUES (%s, %s)", (item, kg))
    conn.commit()
    cursor.close()

    # Generate a barcode based on item name
    barcode_format = barcode.get_barcode_class('code128')  # You can also use 'ean13', 'code39', etc.
    barcode_data = f'{item}-{kg}'  # You can modify the data stored in the barcode

    # Generate the barcode and save it as an image
    barcode_image = barcode_format(barcode_data, writer=ImageWriter())
    
    # Ensure the directory exists
    if not os.path.exists('static/barcodes'):
        os.makedirs('static/barcodes')
        
    # Save the barcode image as PNG
    barcode_image.save(f'static/barcodes/{item}')
# BARCODE GENERATOR

# QR CODE GENERATOR
# Modify the insert_item function to generate a QR code
# def insert_item(item, kg):
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO groceries (item, kg) VALUES (%s, %s)", (item, kg))
#     conn.commit()
#     cursor.close()

#     # Generate a QR code based on item and kg
#     data = f'Item: {item}, Weight: {kg} kg'
#     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#     qr.add_data(data)
#     qr.make(fit=True)

#     # Create an image from the QR code
#     img = qr.make_image(fill='black', back_color='white')

#     # Save the image in the static folder
#     if not os.path.exists('static/qrcodes'):
#         os.makedirs('static/qrcodes')
#     img.save(f'static/qrcodes/{item}.png')
# QR CODE GENERATOR


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