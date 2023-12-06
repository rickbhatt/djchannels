from django.db import models
import uuid
from account.models import CustomUser

# Create your models here.
class Notification(models.Model):
    
    id = models.UUIDField(primary_key=True, editable=False, default= uuid.uuid4)
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    
    message = models.TextField(null=True)
    
    is_seen = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True, null=True)