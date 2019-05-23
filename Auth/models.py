from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class PlatformUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class PlatformUser(AbstractBaseUser):

    class Meta:
        db_table = 'users'

    username = models.CharField(
        unique=True,
        max_length=50,

    )
    email = models.EmailField(
        unique=True,
        max_length=255,
    )

    avatar = models.ImageField(upload_to='media/', null=True, blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_validated = models.BooleanField(default=False)

    objects = PlatformUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_superuser(self):
        return self.is_admin
