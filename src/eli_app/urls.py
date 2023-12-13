from django.urls import path
from .views import (
    ActListView,
)

name = "eli"
urlpatterns = [
    path("acts/", ActListView.as_view(), name="acts"),
]
