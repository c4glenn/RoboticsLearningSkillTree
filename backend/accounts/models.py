from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class User(AbstractUser):
    """Default user for now, gives us the ability to extend later."""
    pass



