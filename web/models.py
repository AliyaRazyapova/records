from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_tag = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True
    )


class Record(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    img = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'Record {self.id} "{self.title}'
