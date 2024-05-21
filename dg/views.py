"""This module describes main logic of server"""
import datetime
import json
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from django.views.decorators.http import require_http_methods
from dg.models import *
from dg.forms import *
from django.contrib import messages


@register.filter
def get_item(dictionary, key):
    """This function returns dictionary value by key"""
    return dictionary[key]


def get_base_context(request):
    """This function returns base page"""
    menu = [
        {"link": "/", "text": "Главная"},
        {"link": "/global_chat", "text": "Глобальный чат"},
    ]

    if request.user.is_authenticated:
        menu.append({"link": "/profile", "text": "Профиль"})
        menu.append({"link": "/logout", "text": "Выход"})
    else:
        menu.append({"link": "/login", "text": "Вход"})
        menu.append({"link": "/register", "text": "Регистрация"})

    context = {'menu': menu, 'error': ''}
    return context


def home_page(request):
    """This function renders main page"""
    context = get_base_context(request)
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        chats1 = Chat.objects.all().filter(uid1=request.user.id)
        chats2 = Chat.objects.all().filter(uid2=request.user.id)
        chats = chats1.union(chats2)
        context['chats'] = chats
        names = {}
        for chat in chats:
            if chat.uid1 == request.user.id:
                names[chat.id] = User.objects.all().filter(id=chat.uid2)[0].username
            elif chat.uid2 == request.user.id:
                names[chat.id] = User.objects.all().filter(id=chat.uid1)[0].username
        context['names'] = names
        messages = {}
        ids = []
        usernames = {}
        last_messages = {}
        for chat in chats:
            if Message.objects.all().filter(chat_id=chat.id):
                last_messages[chat.id] = Message.objects.all().filter(chat_id=chat.id)[0].time
            messages_new = []
            for message in Message.objects.all().filter(chat_id=chat.id):
                messages_new.append(message)
            ids.append(str(chat.id))
            messages[str(chat.id)] = messages_new
            usernames[chat.uid1] = User.objects.all().filter(id=chat.uid1)[0].username
            usernames[chat.uid2] = User.objects.all().filter(id=chat.uid2)[0].username
        context['usernames'] = usernames
        context['ids'] = ids
        context['messages'] = messages
        context['newchatform'] = CreateChatForm()
        context['sendmessageform'] = SendMessageFrom()
        context['last_messages'] = last_messages
    return render(request, "index.html", context)


def register_user(request):
    """function returns register page(/register) to the client and saves new users

    :request: variable containing http parameters
    """
    context = {}
    context['invalid_register'] = ""
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            new_balance = UserBalance(
                user_id=new_user.id,
                money=0)
            new_balance.save()
            context["balance"] = new_balance
            return redirect('/login')
        if User.objects.filter(username=user_form.data.get('username')).exists():
            context['invalid_register'] += "User with this username already exists\n"
        if user_form.data.get('password') != user_form.data.get('password2'):
            context['invalid_register'] += "Passwords don't match\n"
    else:
        user_form = UserRegistrationForm()
        context['user_form'] = user_form
    return render(request, 'registration/register.html', context)


def profile(request):
    """This function renders profile page"""
    context = get_base_context(request)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            if request.user.check_password(form.data.get('old_password')):
                user = User.objects.get(username__exact=request.user.username)
                user.set_password(form.data.get('new_password'))
                user.save()
            else:
                context['error'] = ("You forgot to fill in the password field.")
        return redirect('/logout')
    if not request.user.is_authenticated:
        return redirect('/login')
    change_pass_form = ChangePasswordForm()
    user_balance = UserBalance.objects.all().filter(user_id=request.user.id)[0].money
    context = {'user': request.user, 'change_pass_form':
        change_pass_form, 'user_balance': user_balance}
    return render(request, 'profile.html', context)


@login_required
def send_message(request):
    """This function renders send_message request"""
    context = get_base_context(request)
    if request.method == 'POST':
        user_form = SendMessageFrom(request.POST)
        chat_id = user_form.data.get('chat_id')
        chat = Chat.objects.all().filter(id=chat_id)
        if chat_id != '':
            request_files = request.FILES.getlist('files')
            if not chat:
                context['error'] = 'No such chat'
            chat = chat[0]
            if request.user.id not in (chat.uid1, chat.uid2):
                context['error'] = 'No such chat'
            if user_form.is_valid() or request_files:
                new_field = Message(time=datetime.datetime.now(),
                                    chat_id=chat.id, sender_id=request.user.id,
                                    text=user_form.data.get('text'))
                new_field.save()
                for f in request_files:
                    file = MessageFileDirect(file=f, message=new_field, name=f.name, size=(f.size / 1000))
                    file.save()
    return redirect('/')


@require_http_methods(["POST"])
def new_chat(request):
    """This function processes newChat request"""
    context = get_base_context(request)
    if request.method == 'POST':
        user_form = CreateChatForm(request.POST)
        if user_form.is_valid():
            if not User.objects.all().filter(username=user_form.data.get('user_to')):
                context['error'] = 'No such user'
            else:
                secondusername = user_form.data.get('user_to')
                existing_chats = Chat.objects.all().filter(uid1=request.user.id,
                                                           uid2=User.objects.all().filter(
                                                               username=secondusername)[
                                                               0].id) | \
                                 Chat.objects.all().filter(
                                     uid2=request.user.id,
                                     uid1=User.objects.all().filter(username=secondusername)[0].id)
                if len(existing_chats) != 0:
                    context['error'] = 'Chat already exists'
                    return redirect('/', context=context)
                new_field = Chat(uid1=request.user.id,
                                 uid2=User.objects.all().filter(username=secondusername)[0].id)
                new_field.save()
    return redirect('/')


def global_chat(request):
    """This function renders global chat page"""
    context = {}
    if request.method == "POST":
        form = GlobalChatForm(request.POST)
        request_files = request.FILES.getlist('files')
        if form.data['text'] or request_files:
            if request.user.is_authenticated:
                new_message = GlobalChat(
                    sender_username=request.user.username,
                    text=form.data["text"],
                    time=datetime.datetime.now()
                )
            else:
                new_message = GlobalChat(
                    sender_username='Anonymous',
                    text=form.data["text"],
                    time=datetime.datetime.now()
                )
            new_message.save()
            for f in request_files:
                # f.name = f.name.replace("global_chat/","")
                # print(f.name)

                file = MessageFile(file=f, message=new_message, name=f.name, size=(f.size / 1000))
                file.save()

    form = GlobalChatForm()
    context = {"form": form}
    all_messages = GlobalChat.objects.all()
    msgs = []
    for i in range(len(all_messages) - 1, 0, -1):
        msgs.append(all_messages[i])
    context["messages"] = msgs
    context.update(get_base_context(request))
    return render(request, "global_chat.html", context)


def shop(request):
    """This function renders shop page"""
    context = {}
    all_balances = UserBalance.objects.all()
    flag_user = False
    if request.user.is_authenticated:
        for balance in all_balances:
            if balance.user_id == request.user.id:
                flag_user = True
                context["balance"] = balance
                break
        if not flag_user:
            new_balance = UserBalance(
                user_id=request.user.id,
                money=0)
            new_balance.save()
            context["balance"] = new_balance
    else:
        no_balance = UserBalance(
            user_id=-1,
            money=-1)
        context["balance"] = no_balance
    context.update(get_base_context(request))
    context["user"] = request.user
    return render(request, "shop.html", context)


def shopkey(request):
    """This function renders shopkey page"""
    if request.method == 'POST':
        form = Buy(request.POST)
        if form.is_valid():
            form_key = form.data.get("key")
            key = ShopKeys.objects.all().filter(key=form_key, status=1)
            if key != []:
                key = key[0]
                key.status = 0
                key.save()
                balance = UserBalance.objects.all().filter(user_id=request.user.id)
                balance.money += key.money
                balance.save()


def get_messages(request):
    """This function takes messages"""
    chats1 = Chat.objects.all().filter(uid1=request.user.id)
    chats2 = Chat.objects.all().filter(uid2=request.user.id)
    chats = chats1.union(chats2)
    data = {}
    new_chats = []
    messages_new = []
    for chat in chats:
        if request.user.id == chat.uid1:
            new_chats.append({'chat_id': chat.id, 'name': User.objects.get(id=chat.uid2).username})
        else:
            new_chats.append({'chat_id': chat.id, 'name': User.objects.get(id=chat.uid1).username})

        for message in Message.objects.all().filter(chat_id=chat.id):
            user_from = User.objects.get(id=message.sender_id).username
            if len(message.files.all()) > 0:
                new_msg = {'username': user_from, 'chat_id': message.chat_id, 'text': message.text, 'sender_id': message.sender_id, 'time': message.time.strftime('%y-%m-%d %H:%M'), 'file_p': message.files.all()[0].name, 'is_image' : message.files.all()[0].is_image()}
            else:
                new_msg = {'username': user_from, 'chat_id': message.chat_id, 'text': message.text, 'sender_id': message.sender_id, 'time': message.time.strftime('%y-%m-%d %H:%M'), 'file_p': '0', 'is_image' : 0}
            messages_new.append(new_msg)
    data['new_messages'] = messages_new
    return JsonResponse({'new_messages': messages_new, 'chats': new_chats})


def get_global_msgs(request):
    msgs = GlobalChat.objects.all()
    new = []
    for i in msgs:
        if len(i.files.all()) > 0:
            new.append(
                {'sender': i.sender_username, 'file_p': i.files.all()[0].name, 'time': i.time.strftime('%y-%m-%d %H:%M'),
                 'text': i.text, 'is_image' : i.files.all()[0].is_image()})
        else:
            new.append(
                {'sender': i.sender_username, 'file_p': '0', 'time': i.time.strftime('%y-%m-%d %H:%M'), 'text': i.text, 'is_image' : 0})
    total = []
    for i in range(len(new)-1, -1, -1):
        total.append(new[i])
    return JsonResponse(total, safe=False)


def coverage(request):
    """This function makes coverage"""
    return render(request, '')


def changeuserpic(request):
    raise NotImplementedError
