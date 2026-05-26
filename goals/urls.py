from django.urls import path

# aqui se importan todas las vistas de la app goals
# si se elimina la app goals, este archivo completo debe eliminarse
from goals.views import (
    GoalMetricsApiView,
    GoalCreateApiView,
    GoalRetrieveApiView,
    handleReport
)

urlpatterns = [
    path('', GoalCreateApiView.as_view(), name='goal-create'),
    # ruta para listar y crear metas: GET /api/v1/goal/  POST /api/v1/goal/
    path('metrics/', GoalMetricsApiView.as_view(), name='goal-metrics'),
    # ruta para ver las metricas de la meta activa: GET /api/v1/goal/metrics/
    path('<int:pk>/', GoalRetrieveApiView.as_view(), name='goal-detail'),
    # ruta para ver o editar una meta especifica: GET/PATCH /api/v1/goal/<id>/
    path('metrics/report/', handleReport, name="handlereport")
    # ruta para generar el reporte PDF de la meta activa: GET /api/v1/goal/metrics/report/
]
