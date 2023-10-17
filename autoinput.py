from flask import Flask, render_template

app = Flask(__name__)

@app.route('/example')
def example():
    # Condition to determine if the fields should be pre-populated
    condition = True  # Replace with your actual condition

    # Values to pre-populate the form fields
    name = "John"
    age = 30

    return render_template('example.html', condition=condition, name=name, age=age)


app.run(debug=True)