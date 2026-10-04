from flask import Blueprint, request, send_file, jsonify
import pandas as pd
import io
from flask_login import login_required
from audit_tracker.test import only_one
from audit_tracker.config import get_connection

download = Blueprint('file_download', __name__)

@download.route('/admin/download', methods=["POST"])
@login_required
@only_one('admin')
def file_download():
    req = request.get_json() or {}
    name = req.get('fileName', 'audit_report').strip() or 'audit_report'

    try:
        download_query = "SELECT * FROM audit_report"
        with get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(download_query)
            data = cursor.fetchall()

        if not data:
            return jsonify({"message": "No data available to download"}), 404

        df = pd.DataFrame(data)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Audit Report')

        output.seek(0)
        return send_file(
            output,
            download_name=f"{name}.xlsx",
            as_attachment=True,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        print(f"Error generating download file: {e}")
        return jsonify({"error": str(e)}), 500

