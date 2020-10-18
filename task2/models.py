from django.db import models
from django.utils.translation import ugettext_lazy as _u


class Task(models.Model):
    NEW = "n"
    INPROGRESS = "p"
    DONE = "d"

    STATE_CHOICES = (
        (NEW, _u("New")),
        (INPROGRESS, _u("In Progress")),
        (DONE, _u("Done")),
    )

    title = models.CharField(max_length=250)
    description = models.TextField()
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default=NEW)
    parent = models.ForeignKey(
        "self", related_name="linked", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return self.title
