from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from _helpers.db import TimeModel


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, TimeModel):
    MAX_FREE_POSTS = 5
    history = HistoricalRecords()
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    bio = models.CharField(max_length=100, default="new to Happy-animals")
    avatar = models.ImageField(default='default_avatar.png')
    phone_number = models.CharField(max_length=11, verbose_name='شماره تماس ')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = MyAccountManager()

    def __str__(self):
        return self.email

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'اکانت'
        verbose_name_plural = 'اکانت‌ها'


class Rating(TimeModel):
    scorer = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='send_scores',
                               verbose_name='امتیاز دهنده')
    scored = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_scores',
                               verbose_name='امتیاز گیرنده')
    rate = models.IntegerField(default=3, verbose_name='امتیاز', validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])

    class Meta:
        verbose_name = 'امتیاز'
        verbose_name_plural = 'امتیازها'
