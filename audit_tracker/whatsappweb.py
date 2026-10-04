from flask import Blueprint, jsonify, request
from flask_login import login_required
from audit_tracker.config import get_connection
from audit_tracker.test import only_one
from datetime import datetime

application = Blueprint('application', __name__)

@application.route('/admin/application')
@login_required
@only_one('admin')
def admin_report():
    try:
        query = "SELECT * FROM applications"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            rows = pointer.fetchall()

        data = []
        for r in rows:
            data.append({
                'Audit_id': r.get('audit_id', ''),
                'Auditor_id': r.get('Auditor_id', ''),
                'Auditor_name': r.get('auditor_name', r.get('Auditor_name', '')),
                'audit_type': r.get('audit_type', ''),
                'Date': str(r.get('date', r.get('Date', ''))),
                'phone': r.get('phone', ''),
                'email': r.get('email', ''),
                'state': r.get('state', ''),
                'Client_id': r.get('client_id', r.get('Client_id', '')),
                'status': r.get('status', 'pending')
            })
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching applications: {e}")
        return jsonify([]), 500

@application.route("/applications/status", methods=["PUT", "POST"])
@login_required
@only_one('admin')
def status_update():
    try:
        data = request.get_json() or {}
        auditor_id = data.get('Id')
        status_val = data.get('status')

        if not auditor_id or not status_val:
            return jsonify({'error': 'Missing Auditor Id or status'}), 400

        query = "UPDATE applications SET status = %s WHERE Auditor_id = %s"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query, (status_val, auditor_id))

        return jsonify({'message': 'Application status updated successfully'})
    except Exception as e:
        print(f"Error in status_update: {e}")
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

def get_next_auditor_id():
    try:
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute("SELECT auditor_id FROM audit_report ORDER BY auditor_id DESC LIMIT 1")
            result = pointer.fetchone()
            if result and result.get('auditor_id'):
                last_id = result['auditor_id']
                if str(last_id).startswith('AUD'):
                    numeric_part = int(str(last_id)[3:])
                    return f"AUD{numeric_part + 1:03d}"
            return "AUD001"
    except Exception as e:
        print(f"Error generating auditor_id: {e}")
        return "AUD001"

def clean_date(date_str):
    if not date_str:
        return datetime.now().strftime('%Y-%m-%d')
    try:
        if "-" in date_str:
            return date_str.split(" ")[0]
        parsed_date = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
        return parsed_date.strftime('%Y-%m-%d')
    except Exception:
        return datetime.now().strftime('%Y-%m-%d')

@application.route('/application/audit_report', methods=['POST'])
@login_required
@only_one('admin')
def report():
    try:
        data = request.get_json() or []
        if isinstance(data, dict):
            data = [data]

        if not data:
            return jsonify({"error": "No data provided"}), 400

        created_auditor_id = get_next_auditor_id()

        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)

            for row in data:
                clean_row = {key.strip(): value for key, value in row.items()}
                p_date = clean_date(clean_row.get('Date', ''))
                audit_id = clean_row.get('audit_id', '')

                # Fetch location from audit_details
                pointer.execute("SELECT loction FROM audit_details WHERE Audit_id = %s", (audit_id,))
                loc_res = pointer.fetchone()
                location = loc_res.get('loction', 'N/A') if loc_res else 'N/A'

                aud_id = clean_row.get('auditor_id') or created_auditor_id
                aud_name = clean_row.get('auditor_name', '')
                phone = clean_row.get('phone', '')

                insert_sql = """
                    INSERT INTO audit_report (
                        Audit_id, auditor_id, planned_date, State, Client_id,
                        Contact, Audit_status, payment_amount, payment_status,
                        auditor_name, audit_type, location, email
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                pointer.execute(insert_sql, (
                    audit_id, aud_id, p_date, clean_row.get('state', ''),
                    clean_row.get('client_id', ''), phone, 'Pending',
                    float(clean_row.get('payment', 0) or 0), 'Pending',
                    aud_name, clean_row.get('audit_type', ''), location, clean_row.get('email', '')
                ))

                # Update or delete from audit_details based on requirements count
                pointer.execute("SELECT Auditors_require FROM audit_details WHERE Audit_id = %s", (audit_id,))
                det_res = pointer.fetchone()
                if det_res:
                    req_cnt = det_res.get('Auditors_require', 1)
                    if req_cnt <= 1:
                        pointer.execute("DELETE FROM audit_details WHERE Audit_id = %s", (audit_id,))
                    else:
                        pointer.execute("UPDATE audit_details SET Auditors_require = %s WHERE Audit_id = %s", (req_cnt - 1, audit_id))

                # Remove from applications table
                pointer.execute("DELETE FROM applications WHERE audit_id = %s AND Auditor_id = %s", (audit_id, clean_row.get('auditor_id', '')))

        first_row = data[0]
        return jsonify({
            "message": "Data successfully promoted to audit report!",
            "delete_message": "Application record cleaned up.",
            "auditor_id": created_auditor_id,
            "phone": first_row.get('phone', ''),
            "auditor_name": first_row.get('auditor_name', ''),
            "audit_message": "Audit requirements updated."
        }), 200

    except Exception as e:
        print(f"Error in promote application: {e}")
        return jsonify({"error": str(e)}), 500







