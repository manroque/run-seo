from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_session import Session
import pandas as pd
import os

# Importa funções auxiliares do Google OAuth
from google_auth import iniciar_fluxo, trocar_codigo_por_credenciais

app = Flask(__name__)
app.secret_key = 'runseo-key'
app.config['UPLOAD_FOLDER'] = 'data/'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# =====================
# FUNÇÕES AUXILIARES
# =====================
def carregar_dados_ga4():
    caminho_csv = os.path.join(app.config['UPLOAD_FOLDER'], 'ga4_dados.csv')
    if not os.path.exists(caminho_csv):
        return None
    try:
        df = pd.read_csv(caminho_csv)
        if df.empty:
            return None
        return df
    except Exception as e:
        print("Erro ao carregar CSV:", e)
        return None

def calcular_metricas_ga4(df):
    sessoes = df['sessoes'].sum()
    novos_usuarios = df['novos_usuarios'].sum()
    conversao = round(df['conversoes'].sum() / max(sessoes, 1) * 100, 2)
    receita = df['receita'].sum()
    ticket_medio = round(receita / max(sessoes, 1), 2)
    investimento = df['investimento'].sum()
    roi = round(((receita - investimento) / max(investimento, 1)) * 100, 2)
    return sessoes, novos_usuarios, conversao, receita, ticket_medio, investimento, roi

# =====================
# ROTAS PRINCIPAIS
# =====================

@app.route('/')
def index():
    return render_template('inicio.html')

@app.route('/escolher-opcao')
def escolher_opcao():
    return render_template('escolher_opcao.html')

@app.route('/importar-csv', methods=['GET', 'POST'])
def importar_csv():
    if request.method == 'POST':
        file = request.files.get('csvfile')
        if not file or file.filename == '':
            flash("Arquivo CSV não selecionado.", "danger")
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'ga4_dados.csv'))
            flash("Arquivo importado com sucesso!", "success")
            return redirect(url_for('dashboard_ga4'))
        flash("Formato inválido. Envie um arquivo .csv", "danger")
    return render_template('importar_csv.html')

@app.route('/dashboard/search-console')
def dashboard_search_console():
    metricas = {
        "impressoes": 12000,
        "cliques": 1300,
        "ctr": round((1300 / 12000) * 100, 2),
        "posicao_media": 6.7
    }
    grafico_palavras = {
        "labels": ["Jan", "Fev", "Mar"],
        "datasets": [{"label": "Palavras-chave", "data": [120, 150, 200], "borderColor": "orange", "fill": False}]
    }
    top_palavras = {
        "labels": ["keyword1", "keyword2", "keyword3"],
        "datasets": [{"label": "Top Palavras", "data": [300, 200, 100], "backgroundColor": "blue"}]
    }
    origem_trafego = {
        "labels": ["Google", "Instagram", "Direto"],
        "datasets": [{"data": [60, 25, 15], "backgroundColor": ["#4285F4", "#E1306C", "#34A853"]}]
    }
    consultas_por_pagina = [
        {"pagina": "/home", "consulta": "exemplo1", "cliques": 50, "impressoes": 300},
        {"pagina": "/produto", "consulta": "exemplo2", "cliques": 20, "impressoes": 120}
    ]
    classificacao_palavras = {
        "labels": ["Jan", "Fev", "Mar"],
        "datasets": [{"label": "Posição Média", "data": [6.5, 5.9, 6.7], "borderColor": "purple", "fill": False}]
    }
    return render_template("dashboard_search_console.html",
                           metricas=metricas,
                           grafico_palavras=grafico_palavras,
                           top_palavras=top_palavras,
                           origem_trafego=origem_trafego,
                           consultas_por_pagina=consultas_por_pagina,
                           classificacao_palavras=classificacao_palavras)

@app.route('/dashboard/ga4')
def dashboard_ga4():
    df = carregar_dados_ga4()
    if df is None:
        flash("Erro ao carregar dados do GA4. Importe um CSV primeiro.", "danger")
        return render_template("dashboard_ga4.html", data=None, sessoes=0, novos_usuarios=0, 
                               taxa_conversao=0, receita=0, ticket_medio=0,
                               investimento=0, roi=0, 
                               meses=[], receita_mensal=[], sessoes_mensal=[],
                               canais=[], canais_valores=[], paginas_vencedoras=[])

    sessoes, novos_usuarios, conversao, receita, ticket_medio, investimento, roi = calcular_metricas_ga4(df)

    meses = df['mes'].unique().tolist()
    receita_mensal = df.groupby('mes')['receita'].sum().tolist()
    sessoes_mensal = df.groupby('mes')['sessoes'].sum().tolist()
    canais = df['fonte'].unique().tolist()
    canais_valores = df.groupby('fonte')['sessoes'].sum().tolist()
    paginas_vencedoras = df[['url', 'categoria', 'sessoes', 'receita']].to_dict(orient='records')

    return render_template("dashboard_ga4.html",
                           data=request.args.get('data'),
                           sessoes=sessoes,
                           novos_usuarios=novos_usuarios,
                           taxa_conversao=conversao,
                           receita=receita,
                           ticket_medio=ticket_medio,
                           investimento=investimento,
                           roi=roi,
                           meses=meses,
                           receita_mensal=receita_mensal,
                           sessoes_mensal=sessoes_mensal,
                           canais=canais,
                           canais_valores=canais_valores,
                           paginas_vencedoras=paginas_vencedoras)

@app.route('/roi', methods=['GET', 'POST'])
def calculo_roi():
    roi = None
    if request.method == 'POST':
        receita = float(request.form['receita'])
        investimento = float(request.form['investimento'])
        if investimento != 0:
            roi = round(((receita - investimento) / investimento) * 100, 2)
        else:
            roi = 0
    return render_template('calculo_roi.html', roi=roi)

# =====================
# LOGIN COM GOOGLE
# =====================
@app.route('/login-google')
def login_google():
    auth_url = iniciar_fluxo()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    trocar_codigo_por_credenciais(code)
    flash("Login com Google realizado com sucesso!", "success")
    return redirect(url_for('escolher_opcao'))

if __name__ == '__main__':
    app.run(debug=True)