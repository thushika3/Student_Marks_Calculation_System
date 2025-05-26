from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import timedelta
from flask_cors import CORS
import traceback

app = Flask(__name__)
CORS(app)

# JWT and DB Config
app.config['JWT_SECRET_KEY'] = "myapp"
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "thushika03"
app.config['MYSQL_DB'] = "proj"
app.config['MYSQL_HOST'] = "localhost"
mysql = MySQL(app)

# ------------------ Faculty Register ------------------ #
@app.route("/facultyregister", methods=["POST"])
def faculty_register():
    data = request.json
    f_id = data.get('f_id')
    f_name = data.get('f_name')
    password = data.get('password')
    c_id = data.get('c_id')

    if not all([f_id, f_name, password, c_id]):
        return jsonify({"message": "Missing faculty details"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM faculty WHERE f_id = %s", (f_id,))
    if cur.fetchone():
        return jsonify({"message": "Faculty already registered"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO faculty(f_id, f_name, password, c_id) VALUES (%s, %s, %s, %s)",
                (f_id, f_name, hashed_pw, c_id))
    mysql.connection.commit()
    return jsonify({"message": "Faculty registered successfully"}), 201

# ------------------ Faculty Login ------------------ #
@app.route("/facultylogin", methods=["POST"])
def faculty_login():
    data = request.json
    f_id = data.get('f_id')
    password = data.get('password')

    if not all([f_id, password]):
        return jsonify({"error": "Missing login credentials"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT f_id, f_name, password FROM faculty WHERE f_id = %s", (f_id,))
    user = cur.fetchone()

    if not user:
        return jsonify({"message": "Faculty not found"}), 404

    fid, fname, password_hash = user
    if bcrypt.check_password_hash(password_hash, password):
        access_token = create_access_token(identity=fid, expires_delta=timedelta(hours=1))
        return jsonify({"message": "Login successful", "access_token": access_token, "faculty_name": fname}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401
    
# ------------------ Student Registeration ------------------ #
@app.route("/studentregister", methods=["POST"])
def studentregister():
    data = request.json
    s_id = data.get('s_id')
    s_name = data.get('s_name')
    password = data.get('password')
    c_id = data.get('c_id')

    if not all([s_id, s_name, password, c_id]):
        return jsonify({"message": "Missing student details"}), 400
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM student WHERE s_id = %s", (s_id,))
    if cur.fetchone():
        return jsonify({"message": "Student already registered"}), 409

    hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO student(s_id, s_name, password, c_id) VALUES (%s, %s, %s, %s)",(s_id, s_name, hashed_pw, c_id))
    mysql.connection.commit()
    return jsonify({"message": "Student registered successfully"}), 201

# ------------------ Student Login ------------------ #
@app.route("/studentlogin", methods=["POST"])
def studentlogin():
    data = request.json
    s_id = data.get('s_id')
    password = data.get('password')

    if not all([s_id, password]):
        return jsonify({"message": "Missing login credentials"}), 400

    cur = mysql.connection.cursor()
    cur.execute("SELECT s_id, s_name, password FROM student WHERE s_id = %s", (s_id,))
    user = cur.fetchone()

    if not user:
        return jsonify({"message": "Student not found"}), 404

    s_id, s_name, password_hash = user
    if bcrypt.check_password_hash(password_hash, password):
        access_token = create_access_token(identity=s_id, expires_delta=timedelta(hours=1))
        return jsonify({"message": "Login successful", "access_token": access_token, "student_name": s_name}), 200
    else:
        return jsonify({"message": "Invalid password"}), 401

@app.route('/internals', methods=['POST'])
def submit_internals():
    data = request.get_json()
    s_id = data.get('s_id')
    f_id = data.get('f_id')
    sub_id = data.get('sub_id')
    sub_name = data.get('sub_name')
    mid1 = data.get('mid1')
    mid2 = data.get('mid2')
    mid3 = data.get('mid3')

    if None in [s_id, f_id ,sub_id,sub_name, mid1, mid2, mid3]:
        return jsonify({'message': 'Missing fields'}), 400

    try:
        mids = sorted([mid1, mid2, mid3], reverse=True)
        best_two_avg = round((mids[0] + mids[1]) / 2, 2)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO internals(s_id,f_id,sub_id, sub_name, mid1, mid2, mid3, internal_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (s_id, f_id , sub_id ,sub_name, mid1, mid2, mid3, best_two_avg))
        mysql.connection.commit()

        return jsonify({'message': 'Internal marks submitted', 'average': best_two_avg}), 200

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500

@app.route('/externals', methods=['POST'])
def submit_externals():
    data = request.get_json()
    s_id = data.get('s_id')
    f_id = data.get('f_id')
    sub_id = data.get('sub_id')
    sub_name = data.get('sub_name')
    external_marks = data.get('external_marks')

    if None in [s_id, f_id, sub_id, sub_name, external_marks]:
        return jsonify({'message': 'Missing fields'}), 400

    try:
        # Fetch internal_total from internals table
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT internal_total FROM internals
            WHERE s_id = %s AND sub_id = %s
        """, (s_id, sub_id))
        internal_row = cur.fetchone()

        if not internal_row:
            return jsonify({'message': 'Internal marks not found for this student and subject'}), 404

        internal_total = internal_row[0]
        final_marks = round(internal_total + external_marks, 2)

        # Insert into externals table
        cur.execute("""
            INSERT INTO externals (s_id, f_id, sub_id, sub_name, external_marks, internal_total, final_marks)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (s_id, f_id, sub_id, sub_name, external_marks, internal_total, final_marks))
        mysql.connection.commit()

        return jsonify({
            'message': 'External marks submitted successfully',
            'internal_total': internal_total,
            'external_marks': external_marks,
            'final_marks': final_marks
        }), 200

    except Exception as e:
        return jsonify({'message': 'Error: ' + str(e)}), 500

@app.route('/checkinternals', methods=['GET'])
def check_internals():
    f_id = request.args.get('f_id')

    if not f_id:
        return jsonify({"error": "Missing faculty ID"}), 400

    cur = mysql.connection.cursor()
    query = "SELECT * FROM internals WHERE f_id = %s"
    cur.execute(query, (f_id.strip(),))  # ✅ Execute before fetchall

    rows = cur.fetchall()
    results = []

    for row in rows:
        results.append({
            "s_id": row[2],
            "sub_id": row[3],
            "sub_name": row[4],
            "mid1": row[5],
            "mid2": row[6],
            "mid3": row[7],
            "total_internal": row[8]  # Same as best_two_avg
        })

    return jsonify(results), 200

@app.route('/checkexternals', methods=['GET'])
def check_externals():
    f_id = request.args.get('f_id')

    if not f_id:
        return jsonify({"error": "Missing faculty ID"}), 400

    try:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM externals WHERE f_id = %s"
        cur.execute(query, (f_id.strip(),))
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "s_id": row[1],
                "sub_id": row[3],
                "sub_name": row[4],
                "external": row[5],
                
            })

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in /checkexternals: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/viewinternals', methods=['GET'])
def view_internals():
    s_id = request.args.get('s_id')

    if not s_id:
        return jsonify({"error": "Missing student ID"}), 400

    try:
        cur = mysql.connection.cursor()
        query = "SELECT * FROM internals WHERE s_id = %s"
        cur.execute(query, (s_id.strip(),))
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "sub_id": row[3],
                "sub_name": row[4],
                "mid1": row[5],
                "mid2": row[6],
                "mid3": row[7],
                "internal_total": row[8]
            })

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in /viewinternals: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/viewexternals', methods=['GET'])
def view_externals():
    s_id = request.args.get('s_id')

    if not s_id:
        return jsonify({"error": "Missing student ID"}), 400

    try:
        cur = mysql.connection.cursor()
        query = """
            SELECT sub_id, sub_name, external_marks
            FROM externals
            WHERE s_id = %s
        """
        cur.execute(query, (s_id.strip(),))
        rows = cur.fetchall()

        results = []
        for row in rows:
            results.append({
                "sub_id": row[0],
                "sub_name": row[1],
                "external_marks": row[2]
            })

        return jsonify(results), 200

    except Exception as e:
        print(f"Error in /viewexternals: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/api/reportcard/<s_id>', methods=['GET'])
def generate_report_card(s_id):
    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT s_name FROM student WHERE s_id = %s", (s_id,))
        student = cur.fetchone()
        if not student:
            return jsonify({"message": "Student not found"}), 404
        student_name = student[0]

        cur.execute("""
            SELECT e.sub_id, e.sub_name, i.mid1, i.mid2, i.mid3, 
                   i.internal_total, e.external_marks, e.final_marks
            FROM internals i
            JOIN externals e ON i.s_id = e.s_id AND i.sub_id = e.sub_id
            WHERE i.s_id = %s
        """, (s_id,))
        rows = cur.fetchall()
        cur.close()

        if not rows:
            return jsonify({"message": "No marks found"}), 404

        def grade_calc(score):
            if score >= 85: return "A+"
            elif score >= 75: return "A"
            elif score >= 65: return "B"
            elif score >= 50: return "C"
            else: return "F"

        subjects = []
        total = 0
        for row in rows:
            final = row[7] or 0
            total += final
            subjects.append({
                "subject_id": row[0],
                "subject_name": row[1],
                "mid1": row[2],
                "mid2": row[3],
                "mid3": row[4],
                "internal_total": row[5],
                "external_marks": row[6],
                "final_marks": final,
                "grade": grade_calc(final)
            })

        avg = round(total / len(subjects), 2)

        return jsonify({
            "student_id": s_id,
            "student_name": student_name,
            "subjects": subjects,
            "total_marks": total,
            "average_marks": avg
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
              
if __name__ == "__main__":
    app.run(debug=True)
