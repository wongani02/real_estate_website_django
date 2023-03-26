from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse

from .forms import UserLoginForm
from .helpers import auth_user_should_not_access

# Create your views here.


def contextLoginForm(request):
    login_form = UserLoginForm()
    return {'login_form': login_form}


@auth_user_should_not_access
def loginView(request):
    login_form = UserLoginForm()
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            print('passing')
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect('properties:home')
            else:
                message = 'Invalid Credentials!'
                print(message)
                return redirect('properties:home')
    context = {
        'login_form': login_form
    }
    return render(request, 'users/auth-page.html', context)



def RegisterView(request):
    context = {

    }
    return render(request, 'users/', context)


def logoutView(request):
    logout(request)
    return redirect('properties:home')


def forgotPassword(request):
    context = {

    }
    return render(request, 'users/', context)


def dashboardView(request):
    context = {

    }
    return render(request, 'users/', context)


def profileView(request):
    context = {

    }
    return render(request, 'users/', context)


def bookmarksView(request):
    context = {

    }
    return render(request, 'users/', context)


def myPropertiesView(request):
    context = {

    }
    return render(request, 'users/', context)


def invoices(request):
    context = {

    }
    return render(request, 'users/', context)


def addPropertyView(request):
    context = {

    }
    return render(request, 'users/', context)
