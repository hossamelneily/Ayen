from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import get_language, gettext_lazy as _


class Account(models.Model):
    occupation = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Occupation'))
    user = models.OneToOneField(User, blank=False, null=False, verbose_name=_('User'), on_delete=models.PROTECT)
    passport_copy = models.FileField(blank=True, null=True, verbose_name=_('Passport Copy'),
                                     validators=[
                                         FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])
                                     ])

    def __str__(self):
        return self.user.email


