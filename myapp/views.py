from django.http import HttpResponse, JsonResponse
from .models import Project, Task, Team, TeamUser, TeamUser
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TaskForm, CreateNewProject, EditTaskForm, CreateNewTeam, CreateNewTeamProject

from django.utils.datastructures import MultiValueDictKeyError

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

#import date 
from datetime import date, datetime, timedelta

from django.contrib.auth.views import PasswordChangeView

# Token api rest
from rest_framework.authtoken.models import Token

from django.utils.translation import gettext as _
from django.utils.translation import get_language, activate, gettext


""" 
Rutas de la aplicación
"""

# Index page
def index(request):
    today = date.today()
    tomorrowDay = date.today() + timedelta(days=1)
    todayStr = today.strftime("%A, %d %B %Y")
    numTasksPendingToday = Task.objects.filter(user_id=request.user.id, date_limit=today, done=False).count()
    numTasksPending = Task.objects.filter(user_id=request.user.id, done=False).count()

    projectsUser_id = Project.objects.filter(user_id=request.user.id)
    projectsWithTasksNumber = []
    for project in projectsUser_id:
        tasks = Task.objects.filter(project_id=project.id, done=False)
        #Añadir proyecto y número de tareas a la lista con formato 'project':project, 'tasks':len(tasks)
        projectsWithTasksNumber.append({'project':project, 'numTasks':len(tasks)})

    categoriesTasksList = []
    for task in Task.objects.filter(user_id=request.user.id, done=False):
        taskCategories = task.categories.split(';')
        for category in taskCategories:
            if category not in categoriesTasksList:
                categoriesTasksList.append(category)

    #Si esta logueado
    if request.user.is_authenticated:
        return render(request, 'index.html', {
            'title': 'MyProjects',
            'today': today,
            'todayStr': todayStr,
            'numTasksPendingToday': numTasksPendingToday,
            'numTasksPending': numTasksPending,
            'projectsWithTasksNumber': projectsWithTasksNumber,
            'categoriesTasksList': categoriesTasksList,
        })

    else:
        return render(request, 'indexNoLogged.html', {
            'title': 'Hola',
        })

# About page
def about(request):
    return render(request, 'about.html', {
        'title': 'About'
    })

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Crear usuario
                user = User.objects.create_user(
                    username=request.POST['username'], 
                    password=request.POST['password1'],
                )
                # Guarda el usuario en la base de datos
                user.save()
                # Iniciar sesión
                login(request, user)

                # Crear token para la api rest
                userToken = Token.objects.create(user=user)

                return redirect('/')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'title': 'Signup',
                    'userCreationForm': UserCreationForm,
                    'error': 'Username already taken'
                })
        else:
            return render(request, 'signup.html', {
                'title': 'Signup',
                'userCreationForm': UserCreationForm,
                'error': 'Passwords must match'
            })
        
    return render(request, 'signup.html', {
        'title': 'Signup',
        'userCreationForm': UserCreationForm
    })

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'title': 'Signin',
            'authenticationForm': AuthenticationForm
        })
    else:
        # Autenticar usuario
        user = authenticate(
            request, username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:
            return render(request, 'signin.html', {
                'title': 'Signin',
                'authenticationForm': AuthenticationForm,
                'error': 'User or password is incorrect'
            })
        else:
            login(request, user)

            response = redirect('/')
            response.set_cookie('tokenUser', request.user.auth_token.key)
            return response

@login_required
def signout(request):
    # Cerrar sesión
    logout(request)
    return redirect('/')

# Projects page
# Imprime todos los proyectos de la base de datos.
# Solo se puede acceder si el usuario está logueado.
@login_required
def projects(request):
    title = "Proyectos"
    # Obtiene todos los proyectos del usuario logueado
    projectsUser_id = Project.objects.filter(user_id=request.user.id)
    return render(request, 'projects/projects.html', {
        'title': title,
        'projects': projectsUser_id
    })

# Tasks page
# Imprime todas las tareas de la base de datos.
@login_required
def tasks(request):
    title = "Tareas"

    #Guardar tareas del usuario logueado
    tasksUser = Task.objects.filter(user_id=request.user.id).order_by('date_limit')
 
    tasksDone = tasksUser.filter(done=True)
    tasksPending = tasksUser.filter(done=False)

    todayDate = date.today()

    for task in tasksPending:
        categoriesList = (task.categories).split(";")
        task.categories = categoriesList

        #Comvertir fecha task.date_limit para compararla con todayDate
        today = date.today().strftime("%d/%m/%Y")
        # Almacenar fecha de la tarea en formato dd/mm/yyyy
        task.date_limit = task.date_limit.strftime("%d/%m/%Y")
        if today == task.date_limit:
            print(today)
            task.today = True
        else:
            task.today = False

        #quitar espacios en blanco de cada categoria
        for i in range(len(task.categories)):
            task.categories[i] = task.categories[i].strip()

     # Obtener token del usuario logueado
    tokenUser = Token.objects.filter(user_id=request.user.id).first()

    numTasks = len(tasksUser)
    return render(request, 'tasks/tasks.html', {
        'title': title,
        'tasks': tasksUser,
        'tasksDone': tasksDone,
        'tasksPending': tasksPending,
        'numTasks': numTasks,
    })

# Teams
@login_required
def create_team(request):
    if request.method == 'POST':
        user = request.user
        form = CreateNewTeam(request.POST)

        if form.is_valid():
            team.user = request.user
            
            cleaned_data = form.cleaned_data

            Team.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                user=user,
            )

            # Añadir al usuario que crea el equipo como miembro del equipo
            TeamUser.objects.create(
                user=user,
                team=Team.objects.filter(name=form.cleaned_data['name']).first(),
            )

            return redirect('teams')
    else:
        form = CreateNewTeam()
    return render(request, 'teams/create_team.html', {'form': form})


@login_required
def teams(request):
    title = "Teams",
    
    # Lista de teams del usuario logueado
    userAdminTeams = TeamUser.objects.filter(user_id=request.user.id)
    userTeams = []
    for team in userAdminTeams:
        team = Team.objects.filter(id=team.team_id).first()
        userTeams.append(team)

    return render(request, 'teams/teams.html', {
        'title': title,
        'userAdminTeams': userTeams,
    })

# Team
@login_required
def team(request, id):
    msgError = ""
    title = "Team",
    team = get_object_or_404(Team, pk=id)
    membersTeam = []
    registersTeamUsers = TeamUser.objects.filter(team_id=id)
    for register in registersTeamUsers:
        member = User.objects.filter(id=register.user_id).first()
        membersTeam.append(member)
    
    projectsTeam = Project.objects.filter(team_id=id)

    if request.method == 'GET':
        return render(request, 'teams/team.html', {
            'team': team,
            'membersTeam': membersTeam,
            'msgError': msgError,
            'projectsTeam': projectsTeam
        })

    if request.method == 'POST':
        # Agregar miembro al equipo
        if request.POST['action'] == 'add_member':
            member = request.POST['new_member']

            newMember = User.objects.filter(username=member).first()
        
            # Verificar si el usuario existe
            if newMember is None:
                msgError = "El usuario no existe"
                return render(request, 'teams/team.html', {
                    'team': team,
                    'membersTeam': membersTeam,
                    'msgError': msgError,
                    'projectsTeam': projectsTeam
                })
            
            # Verificar si el usuario ya está en el equipo
            for member in membersTeam:
                if member.username == newMember.username:
                    msgError = "El usuario ya está en el equipo"
                    return render(request, 'teams/team.html', {
                        'team': team,
                        'membersTeam': membersTeam,
                        'msgError': msgError,
                        'projectsTeam': projectsTeam
                    })
            
            member_id = newMember.id
            team_id = request.POST['team_id']
        
            # Agregar miembro al equipo
            TeamUser.objects.create(
                team_id=team_id,
                user_id=member_id,
            )
        
            return redirect('team', id=id)
        
        # Crear proyecto
        if request.POST['action'] == 'create_project':
            _name = request.POST['project_name']
            description = request.POST['project_description']
            team_id = request.POST['team_id']
            user_id = request.user.id

            # Verificar si el proyecto ya existe
            project = Project.objects.filter(name=_name).first()
            if project is not None:
                msgError = "El proyecto ya existe"
                return render(request, 'teams/team.html', {
                    'team': team,
                    'membersTeam': membersTeam,
                    'msgError': msgError,
                    'projectsTeam': projectsTeam
                })

            # Verificar si el nombre del proyecto es válido
            if _name == "":
                msgError = "El nombre del proyecto no es válido"
                return render(request, 'teams/team.html', {
                    'team': team,
                    'membersTeam': membersTeam,
                    'msgError': msgError,
                    'projectsTeam': projectsTeam
                })


            # Crear proyecto
            Project.objects.create(
                name=_name,
                description=description,
                team_id=team_id,
                user_id=user_id,
            )

    return render(request, 'teams/team.html', {
        'team': team,
        'membersTeam': membersTeam,
        'msgError': msgError,
        'projectsTeam': projectsTeam
    })


'''
Tasks
'''
# Task done
@login_required
def done_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        if task is not None:
            task.done = True
            task.date_done = datetime.now()
            task.save()
    
    return redirect(request.POST['redirect_url'])

# Task delete
@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        if task is not None:
            task.delete()
    return redirect(request.POST['redirect_url'])

# Task undone
@login_required
def undone_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        if task is not None:
            task.done = False
            task.date_done = None
            task.save()
    return redirect(request.POST['redirect_url'])

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(request.user, request.POST, task)
    if request.method == 'POST':
      
        if form.is_valid():
            #quitar espacios en blanco de principio y final de cada categoria
            categories = form.cleaned_data['categories']
            categories = categories.strip()
            categories = categories.split(';')
            categories = [category.strip() for category in categories]
            categories = ';'.join(categories)
            form.cleaned_data['categories'] = categories

            cleaned_data = form.cleaned_data
            
            #Actualizar tarea
            task.title = cleaned_data['title']
            task.description = cleaned_data['description']
            task.categories = cleaned_data['categories']
            task.project_id = cleaned_data['project']
            task.date_limit = cleaned_data['date_limit']
            
            task.save()

            return redirect('/tasks/')
    else:
        form = TaskForm(request.user, request.POST, task)
    
    #El campo project de una tarea puede ser nulo, por lo que se debe comprobar si es nulo o no para poder enviarlo a la vista edit_task.html
    if task.project_id is not None:
        taskProject = task.project
    else:
        taskProject = None

    return render(request, 'tasks/edit_task.html', {
        'form': form,
        'task': task,
        'taskProject': taskProject,
    })

# Create task
@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)

        if form.is_valid():
            #quitar espacios en blanco de principio y final de cada categoria
            categories = form.cleaned_data['categories']
            categories = categories.strip()
            categories = categories.split(';')
            categories = [category.strip() for category in categories]
            categories = ';'.join(categories)
            form.cleaned_data['categories'] = categories

            cleaned_data = form.cleaned_data
            Task.objects.create(
                user=request.user,
                title = form.cleaned_data['title'],
                description=request.POST['description'],
                project=form.cleaned_data['project'],
                date_limit=form.cleaned_data['date_limit'],
                categories=form.cleaned_data['categories'].lower(),
            )
          
            return redirect('/tasks/')
    else:
        form = TaskForm(request.user)

    return render(request, 'tasks/create_task.html', {'form': form})

def category(request, name):
    title = "Category"
    
    tasksUser = Task.objects.filter(user_id=request.user.id, done=False).order_by('date_limit')

    tasksWithCategory = []
    for task in tasksUser:
        task.categories = task.categories.split(';')
        if name in task.categories:
            tasksWithCategory.append(task)

    return render(request, 'tasks/category.html', {
        'title': title,
        'tasks': tasksWithCategory,
        'category': name,
    })
'''
Projects
'''
# Create project
@login_required
def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {
            'form': CreateNewProject
        })
    else:
        Project.objects.create(
            name=request.POST['name'], 
            description=request.POST['description'],
            user=request.user
        )

        return redirect('/projects/')

# Delete project
@login_required
def delete_project(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        if project is not None:
            project.delete()
    return redirect('/projects')


# Tasks by project page
@login_required
def project(request, id):
    project = Project.objects.get(id=id)
    tasks = Task.objects.filter(project=project)
    tasksList = []
    tasksDone = []
    tasksPending = []

    for task in tasks:
        categoriesList = (task.categories).split(";")
        task.categories = categoriesList

        #quitar espacios en blanco de cada categoria
        for i in range(len(task.categories)):
            task.categories[i] = task.categories[i].strip()

        #Añadir tarea a la lista 
        tasksList.append(task)

        if task.done == True:
            tasksDone.append(task)
        else:
            tasksPending.append(task)
        
    #Combertir fecha task.date_limit para compararla con todayDate
    today = date.today().strftime("%A, %d %B %Y")
    for task in tasksPending:
        if today == task.date_limit.strftime("%A, %d %B %Y"):
            task.today = True
        else:
            task.today = False

    return render(request, 'projects/project.html', {
        'project': project,
        'tasksDone': tasksDone,
        'tasksPending': tasksPending
    })

@login_required
def account(request):
    user = request.user
    userName = user.username

    tokenUser = Token.objects.filter(user=user)

    return render(request, 'account.html', {
        'title': 'Account',
        'username': userName,
        'tokenUser': tokenUser
    })

def api_docs(request):
    user = request.user
    userName = user.username

    if Token.objects.filter(user=user).exists():
        userToken = Token.objects.get(user=user)
    else:
        userToken = Token.objects.create(user=user)

    userToken = userToken.key


    return render(request, 'api_doc.html', {
        'title': 'API Documentation',
        'user': user,
        'token': userToken
    })


@login_required
def delete_account(request):
    user = request.user
    user.delete()
    return redirect('/')

@login_required
def edit_account(request):
    user = request.user
    if request.method == 'POST':
        form = EditAccountForm(request.POST)
        if form.is_valid():
            user.username = request.POST['username']
            user.password = request.POST['password']
            user.save()
            return redirect('/account')
    else:
        form = EditAccountForm(request.POST)
    return render(request, 'edit_account.html', {
        'form': form,
        'user': user
    })

@login_required
def PasswordChangeView(PasswordChangeView):
    from_class = PasswordChangeForm
