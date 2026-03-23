from branches.views import BranchCreateView, BranchListView, BranchUpdateView, BranchSoftDeleteView
from django.urls import path

urlpatterns = [
    path('create/', BranchCreateView.as_view(), name='branch-create'),
    path('', BranchListView.as_view(), name='branch-list'),
    path('branch/<int:pk>/edit/', BranchUpdateView.as_view(), name='branch-update'),
    path('branch/<int:pk>/delete/', BranchSoftDeleteView.as_view(), name='branch-soft-delete'),
    # path('branch/', B)
]

