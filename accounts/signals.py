"""
This module will contain all the signals which will be received by this app
"""


from .models import *
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    """
    This is the receiver method called when an object of User Model is saved
    :param sender: The Sender Class
    :param instance: The instance which is saved
    :param created: Bool: If new object created or not
    :param kwargs: Other Arguments
    :return: void
    """
    if created:
        if instance.is_stud:
            StudentProfile.objects.create(stud=instance, bra="CSE")
        else:
            TeacherProfile.objects.create(emp=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    """
    This is the receiver method called when an object of User Model is saved
    :param sender: The Sender Class
    :param instance: The instance which is saved
    :param kwargs: Other Arguments
    :return: void
    """
    if instance.is_stud:
        instance.studentprofile.save()
    else:
        instance.teacherprofile.save()

