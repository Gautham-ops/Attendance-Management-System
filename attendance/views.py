from calendar import monthrange
from django.shortcuts import render, get_object_or_404,redirect
from django.http import JsonResponse
from .models import Students, Attendance
from datetime import date, datetime

def add_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        roll_number = request.POST['roll_number']
        Students.objects.get_or_create(name=name, roll_number=roll_number)
        return redirect('add_student')

    return render(request, 'attendance/add_student.html')

def mark_attendance(request):
    students = Students.objects.all()
    if request.method == 'POST':
        roll_number = request.POST['roll_number']
        status = request.POST['status']
        attendance_date = request.POST.get('attendance_date', str(date.today()))
        attendance_date = datetime.strptime(attendance_date, '%Y-%m-%d').date()  

        student = get_object_or_404(Students, roll_number=roll_number)
        attendance, created = Attendance.objects.get_or_create(
            student=student, date=attendance_date, defaults={'status': status}
        )
        if not created:
            attendance.status = status
            attendance.save()
        return redirect('mark_attendance')

    return render(request, 'attendance/mark_attendance.html', {'students': students})

def daily_attendance(request):
    today = date.today()
    attendance_records = Attendance.objects.filter(date=today)
    present = [record.student.name for record in attendance_records if record.status == 'Present']
    absent = [record.student.name for record in attendance_records if record.status == 'Absent']
    
    return render(request, 'attendance/daily_attendance.html', {'date': today, 'present': present, 'absent': absent})

def student_attendance(request, roll_number):
    student = get_object_or_404(Students, roll_no=roll_number)
    attendance_records = Attendance.objects.filter(student=student, date__month=datetime.today().month)
    
    return render(request, 'attendance/student_attendance.html', {'student': student, 'attendance_records': attendance_records})

def monthly_attendance(request):
    students = Students.objects.all()

    month = request.GET.get('month', '').strip()  # Remove any accidental spaces
 
    try:
        date_obj = datetime.strptime(month, '%Y-%m')
        month = date_obj.month
        year = date_obj.year
    except ValueError:
        # If parsing fails, use current month and year
        current_date = datetime.today()
        month = current_date.month
        year = current_date.year


    print("--------------------------------")
    print(month,year)
    print("--------------------------------")

    attendance_records = Attendance.objects.filter(
        date__month=month,
        date__year=year
    )


    for record in attendance_records:
        print(record.date)
        print(record.student.name,record.status)
        print("--------------------------------")


    present_students = {record.student.name for record in attendance_records if record.status == 'Present'}
    absent_students = {record.student.name for record in attendance_records if record.status == 'Absent'}

    return render(request, 'attendance/monthly_attendance.html', {
        'month':month,
        'year': year,
        'present_students': present_students,
        'absent_students': absent_students,
        'students': students
    })

def edit_student(request, roll_number):
    student = get_object_or_404(Students, roll_number=roll_number)

    if request.method == 'POST':
        student.name = request.POST['name']
        student.roll_number = request.POST['roll_number']
        student.save()
        return redirect('view_students')
    
def delete_student(request,roll_number):
    student = get_object_or_404(Students, roll_number=roll_number)

    if request.method == 'POST':
        student.delete()
        return redirect('view_students')
    
    return render(request,'attendance/delete_student.html',{'student':student})

def view_students(request):
    students = Students.objects.all()
    return render(request, 'attendance/view_students.html', {'students': students})


def index(request):
    return render(request, 'attendance/index.html')
