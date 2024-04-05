from django.contrib.auth.base_user import BaseUserManager

from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, email, cnic, city, name, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, CNIC, city, name, and password.
        """
        if not email:
            raise ValueError(_('The Email field must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, cnic=cnic, city=city, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, cnic, city, name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, CNIC, city, name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, cnic, city, name, password, **extra_fields)
