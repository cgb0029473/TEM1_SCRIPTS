from flask import Flask,redirect,render_template, request, jsonify,url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Univalle'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def student_list_json():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return json.dumps(data)

@app.route('/studentlist', methods=['GET'])
def student_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, first_name, last_name, city, semester FROM student')
    data = cursor.fetchall()
    return render_template('list.html', students=data)

@app.route('/studentcreate', methods=['GET'])
def student_create():
    return render_template('create.html')

@app.route('/studentcreate', methods=['POST'])
def student_create_json():
    if request.method == 'POST':
        first_name=request.form['first_name']
        last_name=request.form['last_name']
        city=request.form['city']
        semester=request.form['semester']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO student (first_name,last_name,city,semester)VALUES (%s,%s,%s,%s)",
        (first_name,last_name,city,semester))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('student_list'))
    return render_template('create.html')
            
@app.route('/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if request.method == 'PUT':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        semester = request.form['semester']

        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE student SET first_name=%s, last_name=%s, city=%s, semester=%s WHERE id=%s',
                       (first_name, last_name, city, semester, student_id))
        mysql.connection.commit()

        return jsonify(message='Student updated successfully')
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
