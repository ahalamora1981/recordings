from django.db import models

# Create your models here.
class Recording(models.Model):
    file_name = models.CharField(max_length=200, unique=True)
    start_time = models.DateTimeField(null=False)
    duration = models.IntegerField(null=False)
    direction = models.CharField(max_length=1)
    extension = models.CharField(max_length=50)
    agent_id = models.CharField(max_length=50)
    ani = models.CharField(max_length=50)
    dnis = models.CharField(max_length=50)
    custom_data_01 = models.CharField(max_length=200)
    custom_data_02 = models.CharField(max_length=200)
    custom_data_03 = models.CharField(max_length=200)

    def __str__(self):
        return self.file_name