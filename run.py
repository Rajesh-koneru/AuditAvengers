from audit_tracker import create_App
from flask_cors import CORS
from audit_tracker.config import get_connection

import os
app = create_App()
CORS(app,supports_credentials=True)
if __name__ == '__main__':
    try:
        conn = get_connection()
        if conn:
            print("connected to the Db")
            conn.close()
    except Exception as e:
        print(f"Warning: Startup DB connection check failed: {e}")

    app.run(host="127.0.0.1", port=5000, debug=True)
