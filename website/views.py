from django.views.generic import ListView, TemplateView

from . import models


class IndexView(TemplateView):
    template_name = 'index.html'


class MeView(TemplateView):
    template_name = 'aboutme.html'


class PortfolioView(ListView):
    model = models.Photo
    template_name = 'portfolio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photos = list(models.Photo.objects.filter(category="people").order_by('-created'))
        context['photos'] = photos
        return context
