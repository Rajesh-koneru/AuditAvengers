from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_login import login_required
from audit_tracker.config import get_connection
from audit_tracker.test import only_one

audit_log = Blueprint('audit_log', __name__)

@audit_log.route('/admin/manual_update', methods=['POST'])
@login_required
@only_one('admin')
def manual_update():
    json_data = request.get_json() or {}
    data = json_data.get('data', {})
    if not data:
        return jsonify({"error": "No data received"}), 400

    date_str = str(data.get("Date", "")).strip()
    try:
        if date_str:
            if "-" in date_str:
                date_val = date_str
            else:
                date_val = datetime.strptime(date_str, "%m/%d/%y").strftime("%Y-%m-%d")
        else:
            date_val = datetime.now().strftime("%Y-%m-%d")
    except Exception:
        date_val = datetime.now().strftime("%Y-%m-%d")

    try:
        query = """
            INSERT INTO audit_details (
                Audit_id, Audit_type, industry, Date, Auditors_require,
                Days, Qualification, equipment, loction, state,
                Amount, requirements, Client_id, WhatsappLink
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query, (
                data.get('Audit Id', ''),
                data.get('Auditor type', ''),
                data.get('industry', ''),
                date_val,
                int(data.get('auditor require', 1) or 1),
                int(data.get('Day', 1) or 1),
                data.get('Qualification', ''),
                data.get('equipment', ''),
                data.get('location', ''),
                data.get('State', ''),
                float(data.get('Amount', 0) or 0),
                data.get('requirement', ''),
                data.get('client_id', ''),
                data.get('whatsapp', '')
            ))
        return jsonify('Audit inserted successfully!')
    except Exception as e:
        print(f"Manual update error: {e}")
        return jsonify({"error": str(e)}), 400

@audit_log.route("/audit_details")
def audit_details():
    try:
        query = "SELECT * FROM audit_details"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            rows = pointer.fetchall()

        formatted = []
        for r in rows:
            formatted.append({
                'Audit_id': r.get('Audit_id', ''),
                'Audit_type': r.get('Audit_type', ''),
                'industry': r.get('industry', ''),
                'Date': str(r.get('Date', '')),
                'Auditors_require': r.get('Auditors_require', 1),
                'Days': r.get('Days', 1),
                'Qualification': r.get('Qualification', ''),
                'equipment': r.get('equipment', ''),
                'loction': r.get('loction', r.get('location', '')),
                'state': r.get('state', r.get('State', '')),
                'Amount': float(r.get('Amount', 0) or 0),
                'requirements': r.get('requirements', ''),
                'client_id': r.get('Client_id', ''),
                'whatsappLink': r.get('WhatsappLink', '')
            })
        return jsonify(formatted)
    except Exception as e:
        print(f"Error fetching audit details: {e}")
        return jsonify([]), 200

@audit_log.route("/home_page/audits")
def home_page_audit_details():
    try:
        query = "SELECT * FROM audit_details LIMIT 5"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            rows = pointer.fetchall()

        formatted = []
        for r in rows:
            formatted.append({
                'Audit_id': r.get('Audit_id', ''),
                'Audit_type': r.get('Audit_type', ''),
                'industry': r.get('industry', ''),
                'Date': str(r.get('Date', '')),
                'Auditors_require': r.get('Auditors_require', 1),
                'Days': r.get('Days', 1),
                'Qualification': r.get('Qualification', ''),
                'equipment': r.get('equipment', ''),
                'loction': r.get('loction', r.get('location', '')),
                'state': r.get('state', r.get('State', '')),
                'Amount': float(r.get('Amount', 0) or 0),
                'requirements': r.get('requirements', ''),
                'client_id': r.get('Client_id', ''),
                'whatsappLink': r.get('WhatsappLink', '')
            })
        return jsonify(formatted)
    except Exception as e:
        print(f"Error fetching home page audits: {e}")
        return jsonify([]), 200




