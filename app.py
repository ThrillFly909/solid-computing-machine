from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    emission_factors = {
        "car_per_km": 0.12,
        "bus_per_km": 0.03,
        "train_per_km": 0.05,
        "flight_per_hour": 250,
        "electricity_per_kwh": 0.5,
        "meat_diet_per_year": 2900,
        "vegetarian_diet_per_year": 1600,
        "vegan_diet_per_year": 1000,
        "if_diet_not_entered": 2250,
        "waste_per_kg": 0.5,
    }

    car_km = float(request.form['car_km'])
    bus_km = float(request.form['bus_km'])
    train_km = float(request.form['train_km'])
    flight_hours = float(request.form['flight_hours'])
    electricity_kwh = float(request.form['electricity_kwh'])

    diet_choice = int(request.form['diet_choice'])
    diet_emissions = {
        1: emission_factors["meat_diet_per_year"],
        2: emission_factors["vegetarian_diet_per_year"],
        3: emission_factors["vegan_diet_per_year"]
    }.get(diet_choice, emission_factors["if_diet_not_entered"])

    waste_kg = float(request.form['waste_kg'])

    transport_emissions = (
        car_km * emission_factors["car_per_km"] +
        bus_km * emission_factors["bus_per_km"] +
        train_km * emission_factors["train_per_km"]
    ) * 52 + flight_hours * emission_factors["flight_per_hour"]

    electricity_emissions = electricity_kwh * emission_factors["electricity_per_kwh"] * 12
    waste_emissions = waste_kg * emission_factors["waste_per_kg"] * 52

    total_emissions = transport_emissions + electricity_emissions + diet_emissions + waste_emissions

    target_emissions = 2000

    return render_template(
        'result.html',
        total_emissions=total_emissions,
        target_emissions=target_emissions
    )

if __name__ == '__main__':
    app.run(debug=True)
