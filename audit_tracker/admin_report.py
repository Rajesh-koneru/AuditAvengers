from flask import Blueprint, jsonify, request
from flask_login import login_required
from audit_tracker.config import get_connection
from audit_tracker.test import only_one

report = Blueprint('report', __name__)

@report.route('/admin/report')
@login_required
@only_one('admin')
def admin_report_data():
    try:
        query = "SELECT * FROM audit_report"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            row = pointer.fetchall()

        data = []
        for r in row:
            data.append({
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
        return jsonify(data)
    except Exception as e:
        print(f"Error fetching admin report: {e}")
        return jsonify({'error': str(e)}), 500

@report.route('/admin/total_audits')
@login_required
@only_one('admin')
def total_auditor():
    try:
        query = "SELECT COUNT(*) as total FROM audit_report"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            res = pointer.fetchone()
            total = res.get('total', 0) if res else 0
        return jsonify(total)
    except Exception as e:
        print(f"Error in total_audits: {e}")
        return jsonify(0), 500

@report.route('/admin/active_audits')
@login_required
@only_one('admin')
def active_audits():
    try:
        query = "SELECT COUNT(*) as total FROM audit_report WHERE Audit_status = 'In Progress'"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            res = pointer.fetchone()
            total = res.get('total', 0) if res else 0
        return jsonify(total)
    except Exception as e:
        print(f"Error in active_audits: {e}")
        return jsonify(0), 500

@report.route('/admin/complete')
@login_required
@only_one('admin')
def complete():
    try:
        query = "SELECT COUNT(*) as total FROM audit_report WHERE Audit_status = 'Completed'"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            res = pointer.fetchone()
            total = res.get('total', 0) if res else 0
        return jsonify(total)
    except Exception as e:
        print(f"Error in complete: {e}")
        return jsonify(0), 500

@report.route('/admin/pending')
@login_required
@only_one('admin')
def pending():
    try:
        query = "SELECT COUNT(*) as total FROM audit_report WHERE Audit_status = 'Pending'"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            res = pointer.fetchone()
            total = res.get('total', 0) if res else 0
        return jsonify(total)
    except Exception as e:
        print(f"Error in pending: {e}")
        return jsonify(0), 500

@report.route('/admin/Recent_audit')
@login_required
@only_one('admin')
def recent_audits():
    try:
        query = "SELECT Audit_id, auditor_id, planned_date, auditor_name, Audit_status FROM audit_report LIMIT 5"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query)
            data1 = pointer.fetchall()

        formatted = []
        for d in data1:
            formatted.append({
                'Audit_id': d.get('Audit_id', ''),
                'auditor_id': d.get('auditor_id', ''),
                'planned_Date': str(d.get('planned_date', '')),
                'auditor_name': d.get('auditor_name', ''),
                'audit_status': d.get('Audit_status', d.get('audit_status', ''))
            })
        return jsonify(formatted)
    except Exception as e:
        print(f"Error in recent_audits: {e}")
        return jsonify([]), 500

@report.route('/admin/filter', methods=['POST'])
@login_required
@only_one('admin')
def filter_data():
    try:
        json_data = request.get_json()
        if not json_data or "data" not in json_data:
            return jsonify({"error": "Invalid format"}), 400

        value = str(json_data["data"]).strip()

        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            if value in ['Completed', 'Pending', 'In Progress']:
                query = "SELECT * FROM audit_report WHERE Audit_status = %s"
                pointer.execute(query, (value,))
            elif value in ['Paid', 'Unpaid', 'Requested']:
                query = "SELECT * FROM audit_report WHERE payment_status = %s"
                pointer.execute(query, (value,))
            else:
                query = "SELECT * FROM audit_report WHERE State = %s OR location = %s"
                pointer.execute(query, (value, value))

            rows = pointer.fetchall()

        data = []
        for r in rows:
            data.append({
                'Audit_id': r.get('Audit_id', ''),
                'auditor_name': r.get('auditor_name', ''),
                'planned_date': str(r.get('planned_date', '')),
                'state': r.get('State', r.get('state', '')),
                'Audit_status': r.get('Audit_status', r.get('audit_status', '')),
                'payment_amount': float(r.get('payment_amount', 0) or 0),
                'payment_status': r.get('payment_status', ''),
                'contact': r.get('Contact', r.get('contact', '')),
                'auditor_id': r.get('auditor_id', ''),
                'audit_type': r.get('audit_type', ''),
                'client_id': r.get('Client_id', r.get('client_id', '')),
                'location': r.get('location', ''),
                'email': r.get('email', '')
            })
        return jsonify(data)
    except Exception as e:
        print(f"Error in filter_data: {e}")
        return jsonify({"error": str(e)}), 500

@report.route('/admin/update_status', methods=["POST"])
@login_required
@only_one('admin')
def admin_status_update():
    try:
        data = request.get_json()
        target_id = data.get('Id')
        status = data.get('value')

        if not target_id or not status:
            return jsonify({"error": "Missing Id or status value"}), 400

        update_query = "UPDATE audit_report SET Audit_status = %s WHERE auditor_id = %s OR Audit_id = %s"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(update_query, (status, target_id, target_id))

        return jsonify({"message": "Audit status updated successfully"})
    except Exception as e:
        print(f"Error in admin_status_update: {e}")
        return jsonify({"error": str(e)}), 500

@report.route('/admin/update_payment', methods=['POST'])
@login_required
@only_one('admin')
def payment_update():
    try:
        data = request.get_json()
        target_id = data.get('Id')
        status = data.get('value')

        if not target_id or not status:
            return jsonify({"error": "Missing Id or status value"}), 400

        update_query = "UPDATE audit_report SET payment_status = %s WHERE auditor_id = %s OR Audit_id = %s"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(update_query, (status, target_id, target_id))

        return jsonify({"message": "Payment status updated successfully"})
    except Exception as e:
        print(f"Error in payment_update: {e}")
        return jsonify({"error": str(e)}), 500

