from django.db import models
from django.contrib.auth.models import User


# Un modelo es un objeto que representa una tabla en la base de datos

# Create your models here.
# Modelo de un proyecto
class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        # return f"{self.createdAt.strftime('%d-%m-%Y')}"
        return self.name + " - " + self.user.username


# Modelo de una tarea
class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date_limit = models.DateTimeField(blank=True)
    date_done = models.DateTimeField(blank=True, null=True)
    categories = models.CharField(max_length=200, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + " - " + self.project.name

# Modelo Team
class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " - " + self.user.username

# Modelo TeamUser
class TeamUser(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.team.name + " - " + self.user.username