from flask import Blueprint, request, jsonify
from flask_login import login_required
from audit_tracker.config import get_connection
from audit_tracker.test import only_one

file = Blueprint('file', __name__)

@file.route('/upload-excel', methods=['POST'])
@login_required
@only_one('admin')
def upload_excel():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    try:
        json_data = request.get_json() or {}
        data = json_data.get("data", [])
        if not data:
            return jsonify({"error": "Empty or invalid data array"}), 400

        insert_query = """
            INSERT INTO audit_details (
                Audit_id, Audit_type, industry, Date, Auditors_require,
                Days, Qualification, equipment, loction, state,
                Amount, requirements, Client_id, WhatsappLink
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        with get_connection() as conn:
            pointer = conn.cursor(dictionary=True)
            for row in data:
                clean_row = {key.strip(): value for key, value in row.items()}
                pointer.execute(insert_query, (
                    clean_row.get('Audit_id', clean_row.get('Audit Id', '')),
                    clean_row.get('Audit Type', clean_row.get('audit_type', '')),
                    clean_row.get('audit industry', clean_row.get('industry', '')),
                    clean_row.get('Date', '2025-01-01'),
                    int(clean_row.get('auditors require', clean_row.get('Auditors_require', 1)) or 1),
                    int(clean_row.get('days', clean_row.get('Days', 1)) or 1),
                    clean_row.get('qualification', clean_row.get('Qualification', '')),
                    clean_row.get('equipment', ''),
                    clean_row.get('location', clean_row.get('loction', '')),
                    clean_row.get('state', ''),
                    float(clean_row.get('amount', clean_row.get('Amount', 0)) or 0),
                    clean_row.get('requirements', ''),
                    clean_row.get('client Id', clean_row.get('Client_id', '')),
                    clean_row.get('whatsapp link', clean_row.get('WhatsappLink', ''))
                ))

        return jsonify({"message": f"{len(data)} audit details records saved successfully!"}), 200

    except Exception as e:
        print(f"Error in upload_excel: {e}")
        return jsonify({"error": str(e)}), 500


