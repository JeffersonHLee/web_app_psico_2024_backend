from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from activity.models import Activity
from activity.serializers import ActivityReadSerializer, ActivitySerializer
from django.utils.timezone import now


class ActivityCreateApiView(ListCreateAPIView):
    # Vista para listar y crear actividades
# ListCreateAPIView nos da GET (listar) y POST (crear) automáticamente
    queryset = Activity.objects.all()
    #aqui decimos que nos devolvera y con el .all llamamos a todos los creados
    serializer_class = ActivitySerializer
    #aqui se vuelve Json
    permission_classes = [IsAuthenticated]
#aqui se auntentica para que solo los usuarios creados
class ActivityRetrieveApiView(RetrieveUpdateAPIView):
    queryset = Activity.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return ActivitySerializer
        #aqui lo vuelve un serealizer(Jason)
        return ActivityReadSerializer
    #quie se usa para que se lea el serializer
    permission_classes = [IsAuthenticated]
    
class ActivityGetPendingApiView(ListAPIView):
    today = now().date()
    #aqui se usa para el dia actual
    queryset = Activity.objects.filter(date__gte=today, status="PENDING").order_by('date')
    #aqui se filtra las actividades segun su dia, estatus y fecha
    serializer_class = ActivityReadSerializer
    permission_classes = [IsAuthenticated]