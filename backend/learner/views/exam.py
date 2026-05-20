from rest_framework import viewsets, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from learner.models.Exam import Exam, ExamStatus
from learner.serializers.Exam import ExamCreateSerializer, ExamListSerializer, ExamDetailSerializer, ExamStatusSerializer

class ExamStatusViewSet(viewsets.ModelViewSet):
    queryset = ExamStatus.objects.all()
    serializer_class = ExamStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'create':
            return ExamCreateSerializer
        elif self.action == 'list':
            return ExamListSerializer
        elif self.action == 'retrieve':
            return ExamDetailSerializer
        elif self.action in ['update','partial_update']:
            return ExamCreateSerializer
        return ExamDetailSerializer

    def get_queryset(self):
        queryset = Exam.objects.all()
        learner_id = self.request.query_params.get("learner")
        enrollment_id = self.request.query_params.get("enrollment")
        if learner_id:
            queryset = queryset.filter(enrollment__learner_id=learner_id)
        if enrollment_id:
            queryset = queryset.filter(enrollment_id=enrollment_id)
        return queryset
