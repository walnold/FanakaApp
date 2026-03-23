from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Branch
from branches.serializers import BranchSerializer
from accounts.customPermissions import IsSuperUserOrManager 

class BranchCreateView(CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrManager]

# class BranchListView(ListAPIView):
#     queryset = Branch.objects.all()
#     serializer_class = BranchSerializer
#     permission_classes = [IsAuthenticated]


class BranchUpdateView(UpdateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrManager]


class BranchSoftDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsSuperUserOrManager]

    def delete(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk, is_deleted=False)
        except Branch.DoesNotExist:
            return Response({"error": "Branch not found or already deleted"}, status=status.HTTP_404_NOT_FOUND)

        serializer = BranchSerializer(context={'request': request})
        serializer.soft_delete(branch)
        return Response({"message": "Branch soft-deleted successfully"}, status=status.HTTP_200_OK)
    

class BranchListView(ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return branches that are not deleted
        return Branch.objects.filter(is_deleted=False)