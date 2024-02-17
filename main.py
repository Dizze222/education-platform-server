
from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

fake = Faker()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    second = db.Column(db.String(100), nullable=False)
    password = db.Column(db.Integer, nullable=False)
    course = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.number'), nullable=True)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    second_name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.String(100), nullable=False)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'), nullable=False)


class Group(db.Model):
    number = db.Column(db.Integer, primary_key=True, autoincrement=False)
    start_education = db.Column(db.Integer, nullable=False)
    end_education = db.Column(db.Integer, nullable=False)
    course = db.Column(db.Integer, nullable=False)


class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.number'), nullable=False)


class TrainingProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.number'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)


db.create_all()


@app.route('/fill_db', methods=['GET'])
def populate_db():
    for _ in range(5):
        group = Group(
            start_education=fake.year(),
            end_education=fake.year(),
            course=fake.random_int(min=1, max=5)
        )
        db.session.add(group)

    db.session.commit()

    for _ in range(10):
        teacher = Teacher(
            name=fake.first_name(),
            second_name=fake.first_name(),
            surname=fake.last_name(),
            password=fake.password(),
            grade=fake.job()
        )
        db.session.add(teacher)

    teachers = Teacher.query.all()
    for _ in range(15):
        subject = Subject(
            name=fake.word(),
            teacher_id=fake.random.choice([teacher.id for teacher in teachers])
        )
        db.session.add(subject)

    db.session.commit()

    groups = Group.query.all()
    for _ in range(100):
        student = Student(
            name=fake.first_name(),
            second=fake.last_name(),
            password=fake.random_number(digits=5),
            course=fake.random_int(min=1, max=5),
            group_id=fake.random.choice([group.id for group in groups])
        )
        db.session.add(student)

    subjects = Subject.query.all()
    for _ in range(50):
        homework = Homework(
            description=fake.sentence(),
            subject_id=fake.random.choice([subject.id for subject in subjects]),
            group_id=fake.random.choice([group.id for group in groups])
        )
        db.session.add(homework)

    for group in groups:
        for subject in fake.random.choices(subjects, k=5):
            training_program = TrainingProgram(
                group_id=group.id,
                subject_id=subject.id
            )
            db.session.add(training_program)

    db.session.commit()

    return jsonify({'message': 'Database random data fill'})


@app.route('/students', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(
        name=data['name'],
        second=data['second'],
        password=data['password'],
        course=data['course'],
        group_id=data['group_id']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added'}), 201


@app.route('/teachers', methods=['POST'])
def add_teacher():
    data = request.json
    new_teacher = Teacher(
        name=data['name'],
        second_name=data['second_name'],
        surname=data['surname'],
        password=data['password'],
        grade=data['grade']
    )
    db.session.add(new_teacher)
    db.session.commit()
    return jsonify({'message': 'Teacher added'}), 201


@app.route('/subjects', methods=['POST'])
def add_subject():
    data = request.json
    new_subject = Subject(
        name=data['name'],
        teacher_id=data['teacher_id']
    )
    db.session.add(new_subject)
    db.session.commit()
    return jsonify({'message': 'Subject added'}), 201


@app.route('/groups', methods=['POST'])
def add_group():
    data = request.json
    new_group = Group(
        number=data['number_group'],
        start_education=data['start_education'],
        end_education=data['end_education'],
        course=data['course']
    )
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Group added'}), 201


@app.route('/homeworks', methods=['POST'])
def add_homework():
    data = request.json
    new_homework = Homework(
        description=data['description'],
        subject_id=data['subject_id'],
        group_id=data['group_id']
    )
    db.session.add(new_homework)
    db.session.commit()
    return jsonify({'message': 'Homework added'}), 201


@app.route('/training_programs', methods=['POST'])
def add_training_program():
    data = request.json
    new_program = TrainingProgram(
        group_id=data['group_id'],
        subject_id=data['subject_id']
    )
    db.session.add(new_program)
    db.session.commit()
    return jsonify({'message': 'Training program added'}), 201


@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    students_list = [{'id': student.id, 'name': student.name, 'second': student.second, 'password': student.password,
                      'course': student.course, 'group_id': student.group_id} for student in students]
    return jsonify(students_list)


@app.route('/teachers', methods=['GET'])
def get_teachers():
    teachers = Teacher.query.all()
    teachers_list = [
        {'id': teacher.id, 'name': teacher.name, 'second_name': teacher.second_name, 'surname': teacher.surname,
         'password': teacher.password, 'grade': teacher.grade} for teacher in teachers]
    return jsonify(teachers_list)


@app.route('/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    subjects_list = [{'id': subject.id, 'name': subject.name, 'teacher_id': subject.teacher_id} for subject in subjects]
    return jsonify(subjects_list)


@app.route('/groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    groups_list = [{'id': group.id, 'start_education': group.start_education, 'end_education': group.end_education,
                    'course': group.course} for group in groups]
    return jsonify(groups_list)


@app.route('/homeworks', methods=['GET'])
def get_homeworks():
    homeworks = Homework.query.all()
    homeworks_list = [{'id': homework.id, 'description': homework.description, 'subject_id': homework.subject_id,
                       'group_id': homework.group_id} for homework in homeworks]
    return jsonify(homeworks_list)


@app.route('/training_programs', methods=['GET'])
def get_training_programs():
    training_programs = TrainingProgram.query.all()
    programs_list = [{'id': program.id, 'group_id': program.group_id, 'subject_id': program.subject_id} for program in
                     training_programs]
    return jsonify(programs_list)


@app.route('/clear_db', methods=['GET'])
def clear_db():
    models = [Student, Teacher, Subject, Group, Homework, TrainingProgram]

    for model in models:
        db.session.query(model).delete()

    db.session.commit()

    return jsonify({'message': 'All tables cleared!'})


@app.route('/students/group/<int:group_id>', methods=['GET'])
def get_students_by_group(group_id):
    sql = "SELECT * FROM student WHERE group_id = :group_id"
    result = db.engine.execute(sql, group_id=group_id)
    students = [dict(row) for row in result]
    return jsonify(students)


@app.route('/student/<int:student_id>/group', methods=['GET'])
def get_group_by_student(student_id):
    sql = 'SELECT * FROM "group" WHERE number = (SELECT group_id FROM student WHERE id = :student_id)'
    result = db.engine.execute(sql, student_id=student_id)
    group = [dict(row) for row in result]
    return jsonify(group)


@app.route('/homeworks/group/<int:group_id>', methods=['GET'])
def get_homeworks_by_group(group_id):
    sql = "SELECT * FROM homework WHERE group_id = :group_id"
    result = db.engine.execute(sql, group_id=group_id)
    homeworks = [dict(row) for row in result]
    return jsonify(homeworks)


@app.route('/subjects/group/<int:group_id>', methods=['GET'])
def get_subjects_by_group(group_id):
    sql = """
    SELECT subject.id, subject.name, teacher.name AS teacher_name 
    FROM subject
    JOIN training_program ON subject.id = training_program.subject_id
    JOIN teacher ON subject.teacher_id = teacher.id
    WHERE training_program.group_id = :group_id
    """
    result = db.engine.execute(sql, group_id=group_id)
    subjects = [{"id": row['id'], "name": row['name'], "teacher": row['teacher_name']} for row in result]
    return jsonify(subjects)


@app.route('/subjects/teacher/<int:teacher_id>', methods=['GET'])
def get_subjects_by_teacher(teacher_id):
    sql = "SELECT * FROM subject WHERE teacher_id = :teacher_id"
    result = db.engine.execute(sql, teacher_id=teacher_id)
    subjects = [dict(row) for row in result]
    return jsonify(subjects)


@app.route('/teachers/subject', methods=['GET'])
def get_teachers_by_subject():
    subject_name = request.args.get('name')
    sql = """
    SELECT teacher.* FROM teacher
    JOIN subject ON teacher.id = subject.teacher_id
    WHERE subject.name = :subject_name
    """
    result = db.engine.execute(sql, subject_name=subject_name)
    teachers = [dict(row) for row in result]
    return jsonify(teachers)


if __name__ == '__main__':
    app.run()
