from django.contrib import admin
from . models import Message, Room, Task, Topic, Result, GroupDiscussion,GroupAdmin, Student, Lecturer

# Register your models here.
admin.site.register(Task)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Result)
admin.site.register(GroupDiscussion)
admin.site.register(GroupAdmin)
admin.site.register(Student)
admin.site.register(Lecturer)
