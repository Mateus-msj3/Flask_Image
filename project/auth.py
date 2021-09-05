import os
import base64
from io import BytesIO

from flask import Flask, Response, Blueprint, render_template, redirect, url_for, request, flash
from flask_thumbnails import Thumbnail, thumbnail
from PIL import Image
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Images

import json
from . import db

#IMAGE_UPLOADS = '/home/mateus/Dropbox/Flask_Image_App/save-images'

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        # if user doesn't exist or password is wrong, reload the page
        return redirect(url_for('auth.login'))

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():

    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # if this returns a user, then the email already exists in database
    user = User.query.filter_by(email=email).first()

    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, name=name,
                    password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@auth.route('/profile/<int:id>', methods=['GET', 'POST'])
def profile_post(id):
    # pega o usuário
    user = User.query.filter_by(id=id).first()

    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']

        if email and name:
            user.email = email
            user.name = name

            db.session.commit()
            flash('Usuário alterado com sucesso')

            return redirect(url_for('auth.profile'))
    return render_template('profile.html', user=user)


@auth.route('/upload-image', methods=['GET', 'POST'])
def upload_image():

    if request.method == 'POST':
        name = request.form.get('name')
        resume = request.form.get('resume')

        image = request.files['files']

        if image.filename == '':
            flash('Selecione uma imagem válida')
            return redirect(request.url)

        if image.filename != '':
            converte_imagem = base64.encodestring(image.read())
            #converte_imagem = converte_imagem.decode('utf-8')

        new_image = Images(name=name, resume=resume, image=converte_imagem)

        db.session.add(new_image)
        db.session.commit()
        flash('Salvo com sucesso')
        print('Salvo com sucesso')

    return render_template('upload.html')


@auth.route('/gerenciamento-imagens')
def gerenciamento_imagens():
    all_images = Images.query.all()
    #decode_all_images =Image.open(BytesIO(base64.b64decode(all_images)))
    # Image.open(BytesIO(base64.b64decode(data)))

    return render_template('gerenciar_imagens.html', all_images=all_images)


@auth.route('/excluir-imagens/<int:id>')
def excluir_imagens(id):

    all_image = Images.query.filter_by(id=id).first()

    db.session.delete(all_image)
    db.session.commit()

    all_images = Images.query.all()

    return render_template('gerenciar_imagens.html', all_images=all_images)


@auth.route('/gerenciar-databases')
def gerenciar_databases():
    return 'Gerenciar Databases'


@auth.route('/thumbnails')
def obter_thumbnails():
    thumb_images = Images.query.all()
    

    return render_template('thumbnails.html', thumb_images=thumb_images)
