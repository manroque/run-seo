from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SEOData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sessoes = db.Column(db.Integer)
    novos_usuarios = db.Column(db.Integer)
    conversoes = db.Column(db.Integer)
    receita = db.Column(db.Float)
    ticket_medio = db.Column(db.Float)
    investimento = db.Column(db.Float)
    roi = db.Column(db.Float)

    def __init__(self, sessoes, novos_usuarios, conversoes, receita, ticket_medio, investimento, roi):
        self.sessoes = sessoes
        self.novos_usuarios = novos_usuarios
        self.conversoes = conversoes
        self.receita = receita
        self.ticket_medio = ticket_medio
        self.investimento = investimento
        self.roi = roi
