from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class MyAccountManager(BaseUserManager):
    def create_user(self,name, email, username,role, password=None):
        if not name:
            raise ValueError("user must have a name")
        if not email:
            raise ValueError("user must have an email address")
        if not username:
            raise ValueError("user must have an username")
        if not role:
            raise ValueError("User must select a role")
        if role != "admin" and role != "teacher" and role != "student":
            raise ValueError("Please select a role: teacher/student")

        user = self.model(
                name = name,
                email=self.normalize_email(email),
                username = username,
                role = role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, name, email, role, username, password):
        user = self.create_user(
                name = name,
                email=self.normalize_email(email),
                password = password,
                username = username,
                role = role,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    role_choice = (
        ('teacher','Teacher'),
        ('student','Student'),
        ('admin','Admin')
    )
    name                    = models.CharField(verbose_name="name",max_length=30, null=True)
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    role                    = models.CharField(verbose_name="role",max_length=7,choices=role_choice)
    date_joined             = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','role','name']

    objects = MyAccountManager()
    
    def __str__(self):
        return f"{self.name}"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username