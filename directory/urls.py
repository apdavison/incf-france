from django.urls import path, re_path

from .views import PeopleResource, PeopleListResource, \
                   TeamResource, TeamListResource, \
                   ProjectResource, ProjectListResource, \
                   index, profile, upload_logo, upload_photo

urlpatterns = [
    path('', index, name='index'),
    path('profile/', profile, name='profile'),
    path('people', PeopleListResource.as_view(), name="researcher-list-api"),
    path('people/<slug:id>', PeopleResource.as_view(), name="researcher-profile-api"),
    path('people/<slug:id>/photo', upload_photo, name="researcher-photo-api"),
    path('teams', TeamListResource.as_view(), name="team-list-api"),
    path('teams/<slug:id>', TeamResource.as_view(), name="team-profile-api"),
    path('projects', ProjectListResource.as_view(), name="project-list-api"),
    path('projects/<slug:id>', ProjectResource.as_view(), name="project-profile-api"),
    path('projects/<slug:id>/logo', upload_logo, name="project-logo-api"),
]