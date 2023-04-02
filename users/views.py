from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model

from properties.models import Property

from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, UserProfileForm
from .helpers import auth_user_should_not_access

# Create your views here.

User = get_user_model()


def contextLoginForm(request):
    login_form = UserLoginForm()
    return {'login_form': login_form}

def contextRegisterForm(request):
    register_form = UserRegistrationForm()
    return {'register_form': register_form}


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
                messages.info(request, 'Login successful')
                return redirect('accounts:dashboard')
            else:
                message = 'Invalid Credentials!'
                messages.error(request, message)
                return HttpResponseRedirect(request.META["HTTP_REFERER"])
    context = {
        'login_form': login_form
    }
    return render(request, 'users/auth-page.html', context)


def RegisterView(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            
            user = register_form.save(commit=False)
            user.email = register_form.cleaned_data['email']
            if register_form.cleaned_data['user_type'] == 'Realtor':
                user.is_realtor = True
            else:
                user.is_customer = True
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account creted successfully')
            return redirect('accounts:login')
    
    context = {

    }
    return render(request, 'users/auth-page.html', context)


def logoutView(request):
    logout(request)
    return redirect('properties:home')


def forgotPassword(request):
    context = {

    }
    return render(request, 'users/', context)


@login_required(login_url='accounts:login')
def dashboardView(request):

    context = {

    }
    return render(request, 'users/page-dashboard.html', context)


@login_required(login_url='accounts:login')
def profileView(request):

    if request.method == "POST":
        u_form = UserUpdateForm(instance=request.user, data=request.POST)
        p_form = UserProfileForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            print('valid')
        else:
            print(u_form.errors)
            print(p_form.errors)
            print('invalid')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/page-dashboard-profile.html', context)


@login_required(login_url='accounts:login')
def bookmarksView(request):
    user = get_object_or_404(User, id=request.user.id)
    q = Property.objects.filter(user_bookmark=user)
    context = {
        'bookmarks': q
    }
    return render(request, 'users/page-dashboard-favorites.html', context)


@login_required(login_url='accounts:login')
def myPropertiesView(request):
    user_id = request.user.id
    properties = Property.objects.all().filter(agent_id=user_id)
    context = {
        'properties': properties,
    }
    return render(request, 'users/page-dashboard-property.html', context)


@login_required(login_url='accounts:login')
def invoicesView(request):
    context = {

    }
    return render(request, 'users/page-dashboard-invoices.html', context)


@login_required(login_url='accounts:login')
def addPropertyView(request):
    context = {

    }
    return render(request, 'users/', context)


@login_required(login_url='accounts:login')
def notificationsView(request):
    context = {

    }
    return render(request, 'users/page-dashboard-message.html', context)
