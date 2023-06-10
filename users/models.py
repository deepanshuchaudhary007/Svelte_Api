from django.db import models
from datetime import datetime
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from users.RandomGenerator import RandomGenerator
from django.core.files.storage import FileSystemStorage
from django.conf import settings
# Create your models here.
upload_storage = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url='/images/')

class Country(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    country_name = models.CharField(max_length=100, blank=False)
    country_code = models.CharField(max_length=4, blank=False)   

    def __str__(self) -> str:
        return self.country_name
    class Meta:
        verbose_name_plural = "Country"

class State(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=100, blank=False)
    state_code = models.CharField(max_length=4, blank=False)      

    def __str__(self) -> str:
        return self.state_name
    class Meta:
        verbose_name_plural = "State"


class City(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100, blank=False)
    
    def __str__(self) -> str:
        return self.city_name
    class Meta:
        verbose_name_plural = "City"

class UserManager(BaseUserManager):
    def create_user(self, user_code,  name, email, address, country, state, city, pin_code, mobile, password=None, password2=None):
        """
        Creates and saves a User with the given email, category, first_name,last_name, email, address, country, state, phone, fax and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            name=name,  
            user_code=user_code,       
            address=address,
            country=country,
            state= state,
            city=city,
            pin_code = pin_code,
            mobile=mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, user_code,  name, email, address, country, state, city, pin_code, mobile,  password=None):
        """
        Creates and saves a superuser with the given email, category, first_name,last_name, email, address, country, state, phone, fax and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name,  
            user_code=user_code,         
            address=address,
            country=country,
            state= state,
            city=city,
            pin_code = pin_code,
            mobile=mobile,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    user_code = models.CharField(max_length=20, default=RandomGenerator.user_code(), unique=True, editable=False)    
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(verbose_name="Email", unique=True, max_length=255, blank=False)
    address = models.CharField(max_length=500, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True) 
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True) 
    city= models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True) 
    pin_code = models.IntegerField(blank=True, null=True)    
    mobile =models.BigIntegerField(blank=True, null=True)    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "address", "country", "state", "city", "pin_code", "mobile",]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_deatils")
    profile_pic=models.ImageField(upload_to='user-images', storage=upload_storage, default='', null=True, blank=True)   