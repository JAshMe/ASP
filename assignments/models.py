from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model


def user_directory_path(instance, filename):
    """
    File will be uploaded to MEDIA_ROOT/<id>/<filename>
    :param instance: The instance of model where file field is defined
    :param filename: The name of file with which its stored
    :return: String : Path of the File to be saved
    """
    return str(instance.user.id) + "/" + str(filename)


class Assignment(models.Model):
    """
    This model will store all the data regarding the Assignments of student
    """

    assign_id = models.CharField(verbose_name="Assignment ID", max_length=20, primary_key=True)
    title = models.CharField(verbose_name="Assignment Title", max_length=100, blank=False)
    desc = models.CharField(verbose_name="Assignment Description", max_length=1000, blank=True, default="No Description")
    submission_time = models.DateTimeField(auto_now=True, verbose_name="Time of Submission")
    assign_code = models.FileField(
        upload_to=user_directory_path,
        help_text="Upload .zip Files Only",
        blank=False,
        validators=[FileExtensionValidator(allowed_extensions=["zip"],message="Only '.zip' files are allowed!!")]
    )





