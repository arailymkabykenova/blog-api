from typing import Any
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.db.models import (
    EmailField,
    CharField,
    BooleanField,
)

class UserManager(BaseUserManager):
    EMAIL_ERROR_MESSAGE="The email field is required"
    PASSWORD_ERROR_MESSAGE="The password field is required"
    FIRST_NAME_ERROR_MESSAGE="The first name field is required"
    LAST_NAME_ERROR_MESSAGE="The last name field is required"

    def __obtain_user_instance(self,email:str,password:str,first_name:str,last_name:str,**kwargs:Any)->'User':
        if not email:
            raise ValidationError(self.EMAIL_ERROR_MESSAGE, code='email_required')
        if not password:
            raise ValidationError(self.PASSWORD_ERROR_MESSAGE, code='password_required')
        if not first_name:
            raise ValidationError(self.FIRST_NAME_ERROR_MESSAGE, code='first_name_required')
        if not last_name:
            raise ValidationError(self.LAST_NAME_ERROR_MESSAGE, code='last_name_required')
        new_user:'User'=self.model(
            email=self.normalize_email(email).lower(),
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            **kwargs
            )
        return new_user
        


    def create_user(self,email:str,password:str,first_name:str,last_name:str,**kwargs:Any)->'User':
       new_user:'User'=self.__obtain_user_instance(
           email=email,
           password=password,
            first_name=first_name,
            last_name=last_name,
            **kwargs
       )
       new_user.save(using=self._db)
       return new_user

    def create_superuser(self,email:str,password:str,first_name:str,last_name:str,**kwargs:Any)->'User':
        new_user:'User'=self.__obtain_user_instance(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
            **kwargs
        )
        new_user.save(using=self._db)
        return new_user


class User(AbstractBaseUser,PermissionsMixin):
    NAME_MAX_LENGTH=50
    email=EmailField(unique=True)
    first_name=CharField(max_length=NAME_MAX_LENGTH)
    last_name=CharField(max_length=NAME_MAX_LENGTH)
    is_active=BooleanField(default=True)
    is_staff=BooleanField(default=False)

    REQUIRED_FIELDS=['first_name','last_name']
    USERNAME_FIELD='email'
    objects=UserManager()
    
    def __str__(self)->str:
        return self.email


    

