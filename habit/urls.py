from django.urls import path
from .views import WontListCreateView, PublicWontListView, WontDetailView

urlpatterns = [
    path('', WontListCreateView.as_view(), name='wont_list_create'),
    path('public/', PublicWontListView.as_view(), name='public_wont_list'),
    path('<int:pk>/', WontDetailView.as_view(), name='wont_detail'),
]