from django.db import models

# Create your models here.
class Students(models.Model):
    name=models.CharField(max_length=100)
    roll_number=models.CharField(max_length=20,unique=True)

    def str(self):
        return self.name

class Attendance(models.Model):
    student=models.ForeignKey(Students,on_delete=models.CASCADE)
    date=models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    
    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"

