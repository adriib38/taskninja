from django.contrib import admin
from django.urls import path, include
from myapp import views


from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views

'''
API
'''
from rest_framework import routers
from myapp.api import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, 'projects')
router.register('tasks', TaskViewSet, 'tasks')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('projects/', views.projects, name='projects'),
    path('tasks/', views.tasks, name='tasks'),
    path('project/<int:id>', views.project, name='project'),
    path('create_task/', views.create_task, name='create_task'),
    path('task/<int:id>', views.task, name='task'),
    path('task/<int:id>/done', views.done_task, name='done_task'),
    path('task/<int:id>/delete', views.delete_task, name='delete_task'),
    path('task/<int:id>/undone', views.undone_task, name='undone_task'),
    path('task/<int:id>/edit', views.edit_task, name='edit_task'),
    path('category/<str:name>', views.category, name='category'),
    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:id>/delete', views.delete_project, name='delete_project'),

    path('teams/', views.teams, name='teams'),
    path('team/<int:id>', views.team, name='team'),
    path('create_team/', views.create_team, name='create_team'),

    path('account/', views.account, name='account'),
    path('account/delete', views.delete_account, name='delete_account'),
    path('account/edit', views.edit_account, name='edit_account'),
    path('api/', views.api_docs, name='api_docs'),
    path('password/', PasswordChangeView.as_view(template_name='change_password.html') , name='password_change'),

    #API
    path('api/', include(router.urls)),
]

#crear superusuario
#python manage.py createsuperuser