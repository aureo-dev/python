import math
from flask import render_template, request

def calcular():
    num1 = float(request.form["num1"])
    operacao = request.form["operacao"]

    # Operacoes que utilizam apenas o primeiro numero
    if operacao == "sqrt":
        if num1 < 0:
            resultado = "Erro: número negativo"
            etapas = f"Não existe raiz real de {num1}."
        else:
            resultado = math.sqrt(num1)
            etapas = f"√{num1} = {resultado}"
        return resultado, etapas

    elif operacao == "log":
        if num1 <= 0:
            resultado = "Erro: número inválido"
            etapas = f"O logaritmo só é definido para números maiores que zero ({num1})."
        else:
            resultado = math.log10(num1)  # Logaritmo na base 10
            etapas = f"log10({num1}) = {resultado}"
        return resultado, etapas

    # Validacao do segundo numero para as demais operacoes
    num2_valor = request.form.get("num2", "").strip()
    if not num2_valor:
        return "", "Informe o segundo número para esta operação."

    num2 = float(num2_valor)

    # Operacoes binarias
    if operacao == "+":
        resultado = num1 + num2
        etapas = f"{num1} + {num2} = {resultado}"
    elif operacao == "-":
        resultado = num1 - num2
        etapas = f"{num1} - {num2} = {resultado}"
    elif operacao == "*":
        resultado = num1 * num2
        etapas = f"{num1} × {num2} = {resultado}"
    elif operacao == "/":
        if num2 == 0:
            resultado = "Erro: divisão por zero"
            etapas = f"Não é possível dividir {num1} por zero."
        else:
            resultado = num1 / num2
            etapas = f"{num1} ÷ {num2} = {resultado}"
    elif operacao == "**":
        resultado = num1 ** num2
        etapas = f"{num1} ^ {num2} = {resultado}"
    else:
        resultado = "Erro"
        etapas = "Operação inválida."

    return resultado, etapas