from django.urls import path
from events.views import (
    org_dashboard, user_dashboard, event_list, event_create, view_event,
    event_update, event_delete, participant_create, participant_update, participant_delete,
    category_create, category_update, category_delete 
)

urlpatterns = [
    path('org-dashboard/', org_dashboard, name='org_dashboard'),
    path('user-dashboard/', user_dashboard, name='user_dashboard'),
    path('event-list/', event_list, name='event_list'),
    path('event-create/', event_create, name='event_create'),
    path('event-view/', view_event, name='event_view'),
    path('event-update/<int:id>/', event_update, name='event_update'),
    path('event-delete/<int:id>/', event_delete, name='event_delete'),
    path('participant-create/', participant_create, name='participant_create'),
    path('participant-update/<int:id>/', participant_update, name='participant_update'),
    path('participant-delete/<int:id>/', participant_delete, name='participant_delete'),
    path('category-create/', category_create, name='category_create'),
    path('category-update/<int:id>/', category_update, name='category_update'),
    path('category-delete/<int:id>/', category_delete, name='category_delete'),
]
