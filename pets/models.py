from django.db import models

class Sex(models.TextChoices):
    Male= "Male"
    Female = "Female"
    Default = "Not Informed"

class Pet(models.Model):

    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(default=Sex.Default, choices=Sex.choices, max_length=20)
    group = models.ForeignKey("groups.Group", on_delete=models.PROTECT, related_name='pets')
    traits = models.ManyToManyField("traits.Trait")

    def __repr__(self) -> str:
        return f"<Pet ({self.age} - {self.name}>)"