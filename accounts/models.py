from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Max

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school_admin = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='sub_accounts')
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=30, blank=True, default='')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    custom_id = models.CharField(max_length=10, unique=True, primary_key=True)  # Set custom_id as primary key

    def save(self, *args, **kwargs):
        if not self.custom_id:
            # Generate custom_id based on role
            if self.role == self.ADMIN:
                max_id = CustomUser.objects.filter(role=self.ADMIN).aggregate(Max('custom_id'))['custom_id__max']
                next_id = (int(max_id[2:]) + 1) if max_id else 100
                self.custom_id = f'A_{next_id}'
            elif self.role == self.TEACHER:
                max_id = CustomUser.objects.filter(role=self.TEACHER).aggregate(Max('custom_id'))['custom_id__max']
                next_id = (int(max_id[2:]) + 1) if max_id else 100
                self.custom_id = f'T_{next_id}'
            elif self.role == self.STUDENT:
                max_id = CustomUser.objects.filter(role=self.STUDENT).aggregate(Max('custom_id'))['custom_id__max']
                next_id = (int(max_id[2:]) + 1) if max_id else 100
                self.custom_id = f'S_{next_id}'
        super().save(*args, **kwargs)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.custom_id} {self.user.username}'s Profile"