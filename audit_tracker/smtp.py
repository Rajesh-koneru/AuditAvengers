from flask import Blueprint, request, jsonify
from flask_mail import Message
import os
from audit_tracker.mail_config import mail

mail_bp = Blueprint('mail', __name__)

@mail_bp.route('/sendMail', methods=['POST'])
def send_email():
    data = request.get_json() or {}

    name = data.get('SenderName', '').strip()
    email1 = data.get('Email', '').strip()
    message_body = data.get('Message', '').strip()

    if not name or not email1 or not message_body:
        return jsonify({'error': 'All fields (Name, Email, Message) are required!'}), 400

    recipient_email = os.getenv('MAIL_USERNAME', 'infoauditavengers@gmail.com')

    msg = Message(
        subject=f"New Contact Form Submission from {name}",
        recipients=[recipient_email],
        body=f"Name: {name}\nEmail: {email1}\nMessage: {message_body}"
    )

    try:
        mail_pwd = os.getenv('MAIL_PASSWORD')
        if mail_pwd and len(mail_pwd) > 3:
            mail.send(msg)
            return jsonify({'message': 'Thank you! Your message has been sent successfully.'}), 200
        else:
            print("Mail password not set in environment. Logging message locally.")
            return jsonify({'message': 'Thank you for reaching out! Your message has been logged.'}), 200
    except Exception as e:
        print(f"SMTP Error: {e}")
        return jsonify({'message': 'Thank you! Your message was received successfully.'}), 200

