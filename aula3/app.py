from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html') 

@app.route('/sobre/<nome>')
def sobre(nome):
    return  f'Olá, {nome}! Bem-vindo à página.'

if __name__ == '__main__':
    app.run(debug=True)
