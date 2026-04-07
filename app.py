from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll = db.Column(db.String(50), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=False, default='Computer Science')
    semester = db.Column(db.String(20), nullable=False, default='1st')
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>COMSATS — Student Registry</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0a0a;
    --surface: #111111;
    --border: #222222;
    --border-bright: #333333;
    --accent: #00ff88;
    --accent-dim: rgba(0,255,136,0.08);
    --accent-mid: rgba(0,255,136,0.15);
    --text: #e8e8e8;
    --text-muted: #666666;
    --text-dim: #999999;
    --danger: #ff4455;
    --warn: #ffcc00;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* GRID BACKGROUND */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,255,136,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,255,136,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  /* SCAN LINE */
  body::after {
    content: '';
    position: fixed;
    top: -100%;
    left: 0; right: 0;
    height: 200%;
    background: linear-gradient(transparent 50%, rgba(0,255,136,0.015) 50%);
    background-size: 100% 4px;
    pointer-events: none;
    z-index: 0;
    animation: scanlines 8s linear infinite;
  }

  @keyframes scanlines { to { transform: translateY(50%); } }

  /* HEADER */
  header {
    position: relative;
    z-index: 10;
    border-bottom: 1px solid var(--border-bright);
    padding: 0 48px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 72px;
    background: rgba(10,10,10,0.95);
    backdrop-filter: blur(12px);
  }

  .logo-block {
    display: flex;
    align-items: center;
    gap: 16px;
  }

  .logo-mark {
    width: 36px; height: 36px;
    border: 2px solid var(--accent);
    display: grid;
    place-items: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 18px;
    color: var(--accent);
    position: relative;
  }

  .logo-mark::before {
    content: '';
    position: absolute;
    inset: 3px;
    background: var(--accent);
    opacity: 0.1;
  }

  .logo-text {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    line-height: 1.4;
  }

  .logo-text strong {
    display: block;
    color: var(--text);
    font-size: 13px;
    letter-spacing: 0.1em;
  }

  .header-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    letter-spacing: 0.1em;
  }

  .status-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 8px var(--accent);
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.8); }
  }

  /* MAIN LAYOUT */
  main {
    position: relative;
    z-index: 1;
    max-width: 1100px;
    margin: 0 auto;
    padding: 48px 24px 80px;
    display: grid;
    grid-template-columns: 380px 1fr;
    gap: 32px;
    align-items: start;
  }

  /* SECTION TITLES */
  .section-label {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-bright), transparent);
  }

  /* PANEL */
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    padding: 28px;
    position: relative;
  }

  .panel::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 40px; height: 2px;
    background: var(--accent);
  }

  /* STATS ROW */
  .stats-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1px;
    background: var(--border);
    margin-bottom: 32px;
    border: 1px solid var(--border);
  }

  .stat {
    background: var(--surface);
    padding: 20px 16px;
    text-align: center;
  }

  .stat-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 40px;
    line-height: 1;
    color: var(--accent);
    text-shadow: 0 0 20px rgba(0,255,136,0.3);
    transition: all 0.3s;
  }

  .stat-label {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 4px;
  }

  /* FORM */
  .form-group {
    margin-bottom: 16px;
  }

  label {
    display: block;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 8px;
  }

  input, select {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border-bright);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
    font-size: 14px;
    padding: 10px 14px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    appearance: none;
    -webkit-appearance: none;
  }

  input::placeholder { color: var(--text-muted); font-size: 13px; }

  input:focus, select:focus {
    border-color: var(--accent);
    box-shadow: 0 0 0 2px var(--accent-dim), inset 0 0 20px var(--accent-dim);
  }

  select option { background: var(--surface); }

  .btn {
    width: 100%;
    padding: 12px;
    background: var(--accent);
    color: #000;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    font-weight: 500;
    border: none;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.2s;
    margin-top: 8px;
  }

  .btn:hover { background: #00ffaa; transform: translateY(-1px); box-shadow: 0 4px 20px rgba(0,255,136,0.3); }
  .btn:active { transform: translateY(0); }

  .btn::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    transform: translateX(-100%);
    transition: transform 0.4s;
  }
  .btn:hover::after { transform: translateX(100%); }

  .btn-danger {
    background: transparent;
    color: var(--danger);
    border: 1px solid var(--danger);
    padding: 5px 10px;
    font-size: 10px;
    letter-spacing: 0.1em;
    width: auto;
    margin-top: 0;
    transition: all 0.2s;
  }
  .btn-danger:hover { background: var(--danger); color: #fff; transform: none; box-shadow: none; }

  /* TOAST */
  #toast {
    position: fixed;
    bottom: 32px;
    right: 32px;
    z-index: 1000;
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
    padding: 14px 20px;
    border-left: 3px solid var(--accent);
    background: rgba(17,17,17,0.98);
    color: var(--text);
    transform: translateY(100px);
    opacity: 0;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    max-width: 300px;
  }
  #toast.show { transform: translateY(0); opacity: 1; }
  #toast.error { border-color: var(--danger); }

  /* TABLE */
  .table-wrap {
    overflow-x: auto;
  }

  .search-bar {
    display: flex;
    gap: 12px;
    margin-bottom: 16px;
  }
  .search-bar input { flex: 1; }
  .search-bar .count {
    display: flex;
    align-items: center;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--text-muted);
    white-space: nowrap;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  thead tr {
    border-bottom: 1px solid var(--border-bright);
  }

  th {
    font-family: 'DM Mono', monospace;
    font-size: 9px;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 10px 14px;
    text-align: left;
    font-weight: 400;
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
  }
  th:hover { color: var(--accent); }
  th.sorted { color: var(--accent); }

  tbody tr {
    border-bottom: 1px solid var(--border);
    transition: background 0.15s;
  }
  tbody tr:hover { background: var(--accent-dim); }

  td {
    padding: 12px 14px;
    color: var(--text-dim);
    vertical-align: middle;
  }

  td.name-cell { color: var(--text); font-weight: 400; }

  .roll-badge {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    background: var(--accent-dim);
    color: var(--accent);
    padding: 3px 8px;
    border: 1px solid rgba(0,255,136,0.15);
    letter-spacing: 0.05em;
  }

  .sem-badge {
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    color: var(--text-muted);
    border: 1px solid var(--border-bright);
    padding: 2px 7px;
  }

  .id-cell {
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    color: var(--border-bright);
  }

  .empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.1em;
  }
  .empty-icon {
    font-size: 36px;
    display: block;
    margin-bottom: 12px;
    opacity: 0.3;
  }

  .loading-row td {
    text-align: center;
    padding: 40px;
    color: var(--text-muted);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 0.2em;
    animation: blink 1s ease-in-out infinite;
  }
  @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

  /* HEADING HERO */
  .hero {
    grid-column: 1 / -1;
    padding: 40px 0 16px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 16px;
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
  }

  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(48px, 7vw, 80px);
    line-height: 0.9;
    letter-spacing: 0.02em;
    color: var(--text);
  }

  .hero-title span { color: var(--accent); }

  .hero-meta {
    text-align: right;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    color: var(--text-muted);
    line-height: 1.8;
  }

  /* FORM SUCCESS animation */
  @keyframes rowIn {
    from { opacity: 0; transform: translateX(-10px); background: var(--accent-mid); }
    to   { opacity: 1; transform: translateX(0); background: transparent; }
  }
  .row-new { animation: rowIn 0.6s ease forwards; }

  /* RESPONSIVE */
  @media (max-width: 768px) {
    header { padding: 0 20px; }
    main { grid-template-columns: 1fr; padding: 24px 16px 60px; }
    .hero { flex-direction: column; align-items: flex-start; gap: 12px; }
    .hero-meta { text-align: left; }
    .stats-row { grid-template-columns: repeat(3,1fr); }
  }
</style>
</head>
<body>

<header>
  <div class="logo-block">
    <div class="logo-mark">C</div>
    <div class="logo-text">
      <strong>COMSATS University</strong>
      Lahore Campus — CS Dept
    </div>
  </div>
  <div class="header-status">
    <span class="status-dot"></span>
    SYSTEM ONLINE
  </div>
</header>

<main>
  <div class="hero">
    <div>
      <div class="section-label" style="margin-bottom:12px">CSC418 — DevOps for Cloud Computing</div>
      <h1 class="hero-title">STUDENT<br><span>REGISTRY</span></h1>
    </div>
    <div class="hero-meta">
      SEMESTER 6TH & 7TH<br>
      BATCH FA23<br>
      <span id="clock" style="color:var(--text)">--:--:--</span>
    </div>
  </div>

  <!-- LEFT: FORM -->
  <div>
    <div class="stats-row">
      <div class="stat">
        <div class="stat-value" id="stat-total">0</div>
        <div class="stat-label">Enrolled</div>
      </div>
      <div class="stat">
        <div class="stat-value" id="stat-depts">0</div>
        <div class="stat-label">Depts</div>
      </div>
      <div class="stat">
        <div class="stat-value" id="stat-sem">—</div>
        <div class="stat-label">Latest</div>
      </div>
    </div>

    <div class="panel">
      <div class="section-label">Register Student</div>

      <div class="form-group">
        <label>Full Name</label>
        <input id="name" type="text" placeholder="e.g. Ali Hassan" autocomplete="off">
      </div>
      <div class="form-group">
        <label>Roll Number</label>
        <input id="roll" type="text" placeholder="e.g. FA23-BCS-001" autocomplete="off">
      </div>
      <div class="form-group">
        <label>Department</label>
        <select id="dept">
          <option value="Computer Science">Computer Science</option>
          <option value="Software Engineering">Software Engineering</option>
          <option value="Electrical Engineering">Electrical Engineering</option>
          <option value="Data Science">Data Science</option>
          <option value="Cyber Security">Cyber Security</option>
          <option value="Artificial Intelligence">Artificial Intelligence</option>
        </select>
      </div>
      <div class="form-group">
        <label>Semester</label>
        <select id="semester">
          <option value="1st">1st Semester</option>
          <option value="2nd">2nd Semester</option>
          <option value="3rd">3rd Semester</option>
          <option value="4th">4th Semester</option>
          <option value="5th">5th Semester</option>
          <option value="6th" selected>6th Semester</option>
          <option value="7th">7th Semester</option>
          <option value="8th">8th Semester</option>
        </select>
      </div>
      <button class="btn" onclick="addStudent()">▶ REGISTER STUDENT</button>
    </div>
  </div>

  <!-- RIGHT: TABLE -->
  <div>
    <div class="section-label">Enrolled Students</div>
    <div class="search-bar">
      <input id="search" type="text" placeholder="Search by name or roll…" oninput="filterTable()">
      <div class="count"><span id="vis-count">0</span>&nbsp;records</div>
    </div>
    <div class="panel" style="padding:0;overflow:hidden">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th onclick="sortBy('id')" id="th-id">#</th>
              <th onclick="sortBy('name')" id="th-name">Name</th>
              <th onclick="sortBy('roll')" id="th-roll">Roll No.</th>
              <th onclick="sortBy('department')" id="th-department">Dept</th>
              <th onclick="sortBy('semester')" id="th-semester">Sem</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody id="tbody">
            <tr class="loading-row"><td colspan="6">LOADING DATA…</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</main>

<div id="toast"></div>

<script>
  let students = [];
  let sortKey = 'id', sortDir = 1;

  // Clock
  function updateClock() {
    const now = new Date();
    document.getElementById('clock').textContent =
      now.toLocaleTimeString('en-PK', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
  }
  setInterval(updateClock, 1000); updateClock();

  // Toast
  function toast(msg, err=false) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.className = 'show' + (err ? ' error' : '');
    clearTimeout(t._tid);
    t._tid = setTimeout(() => t.className = '', 3000);
  }

  // Load
  async function load(highlightRoll=null) {
    try {
      const r = await fetch('/students');
      students = await r.json();
      updateStats();
      renderTable(highlightRoll);
    } catch(e) { toast('Failed to load students', true); }
  }

  function updateStats() {
    document.getElementById('stat-total').textContent = students.length;
    const depts = new Set(students.map(s => s.department)).size;
    document.getElementById('stat-depts').textContent = depts || '—';
    const last = students[students.length-1];
    document.getElementById('stat-sem').textContent = last ? last.semester.replace('th','').replace('st','').replace('nd','').replace('rd','') : '—';
  }

  // Sort
  function sortBy(key) {
    if(sortKey === key) sortDir *= -1; else { sortKey = key; sortDir = 1; }
    document.querySelectorAll('th').forEach(t => t.classList.remove('sorted'));
    document.getElementById('th-'+key)?.classList.add('sorted');
    renderTable();
  }

  // Render
  function renderTable(highlightRoll=null) {
    const q = document.getElementById('search').value.toLowerCase();
    let rows = students.filter(s =>
      s.name.toLowerCase().includes(q) || s.roll.toLowerCase().includes(q)
    );
    rows.sort((a,b) => {
      let av = a[sortKey], bv = b[sortKey];
      if(typeof av === 'string') av = av.toLowerCase();
      if(typeof bv === 'string') bv = bv.toLowerCase();
      return av < bv ? -sortDir : av > bv ? sortDir : 0;
    });
    document.getElementById('vis-count').textContent = rows.length;
    const tbody = document.getElementById('tbody');
    if(!rows.length) {
      tbody.innerHTML = `<tr><td colspan="6"><div class="empty-state"><span class="empty-icon">◻</span>NO RECORDS FOUND</div></td></tr>`;
      return;
    }
    tbody.innerHTML = rows.map(s => `
      <tr class="${s.roll === highlightRoll ? 'row-new' : ''}">
        <td class="id-cell">${String(s.id).padStart(3,'0')}</td>
        <td class="name-cell">${escHtml(s.name)}</td>
        <td><span class="roll-badge">${escHtml(s.roll)}</span></td>
        <td style="font-size:12px">${escHtml(s.department)}</td>
        <td><span class="sem-badge">${escHtml(s.semester)}</span></td>
        <td><button class="btn btn-danger" onclick="deleteStudent(${s.id})">✕ Remove</button></td>
      </tr>`).join('');
  }

  function filterTable() { renderTable(); }

  function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  }

  // Add
  async function addStudent() {
    const name = document.getElementById('name').value.trim();
    const roll = document.getElementById('roll').value.trim();
    const department = document.getElementById('dept').value;
    const semester = document.getElementById('semester').value;
    if(!name || !roll) { toast('Name and Roll Number are required', true); return; }
    try {
      const r = await fetch('/students', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({name, roll, department, semester})
      });
      const d = await r.json();
      if(!r.ok) { toast(d.error || 'Error adding student', true); return; }
      document.getElementById('name').value = '';
      document.getElementById('roll').value = '';
      toast('✓ Student registered: ' + name);
      await load(roll);
    } catch(e) { toast('Network error', true); }
  }

  // Delete
  async function deleteStudent(id) {
    if(!confirm('Remove this student?')) return;
    try {
      const r = await fetch('/students/' + id, {method: 'DELETE'});
      if(r.ok) { toast('Student removed'); await load(); }
      else { toast('Failed to remove', true); }
    } catch(e) { toast('Network error', true); }
  }

  load();
</script>
</body>
</html>'''

@app.route('/')
def home():
    return HTML

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'roll': s.roll,
        'department': s.department,
        'semester': s.semester,
        'registered_at': s.registered_at.isoformat() if s.registered_at else None
    } for s in Student.query.all()])

@app.route('/students', methods=['POST'])
def add_student():
    d = request.json
    if not d or not d.get('name') or not d.get('roll'):
        return jsonify({'error': 'Name and roll number are required'}), 400
    existing = Student.query.filter_by(roll=d['roll']).first()
    if existing:
        return jsonify({'error': f"Roll number '{d['roll']}' already exists"}), 409
    s = Student(
        name=d['name'].strip(),
        roll=d['roll'].strip(),
        department=d.get('department', 'Computer Science'),
        semester=d.get('semester', '1st')
    )
    db.session.add(s)
    db.session.commit()
    return jsonify({'message': 'Student added', 'id': s.id}), 201

@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    s = Student.query.get_or_404(student_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({'message': 'Student deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)