import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, render_template

app = Flask(__name__)

def send_email(form_data):
    sender_email = "unknowntsn062@gmail.com"  # Your Gmail address
    sender_password = "uzsb iutc glgt svfp"  # Your new App Password
    receiver_email = "unknowntsn062@gmail.com"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Soundproofing Calculator Information Submission"

    body = "New form submission:\n\n"
    for key, value in form_data.items():
        body += f"{key}: {value}\n"

    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Log in to your email account
            server.send_message(message)  # Send the email
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def form():
    return render_template('form.html')  # Render the form template

@app.route('/submit', methods=['POST'])
def submit():
    form_data = request.form.to_dict()  # Get form data as a dictionary

    # Extract relevant data for calculations
    surface_type = form_data.get('surface_type')
    additional_notes = form_data.get('additional_notes', '')  # Get additional notes

    # Initialize variables for calculations
    total_cost = 0
    materials = []

    # Process materials input from the table
    material_names = request.form.getlist('material_name')
    material_costs = request.form.getlist('material_cost')
    property_names = request.form.getlist('property_name')
    property_values = request.form.getlist('property_value')

    # Create a list to hold properties for calculations
    properties = {}

    for i in range(len(material_names)):
        try:
            material_name = material_names[i].strip()  # Material name
            cost_value = float(material_costs[i].strip())  # Convert cost to float
            property_name = property_names[i].strip()  # Property name
            property_value = property_values[i].strip()  # Property value

            # Store properties in a dictionary
            properties[property_name] = property_value

            materials.append(f"{material_name} - Cost: £{cost_value:.2f}, {property_name}: {property_value}")
            total_cost += cost_value  # Add to total cost

        except (ValueError, IndexError):
            return "Error: Please ensure all material fields are filled correctly."

    # Define material costs based on surface type
    material_costs_dict = {
        'walls': {
            'rubberWallPanelCost': 22.95,
            'adhesiveCost': 6.25,
            'acousticSealantCost': 3.99,
            'finishingCompoundCost': 25.70,
            'jointingTapeCost': 7.95,
            'plasterboardCost': 19.43,
        },
        'ceilings': {
            'ceilingPanelCost': 30.00,
            'ceilingAdhesiveCost': 8.00,
            'ceilingSealantCost': 4.50,
        },
        'floors': {
            'floorPanelCost': 25.00,
            'floorAdhesiveCost': 7.50,
            'floorSealantCost': 5.00,
        }
    }

    # Calculate materials and costs based on selected surface type
    if surface_type == 'walls':
        rubber_wall_panels_needed = int(properties.get('Length', 0))  # Use Length property
        adhesive_needed = rubber_wall_panels_needed
        acoustic_sealant_needed = 1
        finishing_compound_needed = 1
        jointing_tape_needed = 1
        plasterboards_needed = int(rubber_wall_panels_needed / 2.88)

        total_cost += (rubber_wall_panels_needed * material_costs_dict['walls']['rubberWallPanelCost'] +
                       adhesive_needed * material_costs_dict['walls']['adhesiveCost'] +
                       acoustic_sealant_needed * material_costs_dict['walls']['acousticSealantCost'] +
                       finishing_compound_needed * material_costs_dict['walls']['finishingCompoundCost'] +
                       jointing_tape_needed * material_costs_dict['walls']['jointingTapeCost'] +
                       plasterboards_needed * material_costs_dict['walls']['plasterboardCost'])

        materials.append(f"{rubber_wall_panels_needed} x SM20 Rubber Wall Panels (£{material_costs_dict['walls']['rubberWallPanelCost']} each)")
        materials.append(f"{adhesive_needed} x SM20 Adhesive (£{material_costs_dict['walls']['adhesiveCost']} each)")
        materials.append(f"{acoustic_sealant_needed} x Acoustic Sealant (£{material_costs_dict['walls']['acousticSealantCost']} each)")
        materials.append(f"{finishing_compound_needed} x Finishing Compound (£{material_costs_dict['walls']['finishingCompoundCost']} each)")
        materials.append(f"{jointing_tape_needed} x Self Adhesive Jointing Tape (£{material_costs_dict['walls']['jointingTapeCost']} each)")
        materials.append(f"{plasterboards_needed} x Plasterboards (£{material_costs_dict['walls']['plasterboardCost']} each)")

    elif surface_type == 'ceilings':
        ceiling_panels_needed = int(properties.get('Length', 0))
        ceiling_adhesive_needed = ceiling_panels_needed
        ceiling_sealant_needed = 1

        total_cost += (ceiling_panels_needed * material_costs_dict['ceilings']['ceilingPanelCost'] +
                       ceiling_adhesive_needed * material_costs_dict['ceilings']['ceilingAdhesiveCost'] +
                       ceiling_sealant_needed * material_costs_dict['ceilings']['ceilingSealantCost'])

        materials.append(f"{ceiling_panels_needed} x Ceiling Panels (£{material_costs_dict['ceilings']['ceilingPanelCost']} each)")
        materials.append(f"{ceiling_adhesive_needed} x Ceiling Adhesive (£{material_costs_dict['ceilings']['ceilingAdhesiveCost']} each)")
        materials.append(f"{ceiling_sealant_needed} x Ceiling Sealant (£{material_costs_dict['ceilings']['ceilingSealantCost']} each)")

    elif surface_type == 'floors':
        floor_panels_needed = int(properties.get('Length', 0))
        floor_adhesive_needed = floor_panels_needed
        floor_sealant_needed = 1

        total_cost += (floor_panels_needed * material_costs_dict['floors']['floorPanelCost'] +
                       floor_adhesive_needed * material_costs_dict['floors']['floorAdhesiveCost'] +
                       floor_sealant_needed * material_costs_dict['floors']['floorSealantCost'])

        materials.append(f"{floor_panels_needed} x Floor Panels (£{material_costs_dict['floors']['floorPanelCost']} each)")
        materials.append(f"{floor_adhesive_needed} x Floor Adhesive (£{material_costs_dict['floors']['floorAdhesiveCost']} each)")
        materials.append(f"{floor_sealant_needed} x Floor Sealant (£{material_costs_dict['floors']['floorSealantCost']} each)")

    # Add materials and total cost to form data
    form_data['total_cost'] = total_cost
    form_data['materials'] = "\n".join(materials)
    form_data['additional_notes'] = additional_notes  # Include additional notes

    send_email(form_data)  # Call the function to send the email
    return "Form submitted successfully. Thank you!"  # Response after submission

if __name__ == '__main__':
    app.run(debug=True)