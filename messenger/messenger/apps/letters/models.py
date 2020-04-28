from django.db import models
from django.contrib.auth.models import User 

class Message(models.Model) :
    text = models.TextField("Text")
    sender = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Sender', blank = True, null = True)
    recipient = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'Recipient', blank = True, null = True)
    sent_date = models.DateTimeField(auto_now = True)
    read_mark = models.CharField("IsRead", max_length=50, default="unread")
    
    def __str__(self):
        return self.text



    

