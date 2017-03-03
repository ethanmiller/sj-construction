from datetime import datetime
from os import path
import csv
import time

from mapbox import Geocoder
from django.core.management.base import BaseCommand, CommandError
from mapview.models import Entity, SubType, WorkDescription, Permit

OBJCACHE = {} # { str(model): { name: object, ... }, ...}

class Command(BaseCommand):
    help = "Import CSV from http://data.sanjoseca.gov/dataviews/230622/active-building-permits/"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.geocoder = Geocoder(access_token='<api key>')

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def _model_or_none(self, m, name):
        if name.strip() in ('', ',', 'NONE'):
            return None
        else:
            OBJCACHE.setdefault(str(m), {})
            if name in OBJCACHE[str(m)]:
                ob = OBJCACHE[str(m)][name]
            else:
                ob, created =  m.objects.get_or_create(name=name)
                OBJCACHE[str(m)][name] = ob
            return ob

    def _geocode(self, address):
        """ geocodes the address, response is [lon, lat] """
        resp = self.geocoder.forward(address)
        if resp.status_code != 200:
            print("May have hit rate limit, give it a minute")
            time.sleep(60)
            resp = self.geocoder.forward(address)
        if resp.status_code == 200:
            first = resp.geojson()['features'][0]
            return first['geometry']['coordinates']
        else:
            return [0.0, 0.0]

    def handle(self, *args, **options):
        if not path.exists(options['csv_file']):
            raise CommandError("File %s not found" % options['csv_file'])
        f = open(options['csv_file'])
        reader = csv.DictReader(f)
        for row in reader:
            if row['gx_location'].strip() == ',':
                continue
            applicant = self._model_or_none(Entity, row['APPLICANT'])
            owner = self._model_or_none(Entity, row['OWNERNAME'])
            contractor = self._model_or_none(Entity, row['CONTRACTOR'])
            subtype = self._model_or_none(SubType, row['SUBTYPEDESCRIPTION'])
            work_desc = self._model_or_none(WorkDescription, row['WORKDESCRIPTION'])
            lon, lat = self._geocode(row['gx_location'])
            perm = Permit(
                    location=row['gx_location'],
                    parcel=row['ASSESSORS_PARCEL_NUMBER'],
                    applicant=applicant,
                    owner=owner,
                    contractor=contractor,
                    folder_num=row['FOLDERNUMBER'],
                    folder_desc=row['FOLDERDESC'],
                    folder_name=row['FOLDERNAME'],
                    subtype=subtype,
                    work_desc=work_desc,
                    approvals=row['PERMITAPPROVALS'],
                    issued=datetime.strptime(row['ISSUEDATE'], '%Y-%m-%dT00:00:00'),
                    dwelling_units=float(row['DWELLINGUNITS']),
                    valuation=float(row['PERMITVALUATION']),
                    square_footage=float(row['SQUAREFOOTAGE']),
                    latitude=lat,
                    longitude=lon
                    )
            perm.save()

