from django.shortcuts import render
from django.views import generic

class PropertiesHome(generic.ListView):
    def get(self, request):
        return render(request, 'properties/index.html')


class Contact(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-contact.html')


class AboutUs(generic.DetailView):
    def get(self, request):
        return render(request, 'properties/page-about.html')