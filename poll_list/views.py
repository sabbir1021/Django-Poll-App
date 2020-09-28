from django.shortcuts import render
from .models import Poll
from django.views import View, generic
# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class PollView(generic.ListView):
    model = Poll
    paginate_by = 1
    context_object_name = 'polls'
    template_name = "polls/polls_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Frequently Asked Questions'
        return context
    def get_queryset(self):
        qs = Poll.objects.filter(active=True).all()
        return qs