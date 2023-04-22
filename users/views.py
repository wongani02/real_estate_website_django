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
                return redirect('accounts:login')
    context = {
        'login_form': login_form
    }
    return render(request, 'users/auth-page.html', context)


def RegisterView(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            user = register_form.save(commit=False)
            user.email = email
            if register_form.cleaned_data['user_type'] == 'Realtor':
                user.is_realtor = True
            else:
                user.is_customer = True
            user.set_password(register_form.cleaned_data['password'])
            user.save()
            auth = authenticate(email=email, password=register_form.cleaned_data['password'])
            if auth is not None:
                login(request, auth)
                return redirect('accounts:dashboard')
            messages.success(request, 'Account created successfully')
            return redirect('accounts:login')
        
    else :
        register_form = UserRegistrationForm()
    
    context = {
        'register_form':register_form,
    }
    return render(request, 'users/auth-page.html', context)


def logoutView(request):
    logout(request)
    return redirect('properties:home')


def forgotPassword(request):
    context = {

    }
    return render(request, 'users/', context)


#dasboard views
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
            print('error updating form')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = UserProfileForm(instance=request.user.profile)

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


#onbording views
def typeOfPropertyView(request):
    context = {

    }
    return render(request, 'users/onbording-1.html', context)


def postPropertyAsView(request, p_type):
    request.session['property_type'] = p_type

    if p_type == 'lodges_and_cottages':
        context = {
            ''
        }
    elif p_type =='property' :
        context
    else: 
        context = {}
    
    return render(request, 'users/onbording-2.html', context)