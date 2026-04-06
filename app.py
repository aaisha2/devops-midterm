from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return '''
    <html><head><title>Student Portal</title>
    <style>body{font-family:Arial;max-width:600px;margin:40px auto;padding:20px}
    input,button{padding:8px;margin:5px}button{background:#007bff;color:white;border:none;cursor:pointer}</style></head>
    <body>
    <h2>Student Registration — DevOps Midterm</h2>
    <form onsubmit="add(event)">
      <input id="name" placeholder="Student Name" required>
      <input id="roll" placeholder="Roll Number" required>
      <button type="submit">Add Student</button>
    </form>
    <h3>Students:</h3><div id="list"></div>
    <script>
      async function load(){const r=await fetch('/students');const d=await r.json();
        document.getElementById('list').innerHTML=d.map(s=>`<p>${s.id}. ${s.name} — ${s.roll}</p>`).join('')}
      async function add(e){e.preventDefault();
        await fetch('/students',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({name:document.getElementById('name').value,roll:document.getElementById('roll').value})});
        document.getElementById('name').value='';document.getElementById('roll').value='';load();}
      load();
    </script></body></html>
    '''

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify([{'id':s.id,'name':s.name,'roll':s.roll} for s in Student.query.all()])

@app.route('/students', methods=['POST'])
def add_student():
    d = request.json
    db.session.add(Student(name=d['name'], roll=d['roll']))
    db.session.commit()
    return jsonify({'message': 'Student added'}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)