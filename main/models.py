from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True,related_name='lecturers')  

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True, related_name='users')
    # groupadmin = models.BooleanField(default=False)
    assignedgroup = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class GroupDiscussion(models.Model):
    # admin = models.ForeignKey(GroupAdmin, on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, related_name='discussion')
    name= models.CharField(max_length=200)
    progress =  models.CharField(default=1,  max_length=200)
    
    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)
    created_at =models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title +"\n" + self.description

class GroupAdmin(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="admins")
    def __str__(self):
        return self.student.user.username

class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)    
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['complete']

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Result(models.Model):
    group_discussion = models.ForeignKey(GroupDiscussion, on_delete=models.CASCADE, null=True, blank=True)
    consultation = models.CharField(max_length=5)
    score = models.CharField(max_length=5, null=True, blank=True)

# class Progress(models.Model):
#     group_discussion = models.ForeignKey(GroupDiscussion, on_delete=models.CASCADE, null=True, blank=True, related_name="progress")
#     progress = models.CharField(max_length=5)
    

#     def __str__(self):
#         return self.group_discussion.name