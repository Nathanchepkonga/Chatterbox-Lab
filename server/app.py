from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from sqlalchemy import asc
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by(asc(Message.created_at)).all()
        messages_dict = [message.to_dict() for message in messages]
        
        return jsonify(messages_dict), 200
    elif request.method == 'POST':
        data = request.get_json()

        new_message = Message(
            body = data['body'],
            username = data['username']
        )

        db.session.add(new_message)
        db.session.commit()

        new_message_dict = new_message.to_dict()

        return jsonify(new_message_dict), 201

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    if request.method == 'PATCH':

        message = Message.query.get_or_404(id)

        data = request.get_json()

        if 'body' in data:
            message.body = data['body']
        
        if 'username' in data:
            message.username = data['username']
        
        db.session.add(message)
        db.session.commit()

        message_dict = message.to_dict()
        
        return jsonify(message_dict), 200
    elif request.method == 'DELETE':
        message = Message.query.filter(Message.id == id).first()

        db.session.delete(message)
        db.session.commit()

        response_body = {
            "message": "Message deleted successfully."
        }

        return jsonify(response_body), 200

if __name__ == '__main__':
    app.run(port=5555)
