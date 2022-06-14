from django.db import models
from authentication.models import User


class Segment(models.Model):
    start = models.DateTimeField()
    finish = models.DateTimeField()
    length = models.PositiveIntegerField(default=0)
    lengthHM = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.start} - {self.finish} / {self.finish-self.start}'

    # def save(self):
    #     length = self.finish - self.start
    #     super().save()


class Sleep(models.Model):
    startRoutineTime = models.DateTimeField()
    startFallingAsleepTime = models.DateTimeField()
    segments = models.ManyToManyField(Segment, blank=True)
    finishTime = models.DateTimeField()
    isItNightSleep = models.BooleanField(default=False)
    place = models.CharField(max_length=255, blank=True, null=True)
    moodStartOfSleep = models.CharField(max_length=255, blank=True, null=True)
    moodEndOfSleep = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.place} {self.startRoutineTime} {self.startFallingAsleepTime}'


class Client(models.Model):
    client_name = models.CharField(max_length=200)
    birthdate = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    sleeps = models.ManyToManyField(Sleep, blank=True)
    consultant = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return f'{self.client_name} {self.pk} {self.birthdate}'

