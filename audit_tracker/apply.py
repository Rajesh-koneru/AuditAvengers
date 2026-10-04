from flask import Blueprint, session, request, jsonify, render_template
from audit_tracker.config import get_connection

audit_bp = Blueprint('apply', __name__)

@audit_bp.route('/apply/user_Details', methods=['POST', 'GET'])
def register_page():
    if request.method == 'POST':
        data = request.get_json() or {}
        info = data.get('data', {})
        audit_id = info.get('audit_id')
        whatsapp_link = info.get('whatsappLink')

        session['whatsappLink'] = whatsapp_link
        session["Audit_id"] = audit_id
        return jsonify({'message': 'Audit ID stored in session'})
    return render_template('auditor_apply.html')

def generate_auditor_id():
    try:
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute("SELECT Auditor_id FROM applications ORDER BY Auditor_id DESC LIMIT 1")
            result = pointer.fetchone()
            if not result:
                pointer.execute("SELECT auditor_id FROM audit_report ORDER BY auditor_id DESC LIMIT 1")
                result = pointer.fetchone()
            
            if result:
                last_id = result.get('Auditor_id') or result.get('auditor_id', 'AUD000')
                if str(last_id).startswith('AUD'):
                    numeric_part = int(str(last_id)[3:])
                    new_id = f"AUD{numeric_part + 1:03d}"
                else:
                    new_id = "AUD001"
            else:
                new_id = "AUD001"
            return new_id
    except Exception as e:
        print(f"Error generating auditor_id: {e}")
        import time
        return f"AUD{int(time.time()) % 1000:03d}"

@audit_bp.route('/apply/audit_application', methods=['POST', 'GET'])
def application():
    audit_id = session.get('Audit_id')
    if not audit_id:
        return jsonify({'error': 'Session expired or audit ID not set'}), 403

    json_data = request.get_json() or {}
    name = json_data.get('name', '').strip()
    phone = json_data.get('phone', '').strip()
    email = json_data.get('email', '').strip()

    if not name or not phone or not email:
        return jsonify({'error': 'Name, phone, and email are required'}), 400

    try:
        query = "SELECT Audit_id, Audit_type, Date, Client_id, state FROM audit_details WHERE Audit_id = %s"
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(query, (audit_id,))
            audit_data = pointer.fetchone()

        if not audit_data:
            return jsonify({'error': f'No audit details found for ID: {audit_id}'}), 404

        aud_id = generate_auditor_id()

        insert_query = """
            INSERT INTO applications 
            (Auditor_id, auditor_name, phone, email, audit_id, audit_type, date, client_id, state) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            pointer.execute(insert_query, (
                aud_id, name, phone, email,
                audit_data.get('Audit_id'), audit_data.get('Audit_type'), audit_data.get('Date'),
                audit_data.get('Client_id'), audit_data.get('state')
            ))

        return jsonify({
            'message': 'Your application has been submitted successfully!',
            'link': session.get('whatsappLink', '')
        }), 200

    except Exception as e:
        print(f"Error saving application: {e}")
        return jsonify({'error': 'Failed to save application', 'details': str(e)}), 500

