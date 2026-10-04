
from audit_tracker.config import get_connection
from flask import Blueprint, jsonify
from flask_login import login_required
from audit_tracker.test import only_one

mango_base = Blueprint("base", __name__)

@mango_base.route('/admin/delete_data', methods=['DELETE'])
@login_required
@only_one('admin')
def delete_data():
    try:
        del_query = "TRUNCATE TABLE audit_report"
        with get_connection() as conn:
            pointer = conn.cursor()
            pointer.execute(del_query)
        return jsonify({"message": "Audit report table truncated successfully."})
    except Exception as e:
        print(f"Error truncating table: {e}")
        return jsonify({"error": str(e)}), 500

