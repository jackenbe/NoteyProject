from tokenize import group

from django.urls import path
from .views import home
from .views import sign_up, group_create, group_list, view_universities,group_view, note_view, note_create, personal_view, personal_note_create

app_name = "Core"
urlpatterns = [
    path('', home, name='home'),
    path('home/', home, name='home'),
    path('sign-up/', sign_up, name='sign_up'),
    path('groups/', group_list, name="groups_list"),
    path('group-create/', group_create, name="group_create"),
    path('universities/', view_universities, name="universities"),
    path('group/<int:id>/', group_view, name='group_view'),
    path('note/<int:id>', note_view, name="note_view"),
    path('group/<int:id>/create/', note_create, name="note_create"),
    path('personal/', personal_view, name="personal_view"),
    path('personal/create', personal_note_create, name='personal_note_create')
]