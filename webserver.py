from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3

app = Flask(__name__)

app.secret_key = 'zattirizortzort'
username = 'admin'
password = 'admin'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form.get("username")
        form_password = request.form.get("password") 

        if form_username == username and form_password == password:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('giris bilgileri yanlis')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        conn = sqlite3.connect('database.db')
        col = int(request.form.get('delete'))
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM commands WHERE id = ?;''', (col,))
        conn.commit()
        conn.close()

        return redirect(url_for('dashboard'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM commands''')
    rows = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)