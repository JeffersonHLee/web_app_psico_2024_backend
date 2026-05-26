from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from appointments.models import Appointment
from django.utils.timezone import now
from goals.models import Goal, GoalMetrics
from goals.serializers import GoalSerializer, GoalMetricsSerializer
from django.core import exceptions
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django_xhtml2pdf.utils import pisa
from io import BytesIO
from django.shortcuts import HttpResponse

class GoalCreateApiView(ListCreateAPIView):
    # Vista para listar y crear metas
    queryset = Goal.objects.all()
    # aqui trae todas las metas creadas
    serializer_class = GoalSerializer
    # aqui se convierte la informacion de la meta a Json
    permission_classes = [IsAuthenticated]
    # aqui se autentica paraokay ahora revisa que solo usuarios registrados puedan acceder

class GoalRetrieveApiView(RetrieveUpdateAPIView):
    # Vista para obtener y actualizar una meta especifica por su id
    queryset = Goal.objects.all()
    # aqui trae todas las metas para buscar la que se necesita

    def get_serializer_class(self):
        # aqui se decide que serializer usar segun el tipo de peticion
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return GoalSerializer
            # si es una actualizacion se usa el serializer de escritura
        return GoalSerializer
        # si es una lectura se usa el mismo serializer
    permission_classes = [IsAuthenticated]
    # aqui se autentica para que solo usuarios registrados puedan acceder

class GoalMetricsApiView(ListAPIView):
    # Vista para calcular y devolver las metricas de la meta activa

    def get(self, request, format=None):
        # aqui se maneja la peticion GET para obtener las metricas

        try:
            set_goal = Goal.objects.get(start_time__lte = now().date(), end_time__gte = now().date())
            # aqui se busca la meta activa segun la fecha actual
            goal_appointments = Appointment.objects.filter(goal=set_goal.pk)
            # aqui se filtran las citas que pertenecen a la meta activa
            goal_metric = GoalMetrics(appointments = goal_appointments.count(), monthly_goal_porcentage = goal_appointments.count()/set_goal.apponitments_goal, assistance =goal_appointments.filter(status="DONE").count(), totalAppointments = set_goal.apponitments_goal)
            # aqui se calcula el total de citas, el porcentaje de avance y la asistencia
            goal_metric_serialied = GoalMetricsSerializer(goal_metric)
            # aqui se convierte el resultado a Json
            return Response(goal_metric_serialied.data)
        except exceptions.ObjectDoesNotExist:
            # excepto cuando no hay una meta activa devuelve el mensaje y error 404
            return Response(
                {'message': 'No set goal'},
                status=HTTP_404_NOT_FOUND
            )
        
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def handleReport(request):
    if request.method == "GET":
        try:
            set_goal = Goal.objects.get(start_time__lte = now().date(), end_time__gte = now().date())
            goal_appointments = Appointment.objects.filter(goal=set_goal.pk)
            data = {"appointments" : goal_appointments.count(), "monthly_goal_porcentage" : goal_appointments.count()/set_goal.apponitments_goal, "assistance" : goal_appointments.filter(status="DONE").count()}
            print(data)
            pdf = render_to_pdf('goal/report.html',data)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "report.pdf"
                content = "inline; filename='%s'" %(filename)
                content = "attachment; filename=%s" %(filename)
                response['Content-Disposition'] = content
                return response
            return HttpResponse("Not found")
        except exceptions.ObjectDoesNotExist:
            return Response(
                {'message': 'No set goal'},
                status=HTTP_404_NOT_FOUND
            )