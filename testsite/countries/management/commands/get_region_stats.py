import csv

from django.core.management.base import BaseCommand
from django.db.models import Count, Sum

from countries.models import Region


class Command(BaseCommand):
    help = "Exports stats on region."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-file",
            default="stats",
            help="Filename for output file.",
        )

    def handle(self, *args, **options):
        regions = Region.objects.annotate(
            num_countries=Count("countries"),
            total_population=Sum("countries__population"),
        )

        headings = ["Name", "Number Countries", "Total Population"]

        data = [
            [region.name, region.num_countries, region.total_population]
            for region in regions
        ]

        with open(options["output_file"], "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headings)
            writer.writerows(data)

        print(f"Stats exported to: {options['output_file']}")
