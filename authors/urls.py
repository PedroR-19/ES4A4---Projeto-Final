from django.urls import path

from . import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/task/new/',
        views.DashboardTask.as_view(),
        name='dashboard_task_new'
    ),
    path(
        'dashboard/task/delete/',
        views.DashboardTaskDelete.as_view(),
        name='dashboard_task_delete'
    ),
    path(
        'dashboard/task/<int:id>/edit/',
        views.DashboardTask.as_view(),
        name='dashboard_task_edit'
    ),
]
