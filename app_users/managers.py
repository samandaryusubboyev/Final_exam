
from django.contrib.auth.models import UserManager, User
from django.core.exceptions import ValidationError


class UserModelManager(UserManager):
    def create_user(self,
                    email: str,
                    first_name: str = '',
                    last_name: str = '',
                    password: str = None) -> User:
        if not email:
            raise ValidationError('Users must have email! ')


        email = self.normalize_email(email=email)

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
        )
        user.set_password(raw_password=password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(email, first_name, last_name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
