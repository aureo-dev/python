from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Bem-vindo à Aplicação Flask!</h1>
    <p>Para aprender sobre decorators, acesse: <a href="/decorator">/decorator</a></p>
    """

@app.route('/decorator')
def explicar_decorator():
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Explicação sobre Decorators em Python</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background-color: #f5f5f5; line-height: 1.8; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #2980b9; margin-top: 30px; }
        .conceito { background-color: #e8f4f8; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; margin: 20px 0; }
        .exemplo { background-color: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 8px; margin: 15px 0; font-family: 'Courier New', monospace; overflow-x: auto; }
        .destaque { color: #e74c3c; font-weight: bold; }
        .flask-exemplo { background-color: #fef9e7; padding: 15px; border-radius: 8px; border: 1px solid #f39c12; margin: 20px 0; }
        pre { margin: 0; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>Entendendo Decorators em Python</h1>

    <div class="conceito">
        <h2>O que é um Decorator?</h2>
        <p>Um <span class="destaque">decorator</span> é uma função especial que permite <strong>modificar ou estender o comportamento</strong> de outras funções sem alterar seu código original.</p>
    </div>

    <h2>Exemplo Básico</h2>
    <div class="exemplo">
<pre>
<span style="color: #3498db">def</span> <span style="color: #f1c40f">meu_decorator</span>(func):
    <span style="color: #3498db">def</span> <span style="color: #f1c40f">wrapper</span>():
        print(<span style="color: #e67e22">"Antes da execução"</span>)
        func()
        print(<span style="color: #e67e22">"Depois da execução"</span>)
    <span style="color: #3498db">return</span> wrapper

@meu_decorator
<span style="color: #3498db">def</span> <span style="color: #f1c40f">diga_ola</span>():
    print(<span style="color: #e67e22">"Olá!"</span>)
</pre>
    </div>

    <div class="flask-exemplo">
        <h2>Decorators no Flask: @app.route</h2>
        <p>Associa uma URL a uma função. O Flask registra a rota internamente antes de executar a lógica da função.</p>
    </div>

    <h2>Resumo</h2>
    <ul>
        <li>Reutilização de código (DRY).</li>
        <li>Separação de lógica (ex: autenticação, logs).</li>
        <li>Sintaxe elegante com o símbolo <b>@</b>.</li>
    </ul>
</body>
</html>"""

if __name__ == '__main__':
    app.run(debug=True, port=5000)