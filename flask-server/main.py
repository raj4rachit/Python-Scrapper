import re

from flask import Flask, jsonify, request
from flask_cors import CORS
from config import app,db
from models import Contact

cors = CORS(app,origin='*')

@app.route('/api/members',methods=['GET'])
def members():
    return jsonify({"members": ["Rachit","M.","Patel"]})


def validate_contact_data(data,required_fields):
    # Check if all required fields are present in the data
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"
        elif data[field] == '':
            return False, f"Enter required field data: {field}"
        elif field == 'email':
            if not re.match(r"[^@]+@[^@]+\.[^@]+", data[field]):
                return False, "Enter valid email address"
        elif field =='phone':
            if not re.match(r"\d{10}", data[field]):
                return False, "Invalid phone number format. Please enter a 10-digit number without spaces or symbols."

    return True, None  # Validation passed

@app.route('/api/contacts',methods=['GET'])
def get_contacts():
    contacts=Contact.query.all()
    json_contacts=list(map(lambda x: x.to_json(),contacts))
    return jsonify({"contacts":json_contacts}),200

@app.route('/api/contacts/create',methods=['POST'])
def create_contact():
    data = request.get_json()
    required_fields = ['name', 'email', 'phone']

    # Validate the incoming data
    is_valid, validation_error = validate_contact_data(data,required_fields)
    if not is_valid:
        return jsonify({"message": validation_error}), 400

    contact = Contact(**data)
    try:
        db.session.add(contact)
        db.session.commit()
    except Exception as e:
        return jsonify({"message":str(e)}),400

    return jsonify({"message":"Contact created!"}),201

@app.route('/api/contacts/<int:id>',methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message":"Contact not found"}),404

    return jsonify({"contact":contact.to_json()}),200

@app.route('/api/contacts/update/<int:id>',methods=['PATCH'])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message":"Contact not found"}),404

    data = request.get_json()
    required_fields = ['name', 'email', 'phone']

    # Validate the incoming data
    is_valid, validation_error = validate_contact_data(data, required_fields)
    if not is_valid:
        return jsonify({"message": validation_error}), 400

    if data:
        for key, value in data.items():
            setattr(contact, key, value)

    db.session.commit()
    return jsonify({"message":"Contact updated!"}),200

@app.route('/api/contacts/delete/<int:id>',methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message":"Contact not found"}),404

    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message":"Contact deleted!"}),200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,port=8080)
