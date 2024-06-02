from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Charger le modèle et les encodeurs de labels
model = pickle.load(open('model_rf.pkl', 'rb'))
label_encoders = pickle.load(open('label_encoders_rf.pkl', 'rb'))

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/predict_price", methods=["POST"])
def predict_price():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        input_data = {
            'CODESITE': request.form["CODESITE"],
            'LIBSITE': request.form["LIBSITE"],
            'VILLE': request.form["VILLE"],
            'CODE_INTERNE_ARTICLE': request.form["CODE_INTERNE_ARTICLE"],
            'CODE_ARTICLE': request.form["CODE_ARTICLE"],
            'LIBELLE_ARTICLE_x': request.form["LIBELLE_ARTICLE_x"],
            'LIBFRS': request.form["LIBFRS"],
            'MARQUE': request.form["MARQUE"],
            'LIB_RAY': request.form["LIB_RAY"],
            'LIB_SSFAM': request.form["LIB_SSFAM"],
            'temperature': float(request.form["temperature"]),
            'pluie': float(request.form["pluie"]),
            'year': int(request.form["year"]),
            'month': int(request.form["month"]),
            'day': int(request.form["day"])
        }

        # Convertir les données en DataFrame
        input_df = pd.DataFrame([input_data])

       # Appliquer les encodeurs de label aux nouvelles données
        for column, encoder in label_encoders.items():
                if column in input_df.columns:
                    input_df[column] = input_df[column].astype(str)  # Convertir en string pour correspondre aux classes de l'encodeur
                    classes = encoder.classes_
                    # Utiliser la première classe par défaut si la valeur n'est pas dans les classes connues
                    input_df[column] = input_df[column].apply(lambda x: x if x in classes else classes[0])
                    input_df[column] = encoder.transform(input_df[column])



        # Prédire le prix
        predicted_price = model.predict(input_df)[0]

        return render_template("result.html", prediction=predicted_price)

if __name__ == "__main__":
    app.run(debug=True)