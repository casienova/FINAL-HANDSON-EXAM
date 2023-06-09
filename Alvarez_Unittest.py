import unittest
from Alvarez_FlaskAPI import app, db, Client, Partner, Event, Theme, Venue

class FlaskAPITestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.create_all()


    def tearDown(self):
        db.session.remove()
        db.drop_all()


    def test_client_data(self):
        response = self.client.post('/clients', json={"client_name": "John Doe", "contact_number": "1234567890"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['client_name'], "John Doe")
        self.assertEqual(data['contact_number'], "1234567890")


    def test_partner_data(self):
        response = self.client.post('/partners', json={"partner_name": "ABC Company", "partner_type": "Type A"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['partner_name'], "ABC Company")
        self.assertEqual(data['partner_type'], "Type A")


    def test_event_data(self):
        response = self.client.post('/events', json={"event_name": "Birthday Party", "event_date": "2023-06-08", "event_cost": 1000, "client_id": 1, "venue_id": 1, "theme_id": 1})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)


    def test_theme_data(self):
        response = self.client.post('/themes', json={"theme_code": 123, "theme_name": "Pool Party"})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)


    def test_venue_data(self):
        response = self.client.post('/venues', json={"venue_address": "Palawan, P.P.C.", "venue_fee": 500})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)


    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Welcome to the Flask API")

if __name__ == '__main__':
    unittest.main()
