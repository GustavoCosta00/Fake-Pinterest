# cria os formulários do site 
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from fakePinterest.models import Usuario

class Login(FlaskForm):
    email = StringField("Email", validators=[DataRequired(),Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer Login")

class criarUsuario(FlaskForm):
    userName = StringField("Nome do Usuário", validators=[DataRequired()])
    email = StringField("Email do Usuário", validators=[DataRequired()])
    senha = PasswordField("Senha do Usuário", validators=[DataRequired()])
    confirmar_senha = PasswordField("Confimar senha", validators=[DataRequired(), EqualTo("senha")])
    botao = SubmitField("Criar Conta!", validators=[DataRequired()])

    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email = email.data).first()
        if(usuario):
            return ValidationError("O Email inserido já está em uso")
        
class FormFoto(FlaskForm):
    foto = FileField("Inserir Foto", validators=[DataRequired()])
    botao = SubmitField("Enviar")
