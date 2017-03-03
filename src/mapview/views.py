import json

from django.http import HttpResponse
from django.template import loader
from django.core.serializers.json import DjangoJSONEncoder

from mapview.models import Entity, SubType, WorkDescription, Permit

def index(request):
    template = loader.get_template('mapview/index.html')
    return HttpResponse(template.render({}, request))

def init(request):
    data = {
        'bannerMsg': "There are %s active building permits in the database." % Permit.objects.count(),
        'filtersSubType': list(SubType.objects.all().values())
    }
    return HttpResponse(json.dumps(data), content_type='application/json')

def subtype_filters(request, fid):
    permits = Permit.objects.filter(subtype_id=fid)
    data = {'places': list(permits.values())}
    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder), content_type='application/json')
