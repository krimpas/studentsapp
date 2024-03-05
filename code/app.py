from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# Configure the database connection
connection = psycopg2.connect(
    database="test",
    user="postgres",
    password="postgres",
    host="localhost",
    port="54320"
)

# Routes
@app.route('/')
def index():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students order by stud_surname, stud_name")
        students = cursor.fetchall()

    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = request.form
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO students (stud_surname, stud_name, stud_gender, stud_age, stud_city, stud_tel) VALUES (%s, %s, %s, %s, %s, %s)",
                           (data['stud_surname'], data['stud_name'], data['stud_gender'], data['stud_age'], data['stud_city'], data['stud_tel']))
        connection.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/search', methods=['POST'])
def search_students():
    search_term = request.form.get('search_term')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE stud_surname ILIKE %s OR stud_tel ILIKE %s",
                       ('%' + search_term + '%', '%' + search_term + '%'))
        search_results = cursor.fetchall()

    return render_template('index.html', students=search_results)

@app.route('/update/<int:stud_id>', methods=['GET', 'POST'])
def update_student(stud_id):
    if request.method == 'POST':
        data = request.form
        with connection.cursor() as cursor:
            cursor.execute("UPDATE students SET stud_surname=%s, stud_name=%s, stud_gender=%s, stud_age=%s, stud_city=%s, stud_tel=%s WHERE stud_id=%s",
                           (data['stud_surname'], data['stud_name'], data['stud_gender'], data['stud_age'], data['stud_city'], data['stud_tel'], stud_id))
        connection.commit()
        return redirect(url_for('index'))

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students WHERE stud_id=%s", (stud_id,))
        student = cursor.fetchone()

    return render_template('update.html', student=student)

@app.route('/delete/<int:stud_id>')
def delete_student(stud_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM students WHERE stud_id=%s", (stud_id,))
    connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

