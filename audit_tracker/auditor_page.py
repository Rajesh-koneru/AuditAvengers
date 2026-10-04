from flask import Blueprint, request, jsonify, session
from flask_login import login_required
from audit_tracker.config import get_connection

status = Blueprint('status', __name__)

@status.route('/auditor/auditor_details')
@login_required
def auditor_details():
    if session.get('role') == 'auditor':
        return jsonify({
            "username": session.get('username', ''),
            "id": session.get('id', '')
        })
    return jsonify({"error": "Unauthorized"}), 403

@status.route('/auditor/data', methods=["POST"])
@login_required
def status_update():
    try:
        data = request.get_json() or {}
        username = data.get('Id') or session.get('id')
        auditor_name = data.get('username') or session.get('username')

        query = "SELECT * FROM audit_report WHERE auditor_id = %s OR auditor_name = %s"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query, (username, auditor_name))
            rows = pointer.fetchall()

        if rows:
            details = []
            for r in rows:
                details.append({
                    'Audit_id': r.get('Audit_id', ''),
                    'auditor_name': r.get('auditor_name', ''),
                    'planned_date': str(r.get('planned_date', '')),
                    'state': r.get('State', r.get('state', '')),
                    'audit_status': r.get('Audit_status', r.get('audit_status', '')),
                    'payment_amount': float(r.get('payment_amount', 0) or 0),
                    'payment_status': r.get('payment_status', ''),
                    'contact': r.get('Contact', r.get('contact', '')),
                    'auditor_id': r.get('auditor_id', ''),
                    'audit_type': r.get('audit_type', ''),
                    'client_id': r.get('Client_id', r.get('client_id', '')),
                    'location': r.get('location', ''),
                    'email': r.get('email', '')
                })
            return jsonify(details)
        else:
            return jsonify([]), 200
    except Exception as e:
        print(f"Error in auditor data route: {e}")
        return jsonify({"error": str(e)}), 500

@status.route('/auditor/status_update', methods=['POST'])
@login_required
def update():
    try:
        data = request.get_json() or {}
        audit_status = data.get('status')
        audit_id = data.get('id') or session.get('id')

        if not audit_status or not audit_id:
            return jsonify({"error": "Missing status or id"}), 400

        update_query = "UPDATE audit_report SET Audit_status = %s WHERE Audit_id = %s OR auditor_id = %s"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(update_query, (audit_status, audit_id, audit_id))

        return jsonify({"message": "Status updated successfully!"})
    except Exception as e:
        print(f"Error updating auditor status: {e}")
        return jsonify({"error": str(e)}), 500













