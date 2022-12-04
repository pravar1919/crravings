from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, AbstractUser
)
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# from .signals import user_logged_in
from .signals import object_viewed_signal


def validate_length(value):
    if len(str(value))>10:
        raise ValidationError("This is not a valid Phone Number")
    return value


class MyUserManager(BaseUserManager):
    def create_user(self, email, mob_number, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            mob_number=mob_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mob_number, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            mob_number=mob_number,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mob_number = models.IntegerField(validators=[validate_length])
    gst_number = models.CharField(max_length=255, null=True, blank=True)
    pan_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_vendor = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mob_number']

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    

class VendorManager(models.Manager):

    def get_queryset(self):
        return super(VendorManager, self).get_queryset().filter(is_vendor=True)

class Vendor(User):
    objects = VendorManager()

    def clean(self):
        if not self.gst_number:
            raise ValidationError('GST Number cannot be blank')
        if not self.pan_number:
            raise ValidationError('PAN Number cannot be blank')

    class Meta:
        proxy = True
    
    # def save(self, *args, **kwargs):
    #     super(User).save(*args, **kwargs)

class BuyersManager(models.Manager):

    def get_queryset(self):
        return super(BuyersManager, self).get_queryset().filter(is_buyer=True)

class Buyer(User):
    objects = BuyersManager()

    class Meta:
        proxy = True

class ObjectViewed(models.Model):
    user                = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    content_type        = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id           = models.PositiveIntegerField()
    path                = models.CharField(max_length=220, blank=True, null=True)
    content_object      = GenericForeignKey('content_type', 'object_id')
    model_name          = models.CharField(max_length=220, blank=True, null=True)
    model_product_id    = models.CharField(max_length=220, blank=True, null=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return f"{self.content_object} viewed: {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'


def object_viewed_reciever(sender,instance,request,*args,**kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    try:
        app_name = request.resolver_match.app_name
        app_instance_id = request.resolver_match.kwargs['pk']
    except:
        app_instance_id = ""
    ObjectViewed.objects.create(
                user=request.user, 
                content_type=c_type,
                object_id=instance.id,
                path=request.get_full_path(),
                model_name = app_name,
                model_product_id = app_instance_id
                )

object_viewed_signal.connect(object_viewed_reciever)