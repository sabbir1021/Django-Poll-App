from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField()

    def __str__(self):
        return self.subject

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE,related_name='choise')
    choice_option = models.CharField(max_length=50)

    def __str__(self):
        return str(self.poll)+'--' + str(self.choice_option)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.choice) +'--' + str(self.user)
