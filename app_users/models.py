from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserModelManager


class UserModel(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=True, null=True)
    profile_image = models.ImageField(upload_to='user-images/',
                                      default='user-images/user-default.png',
                                      null=True, blank=True)



    objects = UserModelManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def fullname(self):
        return f'{self.first_name} {self.last_name}'

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"
    def set_fullname(self, value):
        names = value.split()
        self.first_name, self.last_name = names[0], " ".join(names[1:])

    fullname = property(get_fullname, set_fullname)

    def __str__(self):
        return f'{self.fullname} - {self.email}'
