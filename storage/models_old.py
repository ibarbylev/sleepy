from django.db import models


class Segment(models.Model):
    start = models.DateTimeField()
    finish = models.DateTimeField()
    length = models.PositiveIntegerField(default=0)
    lengthHM = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.start} - {self.finish} / {self.finish-self.start}'

    # def save(self):
    #     length = self.finish - self.start
    #     super().save()


class Sleep(models.Model):
    startRoutineTime = models.DateTimeField()
    startFallingAsleepTime = models.DateTimeField()
    segments = models.ForeignKey(Segment, on_delete=models.CASCADE, blank=True, null=True)
    finishTime = models.DateTimeField()
    isItNightSleep = models.BooleanField(default=False)
    place = models.CharField(max_length=255)
    moodStartOfSleep = models.CharField(max_length=255)
    moodEndOfSleep = models.CharField(max_length=255)


class Client(models.Model):
    client_name = models.CharField(max_length=200)
    birthdate = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    sleeps = models.ForeignKey(Sleep, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.client_name} {self.birthdate}'

