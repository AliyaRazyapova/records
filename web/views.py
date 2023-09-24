from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from web.forms import RecordForm, AuthForm
from web.models import Record, Tag, User


def main_view(request):
    return redirect("records_list")


def records_view(request):
    records = Record.objects.all()
    search = request.GET.get('search', None)
    try:
        tag_id = int(request.GET.get("tag_id", None))
    except (TypeError, ValueError):
        tag_id = None

    if request.user.is_authenticated:
        record = Record.objects.filter(user=request.user)
    else:
        record = Record.objects.none()

    records = Record.objects.all()

    if tag_id:
        tag = Tag.objects.get(id=tag_id)
        notes = records.filter(tags__in=[tag])

    if search:
        records = records.filter(
            Q(title__icontains=search) |
            Q(text__icontains=search)
        )

    return render(request, "web/main.html", {
        'count': Record.objects.count(),
        'records': records,
        'search': search,
        'tags': Tag.objects.all(),
        'tag_id': tag_id,
    })


@login_required
def record_view(request, id):
    record = get_object_or_404(Record, id=id)
    return render(request, "web/record.html", {
        'record': record
    })


@login_required
def record_edit_view(request):
    form = RecordForm()

    user = request.user
    record = None
    # if id is not None:
    #     record = get_object_or_404(Record, id=id)
    #     title = record.title
    #     text = record.text
    error, title, text = None, None, None
    if request.method == 'POST':
        title = request.POST.get("title")
        text = request.POST.get("text")
        price = request.POST.get("price")
        rating = request.POST.get("rating")
        if not title or not text:
            error = 'Название или текст не заполнены. Их нужно заполнить.'
        else:
            record = Record.objects.create(
                title=title, text=text, price=price, rating=rating, user=user
            )
            return redirect('record', record.id)
    return render(request, "web/record_form.html", {
        'error': error,
        'title': title,
        'text': text
    })


def registration_view(request):
    form = AuthForm()
    is_success = False
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User(username=username)
            user.set_password(form.cleaned_data['password'])
            user.save()
            is_success = True
    return render(request, 'web/registration.html',{
        'form': form,
        'is_success': is_success
    })

def login_view(request):
    form = AuthForm()
    message = None
    if request.method == 'POST':
        form = AuthForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            user = authenticate(request, **form.cleaned_data)
            if user is None:
                message = "Электронная почта или пароль неправильные"
            else:
                login(request, user)
                next_url = 'main'
                if 'next' in request.GET:
                    next_url = request.GET.get("next")
                return redirect(next_url)
    return render(request, "web/login.html", {
        "form": form,
        'message': message
    })


def logout_view(request):
    logout(request)
    return redirect('main')
