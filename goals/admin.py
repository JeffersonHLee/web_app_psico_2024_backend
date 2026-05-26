from django.contrib import admin

from goals.models import Goal, GoalMetrics
# se importan los modelos de la app goals para registrarlos en el panel de administracion
# si se elimina la app goals, este archivo completo debe eliminarse


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    # aqui se registra el modelo Goal para que sea visible y editable desde el admin de Django
    ...

@admin.register(GoalMetrics)
class GoalMetricsAdmin(admin.ModelAdmin):
    # aqui se registra GoalMetrics en el admin, aunque este modelo no se guarda en base de datos
    ...
