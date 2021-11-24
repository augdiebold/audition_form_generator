from django.urls import path, include

from form_generator.core.views import new, index, update, delete, detail

urlpatterns = [
    path('', index, name='index'),
    path('audition/', new, name='new_audition'),
    path('audition/<int:pk>', detail, name='audition_detail'),
    path('audition/<int:pk>/edit', update, name='edit_audition'),
    path('audition/<int:pk>/delete', delete, name='delete_audition'),

]
