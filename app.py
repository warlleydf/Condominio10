from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///encomendas.db'
db = SQLAlchemy(app)

# Form Definitions

class RegistrarEncomendaForm(FlaskForm):
    unidade = SelectField('Unidade', choices=[('101', '101'), ('102', '102'), ('201', '201'), ('301', '301'), ('302', '302'), ('401', '401'), ('402', '402'), ('501', '501'), ('502', '502')], validators=[DataRequired()])
    tipo = SelectField('Tipo de Encomenda', choices=[('carta', 'Carta'), ('envelope', 'Envelope'), ('pacote', 'Pacote'), ('caixa', 'Caixa')], validators=[DataRequired()])
    porteiro_recebimento = StringField('Nome do Porteiro', validators=[DataRequired()])
    data_recebimento = DateField('Data de Recebimento', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Registrar')

class DarBaixaForm(FlaskForm):
    id = SelectField('ID da Encomenda', coerce=int, validators=[DataRequired()])
    morador_retirada = StringField('Nome do Morador', validators=[DataRequired()])
    porteiro_entrega = StringField('Nome do Porteiro', validators=[DataRequired()])
    data_retirada = DateField('Data de Retirada', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Dar Baixa')


# Views

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    form = RegistrarEncomendaForm()
    if form.validate_on_submit():
        encomenda = Encomenda(
            unidade=form.unidade.data,
            tipo=form.tipo.data,
            porteiro_recebimento=form.porteiro_recebimento.data,
            data_recebimento=form.data_recebimento.data
        )
        db.session.add(encomenda)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('registrar_encomenda.html', form=form)
    
@app.route('/dar_baixa', methods=['GET', 'POST'])
def dar_baixa():
    encomendas_pendentes = Encomenda.query.filter_by(morador_retirada=None).all()
    form = DarBaixaForm()
    
    # Preencher as opções de seleção com os IDs das encomendas pendentes
    form.id.choices = [(encomenda.id, encomenda.id) for encomenda in encomendas_pendentes]
    
    if form.validate_on_submit():
        encomenda = Encomenda.query.get(form.id.data)
        encomenda.morador_retirada = form.morador_retirada.data
        encomenda.porteiro_entrega = form.porteiro_entrega.data
        encomenda.data_retirada = form.data_retirada.data
        db.session.commit()
        return redirect(url_for('dar_baixa'))
    
    return render_template('dar_baixa.html', form=form, encomendas_pendentes=encomendas_pendentes)

@app.route('/historico')
def historico():
    encomendas_retiradas = Encomenda.query.filter(Encomenda.morador_retirada.isnot(None)).all()
    return render_template('historico.html', encomendas_retiradas=encomendas_retiradas)

# Models

class Encomenda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unidade = db.Column(db.String(4), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    porteiro_recebimento = db.Column(db.String(100), nullable=False)
    data_recebimento = db.Column(db.Date, nullable=False)
    morador_retirada = db.Column(db.String(100))
    porteiro_entrega = db.Column(db.String(100))
    data_retirada = db.Column(db.Date)

if __name__ == '__main__':
    app.run(debug=True)
