from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', message='')

@app.route('/movie', methods=['POST'])
def movie():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        title = request.form['title']
        genre = request.form['genre']
        print('Trying to add "' + title + '", in genre "' + genre + '"')
        cursor.execute('INSERT INTO movies (title, genre) VALUES (?,?)', (title, genre))
        connection.commit()
        message = 'Title "' + title + '" added to database'
    except:
        connection.rollback()
        mesage = 'Nothing added'
    finally:
        connection.close()
        return render_template('home.html', message = message)

@app.route('/movies')
def movies():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT * FROM movies')
        results = jsonify(cursor.fetchall())
        connection.close()
    except:
        results = 'Couldn\'t find movies'
    finally:
        return results

@app.route('/search')
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    try:
        title = request.args['title']
        print('Searching database for ' + title)
        cursor.execute('SELECT * FROM movies WHERE title IS ?', (title,))
        print('Search successful')
        results = jsonify(cursor.fetchall())
    except:
        results = 'Couldn\'t find movies'
    finally:
        connection.close()
        return results
