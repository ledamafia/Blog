from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from wtforms import RadioField

from blog.models import Usuario


class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Campo obrigatório.")])
    email = StringField('E-mail', validators=[DataRequired(), Email(message="E-mail inválido.")])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20, message="A senha deve ter entre 6 e 20 caracteres.")])
    confirmacao_senha = StringField('Confirme sua senha', validators=[DataRequired(), EqualTo('senha', message="As senhas não coincidem.")])
    submit = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login para continuar')

    def validate_username(self, username):
        usuario = Usuario.query.filter_by(username=username.data).first()
        if usuario:
            raise ValidationError('Username já cadastrado. Cadastre-se com outro username ou faça login com e-mail para continuar')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email(message="E-mail inválido.")])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6, max=20, message="A senha deve ter entre 6 e 20 caracteres.")])
    submit = SubmitField('Login')
    lembrar_dados = BooleanField('Lembrar dados')



class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(message="Campo obrigatório.")])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    temas_amor = BooleanField('Amor')
    temas_espitualidade = BooleanField('Espiritualidade')
    temas_social = BooleanField('Social')
    temas_fe = BooleanField('Fé')
    temas_sexualidade = BooleanField('Sexualidade')
    temas_familia = BooleanField('Familia')
    submit = SubmitField('Editar Perfil')

    def validate_username(self, username):
        if current_user.username != username.data:
            usuario = Usuario.query.filter_by(username=username.data).first()
            if usuario:
                raise ValidationError('Username já cadastrado. Por favor, escolha outro.')



class FormCriarPost(FlaskForm):
    titulo = StringField('Título do post', validators=[DataRequired(), Length(2, 40)])
    conteudo = TextAreaField('Escreva seu post', validators=[DataRequired(message="Campo obrigatório.")])
    tema = SelectField('Tema', choices=[('Amor', 'Amor'), ('Espiritualidade', 'Espiritualidade'), ('Social', 'Social'), ('Fé', 'Fé'), ('Sexualidade', 'Sexualidade'), ('Familia', 'Família')], validators=[DataRequired()])
    submit = SubmitField('Postar')

