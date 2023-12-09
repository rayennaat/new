from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission, Group
from django.utils import timezone




class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey('Course', related_name='assignments', on_delete=models.CASCADE)
    dueDate = models.DateField()

class Submission(models.Model):
    student = models.CharField(max_length=255)
    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    submissionContent = models.TextField()
    submissionDate = models.DateField()

class Grade(models.Model):
    student = models.CharField(max_length=255)
    assignment = models.ForeignKey(Assignment, related_name='grades', on_delete=models.CASCADE)
    grade = models.CharField(max_length=255)
    feedback = models.TextField()

class Course(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    tutor = models.CharField(max_length=255)
    enrollmentCapacity = models.IntegerField()

class Enrollment(models.Model):
    student = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrollmentDate = models.DateField()

class Material(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    course = models.ForeignKey(Course, related_name='materials', on_delete=models.CASCADE)
    uploadDate = models.DateField()
    documentType = models.CharField(max_length=255)

class InteractionHistory(models.Model):
    student = models.CharField(max_length=255)
    material = models.ForeignKey(Material, related_name='interaction_history', on_delete=models.CASCADE)
    interactionType = models.CharField(max_length=255)
    interactionDate = models.DateField()


class CustomUserManager(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_user_managers')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_managers_permissions'
    )

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=255)
    joiningDate = models.DateTimeField(auto_now_add=True)

    enrollments = models.ManyToManyField('Enrollment', related_name='user_enrollments')  
    grades = models.ManyToManyField('Grade', related_name='user_grades') 
    interaction_histories = models.ManyToManyField('InteractionHistory', related_name='user_interaction_histories')
    submissions = models.ManyToManyField('Submission', related_name='user_submissions')  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email




class ReadingState(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    read_state = models.FloatField()  # e.g., percentage completed
    last_read_date = models.DateField()

    class Meta:
        db_table = "ReadingState"    