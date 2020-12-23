import pyrebase
from django.shortcuts import render
from django.contrib import auth as autent
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("/app/mix_brasil/credencial.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
pyrebase = pyrebase.initialize_app()
auth = pyrebase.auth()

@login_required(login_url='')
def index(request):
    teste = db.collection('categorias')
    docs = teste.stream()
    return render(request, 'index.html',{'lista': docs})


def logar(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
        except:
            mensagem = "Login inválido"
            return render(request, 'login.html', {"msg": mensagem})
        print(user['idToken'])
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        return HttpResponseRedirect("index")
    return render(request, "login.html")

@login_required(login_url='')
def logout(request):
    autent.logout(request)
    return HttpResponseRedirect("logar")


