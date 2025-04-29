import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import pandas as pd
from models import db, User, Upload

app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = 'chave_secreta_runseo'

# Crie a pasta instance para banco (evita problemas de permissão no Railway)
if not os.path.exists('instance'):
    os.makedirs('instance')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/runseo.db'

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

# Crie a pasta uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Inicializa banco e login
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, faça login para acessar esta página."
login_manager.init_app(app)

# Cria tabelas
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('E-mail já registrado.')
            return redirect(url_for('register'))
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Cadastro realizado com sucesso. Faça login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Credenciais inválidas.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    uploads = Upload.query.filter_by(user_id=current_user.id).order_by(Upload.upload_date.desc()).all()
    return render_template('dashboard.html', uploads=uploads)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files.get('csv_file')
        if file and file.filename.endswith('.csv'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            df = pd.read_csv(filepath)
            preview = df.head().to_json()
            new_upload = Upload(filename=filename, user_id=current_user.id, content_preview=preview)
            db.session.add(new_upload)
            db.session.commit()
            return redirect(url_for('insights', upload_id=new_upload.id))
        flash('Por favor, envie um arquivo CSV válido.')
    return render_template('upload.html')

@app.route('/insights/<int:upload_id>')
@login_required
def insights(upload_id):
    upload = Upload.query.get_or_404(upload_id)
    if upload.user_id != current_user.id:
        flash('Acesso negado.')
        return redirect(url_for('dashboard'))

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], upload.filename)

    try:
        df_raw = pd.read_csv(filepath, sep=None, engine='python', encoding='utf-8', decimal=',', thousands='.')
    except Exception as e:
        flash(f'Erro ao ler o CSV: {str(e)}')
        return redirect(url_for('dashboard'))

    df = df_raw.copy()
    df = df.apply(pd.to_numeric, errors='coerce')

    def get_col(df, names, fallback_idx):
        for name in names:
            if name in df.columns:
                return df[name]
        if fallback_idx < len(df.columns):
            return df.iloc[:, fallback_idx]
        return pd.Series([0]*len(df))

    try:
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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
