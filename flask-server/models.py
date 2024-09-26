from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=False, nullable=False)
    # address = db.Column(db.String(120), unique=False, nullable=True)
    # city = db.Column(db.String(120), unique=False, nullable=True)
    # state = db.Column(db.String(120), unique=False, nullable=True)
    # country = db.Column(db.String(120), unique=False, nullable=True)
    # postal = db.Column(db.String(120), unique=False, nullable=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            # 'address': self.address,
            # 'city': self.city,
            # 'state': self.state,
            # 'country': self.country,
            # 'postal': self.postal
        }

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        # self.address = address
        # self.city = city
        # self.state = state
        # self.country = country
        # self.postal = postal
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Contact %r>' % self.name

