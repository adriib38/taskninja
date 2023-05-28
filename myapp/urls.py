from django.urls import path, include

from taskninja.myapp import admin
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views

#404 file not found
from django.conf.urls import handler404

from django.conf import settings
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
    path('task/<int:id>/done', views.done_task, name='done_task'),
    path('task/<int:id>/delete', views.delete_task, name='delete_task'),
    path('task/<int:id>/undone', views.undone_task, name='undone_task'),
    path('task/<int:id>/edit', views.edit_task, name='edit_task'),

    path('category/<str:name>', views.category, name='category'),

    path('create_project/', views.create_project, name='create_project'),
    path('project/<int:id>/delete', views.delete_project, name='delete_project'),

    path('account/', views.account, name='account'),
    path('account/delete', views.delete_account, name='delete_account'),
    path('account/edit', views.edit_account, name='edit_account'),

    path('password/', PasswordChangeView.as_view(template_name='change_password.html') , name='password_change'),
    path('logout/', auth_views.PasswordChangeDoneView.as_view(template_name='index.html'), name='password_change_done'),

]

