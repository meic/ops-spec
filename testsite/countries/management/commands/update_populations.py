import csv

from django.core.management.base import BaseCommand

from countries.models import Country


class Command(BaseCommand):
    help = "Updates Country populations"

    REQUIRED_HEADERS = ["alpha3Code", "population"]

    def add_arguments(self, parser):
        parser.add_argument(
            "input_file",
            help="Filename for input file.",
        )

    def handle(self, *args, **options):
        count = 0
        with open(options["input_file"]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                headers = (key for key in row.keys())
                for header in self.REQUIRED_HEADERS:
                    if header not in headers:
                        raise Exception(f"Column not found: {header}")
                country = Country.objects.get(alpha3Code=row["alpha3Code"])
                country.population = int(row["population"])
                country.save()
                count += 1

        print(f"{count} populations updated.")
