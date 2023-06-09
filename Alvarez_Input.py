import requests
import json
import xml.etree.ElementTree as ET

url = "http://127.0.0.1:5000"

while True:
    table_options = {
        1: "clients",
        2: "partners",
        3: "events",
        4: "themes",
        5: "venues"
    }

    print("Enter the Number of your Choice: ")
    for key, value in table_options.items():
        print(f"{key}. {value.capitalize()}")

    choice = int(input("Enter the table number: "))
    table_name = table_options.get(choice)

    if not table_name:
        print("Invalid table choice. Exiting...")
        continue

    data = {}
    if choice == 1:
        data['client_name'] = input("Enter the Client name: ")
        data['contact_number'] = int(input("Enter the Contact Number: "))

    elif choice == 2:
        data['partner_name'] = input("Enter the partner name: ")
        data['partner_type'] = input("Enter the partner type: ")

    elif choice == 3:
        data['event_name'] = input("Enter the Event name: ")
        data['event_date'] = input("Enter the Event date (YYYY-MM-DD): ")
        data['event_cost'] = int(input("Enter the Event cost: "))
        data['client_id'] = int(input("Enter the Client ID: "))
        data['venue_id'] = int(input("Enter the Venue ID: "))
        data['theme_id'] = int(input("Enter the Theme ID: "))

    elif choice == 4:
        data['theme_code'] = int(input("Enter the Theme code: "))
        data['theme_name'] = input("Enter the Theme name: ")

    elif choice == 5:
        data['venue_address'] = input("Enter the Venue address: ")
        data['venue_fee'] = int(input("Enter the Venue fee: "))

    response = requests.post(f"{url}/{table_name}", json=data)

    if response.status_code == 200:
        print("Data inserted successfully!")

    else:
        print("ERROR:", response.text)

    format_choice = input("Save data as XML = 1 or JSON = 2: ")

    if format_choice == '1':
        root = ET.Element(table_name)
        for key, value in data.items():
            child = ET.SubElement(root, key)
            child.text = str(value)
        xml_data = ET.tostring(root).decode('utf-8')
        print("Data saved in XML format.")
        print(xml_data)

    elif format_choice == '2':
        json_data = json.dumps(data)
        print("Data saved in JSON format.")
        print(json_data)

    else:
        print("Invalid format choice.")

    y_n = input("Do you want to insert data again? (y/n): ")
    if y_n == 'y':
        continue
    else:
        print("Thank you, for using my program!")
        break
    