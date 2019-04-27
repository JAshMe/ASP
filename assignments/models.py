from django.db import models
from django.core.validators import FileExtensionValidator
from ASP import settings
import os
from django.contrib.auth import get_user_model


def user_code_directory_path(instance, filename):
    """
    Code File will be uploaded to MEDIA_ROOT/<id>/code/<filename>
    :param instance: The instance of model where file field is defined
    :param filename: The name of file with which its stored
    :return: String : Path of the File to be saved
    """
    return str(instance.user.username) + "/code/" + str(filename)


def user_directory_path(instance, filename):
    """
    Code File will be uploaded to MEDIA_ROOT/<id>/code/<filename>
    :param instance: The instance of model where file field is defined
    :param filename: The name of file with which its stored
    :return: String : Path of the File to be saved
    """
    return str(instance.user.username) + "/" + str(filename)


def user_req_directory_path(instance, filename):
    """
    Requirements File will be uploaded to MEDIA_ROOT/<id>/requirements/<filename>
    """
    return str(instance.user.username) + "/requirements/" + str(filename)


class Environment(models.Model):
    """
    This model will contain all the environments and their bash files
    """

    ENVIRONMENT_CHOICES = (
        ('ap_sp', 'Apache Spark'),
        ('ap_hp', 'Apache Hadoop'),
        ('hb', 'HBase'),
    )

    env_id = models.CharField(
        verbose_name="Environment",
        choices=ENVIRONMENT_CHOICES,
        default='ap-sp',
        blank=False,
        max_length=10,
        primary_key=True
    )

    bash_file_url = models.FilePathField(
        path=settings.ENV_ROOT,
        recursive=False,
        allow_files=True,
        allow_folders=False,
    )

    def __str__(self):
        return self.get_env_id_display()


class Assignment(models.Model):
    """
    This model will store all the data regarding the Assignments of student
    """

    assign_id = models.CharField(verbose_name="Assignment ID", max_length=20, primary_key=True)
    title = models.CharField(verbose_name="Assignment Title", max_length=100, blank=False)
    desc = models.CharField(verbose_name="Assignment Description", max_length=1000, blank=True, default="No Description")

    submission_time = models.DateTimeField(auto_now=True, verbose_name="Time of Submission")

    assign_code = models.FileField(
        verbose_name="Code of Assignment",
        upload_to=user_code_directory_path,
        help_text="Upload .zip Files Only",
        validators=[FileExtensionValidator(allowed_extensions=["zip"], message="Only '.zip' files are allowed!!")],
    )

    assign_requirements = models.FileField(
        verbose_name="Requirements of Assignment",
        upload_to=user_req_directory_path,
        help_text="File which contains all the Alpine-Package requirements",
        validators=[FileExtensionValidator(allowed_extensions=["txt"],
                                           message="Only '.txt' files are allowed!!")]
    )
    run_command = models.CharField(
        verbose_name="Run Command",
        max_length=500,
        help_text="Enter the command for running your project",
        blank=False,
    )
    is_eval = models.BooleanField(
        verbose_name="Is Evaluated",
        default=False
    )

    user = models.ForeignKey(verbose_name="Student", to=get_user_model(), on_delete=models.CASCADE, blank=False)

    env = models.ForeignKey(verbose_name="Environment Selected",
                            to=Environment,
                            on_delete=models.CASCADE,
                            )

    def __str__(self):
        return self.title + " - " + self.user.username


class VM(models.Model):
    """
    This model will store the info of VM spawned for each user
    """

    teacher = models.OneToOneField(verbose_name="Teacher",
                                   to=get_user_model(),
                                   on_delete=models.CASCADE,
                                   primary_key=True
                                   )

    port_used = models.IntegerField(
        verbose_name="Port Used",
    )

    def __str__(self):
        return self.teacher.get_full_name() + ": " + str(self.port_used)









