from flask import Flask, render_template_string, request

app = Flask(__name__)


USER_DATABASE = {
    "Arthur": "1010",
    "Janaina": "cotemig2026",
    "Antonio": "cotemig2026",
    "Matheus": "cotemig2026"
}


def authenticate_user():
    username_input = request.form.get('usuario')
    password_input = request.form.get('senha')

    if username_input in USER_DATABASE and USER_DATABASE[username_input] == password_input:
        return f"Acesso autorizado! Seja bem-vindo(a), {username_input}."
    
    return "Falha na autenticação! Usuário ou senha inválidos."


def render_login_page():
    html_form = """
    <div style="font-family: Arial, sans-serif; margin: 20px;">
        <h3>Área de Autenticação</h3>
        <form method="POST" action="/">
            <label>Login:</label><br>
            <input type="text" name="usuario" required><br><br>
            <label>Senha:</label><br>
            <input type="password" name="senha" required><br><br>
            <input type="submit" value="Acessar Sistema">
        </form>
    </div>
    """
    return render_template_string(html_form)

@app.route('/', methods=['GET', 'POST'])
def handle_login_route():
    if request.method == 'POST':
        return authenticate_user()
    return render_login_page()

if __name__ == "__main__":
    app.run(debug=True)