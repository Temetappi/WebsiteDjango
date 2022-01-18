from django.shortcuts import render
from django.views.generic import ListView, TemplateView, FormView
from . import models
from . import forms


class IndexView(TemplateView):
    template_name = 'index.html'


class MeView(TemplateView):
    template_name = 'aboutme.html'


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = forms.ContactForm
    success_url = '/contact'

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class GalleryView(ListView):
    model = models.Photo
    template_name = 'gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = {}
        categories = models.Photo.objects.order_by('category').values_list('category', flat=True).distinct()
        for c in categories:
            photos[c] = list(models.Photo.objects.filter(category=c).order_by('-filename'))
        context['photos'] = photos
        return context
