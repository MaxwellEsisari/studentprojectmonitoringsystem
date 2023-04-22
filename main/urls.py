from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate, DeleteView
from  . import views

urlpatterns = [
    
    path('home/',views.home, name="home"),
    path('', views.signin, name='signin'),
    path('signout/', views.logout_view, name='signout'),

    path('student_signup/', views.student_signup, name="student_signup"),
    path('lecturer_signup/', views.lecturer_signup, name="lecturer_signup"),
    path('add-group-admin/<str:pk>', views.add_group_admin, name="add-group-admin"),
    path('add-group-admin-home/', views.add_group_admin_home, name="add-group_admin-home"),
    path('participants-home/', views.participants_home, name="participants-home"),
    path('add-participant/<str:pk>/', views.add_participant, name="add-participant"),
    path('report', views.report, name="report"),
     path('materials', views.materials, name="materials"),



    
    path('chat', views.chat, name='chat'),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('notifications/', views.notifications, name="notifications"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
    path('create-post', views.create_post, name='create-post'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('progress', views.progress, name='progress'),
    path('set-session<str:groupname>/', views.set_session, name='set-session'),

     path('task-list/', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
    


    

]