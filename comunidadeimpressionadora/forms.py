from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired(message="Digite o seu nome de usuario")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Digite o seu email")])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação de senha',
                                      validators=[DataRequired(),
                                                  EqualTo('senha',
                                                          message="Confirme a senha corretamente")])
    botao_submite_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail ja cadastrado. Cadastatre-se com outro email ou faça login')


class Formlogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('Lembrar Dados de Acesso')
    botao_submite_login = SubmitField('Entrar')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome do Usuário', validators=[DataRequired(message="Digite o seu nome de usuario")])
    email = StringField('Email', validators=[DataRequired(), Email(message="Digite o seu email")])
    foto_perfil = FileField('Atualizar foto de perfil ',
                            validators=[FileAllowed(['jpg', 'png'],
                                                    message='[ERRO] - O arquivo deve estar no formato jpg ou png')])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA Impressionador')
    curso_python = BooleanField('Python Impressionador')
    curso_powerbi = BooleanField('Power BI Impressionador')
    curso_ppt = BooleanField('Apresentações Impressionadoras')
    curso_sql = BooleanField('SQL Impressionador')

    botao_submite_editarperfil = SubmitField('Confirmar edição')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Ja existe um usuario com esse email')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do post', validators=[DataRequired('Digite o titulo do post'), Length(2, 140)])
    corpo = TextAreaField('Escreva seu post aqui', validators=[DataRequired(message='Você precisa digitar algo')])
    botao_submite = SubmitField('Enviar')
