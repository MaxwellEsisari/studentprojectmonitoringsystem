from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from .models import GroupAdmin, GroupDiscussion, Lecturer, Post, Room, Student, Task, Topic, Message, User
from .forms import  PostForm, RoomForm, LoginForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import Group
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin
import smtplib
import ssl
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from email.mime.image import MIMEImage

def send_email( subject, body, emails=[]):
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = emails
    # subject = 'Website registration'
    # body = 'Activate your account.'
    message = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return 1

def is_student(user):
    return user.groups.filter(name='student').exists()

def is_lecturer(user):
    return user.groups.filter(name='lecturer').exists()

@login_required(login_url="signin")
def home(request):
    send_email('welcome', 'to our website', ['maxwellmubasu@gmail.com'])
    group = str(Group.objects.get(user=request.user))
    user = request.user
    is_admin = False
    if group == "student":
        print("fuwuivhjivhhvuhv")
          
        student = Student.objects.get(user=user)
        g = GroupDiscussion.objects.filter(student=student)
        if g:
            is_admin = True
        else:
            is_admin = False
   
    return render(request, 'main/home.html', {"group":group, "is_admin":is_admin, "user":user})

def add_participant(request, pk):
    student = Student.objects.get(id=pk) 
    students = Student.objects.all() 
    name = request.session.get('name', None) 
    group = GroupDiscussion.objects.filter(name=name).first()
    members = GroupDiscussion.objects.filter(name=name)
    if name:
        del request.session['name']
        request.session.modified = True
        if student.assignedgroup == False:
            GroupDiscussion.objects.create(student=student, name=name) 
            student.assignedgroup = True 
            student.save()
    
    return redirect("participants-home")

@csrf_exempt
def participants_home(request):
   user = request.user
   student = Student.objects.get(user=user)
   students = Student.objects.all()
   group = GroupDiscussion.objects.all().filter(student=student).first()
   members=[]
   if group is None:
        None
   else:
        members = GroupDiscussion.objects.filter(name=group.name) 
   if group is None:
        group_exist = False
   else:
        group_exist = True
        name = str(group.name)
        request.session['name'] = name
        

   if request.method == "POST":
       name = request.POST["name"]
       request.session['name'] = name
       if student.assignedgroup == False:
            group = GroupDiscussion.objects.create(student=student, name=name)
            group_exist = True
            student.assignedgroup = True
            student.save()     
#    if group == None:
#         form = groupForm()
#    group_admin = GroupAdmin.objects.get(id=pk)
#    student = group_admin.student
#    group = GroupDiscussion.objects.get(student=student)
   return render(request, 'main/participantshome.html',{"students":students, "group":group,"group_exist":group_exist,"members":members})

def add_group_admin(request, pk):
    students = Student.objects.all()
    student = Student.objects.get(id=pk)  
    subject = 'Account creation'
    body = 'Hello' +  str(student.user.username) + 'you have been succesfully added as a group admin.'
           
    send_email(subject=subject, body=body, emails=[student.user.email])
    groups = GroupDiscussion.objects.all()
    
    groupadmins = GroupAdmin.objects.all()
    GroupAdmin.objects.create(student=student)  
    # if student not in groupadmins:
    #     GroupAdmin.objects.create(student=student)  
    # else:
    #     None         
    return render(request, 'main/add-group-admin.html', {"students":students, "groupadmins":groupadmins, "groups":groups})

def add_group_admin_home(request):
    students = Student.objects.all()
    groupadmins = GroupAdmin.objects.all()    
    return render(request, 'main/add-group-admin.html', {"students":students, "groupadmins":groupadmins})

def remove_group_admin_home(request, pk):
    students = Student.objects.all()
    groupadmins = GroupAdmin.objects.all()    
    groupadmin = GroupAdmin.objects.get(id=pk)    
    groupadmin.delete()
    return render(request, 'main/add-group-admin.html', {"students":students, "groupadmins":groupadmins})

def signin(request):
    loginForm=LoginForm()
    if request.method == "POST":
        username = request.POST['username']
        password =  request.POST['password']
        print(username)
        print(password)
        user = authenticate(
    		    request, 
    		    username=username, 
    		    password=password
        )
        
        if user:
            login(request, user)
            if is_student(request.user):              
                return redirect('home')
            else:                
                return redirect('home')
    return render(request, 'registration/login.html', {"loginForm":loginForm}) 

def logout_view(request):
    logout(request)
    
    print('hbhjjhhhjjjjjjjjjjjjjjjjj')
    return redirect(signin)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

@login_required(login_url="login")
def chat(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'main/home.html', context)
import json
@csrf_exempt
def progress(request):
    if request.method == "POST":
        progress = request.POST.get("progress")  
        grp = request.POST.get("group")
        dictionary = json.loads(grp.replace("'", "\""))
        g = GroupDiscussion.objects.filter(name=str(dictionary["name"]))
        for n in g:
            n.progress=progress
            n.save()
        # progress = Progress.objects.create(group_discussion=g, progress=progress) 
        return redirect("dashboard")  

    return render(request, 'main/dashboard.html')
def set_session(request,groupname):
    # request.session.flush()
    name = request.session.get('groupname', None) 
    if name:
        del request.session['groupname']
        request.session.modified = True
    request.session['groupname'] = groupname
    return redirect("dashboard")

def dashboard(request):
    posts = Post.objects.all()
    user = request.user
    
    groups = GroupDiscussion.objects.values("name").distinct()
    allgroups = GroupDiscussion.objects.all()
    groupname = request.session.get('groupname')
    g = GroupDiscussion.objects.filter(name=groupname).first()
    # progress = Progress.objects.filter(group_discussion=g).first()
    studentgroup=''
    if is_student(request.user): 
         student = Student.objects.get(user=user)
         print(student.discussion)
         studentgroup = GroupDiscussion.objects.filter(student=student).first()
         print(studentgroup,'eeeeeeeeeeed')
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("base.delete_post")):
              post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'main/dashboard.html',{"posts":posts, "studentgroup":studentgroup, "g":g, "groups":groups, "allgroups":allgroups})

@login_required(login_url="/login")

def create_post(request):
    posts = Post.objects.all()
    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")
        
        if post_id:            
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
              post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.lecturer
            post.save()
            return redirect("/create-post")
    else:
        form = PostForm()  
    return render(request, 'main/create_post.html', {"form": form, "posts":posts})

def chat(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    
    return render(request, 'main/chat.html', context)

def notifications(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    
    return render(request, 'main/notifications.html', context)

@csrf_exempt
def student_signup(request):
    userForm=UserForm()
    if request.method == 'POST':
        userForm=UserForm(request.POST)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            student = Student.objects.create(user=user, assignedgroup=False)
            subject = 'Account creation'
            body = 'Hello'  +  str(student.user.username) + 'you have succesfully created your students account in Student Project Management System(SPMS).Hoping we have a greater experience together'
           
            send_email(subject=subject, body=body, emails=[student.user.email])
            login(request, user)
            student =  Group.objects.get_or_create(name='student')
            student[0].user_set.add(user)
            login(request, user)

            if is_student(request.user):
                return redirect('/home')            
            else:
                return redirect('/dashboard')            
            return redirect('/home')
           
    return render(request, 'registration/sign_up.html', {"userForm":userForm}) 

def lecturer_signup(request):
    userForm=UserForm()
    if request.method == 'POST':
        userForm=UserForm(request.POST)
        if userForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            lecturer = Lecturer.objects.create(user=user)
            subject = 'Account creation'
            body = 'Hello' +  str(lecturer.user.username) + 'you have succesfully created your staff account.'
           
            send_email(subject=subject, body=body, emails=[lecturer.user.email])
            login(request, user)
            lecturer =  Group.objects.get_or_create(name='lecturer')
            lecturer[0].user_set.add(user)
            

            login(request, user)
            if is_lecturer(request.user):
                return redirect('/home')            
            else:
                return redirect('/dashboard')            
            return redirect('/home')
    return render(request, 'registration/sign_up_lecturer.html',{"userForm":userForm})

# def chat(request):
#     q = request.GET.get('q') if request.GET.get('q') != None else ''

#     rooms = Room.objects.filter(
#         Q(topic__name__icontains=q) |
#         Q(name__icontains=q) |
#         Q(description__icontains=q)
#     )

#     topics = Topic.objects.all()[0:5]
#     room_count = rooms.count()
#     room_messages = Message.objects.filter(
#         Q(room__topic__name__icontains=q))[0:3]

#     context = {'rooms': rooms, 'topics': topics,
#                'room_count': room_count, 'room_messages': room_messages}    
#     return render(request, 'main/chat.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    
    return render(request, 'main/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    print(rooms,'rgjngkrgkrgg')
    return render(request, 'main/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),        )
        return redirect('chat')

    context = {'form': form, 'topics': topics}
    return render(request, 'main/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'main/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'main/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):   
    return render(request, 'main/update-user.html')

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'main/topics.html', {'topics': topics})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'main/activity.html', {'room_messages': room_messages})

from django.db.models import F

def report(request):
    groups = GroupDiscussion.objects.values("name", "progress").distinct()
    names = []
    prgs = []
    for group in groups:
        name = group["name"]
        names.append(name)

        progress = int(group["progress"])
        prgs.append(progress)

    context = {'prgs': prgs,"names":names}
    
    return render(request, 'main/report.html',context)

def materials(request):
       
    return render(request, 'main/materials.html')







class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

     #for count you have specifiy in get_context_data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = self.model.objects.filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area','')
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context   
        


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'
    
    
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description','complete']
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)
        
        
class TaskUpdate(LoginRequiredMixin,UpdateView): 
    model = Task
    fields = ['title', 'description','complete']
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin,DeleteView):
    model = Task  
    context_object_name = 'task' 
    success_url = reverse_lazy('tasks')



  



   
