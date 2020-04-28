from django.shortcuts import render
from django.http import HttpResponse
from .models import Message
from django.contrib.auth.models import User 

def index(request) :
    messages = Message.objects.filter(recipient = request.user)
    unique_users = list()
    res = list()
    for message in messages :
        if message.sender in unique_users :
            continue
        user_messages = list(messages.filter(sender = message.sender)) + list(Message.objects.filter(sender = request.user, recipient = message.sender))
        user_messages.sort(key = lambda message: message.sent_date, reverse  = True)
        cur_mes = user_messages[0]
        if cur_mes.sender == request.user :
            cur_mes.read_mark = 'read'
        cur_mes.sender = message.sender
        res.append(cur_mes)
        unique_users.append(message.sender)
    res.sort(key = lambda message: message.sent_date, reverse=True)
    for i in res :
        i.text = i.text if len(i.text) < 50 else i.text[0:50] + "..."

    return render(request, 'letters/messages.html', {'messages' : res})


def users(request) :
    if request.method == 'GET' :
        username = request.GET.get('user_substr', '')
        if username != '' :
            users = User.objects.filter(username__contains=username)
            return render(request, 'letters/users.html', {'users' : users})
    
    return render(request, 'messenger/main.html')


def dialog(request) :
    if request.method == 'GET' :
        username = request.GET.get('name', '')
        if username != '' :
            db_set = Message.objects.filter(sender = User.objects.get(username = username), recipient = request.user)
            messages = list(db_set)
            if username != request.user.username :
                messages = messages + list(Message.objects.filter(sender = request.user, recipient = User.objects.get(username = username)))
            messages.sort(key = lambda message: message.sent_date)
            if messages[len(messages) - 1].sender != request.user :
                db_set.update(read_mark = 'read')
            return render(request, 'letters/dialog.html', {'messages' : messages, 'username': username})
    return render(request, 'messenger/main.html')


def send_message(request) :
    if request.method == 'GET' :
        usermessage = request.GET.get('message', '')
        if usermessage != '' :
            username = request.GET.get('name', '')
            if username != '' :
                message = Message()
                message.recipient = User.objects.get(username=username)
                message.sender = User.objects.get(username=request.user)
                message.text = usermessage
                message.read_mark = 'unread'
                message.save()
        return dialog(request)
    return render(request, 'messenger/main.html')