from flask import Flask, render_template, request, redirect

from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] =  "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = 'toteinventory'

mysql = MySQL(app)

@app.route('/')
def admin():
    
    conn = mysql.connection.cursor()
    items = conn.execute("SELECT * from items")

    if items > 0:
        itemDetails = conn.fetchall()
        return render_template('admin.html', itemDetails=itemDetails)

    return render_template('admin.html')


@app.route('/add', methods=['GET', 'POST'])
def addItems():
    
    if request.method == 'POST':
        picture = request.form['picture']
        name = request.form['name']
        style = request.form['style']
        color = request.form['color']
        collection = request.form['collection']
        amount = request.form['amount']
        price = request.form['price']
        
        conn = mysql.connection.cursor()
        conn.execute("INSERT INTO items(picture, name, style, color, collection, amount, price) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                     (picture, name, style, color, collection, amount, price))
        mysql.connection.commit()
        conn.close()

        return redirect('/')

    return render_template('add.html')


@app.route('/edit', methods=['GET', 'POST'])
def editItems():

    if request.method == 'POST':
        itemID = request.form['itemID']
        picture = request.form['picture']
        name = request.form['name']
        style = request.form['style']
        color = request.form['color']
        collection = request.form['collection']
        amount = request.form['amount']
        price = request.form['price']
        
        conn = mysql.connection.cursor()
        conn.execute("UPDATE items SET picture = %s, name = %s, style = %s, color = %s, collection = %s, amount = %s, price = %s WHERE itemID = %s", 
                     (picture, name, style, color, collection, amount, price, itemID))
        mysql.connection.commit()
        conn.close()

        return redirect('/')
    return render_template('edit.html')


@app.route('/delete', methods=['GET', 'POST'])
def deleteItems():

    if request.method == 'POST':
        itemID = request.form['itemID']

        conn = mysql.connection.cursor()
        conn.execute("DELETE FROM items WHERE itemID = %s",[itemID])
        mysql.connection.commit()
        conn.close()
        return redirect('/')
    return render_template('delete.html')

if __name__ == "__main__":
    app.run(debug=True)