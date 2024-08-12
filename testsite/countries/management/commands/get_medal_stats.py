from django.core.management.base import BaseCommand
from django.db.models import Sum, Case, When, IntegerField

from countries.models import Country, Medals


class Command(BaseCommand):
    help = "Print Medal Stats"

    def handle(self, *args, **options):
        countries = Country.objects.annotate(total_medals=Sum("medals__count"))

        print("Country with the highest number of medals:")
        country = countries.order_by("-total_medals").first()
        print(f"{country.name} - {country.total_medals} total medals\n")

        countries_with_gold_medals = Country.objects.annotate(
            gold_medals=Sum(
                Case(
                    When(medals__type="go", then="medals__count"),
                    output_field=IntegerField(),
                )
            )
        )

        print("Country with 10 or more Gold medals:")
        countries = countries_with_gold_medals.filter(gold_medals__gte=10).order_by(
            "-gold_medals"
        )
        for country in countries:
            print(f"{country.name} - {country.gold_medals} Gold medals")
