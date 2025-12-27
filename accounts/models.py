from django.contrib.auth.models import AbstractUser, Group
from django.db import models

class CustomUser(AbstractUser):
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.groups:
            self.groups.add(Group.objects.get(name='User'))
            self.save()
        
