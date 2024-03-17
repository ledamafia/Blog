from flask import render_template, flash, redirect, url_for, request, abort
from blog import app, db, bcrypt
from blog.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from blog.models import Usuario, Post
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image

temas_disponiveis = ["Amor", "Espiritualidade", "Social", "Fé", "Sexualidade", "Família"]


@app.route("/")
def home():
    posts = Post.query.order_by(Post.data_criacao.desc()).limit(6).all()
    return render_template('home.html', posts=posts, temas_disponiveis=temas_disponiveis)

@app.route("/contato")
def contato():
    return render_template('contato.html', temas_disponiveis=temas_disponiveis)

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('usuarios.html', lista_usuarios=lista_usuarios, foto_perfil=foto_perfil, temas_disponiveis=temas_disponiveis)

@app.route("/feed")
@login_required
def feed():
    posts = Post.query.order_by(Post.data_criacao.desc()).limit(10).all()
    return render_template('feed.html', posts=posts, temas_disponiveis=temas_disponiveis)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash('Login efetuado com sucesso', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('home'))
        else:
            flash('Falha no Login. E-mail ou Senha Invalida', 'alert-danger')
    return render_template('login.html', form_login=form_login, temas_disponiveis=temas_disponiveis)

@app.route("/criarconta", methods=['GET', 'POST'])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        with app.app_context():
            senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
            usuario = Usuario(username=form_criarconta.username.data, email=form_criarconta.email.data, senha=senha_crypt)
            db.session.add(usuario)
            db.session.commit()
            flash('Conta criada com sucesso', 'alert-success')
            login_user(usuario)
            return redirect(url_for('home'))
    return render_template('criarconta.html', form_criarconta=form_criarconta, temas_disponiveis=temas_disponiveis)


@app.route("/sair")
@login_required
def sair():
    logout_user()
    flash('Logout realizado com sucesso', 'alert-light')
    return redirect(url_for('feed'))


@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil, temas_disponiveis=temas_disponiveis)


temas_disponiveis = ["Amor", "Espiritualidade", "Social", "Fé", "Sexualidade", "Família"]

@app.route("/tema")
def tema():
    return render_template("tema.html", temas_disponiveis=temas_disponiveis)


def obter_posts_por_tema(tema):
    # Aqui você deve consultar o banco de dados para encontrar os posts com o tema especificado
    posts = Post.query.filter_by(tema=tema).all()
    return posts

@app.route("/temas/<tema>")
@login_required
def posts_por_tema(tema):
    posts = obter_posts_por_tema(tema)
    print(posts)  # Adicione esta linha para verificar os posts recuperados
    return render_template("temas.html", tema=tema, posts=posts, temas_disponiveis=temas_disponiveisgit)

@app.route("/post/criar", methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, conteudo=form.conteudo.data, autor=current_user, tema=form.tema.data)
        db.session.add(post)
        db.session.commit()
        flash('Post criado com sucesso!', 'success')
        return redirect(url_for('feed'))  # Redireciona para a página de feed após a criação do post
    return render_template('criarpost.html', form=form, temas_disponiveis=temas_disponiveis)

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_arquivo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho_arquivo = (400, 400)
    imagem_reduzido = Image.open(imagem)
    imagem_reduzido.thumbnail(tamanho_arquivo)
    imagem_reduzido.save(caminho_arquivo)
    return nome_arquivo


def atualizar_temas(form):
    lista_temas = []
    for campo in form:
        if 'temas_' in campo.name:
            if campo.data:
                lista_temas.append(campo.label.text)
    return ' '.join(lista_temas)


@app.route("/perfil/editar", methods=['GET', 'POST'] )
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.username = form.username.data
        if form.foto_perfil.data:
            imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = imagem
        current_user.temas = atualizar_temas(form)
        db.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-light')
        return render_template('feed.html')
    elif request.method == 'GET':
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', form=form, foto_perfil=foto_perfil, temas_disponiveis=temas_disponiveis)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.conteudo.data = post.conteudo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.conteudo = form.conteudo.data
            db.session.commit()
            flash('Post atualizado com sucesso')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form, temas_disponiveis=temas_disponiveis)



from flask import request

@app.route('/post/<post_id>/excluir', methods=['POST', 'DELETE'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        if request.method == 'POST' or request.method == 'DELETE':
            db.session.delete(post)
            db.session.commit()
            flash('Post excluído com sucesso', 'alert-danger')
            return redirect(url_for('home'))
    else:
        abort(403)
    return render_template('feed.html', post=post)


















