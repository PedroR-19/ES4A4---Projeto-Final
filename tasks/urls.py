from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.TaskListViewHome.as_view(), name="home"),
    path(
        'tasks/search/',
        views.TaskListViewSearch.as_view(), name="search"
    ),
    path(
        'tasks/category/<int:category_id>/',
        views.TaskListViewCategory.as_view(), name="category"
    ),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name="task"),
]
