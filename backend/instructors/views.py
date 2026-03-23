from rest_framework.viewsets import ModelViewSet
from instructors.models import Instructor, InstructorStatus
from instructors.serializers import (
    InstructorListSerializer,
    InstructorDetailSerializer,
    InstructorStatusSerializer,
)

class InstructorViewSet(ModelViewSet):
    queryset = Instructor.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return InstructorListSerializer
        return InstructorDetailSerializer


class InstructorStatusViewSet(ModelViewSet):
    queryset = InstructorStatus.objects.all()
    serializer_class = InstructorStatusSerializer
