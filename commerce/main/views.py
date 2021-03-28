from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Главная"
        context['turn_on_block'] = True
        return context


