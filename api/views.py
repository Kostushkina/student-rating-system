from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Student, Event, Request
from .serializers import StudentSerializer, EventSerializer, RequestSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @action(detail=False, methods=['get'])
    def rating(self, request):
        students = Student.objects.all().order_by('-total_points')
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer