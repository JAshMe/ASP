from django.db import models
from ASP import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    This is Custom User Model with added Boolean Field to decide whether the user is student or a teacher
    """
    username = models.CharField(
        verbose_name="UID",
        primary_key=True,
        max_length=50,
        help_text="Your Registration Number or EID",
        validators=[RegexValidator("^[A-Z0-9]+$", message="Only Numbers and Capital English Letters allowed")]

    )
    is_stud = models.BooleanField(verbose_name="Is Student", default=False)

    def __str__(self):
        if self.is_stud:
            return "Student - " + self.username
        elif self.is_superuser:
            return "Admin - " + self.username
        else:
            return "Teacher - " + self.username


class StudentProfile(models.Model):
    """
    This model will store the other information for user who is a student
    """

    PROGRAM_CHOICES = (
        ('bt', 'Bachelor of Technology (B. Tech) '),
        ('mt', 'Master of Technology (M. Tech)'),
        ('mc', 'Master of Computer Applications (MCA)'),
        ('ms', 'Master of Science (MSc)'),
        ('phd', 'PhD'),
    )

    SEM_CHOICES = ((x, x) for x in range(1, 21))  # tuple populated dynamically

    # one to one relation with user model
    stud = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    prog = models.CharField(
        verbose_name="Program",
        choices=PROGRAM_CHOICES,
        max_length=3,
        blank=False,
        default='bt',
    )

    bra = models.CharField(
        verbose_name="Branch",
        max_length=150,
        blank=False,  # required
    )

    sem = models.IntegerField(
        verbose_name="Semester",
        choices=SEM_CHOICES,
        blank=False,
        default=1,
    )

    def __str__(self):
        return self.stud.username + " - " + self.stud.get_full_name()


class TeacherProfile(models.Model):
    """
    This model will store info about the user who are teachers
    """

    DEPT_CHOICES = (
        ('csed', 'CSE Department'),
        ('med', 'Mechanical Department'),
        ('eed', 'Electrical Department'),
        ('phyd', 'Physics Department'),
        ('eced', 'ECE Department')
    )

    # one to one relation with user model
    emp = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    bio = models.TextField(max_length=500, blank=True)
    dept = models.CharField(max_length=10, default='csed', choices=DEPT_CHOICES)

    def __str__(self):
        return self.emp.username + " - " + self.emp.get_full_name()



