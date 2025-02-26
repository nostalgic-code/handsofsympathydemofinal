from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Flask-Mail Configuration (Use Environment Variables for Security)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")  # Store in an environment variable
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")  # Store in an environment variable
app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_USERNAME")  # Set default sender

mail = Mail(app)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.json
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    contactDetails = data.get('contactDetails')

    if not firstName or not lastName or not contactDetails:
        return jsonify({'error': 'All fields are required!'}), 400

    try:
        # Send email
        msg = Message(
            subject=f"New Contact Request from {firstName} {lastName}",
            sender=app.config['MAIL_DEFAULT_SENDER'],  # Use a valid sender
            recipients=["syloncube837@gmail.com"],  # Change to your receiving email
            body=f"Name: {firstName} {lastName}\nContact: {contactDetails}"
        )
        mail.send(msg)

        return jsonify({'message': 'Form submitted successfully!'}), 200

    except Exception as e:
        return jsonify({'error': f"Failed to send email: {str(e)}"}), 500  # Fix indentation

if __name__ == '__main__':
    app.run(debug=True)
