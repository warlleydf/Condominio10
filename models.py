from app import db

class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unidade = db.Column(db.String(10), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)
    porteiro_recebimento = db.Column(db.String(50), nullable=False)
    data_recebimento = db.Column(db.Date, nullable=False)
    morador_retirada = db.Column(db.String(50), nullable=True)
    porteiro_entrega = db.Column(db.String(50), nullable=True)
    data_retirada = db.Column(db.Date, nullable=True)
