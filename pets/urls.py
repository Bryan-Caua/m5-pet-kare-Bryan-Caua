from django.urls import path
from .views import PetsViews, PetsDatailView

urlpatterns = [
    path("pets/", PetsViews.as_view()),
    path("pets/<int:pet_id>/", PetsDatailView.as_view()),
]
