import pyrebase
from django.shortcuts import render
from django.contrib import auth as autent
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebaseConfig = {
    'apiKey' : "AIzaSyBh-DC_fXWzzcHV6XYhFQ1Ya6MWG5OjH_w",
    'authDomain' : "mix-brasil.firebaseapp.com",
    'databaseURL': "https://mix-brasil.firebaseio.com",
    'projectId': "mix-brasil",
    'storageBucket': "mix-brasil.appspot.com",
    'messagingSenderId': "132448934641",
    'appId': "1:132448934641:web:0843ac2954464054822750",
    'measurementId': "G-VH0XXQFXES"
}

pyrebase = pyrebase.initialize_app(firebaseConfig)
auth = pyrebase.auth()

cred = credentials.Certificate("/app/mix_brasil/credencial.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@login_required("if request.session['uid'] == True", login_url='/index/')
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
        session_id = user['idToken']
        request.session['uid'] = str(session_id)
        return HttpResponseRedirect("index")
    return render(request, "login.html")

@login_required("if request.session['uid'] == True", login_url='/index/')
def logout(request):
    autent.logout(request)
    return HttpResponseRedirect("logar")


