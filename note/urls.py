from . import views  # if views is in note app
from django.urls import path
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # 127.0.0.1:8000
    path("", views.frontpage, name='frontpage'), # Landing page for all users
    path("signup/", views.signup, name='signup'), # Signup page
    path("login/", views.userlogin, name='login'), # Login page
    path("home/", views.home, name='home'), # Dashboard/home page after login
    path("logout/", LogoutView.as_view(next_page='frontpage'), name='logout'),
    path('about/', views.about, name='about'),
    path('notebook/', views.notes, name='notes'),
    path('notes/<int:id>/', views.note_detail, name='note_detail'),
    path('notes/<int:id>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:id>/edit/', views.edit_note, name='edit_note'),
]