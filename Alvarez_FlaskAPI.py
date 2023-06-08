from flask import Flask, request, jsonify
from marshmallow import Schema, fields
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost:3306/mydb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(40), nullable=False)
    contact_number = db.Column(db.Integer, nullable=False)


class Partner(db.Model):
    partner_id = db.Column(db.Integer, primary_key=True)
    partner_name = db.Column(db.String(40), nullable=False)
    partner_type = db.Column(db.String(40), nullable=False)


class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(40), nullable=False)
    event_date = db.Column(db.Date(), nullable=False)
    event_cost = db.Column(db.Integer)
    client_id = db.Column(db.Integer, db.ForeignKey('client.client_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.venue_id'), nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('theme.theme_id'), nullable=False)


class Theme(db.Model):
    theme_id = db.Column(db.Integer, primary_key=True)
    theme_code = db.Column(db.Integer, nullable=False)
    theme_name = db.Column(db.String(40), nullable=False)


class Venue(db.Model):
    venue_id = db.Column(db.Integer, primary_key=True)
    venue_address = db.Column(db.String(40), nullable=False)
    venue_fee = db.Column(db.Integer, nullable=False)


class ClientSchema(ma.Schema):
    class Meta:
        fields = ('client_id', 'client_name', 'contact_number')


class PartnerSchema(ma.Schema):
    class Meta:
        fields = ('partner_id', 'partner_name', 'partner_type')


class EventSchema(ma.Schema):
    class Meta:
        fields = ('event_id', 'event_name', 'event_date', 'event_cost', 'client_id', 'venue_id', 'theme_id')


class ThemeSchema(ma.Schema):
    class Meta:
        fields = ('theme_id', 'theme_code', 'theme_name')


class VenueSchema(ma.Schema):
    class Meta:
        fields = ('venue_id', 'venue_address', 'venue_fee')


client_schema = ClientSchema()
clients_schema = ClientSchema(many=True)

partner_schema = PartnerSchema()
partners_schema = PartnerSchema(many=True)

event_schema = EventSchema()
events_schema = EventSchema(many=True)

theme_schema = ThemeSchema()
themes_schema = ThemeSchema(many=True)

venue_schema = VenueSchema()
venues_schema = VenueSchema(many=True)


@app.route('/clients', methods=['POST'])
def client_data():
    client_name = request.json['client_name']
    contact_number = request.json['contact_number']

    client_input = Client(client_name=client_name, contact_number=contact_number)

    db.session.add(client_input)
    db.session.commit()

    response_data = client_schema.dump(client_input)

    format_choice = request.args.get('format', default='json')

    if format_choice == 'json':
        return jsonify(response_data)
    elif format_choice == 'xml':
        root = ET.Element('client')
        for key, value in response_data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_data = ET.tostring(root).decode('utf-8')
        return xml_data, {'Content-Type': 'application/xml'}
    else:
        return jsonify(response_data)

@app.route('/partners', methods=['POST'])
def partner_data():
    partner_name = request.json['partner_name']
    partner_type = request.json['partner_type']

    partner_input = Partner(partner_name=partner_name, partner_type=partner_type)

    db.session.add(partner_input)
    db.session.commit()

    response_data = partner_schema.dump(partner_input)

    format_choice = request.args.get('format', default='json')

    if format_choice == 'json':
        return jsonify(response_data)
    elif format_choice == 'xml':
        root = ET.Element('partner')
        for key, value in response_data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_data = ET.tostring(root).decode('utf-8')
        return xml_data, {'Content-Type': 'application/xml'}
    else:
        return jsonify(response_data)

@app.route('/events', methods=['POST'])
def event_data():
    event_name = request.json['event_name']
    event_date = request.json['event_date']
    event_cost = request.json['event_cost']
    client_id = request.json['client_id']
    venue_id = request.json['venue_id']
    theme_id = request.json['theme_id']

    event_input = Event(
        event_name=event_name,
        event_date=event_date,
        event_cost=event_cost,
        client_id=client_id,
        venue_id=venue_id,
        theme_id=theme_id
    )

    db.session.add(event_input)
    db.session.commit()

    response_data = event_schema.dump(event_input)

    format_choice = request.args.get('format', default='json')

    if format_choice == 'json':
        return jsonify(response_data)
    elif format_choice == 'xml':
        root = ET.Element('event')
        for key, value in response_data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_data = ET.tostring(root).decode('utf-8')
        return xml_data, {'Content-Type': 'application/xml'}
    else:
        return jsonify(response_data)

@app.route('/themes', methods=['POST'])
def theme_data():
    theme_code = request.json['theme_code']
    theme_name = request.json['theme_name']

    theme_input = Theme(theme_code=theme_code, theme_name=theme_name)

    db.session.add(theme_input)
    db.session.commit()

    input_data = theme_schema.dump(theme_input)

    format_choice = request.args.get('format', default='json')

    if format_choice == 'json':
        return jsonify(input_data)
    elif format_choice == 'xml':
        root = ET.Element('theme')
        for key, value in input_data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_data = ET.tostring(root).decode('utf-8')
        return xml_data, {'Content-Type': 'application/xml'}
    else:
        return jsonify(input_data)

@app.route('/venues', methods=['POST'])
def venue_data():
    venue_address = request.json['venue_address']
    venue_fee = request.json['venue_fee']

    venue_input = Venue(venue_address=venue_address, venue_fee=venue_fee)

    db.session.add(venue_input)
    db.session.commit()

    response_data = venue_schema.dump(venue_input)

    format_choice = request.args.get('format', default='json')

    if format_choice == 'json':
        return jsonify(response_data)
    elif format_choice == 'xml':
        root = ET.Element('venue')
        for key, value in response_data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_data = ET.tostring(root).decode('utf-8')
        return xml_data, {'Content-Type': 'application/xml'}
    else:
        return jsonify(response_data)


@app.route('/')
def home():
    return "Welcome to the Flask API"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
