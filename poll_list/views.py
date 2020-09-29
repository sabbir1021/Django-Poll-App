from django.shortcuts import render , redirect , get_object_or_404
from .models import Poll , Choice ,Vote
from django.views import View, generic
from django.contrib.auth.models import User
from .forms import AddPollForm , AddChoiceForm , SearchForm
from authenticate.mixins import AictiveUserRequiredMixin
from django.contrib import messages
from django.db.models import Count
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
        context['form'] = SearchForm()
        return context
    def get_queryset(self):
        qs = Poll.objects.all()
        search = self.request.GET.get('search')
        if search:
            qs = Poll.objects.filter(subject__icontains=search)
        if 'name' in self.request.GET:
            qs = Poll.objects.all().order_by('subject')

        if 'date' in self.request.GET:
            qs = Poll.objects.all().order_by('-pub_date')

        if 'vote' in self.request.GET:
            qs = Poll.objects.all().annotate(Count('vote')).order_by('-vote__count')
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

class AddPollView(AictiveUserRequiredMixin,View):
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
    

class PollEndView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        if poll.active:
            poll.active = False
            poll.save()
        return redirect('poll:poll')

class EditPollView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        form = AddPollForm(instance=poll)
        return render(request, 'polls/poll_edit.html', {'form': form , 'poll':poll})

    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        form = AddPollForm(instance=poll)
        if request.method == 'POST':
            form = AddPollForm(request.POST or None, instance=poll)
            if form.is_valid():
                form.save()
                return redirect('poll:poll')

class DeletePollView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        instance = poll
        instance.delete()
        return redirect('poll:poll')
        
class AddChoiceView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        choiceform = AddChoiceForm()
        context = {
            'choiceform':choiceform,
            'poll':poll
        }
        return render(request, 'polls/add_choice.html', context)
    
    def post(self, request, *args, **kwargs):
        choiceform = AddChoiceForm(request.POST or None )
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        if choiceform.is_valid():
            instance = choiceform.save(commit=False)
            instance.poll = poll
            instance.save()
            return redirect('poll:poll')

class EditChoiceView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        choice = get_object_or_404(Choice , id = self.request.resolver_match.kwargs['cid'])
        choiceform = AddChoiceForm(instance=choice)
        context = {
            'choiceform':choiceform,
            'poll':poll,
            'choice':choice
        }
        return render(request, 'polls/edit_choice.html', context)
    
    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        choice = get_object_or_404(Choice , id = self.request.resolver_match.kwargs['cid'])
        choiceform = AddChoiceForm(request.POST or None,instance=choice )
        if choiceform.is_valid():
            instance = choiceform.save(commit=False)
            instance.poll = poll
            instance.save()
            return redirect('poll:poll')

class DeleteChoiceView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        choice = get_object_or_404(Choice , id = self.request.resolver_match.kwargs['cid'])
        instance = choice
        instance.delete()
        return redirect('poll:poll')

class PollDetailsView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        context = {
            'poll':poll,
        }
        return render(request, 'polls/poll_detail.html', context)
    def post(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        choice_id = request.POST.get('choice')
        if not poll.user_can_vote(request.user):
            messages.error(
                request, "You already voted this poll", extra_tags='alert alert-warning alert-dismissible fade show')
            return redirect("poll:poll")
        if choice_id:
            choice = Choice.objects.get(id=choice_id)
            vote = Vote(user=request.user, poll=poll, choice=choice)
            vote.save()
            return redirect('poll:result',id=poll.id)


class ResultView(View):
    def get(self, request, *args, **kwargs):
        poll = get_object_or_404(Poll, id=self.request.resolver_match.kwargs['id'])
        vot = Vote.objects.filter(poll__id=self.request.resolver_match.kwargs['id'])
        vote_count = Vote.objects.filter(poll__id=self.request.resolver_match.kwargs['id']).count()
        choice = Choice.objects.filter(poll__id=self.request.resolver_match.kwargs['id'])
        
        context = {
            'poll':poll,
            'vot':vot,
            'vote_count':vote_count,
            'choice':choice
        }
        return render(request , "polls/poll_result.html",context)