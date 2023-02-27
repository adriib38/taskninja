from django.contrib import admin
from .models import Project, Task, Team, TeamUser

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)

# Register your models here.
admin.site.register(Project)
admin.site.register(Task, TaskAdmin)
admin.site.register(Team)
admin.site.register(TeamUser)

