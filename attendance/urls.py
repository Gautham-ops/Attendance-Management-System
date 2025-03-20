from django.urls import path
# from .views import add_student, mark_attendance, daily_attendance, student_attendance,monthly_attendance,view_students,edit_student,delete_student
from .views import *
urlpatterns = [
    path('index/',index,name='index'),
    path('add_student/', add_student, name='add_student'),
    path('mark_attendance/', mark_attendance, name='mark_attendance'),
    path('daily_attendance/', daily_attendance, name='daily_attendance'),
    path('student_attendance/<str:roll_number>/', student_attendance, name='student_attendance'),
    path('monthly_attendance/', monthly_attendance, name='monthly_attendance'),
    path('', view_students, name='view_students'),
    path('edit_student/<str:roll_number>/',edit_student,name='edit_student'),
    path('delete_student/<str:roll_number>/',delete_student,name='delete_student'),
]
