from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired

class RegistrarEncomendaForm(FlaskForm):
    unidade = SelectField('Unidade', choices=[('101', '101'), ('102', '102'), ('201', '201'), ('301', '301'), ('302', '302'), ('401', '401'), ('402', '402'), ('501', '501'), ('502', '502')], validators=[DataRequired()])
    tipo = SelectField('Tipo', choices=[('carta', 'Carta'), ('envelope', 'Envelope'), ('pacote', 'Pacote'), ('caixa', 'Caixa')], validators=[DataRequired()])
    porteiro = StringField('Porteiro', validators=[DataRequired()])
    data_recebimento = DateField('Data de Recebimento', format='%Y-%m-%d', validators=[DataRequired()])

class DarBaixaForm(FlaskForm):
    id = IntegerField('ID da Encomenda', validators=[DataRequired()])
    morador = StringField('Morador', validators=[DataRequired()])
    porteiro = StringField('Porteiro', validators=[DataRequired()])
    data_retirada = DateField('Data de Retirada', format='%Y-%m-%d', validators=[DataRequired()])
