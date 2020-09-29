from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    def __str__(self):
        return self.subject

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE,related_name='choises')
    choice_option = models.CharField(max_length=50)

    def __str__(self):
        return str(self.poll)+'--' + str(self.choice_option)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE , related_name="votes")

    def __str__(self):
        return str(self.choice) +'--' + str(self.user)
