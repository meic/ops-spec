import csv

from django.core.management.base import BaseCommand

from countries.models import Country, Medals


class Command(BaseCommand):
    help = "Updates Country Medals"

    REQUIRED_HEADERS = ["ISO", "Gold", "Silver", "Bronze"]

    def add_arguments(self, parser):
        parser.add_argument(
            "input_file",
            help="Filename for input file.",
        )

    def handle(self, *args, **options):
        with open(options["input_file"]) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                headers = (key for key in row.keys())
                for header in self.REQUIRED_HEADERS:
                    if header not in headers:
                        raise Exception(f"Column not found: {header}")
                print(f"Importing: {row['ISO']} - {row}")

                country = Country.objects.get(alpha3Code=row["ISO"])
                Medals.objects.update_or_create(
                    country=country, type="go", defaults={"count": row["Gold"]}
                )
                Medals.objects.update_or_create(
                    country=country, type="si", defaults={"count": row["Silver"]}
                )
                Medals.objects.update_or_create(
                    country=country, type="br", defaults={"count": row["Bronze"]}
                )
        print("\nImport Complete")
