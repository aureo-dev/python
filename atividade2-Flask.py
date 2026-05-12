from flask import Flask, render_template_string

app = Flask(__name__)

# Template HTML com CSS incorporado - Emojis removidos e estrutura finalizada
CURRICULO_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
 <meta charset="UTF-8">
 <meta name="viewport" content="width=device-width, initial-scale=1.0">
 <title>Currículo - Áureo Henrique Badaró de Carvalho</title>
 <style>
 * {
 margin: 0;
 padding: 0;
 box-sizing: border-box;
 }
 
 body {
 font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
 min-height: 100vh;
 padding: 20px;
 line-height: 1.6;
 }
 
 .container {
 max-width: 900px;
 margin: 0 auto;
 background: white;
 border-radius: 15px;
 box-shadow: 0 10px 40px rgba(0,0,0,0.2);
 overflow: hidden;
 }
 
 .header {
 background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
 color: white;
 padding: 30px 40px;
 text-align: center;
 }
 
 .header h1 {
 font-size: 2.2em;
 margin-bottom: 10px;
 font-weight: 700;
 }
 
 .header .subtitle {
 font-size: 1.1em;
 opacity: 0.9;
 margin-bottom: 15px;
 }
 
 .contact-info {
 display: flex;
 justify-content: center;
 gap: 30px;
 flex-wrap: wrap;
 font-size: 0.9em;
 }
 
 .content {
 padding: 30px 40px;
 }
 
 .section {
 margin-bottom: 30px;
 padding-bottom: 20px;
 border-bottom: 2px solid #ecf0f1;
 }
 
 .section:last-child {
 border-bottom: none;
 margin-bottom: 0;
 }
 
 .section-title {
 color: #2c3e50;
 font-size: 1.4em;
 margin-bottom: 15px;
 padding-bottom: 5px;
 border-bottom: 3px solid #3498db;
 display: inline-block;
 }
 
 .objective-text {
 background: #e8f4f8;
 padding: 15px 20px;
 border-radius: 8px;
 border-left: 4px solid #3498db;
 font-style: italic;
 }
 
 .education, .experience {
 margin-bottom: 20px;
 }
 
 .education h4, .experience h4 {
 color: #2c3e50;
 font-size: 1.1em;
 margin-bottom: 5px;
 }
 
 .education .institution, .experience .company {
 color: #7f8c8d;
 font-style: italic;
 margin-bottom: 8px;
 }
 
 .skills-grid {
 display: grid;
 grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
 gap: 10px;
 }
 
 .skill-item {
 background: #f8f9fa;
 padding: 10px 15px;
 border-radius: 5px;
 display: flex;
 align-items: center;
 gap: 8px;
 }
 
 .skill-icon {
 width: 8px;
 height: 8px;
 background: #3498db;
 border-radius: 50%;
 flex-shrink: 0;
 }
 
 .activities-list {
 list-style: none;
 padding: 0;
 }
 
 .activities-list li {
 padding: 5px 0;
 padding-left: 25px;
 position: relative;
 }
 
 .activities-list li::before {
 content: "▹";
 position: absolute;
 left: 0;
 color: #3498db;
 font-weight: bold;
 }
 
 .soft-skills {
 display: flex;
 flex-wrap: wrap;
 gap: 10px;
 }
 
 .soft-skill-tag {
 background: #3498db;
 color: white;
 padding: 8px 15px;
 border-radius: 20px;
 font-size: 0.9em;
 }

 .footer {
 background: #2c3e50;
 color: white;
 text-align: center;
 padding: 20px;
 font-size: 0.9em;
 }
 </style>
</head>
<body>
 <div class="container">
 <div class="header">
 <h1>Áureo Henrique Badaró de Carvalho</h1>
 <div class="subtitle">Estágio em Suporte em Informática / TI</div>
 <div class="contact-info">
 <span>Localidade: Belo Horizonte/MG</span>
 <span>Telefone: (31) 98492-9169</span>
 <span>E-mail: aureoykz@gmail.com</span>
 </div>
 </div>
 
 <div class="content">
 <div class="section">
 <h3 class="section-title">Objetivo</h3>
 <div class="objective-text">
 Atuar como estagiário na área de Suporte em Tecnologia da Informação, em 
 empresa do ramo de software e desenvolvimento, aplicando conhecimentos 
 técnicos adquiridos na formação técnica.
 </div>
 </div>
 
 <div class="section">
 <h3 class="section-title">Formação Acadêmica</h3>
 <div class="education">
 <h4>Ensino Médio + Técnico em Informática</h4>
 <div class="institution">
 <strong>Série:</strong> 3ª série do Ensino Médio<br>
 <strong>Previsão de conclusão:</strong> Dezembro/2026
 </div>
 </div>
 </div>
 
 <div class="section">
 <h3 class="section-title">Experiência Profissional</h3>
 <div class="experience">
 <h4>Estagiário de Suporte em Informática</h4>
 <div class="company">
 <strong>Empresa de Software / Desenvolvimento</strong><br>
 <strong>Período:</strong> Janeiro/2025 — Abril/2026
 </div>
 <ul class="activities-list">
 <li>Atendimento a usuários (help desk)</li>
 <li>Suporte técnico de primeiro nível (N1)</li>
 <li>Instalação e configuração de softwares</li>
 <li>Apoio na configuração de estações de trabalho</li>
 </ul>
 </div>
 </div>
 
 <div class="section">
 <h3 class="section-title">Conhecimentos Técnicos</h3>
 <div class="skills-grid">
 <div class="skill-item"><span class="skill-icon"></span>Suporte técnico</div>
 <div class="skill-item"><span class="skill-icon"></span>Windows / Linux</div>
 <div class="skill-item"><span class="skill-icon"></span>Python, C#, PHP</div>
 <div class="skill-item"><span class="skill-icon"></span>Pacote Office</div>
 </div>
 </div>

 <div class="section">
 <h3 class="section-title">Competências Comportamentais</h3>
 <div class="soft-skills">
 <span class="soft-skill-tag">Boa comunicação</span>
 <span class="soft-skill-tag">Organização</span>
 <span class="soft-skill-tag">Responsabilidade</span>
 <span class="soft-skill-tag">Trabalho em Equipe</span>
 </div>
 </div>
 </div>
 <div class="footer">
 Currículo atualizado - 2026
 </div>
 </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(CURRICULO_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)
