from flask import Flask, request, render_template
import numpy as np
import joblib  

app = Flask(__name__)

model = joblib.load(open("model.pkl","rb"))  

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])

def predict_water_quality():
    if request.method == 'POST':
        fields = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", 
                  "Conductivity", "Organic_carbon", "Trihalomethanes", "Turbidity"]

       
        for field in fields:
            if not request.form.get(field): 
                return render_template("index.html", message="Input cannot be blank")

        
        values = []
        for field in fields:
            value = request.form.get(field).strip() 
            if not value.replace('.', '', 1).isdigit():  
                return render_template("index.html", message="Please enter only numbers")

            values.append(float(value))  

        result = model.predict(np.array(values).reshape(1, -1))

        
        result_text = "Water is safe to drink" if result[0] == 1 else "Water is not safe to drink"
        return render_template("index.html", result=result_text)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
