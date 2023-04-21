from django.shortcuts import render
from django.views.generic import ListView
from properties.models import Property
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.forms.formsets import formset_factory

from .create_lodge import Lodge
from .models import Amenity, Picture
from .forms import RoomCreationForm, RoomFormset, LodgeCreationForm

# Create your views here.


def createLodgeView(request):
    amenities = Amenity.objects.all()
    room_form = RoomFormset()
    lodge_form = LodgeCreationForm()
    
    context = {
        'amenities':amenities,
        'room_form': room_form,
        'lodge_form': lodge_form,
    }
    return render(request, 'lodges/create-lodges.html', context)


@require_POST
def handleLodge(request):
    if request.method == 'POST':
        form = LodgeCreationForm(request.POST)
        if form.is_valid():
            request.session['lodge-details'] = {
                'property_name': form.cleaned_data['property_name'],
                'address': form.cleaned_data['address'],
                'city': form.cleaned_data['city'],
                'long': form.cleaned_data['long'],
                'lat': form.cleaned_data['lat'],
                'description': form.cleaned_data['description'],
                'location': form.cleaned_data['location'],
                'contact_email':form.cleaned_data['contact_email'],
                'contact_number': form.cleaned_data['contact_number'],
            }
        print(request.session['lodge-details'])
    return HttpResponse({'status': 200})


@require_POST
def handleRoomForm(request):
    rooms = []
    if request.method == 'POST':
        room_form = RoomFormset(request.POST)
        if room_form.is_valid():
            for form in room_form:

                room_detials = {
                    'ROOMTYPE': form.cleaned_data['ROOMTYPE'],
                    'room_type': form.cleaned_data['adults'],
                    'children': form.cleaned_data['children'],
                    'beds': form.cleaned_data['beds'],
                }

                rooms.append(room_detials)
        request.session['lodge_rooms'] = rooms
        print(request.session['lodge_rooms'])
    return HttpResponse({'status': 200})


def fileUploadView(request):
    session = request.session
    
    if request.method == 'POST':
        image = request.FILES.get('file')
        if 'lodge_images' not in session:
            session['lodge_images'] = []
            session['lodge_images'].append(image)
            session.modified = True
        else:
            session['lodge_images'].append(image)
            session.modified=True
        print(session['lodge_images'])
    return HttpResponse('upload')


@require_POST
def handleAmenities(request):
    session = request.session
    amenity = request.POST.get("amenityID")
    
    if 'amenities' not in session:
        session['amenities'] = []
        if amenity in session['amenities']:
            session['amenities'].remove(amenity)
        else:
            session['amenities'].append(amenity)
        session.modified = True
    else: 
        if amenity in session['amenities']:
            session['amenities'].remove(amenity)
        else:
            session['amenities'].append(amenity)
        session.modified = True
    return HttpResponse({'status': 'ok'})