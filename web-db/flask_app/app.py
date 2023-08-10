from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'web-db-service'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 8306

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

@app.route('/update_student/<int:student_id>', methods=['POST'])
def update_student(student_id):
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        city = request.form.get('city')
        semester = request.form.get('semester')
        
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE student SET first_name=%s, last_name=%s, city=%s, semester=%s WHERE id=%s', (first_name, last_name, city, semester, student_id))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({"message": "Student updated successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
