# cria as rotas do site 
from flask import render_template, redirect, url_for
from fakePinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from fakePinterest.forms import Login, criarUsuario, FormFoto
from fakePinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET","POST"])
def homepage():
    formLogin =  Login()
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email = formLogin.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for("usuario",id_usuario = usuario.id))
    
    return render_template("homePage.html", form = formLogin)

@app.route("/criarConta", methods=["GET","POST"])
def newUser():
    formCriarConta = criarUsuario()
    if formCriarConta.validate_on_submit():
        senha_hash = bcrypt.generate_password_hash(formCriarConta.senha.data).decode('utf-8')
        usuario = Usuario(nome=formCriarConta.userName.data,
                          email=formCriarConta.email.data,
                          senha=senha_hash)  # Armazenar a senha como hash
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("usuario", id_usuario = usuario.id))
    return render_template("criarConta.html", form=formCriarConta)


@app.route("/usuario/<id_usuario>", methods=["GET","POST"])
@login_required
def usuario(id_usuario):
    if int(id_usuario) == int(current_user.id):
            # NESSE CAMPO O USUÁRIO VISUALIZA O PRÓPRO PERFIL 
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                              app.config["UPLOAD_FOLDER"], nome_seguro)
            arquivo.save(caminho)
            foto = Foto(imagem = nome_seguro ,id_usuario =  id_usuario )
            database.session.add(foto)
            database.session.commit()
        return render_template("usuario.html", usuario = current_user, form = form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("usuario.html", usuario = usuario, form = None)

@app.route("/logOut")
@login_required
def Sair():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/Feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos = fotos)