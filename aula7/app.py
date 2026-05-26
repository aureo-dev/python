from flask import Flask, render_template, request
from calculadora import calcular

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultados = ""
    etapas = ""
    
    if request.method == "POST":
        resultados, etapas = calcular()
        
    return render_template("calculadora.html", resultados=resultados, etapas=etapas)

if __name__ == "__main__":
    app.run(debug=True)