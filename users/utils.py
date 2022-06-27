from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def __create_user__(self, email, password,first_name,last_name,is_seller, is_superuser, **extra_fields):
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_seller=is_seller,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_user(self, email, password, first_name, last_name,is_seller, **extra_fields):
        return self.__create_user__(
            email, 
            password,
            first_name, 
            last_name, 
            is_seller, 
            False, 
            **extra_fields
        )

    def create_superuser(self, email, password,first_name, last_name, **extra_fields):
        return self.__create_user__(
            email, 
            password,
            first_name, 
            last_name, 
            False, 
            True, 
            **extra_fields
        )