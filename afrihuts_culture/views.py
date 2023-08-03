from django.shortcuts import render
from django.views import generic

from .models import *

# Create your views here.


class Contact(generic.DetailView):
    def get(self, request):
        return render(request, 'afrihuts-culture/page-contact.html')


class AboutUs(generic.DetailView):
    def get(self, request):
        return render(request, 'afrihuts-culture/page-about.html')
    

class BlogDetailView(generic.DetailView):
    model = BlogPost
    template_name = 'afrihuts-culture/blog-detail.html'

    def get(self, request, **kwargs):
        qs = self.model.objects.prefetch_related('blog_images').get(slug=kwargs.get('slug'))
        get_current_id = self.model.objects.filter(slug=self.kwargs['slug']).first()
        
        context = {
            'blog': qs,
            'next': self.model.objects.filter(id__gt=get_current_id.pk).first(),
            'previous':  self.model.objects.filter(id__lt=get_current_id.pk).first(),
        }
        return render(request, self.template_name, context)


class BlogList(generic.ListView):
    def get(self, request):
        blogs = BlogPost.objects.filter(is_active=True)
        blog_cat = BlogCategory.objects.filter(is_active=True)
        context = {
            'blogs': blogs,
            'blog_cats': blog_cat,
        }
        return render(request, 'pafrihuts-culture/page-blog-list.html', context)


class BlogGrid(generic.ListView):
    def get(self, request):
        return render(request, 'afrihuts-culture/page-blog-grid.html')
    

class TermsAndCondiotions(generic.View):
    def get(self, request):
        context = {
            
        }
        return render(request, 'afrihuts-culture/', context)
    