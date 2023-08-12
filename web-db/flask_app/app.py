from flask import Flask,redirect,render_template, request, jsonify,url_for,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
import logging

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'web-db-service'
app.config['MYSQL_USER'] = 'example_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'example'
app.config['MYSQL_PORT'] = 8306

app.secret_key="mysecretkey"

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
            
@app.route('/studentupdate/<string:id>',methods=['GET'])
def student_update(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id,first_name,last_name,city,semester FROM student WHERE id =%s",(id))
    data=cur.fetchall()
    print(data)
    logging.debug(data)
    return render_template('update.html',student=data[0])

@app.route('/studentupdate/<string:id>', methods=['POST'])
def student_update_json(id):
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        semester = request.form['semester']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE student SET first_name=%s, last_name=%s, city=%s, semester=%s WHERE id=%s',
                       (first_name, last_name, city, semester, id))
        mysql.connection.commit()
        cur.close()
        flash('successfully updated')
        return redirect(url_for('student_list'))
    return render_template('update.html')

@app.route('/studentdelete/<string:id>')
def student_delet(id):
    cur=mysql.connection.cursor()
    cur.execute('DELETE FROM student WHERE id=%s',(id))
    mysql.connection.commit()
    cur.close()
    flash('successfully removed')
    return redirect(url_for('student_list'))
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
