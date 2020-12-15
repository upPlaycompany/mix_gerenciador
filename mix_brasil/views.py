import pyrebase
from django.shortcuts import render
from django.contrib import auth as autent
from firebase_admin import firestore, initialize_app, credentials

firebaseConfig = {
    'apiKey': "AIzaSyBh-DC_fXWzzcHV6XYhFQ1Ya6MWG5OjH_w",
    'authDomain': "mix-brasil.firebaseapp.com",
    'databaseURL': "https://mix-brasil.firebaseio.com",
    'projectId': "mix-brasil",
    'storageBucket': "mix-brasil.appspot.com",
    'messagingSenderId': "132448934641",
    'appId': "1:132448934641:web:0843ac2954464054822750",
    'measurementId': "G-VH0XXQFXES"
}

firebase_with_admin = firebase_admin.initialize_app(firebaseConfig)
firebase_normal = pyrebase.initialize_app(firebaseConfig)
auth = firebase_normal.auth()
a = firebase.credentials.from_json(firebaseConfig)
db = firestore.client()

def index(request):
    teste = db.collection(u'categorias')
    doc = teste.stream()
    return render(request, 'index.html', {'lista': doc})


def login(request):
    return render(request, 'login.html')


def post_sign_in(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = auth.sign_in_with_email_and_password(email, password)
    except:
        mensagem = "Login inválido"
        return render(request, 'login.html', {"msg": mensagem})
    print(user['idToken'])
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request, "index.html", {'e': email})


def logout(request):
    autent.logout(request)
    return render(request, 'login.html')

