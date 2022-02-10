from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("clients/<int:pk>/", views.ClientView.as_view(), name="clients-overview"),
    path("client/<int:pk>/", views.ClientInfoView.as_view(), name="client-info"),
    path(
        "submission/<int:pk>/",
        views.ClientSubmissionView.as_view(),
        name="client-submission",
    ),
    path(
        "success/<int:pk>/", views.submission_success, name="client-submission-success"
    ),
]
