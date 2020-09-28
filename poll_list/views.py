from django.shortcuts import render , redirect , get_object_or_404
from .models import Poll
from django.views import View, generic
from django.contrib.auth.models import User
from .forms import AddPollForm , AddChoiceForm
from authenticate.mixins import AictiveUserRequiredMixin
# Create your views here.

class HomeView(generic.TemplateView):
    template_name = 'home.html'

class PollView(AictiveUserRequiredMixin,generic.ListView):
    model = Poll
    paginate_by = 10
    context_object_name = 'polls'
    template_name = "polls/polls_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Poll List'
        return context
    def get_queryset(self):
        qs = Poll.objects.all()
        return qs

class MyPollView(generic.ListView):
    model = Poll
    paginate_by = 10
    context_object_name = 'polls'
    template_name = "polls/polls_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Poll List'
        return context
    def get_queryset(self):
        qs = Poll.objects.filter(owner__username=self.request.resolver_match.kwargs['username']).all()
        return qs

class AddPollView(generic.View):
    def get(self, request, *args, **kwargs):
        pollform = AddPollForm()
        choiceform = AddChoiceForm(prefix="choiceform")
        choiceform2 = AddChoiceForm(prefix="choiceform2")
        context = {
            'title': 'Add Poll',
            'pollform': pollform,
            'choiceform':choiceform,
            'choiceform2':choiceform2
        }
        return render(request, 'polls/add_poll.html', context)
    
    def post(self, request, *args, **kwargs):
        user = self.request.user
        pollform = AddPollForm(request.POST or None)
        choiceform = AddChoiceForm(request.POST or None ,prefix="choiceform")
        choiceform2 = AddChoiceForm(request.POST or None ,prefix="choiceform2")
        if pollform.is_valid():
            instance = pollform.save(commit=False)
            instance.owner = user
            instance.save()
            poll = Poll.objects.last()

            if choiceform.is_valid() and choiceform2.is_valid():
                instance = choiceform.save(commit=False)
                instance.poll = poll
                instance.save()
            
                instance = choiceform2.save(commit=False)
                instance.poll = poll
                instance.save()
                return redirect('poll:poll')
    
