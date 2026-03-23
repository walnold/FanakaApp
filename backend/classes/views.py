from rest_framework.viewsets import ModelViewSet
from classes.models import Course, ClassStatus
from classes.serializers import (
    CourseListSerializer,
    CourseDetailSerializer,
    ClassStatusSerializer,
)

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        return CourseDetailSerializer


class ClassStatusViewSet(ModelViewSet):
    queryset = ClassStatus.objects.all()
    serializer_class = ClassStatusSerializer
