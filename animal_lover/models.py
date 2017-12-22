from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):

    def create_user(self, username, **fields):

        try:
            user = User.objects.get(username=username)

        except Exception as ex:
            if not fields['email']:
                raise ValueError('Users must have an email address')

            user = self.model(
                name=fields.get('full_name'),
                image=fields.get('picture'),
                gender=fields.get('gender'),
                username=username,
                email=self.normalize_email(fields.get('email')),
                is_active=True
            )
            if fields.has_key('password'):
                user.set_password(fields['password'])
            else:
                user.set_unusable_password()
            user.save(using=self._db)

        return user

    def create_superuser(self, username, **fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            name=fields.get('name'),
            username=username,
            email=self.normalize_email(fields['email']),
        )
        if fields.has_key('password'):
            user.set_password(fields['password'])
        else:
            user.set_unusable_password()
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(max_length=255, null=True, blank=True)

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )

    image = models.ImageField(upload_to=u'profile_pic/%Y/%m/%d', null=True, blank=True, max_length=5000)
    gender = models.CharField(max_length=10, null=True)
    birth_date = models.DateField(null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_username(self):
        return self.username

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def get_less_identity(self):
        return self.name

    def __str__(self):  # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


class Animal(models.Model):
    """
    1 for dog
    2 for cat
    """
    name = models.CharField(max_length=255, null=True)
    type = models.IntegerField(default=1)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='animal_owner')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

