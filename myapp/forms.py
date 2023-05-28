from django import forms
from .models import Project, Task, Team
from django.contrib.auth.models import User


'''
#Almacenamos los nombres de los proyectos en una lista
projectsUser = Project.objects.filter(user=usernameLog)
projects = Project.objects.all()
project_names = []
for project in projects:
    project_names.append((project.id, (project.name + " - id: " + str(project.id))))
'''


'''
class CreateNewTask(forms.Form):

    title = forms.CharField(label='Título', max_length=200)
    description = forms.CharField(label="Descripción de la tarea", widget=forms.Textarea, max_length=500)

    project_id = forms.ChoiceField(
        label="Proyecto",
        required=True,
        widget=forms.RadioSelect,
        # Opciones de proyecto a elegir
        #choices=project_names, 
        choices=[]
    )
    
'''

class TaskForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=user)

    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea, required=False)
    #project, puede ser null
    project = forms.ModelChoiceField(queryset=Project.objects.none(), required=False, empty_label="Sin proyecto")
    date_limit = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    categories = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'placeholder': 'Categories separated by ;'}))


class EditTaskForm(forms.Form):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'date_limit']
    
    def __init__(self, user, *args, **kwargs):
        super(EditTaskForm, self).__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(user=user)

    title = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'New title'}))
    description = forms.CharField(widget=forms.Textarea)
    #project, puede ser null
    project = forms.ModelChoiceField(queryset=Project.objects.none(), required=False, empty_label="Sin proyecto")
    date_limit = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    categories = forms.CharField(max_length=255, required=False, widget=forms.Textarea(attrs={'placeholder': 'Categories separated by ;'}))

class CreateNewProject(forms.Form):
    name = forms.CharField(label='Nombre del proyecto', max_length=200)
    description = forms.CharField(label="Descripción del proyecto", widget=forms.Textarea, max_length=500)

class EditAccountForm(forms.Form):
    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'New username'}))
    #password cifrate   
    password = forms.CharField(max_length=255, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))

class CreateNewTeam(forms.Form):
    name = forms.CharField(label='Nombre del equipo', max_length=200)
    description = forms.CharField(label="Descripción del equipo", widget=forms.Textarea, max_length=500)

    
# Crear proyecto de team
class CreateNewTeamProject(forms.Form):
    name = forms.CharField(label='Nombre del proyecto', max_length=200)
    description = forms.CharField(label="Descripción del proyecto", widget=forms.Textarea, max_length=500)

    team_id = forms.ChoiceField(
        label="Equipo",
        required=True,
        widget=forms.RadioSelect,
        # Opciones de proyecto a elegir
        #choices=project_names, 
        choices=[]
    )
    
