from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)
    alpha2Code = models.CharField(max_length=2)
    alpha3Code = models.CharField(max_length=3)
    population = models.IntegerField()

    region = models.ForeignKey(
        "Region",
        on_delete=models.CASCADE,
        related_name="countries",
    )

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Medals(models.Model):
    TYPES = [
        ("go", "Gold"),
        ("si", "Silver"),
        ("br", "Bronze"),
    ]

    type = models.CharField(
        max_length=2,
        choices=TYPES,
    )
    count = models.IntegerField()

    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE, related_name="medals"
    )

    def __str__(self):
        return f"{self.country.name} - {self.get_type_display()} - {self.count}"
