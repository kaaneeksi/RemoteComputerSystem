from flask import Flask, request, render_template, session, redirect, url_for, flash
import sqlite3
import subprocess
import jwt
from functools import wraps
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 's3cr3t' 

app.secret_key = 'zattirizortzort'
username = 'admin'
password = 'admin'

users = {
    'admin': 'admin'
}



# Kullanıcı giriş işlemi
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form.get("username")
        form_password = request.form.get("password") 

        if form_username in users and users[form_username] == form_password:
            session['logged_in'] = True
            return redirect(url_for('mainpage'))
        else:
            flash("Invalid credentials.")
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST': 

        data = request.data.decode('utf-8')
        

        if data == 'true':
            subprocess.Popen(['python3', '-c', 'import os; os.system("python3 socket_listener.py")'])

            return "Listener started from webserver."
        elif data == 'false':
            subprocess.Popen(['killall', 'socket_listener.py'])
            return "Listener already stopped."
            
        else:
            return "Unknown command."        

    return render_template('mainpage.html')

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

@app.route('/attacks', methods=['GET', 'POST'])
def attacks():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    return render_template('attacks.html')



if __name__ == '__main__':
    app.run(debug=True, port=5555)