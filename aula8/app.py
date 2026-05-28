from flask import Flask, render_template, request

app = Flask(__name__)


dados_especialidades = {
    "Cardiologia": [
        {
            "nome": "Dr. André Souza",
            "crm": "18432",
            "planos": ["Unimed", "Amil", "SulAmérica"]
        },
        {
            "nome": "Dra. Fernanda Melo",
            "crm": "22105",
            "planos": ["Bradesco Saúde", "Unimed"]
        },
    ],

    "Pediatria": [
        {
            "nome": "Dra. Carla Nunes",
            "crm": "15780",
            "planos": ["Unimed", "Hapvida", "Amil"]
        },
        {
            "nome": "Dr. Lucas Ribeiro",
            "crm": "31209",
            "planos": ["SulAmérica", "NotreDame"]
        },
    ],

    "Dermatologia": [
        {
            "nome": "Dra. Juliana Costa",
            "crm": "29801",
            "planos": ["Amil", "Bradesco Saúde"]
        },
    ],
}


@app.route("/", methods=["GET", "POST"])
def index():

    medicos = []
    especialidade = ""
    erro = ""

    if request.method == "POST":

        especialidade = request.form.get("especialidade", "").strip()

        especialidade = especialidade.title()

        if especialidade in dados_especialidades:
            medicos = dados_especialidades[especialidade]
        else:
            erro = f'A especialidade "{especialidade}" não foi encontrada.'

    return render_template(
        "painel.html",
        medicos=medicos,
        especialidade=especialidade,
        erro=erro
    )


if __name__ == "__main__":
    app.run(debug=True)

