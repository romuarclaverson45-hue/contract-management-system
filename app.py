import os
import sqlite3
import uuid
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template, request, redirect, url_for,
    session, jsonify, send_file, flash
)
from werkzeug.utils import secure_filename
import pandas as pd

# ---------------------------------------------------------------------------
# Paths & Config
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
EXPORT_FOLDER = os.path.join(BASE_DIR, 'exports')
DB_PATH = os.path.join(BASE_DIR, 'database.db')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

app = Flask(__name__)
app.secret_key = 'change-this-secret-key-in-production'  # change for real deployments
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# ---------------------------------------------------------------------------
# Hardcoded login credentials -- change these for your own use
# ---------------------------------------------------------------------------
USERNAME = 'admin'
PASSWORD = 'admin123'


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id TEXT NOT NULL,
            contract_name TEXT NOT NULL,
            contract_amount REAL DEFAULT 0,
            premium REAL DEFAULT 0,
            others REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            email TEXT,
            phone TEXT,
            photo_filename TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    return redirect(url_for('dashboard') if session.get('logged_in') else url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    total_records = conn.execute('SELECT COUNT(*) AS c FROM contracts').fetchone()['c']
    total_amount = conn.execute('SELECT COALESCE(SUM(total_amount), 0) AS s FROM contracts').fetchone()['s']
    with_photo = conn.execute(
        "SELECT COUNT(*) AS c FROM contracts WHERE photo_filename IS NOT NULL AND photo_filename != ''"
    ).fetchone()['c']
    recent = conn.execute('SELECT * FROM contracts ORDER BY id DESC LIMIT 6').fetchall()
    conn.close()
    return render_template(
        'dashboard.html',
        active_page='dashboard',
        total_records=total_records,
        total_amount=total_amount,
        with_photo=with_photo,
        recent=recent
    )


@app.route('/data-entry')
@login_required
def data_entry_page():
    return render_template('data_entry.html', active_page='data-entry')


@app.route('/search')
@login_required
def search_page():
    return render_template('search.html', active_page='search')


# ---------------------------------------------------------------------------
# API: Create record (with photo upload or captured webcam image)
# ---------------------------------------------------------------------------
@app.route('/api/contracts', methods=['POST'])
@login_required
def create_contract():
    form = request.form
    contract_id = form.get('contract_id', '').strip()
    contract_name = form.get('contract_name', '').strip()

    if not contract_id or not contract_name:
        return jsonify({'success': False, 'message': 'Contract ID and Contract Name are required.'}), 400

    def to_float(v):
        try:
            return float(v)
        except (TypeError, ValueError):
            return 0.0

    contract_amount = to_float(form.get('contract_amount'))
    premium = to_float(form.get('premium'))
    others = to_float(form.get('others'))
    total_amount_raw = form.get('total_amount')
    total_amount = to_float(total_amount_raw) if total_amount_raw not in (None, '') else (
        contract_amount + premium + others
    )
    email = form.get('email', '').strip()
    phone = form.get('phone', '').strip()

    photo_filename = None
    photo_file = request.files.get('photo')
    if photo_file and photo_file.filename:
        if not allowed_file(photo_file.filename):
            return jsonify({'success': False, 'message': 'Unsupported image file type.'}), 400
        ext = photo_file.filename.rsplit('.', 1)[-1].lower()
        photo_filename = f"{uuid.uuid4().hex}.{ext}"
        safe_name = secure_filename(photo_filename)
        photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], safe_name))
        photo_filename = safe_name

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO contracts
            (contract_id, contract_name, contract_amount, premium, others,
             total_amount, email, phone, photo_filename, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        contract_id, contract_name, contract_amount, premium, others,
        total_amount, email, phone, photo_filename,
        datetime.now().isoformat(timespec='seconds')
    ))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Record saved successfully.'})


# ---------------------------------------------------------------------------
# API: Search
# ---------------------------------------------------------------------------
@app.route('/api/search')
@login_required
def api_search():
    q = request.args.get('q', '').strip()
    conn = get_db_connection()
    if q:
        like = f"%{q}%"
        rows = conn.execute('''
            SELECT * FROM contracts
            WHERE contract_id LIKE ? OR contract_name LIKE ?
               OR email LIKE ? OR phone LIKE ?
            ORDER BY id DESC
        ''', (like, like, like, like)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM contracts ORDER BY id DESC').fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            'id': r['id'],
            'contract_id': r['contract_id'],
            'contract_name': r['contract_name'],
            'contract_amount': r['contract_amount'],
            'premium': r['premium'],
            'others': r['others'],
            'total_amount': r['total_amount'],
            'email': r['email'],
            'phone': r['phone'],
            'photo_url': url_for('static', filename=f'uploads/{r["photo_filename"]}')
                if r['photo_filename'] else None,
            'created_at': r['created_at'],
        })
    return jsonify({'success': True, 'count': len(results), 'results': results})


@app.route('/api/contracts/<int:record_id>', methods=['DELETE'])
@login_required
def delete_contract(record_id):
    conn = get_db_connection()
    row = conn.execute('SELECT photo_filename FROM contracts WHERE id = ?', (record_id,)).fetchone()
    if row is None:
        conn.close()
        return jsonify({'success': False, 'message': 'Record not found.'}), 404
    conn.execute('DELETE FROM contracts WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()
    if row['photo_filename']:
        path = os.path.join(app.config['UPLOAD_FOLDER'], row['photo_filename'])
        if os.path.exists(path):
            os.remove(path)
    return jsonify({'success': True})


# ---------------------------------------------------------------------------
# Export to Excel
# ---------------------------------------------------------------------------
@app.route('/export')
@login_required
def export_excel():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM contracts ORDER BY id DESC').fetchall()
    conn.close()

    columns = ['id', 'contract_id', 'contract_name', 'contract_amount', 'premium',
               'others', 'total_amount', 'email', 'phone', 'photo_filename', 'created_at']
    data = [dict(row) for row in rows]
    df = pd.DataFrame(data, columns=columns)
    df.rename(columns={
        'id': 'Record ID',
        'contract_id': 'Contract ID',
        'contract_name': 'Contract Name',
        'contract_amount': 'Contract Amount',
        'premium': 'Premium',
        'others': 'Others',
        'total_amount': 'Total Amount',
        'email': 'Email',
        'phone': 'Phone',
        'photo_filename': 'Photo File',
        'created_at': 'Date Created',
    }, inplace=True)

    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    filename = f"contracts_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    filepath = os.path.join(EXPORT_FOLDER, filename)

    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Contracts')
        worksheet = writer.sheets['Contracts']
        for column_cells in worksheet.columns:
            max_length = max(
                (len(str(cell.value)) if cell.value is not None else 0) for cell in column_cells
            )
            worksheet.column_dimensions[column_cells[0].column_letter].width = max_length + 4

    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='127.0.0.1', port=5000)
