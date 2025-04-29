import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from models import db, User, Upload

# === CONFIGURAÇÃO DE PASTAS E CAMINHOS ===

# Caminho absoluto da raiz do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Pasta 'instance' para armazenar banco e uploads (garante permissão de escrita no Railway)
INSTANCE_PATH = os.path.join(BASE_DIR, 'instance')
os.makedirs(INSTANCE_PATH, exist_ok=True)  # Cria a pasta se não existir

# Pasta para uploads dentro de 'instance'
UPLOAD_PATH = os.path.join(INSTANCE_PATH, 'uploads')
os.makedirs(UPLOAD_PATH, exist_ok=True)  # Cria a pasta se não existir

# === CONFIGURAÇÃO DO FLASK ===

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chave_secreta_runseo'  # Defina uma chave secreta segura para produção

# Configura o banco SQLite dentro da pasta instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(INSTANCE_PATH, 'runseo.db')

# Configura a pasta de uploads e tamanho máximo de arquivo (10MB)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

# === INICIALIZAÇÃO DO BANCO E LOGIN ===

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'  # Redireciona para login se não autenticado
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.init_app(app)

# Cria as tabelas do banco se não existirem
with app.app_context():
    db.create_all()

# === FUNÇÃO PARA CARREGAR USUÁRIO NA SESSÃO ===

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# === ROTAS ===

@app.route('/')
def home():
    # Redireciona para login
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Cadastro de usuário
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Verifica se email já existe
        if User.query.filter_by(email=email).first():
            flash('E-mail já registrado.')
            return redirect(url_for('register'))

        # Cria hash da senha para segurança
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')

        # Cria novo usuário e salva no banco
        new_user = User(email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Cadastro realizado com sucesso. Faça login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Login de usuário
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        # Verifica usuário e senha
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))

        flash('Credenciais inválidas.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    # Logout do usuário
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Página principal do usuário com lista de uploads
    uploads = Upload.query.filter_by(user_id=current_user.id).order_by(Upload.upload_date.desc()).all()
    return render_template('dashboard.html', uploads=uploads)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # Upload de arquivo CSV
    if request.method == 'POST':
        file = request.files.get('csv_file')

        # Verifica se arquivo enviado e se é CSV
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)  # Salva arquivo no diretório correto

            # Lê o CSV para gerar preview
            df = pd.read_csv(filepath)
            preview = df.head().to_json()

            # Salva upload no banco
            new_upload = Upload(filename=filename, user_id=current_user.id, content_preview=preview)
            db.session.add(new_upload)
            db.session.commit()

            return redirect(url_for('insights', upload_id=new_upload.id))

        flash('Por favor, envie um arquivo CSV válido.')

    return render_template('upload.html')

@app.route('/insights/<int:upload_id>')
@login_required
def insights(upload_id):
    # Página de insights baseada no upload CSV
    upload = Upload.query.get_or_404(upload_id)

    # Verifica se upload pertence ao usuário logado
    if upload.user_id != current_user.id:
        flash('Acesso negado.')
        return redirect(url_for('dashboard'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload.filename)

    try:
        # Lê o CSV com opções para lidar com diferentes formatos
        df_raw = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8', decimal=',', thousands='.')
    except Exception as e:
        flash(f'Erro ao ler o CSV: {str(e)}')
        return redirect(url_for('dashboard'))

    df = df_raw.copy()
    df = df.apply(pd.to_numeric, errors='coerce')

    # Função para pegar coluna por nomes possíveis ou índice fallback
    def get_col(df, names, fallback_idx):
        for name in names:
            if name in df.columns:
                return df[name]
        if fallback_idx < len(df.columns):
            return df.iloc[:, fallback_idx]
        return pd.Series([0]*len(df))

    try:
        # Calcula métricas principais
        total_impressao = get_col(df, ['Impressões'], 0).sum()
        total_cliques = get_col(df, ['Cliques'], 1).sum()
        ctr = (total_cliques / total_impressao) * 100 if total_impressao > 0 else 0
        posicao_media = get_col(df, ['Posição Média'], 2).mean()
        novos_usuarios = get_col(df, ['Novos Usuários'], 3).sum()
        conversoes = get_col(df, ['Conversões'], 4).sum()
        taxa_conversao = (conversoes / total_cliques) * 100 if total_cliques > 0 else 0
        receita = get_col(df, ['Receita'], 5).sum()
        ticket_medio = receita / conversoes if conversoes > 0 else 0
        total_sessoes = get_col(df, ['Sessões'], 6).sum()
    except Exception as e:
        flash(f'Erro ao calcular métricas: {str(e)}')
        return redirect(url_for('dashboard'))

    return render_template('insights.html',
                           total_impressao=total_impressao,
                           total_cliques=total_cliques,
                           ctr=ctr,
                           posicao_media=posicao_media,
                           novos_usuarios=novos_usuarios,
                           conversoes=conversoes,
                           taxa_conversao=taxa_conversao,
                           receita=receita,
                           ticket_medio=ticket_medio,
                           receita_total=receita,
                           total_sessoes=total_sessoes,
                           origem_trafego="Orgânico",
                           headers=list(df_raw.columns),
                           rows=df_raw.values.tolist())

@app.route('/roi', methods=['GET', 'POST'])
@login_required
def roi():
    # Página para cálculo de ROI
    resultado = None
    if request.method == 'POST':
        receita = float(request.form['receita'])
        custo = float(request.form['custo'])
        if custo == 0:
            resultado = "O custo não pode ser zero."
        else:
            roi_valor = (receita - custo) / custo
            resultado = f"ROI: {roi_valor:.2f} ({roi_valor * 100:.2f}%)"
    return render_template('roi.html', resultado=resultado)

# Rota simples para teste de funcionamento no Railway
@app.route('/ping')
def ping():
    return 'pong'

print("==== APP PRONTO PARA SERVIDOR ====")

# === INICIALIZAÇÃO DO SERVIDOR ===

if __name__ == '__main__':
    # Porta definida pela variável de ambiente PORT no Railway (ou 5000 local)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
