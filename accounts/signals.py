from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
       if created:
        Profile.objects.create(
            user=instance,
            first_name=instance.first_name,
            middle_name=instance.middle_name,
            last_name=instance.last_name,
            email=instance.email,
            school_name=instance.school_name,
            pic=None,
        )

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # Save the profile if it exists
    if hasattr(instance, 'profile'):
        instance.profile.save()
