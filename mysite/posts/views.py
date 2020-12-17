from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Post, Account
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from posts.forms import SignUpForm
import datetime
import sqlite3

if len(User.objects.all()) < 1:
    User.objects.create_user('jack', 'aa@aa.aa', 'kittens')
    User.objects.create_user('connie', 'bb@bb.bb', 'puppers')
    jack = User.objects.filter(username='jack')
    if jack is not None:
        jackAccount = Account(user=jack)
        jackAccount.save()
    connie = User.objects.filter(username='connie')
    if connie is not None:
        connieAccount = Account(user=connie)
        connieAccount.save()

def index(request):
    return render(request, 'posts/index.html')

def postlist(request):
    posts_list = Post.objects.all().order_by('date')
    if request.method == 'POST':
        conn = sqlite3.connect('db.sqlite3')
        cursor = conn.cursor()
        response = cursor.execute("SELECT id, text FROM Posts_post WHERE text LIKE '%%%s%%'" % (request.POST.get('search', ''))).fetchall()
        posts_list = []
        for i in response:
            post = {'id': i[0], 'text': i[1]}
            posts_list.append(post)
    context = {'posts_list': posts_list}
    return render(request, 'posts/posts.html', context)

def add_post(request):
    posts_list = request.session.get('posts_list', [])
    if request.method == 'POST':
        text = request.POST.get('new_post', '').strip()
        price = request.POST.get('price', '')
        # conn = sqlite3.connect('db.sqlite3')
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO Posts_post (text, price, date, sold, account_id) VALUES ('%s', '%s', '%s', 'False', '%s')" % (text, price, datetime.datetime.now(), request.user.account.id)).fetchall()
        post = Post(text=text, price=price, date=datetime.datetime.now(), account=request.user.account)
        post.save()
        return redirect('/posts/list', {'posts_list': posts_list})

def posting(request, post_id):
    post = Post.objects.filter(id=post_id)[0]
    owner_account = Account.objects.filter(id=post.account_id)[0]
    owner_user = User.objects.filter(id=owner_account.user_id)[0]
    return render(request, 'posts/post.html', {'posting': post, 'email': owner_user.email})

def purchase(request, post_id, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        account = Account.objects.filter(user_id=user.id)[0]
        post = Post.objects.get(id=post_id)

        owner_account = Account.objects.filter(id=post.account_id)[0]
        owner_user = User.objects.filter(id=owner_account.user_id)[0]

        if account.points < post.price:
            return render(request, 'posts/post.html', {'posting': post, 'email': owner_user.email, 'invalid': True})
        
        account = Account.objects.get(user_id=user.id)
        account.points = account.points - post.price
        account.save()
        post.sold = True
        post.save()

        return  render(request, 'posts/post.html', {'posting': post, 'email': owner_user.email})

def profile(request, user_id):
    user = User.objects.filter(id=user_id)[0]
    account = Account.objects.filter(user_id=user_id)[0]
    return render(request, 'posts/profile.html', {'user': user, 'account': account})

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        redirect('/posts/')

def logout_view(request):
    logout(request)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'posts/register.html', {'form': form})
