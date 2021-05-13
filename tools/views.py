import ast
import datetime
import json
import urllib
from urllib.parse import quote_plus
from urllib.parse import quote_plus, unquote_plus

import pytz
from dateutil import parser
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework import views
from rest_framework.response import Response


class EncodeDecodeView(TemplateView):
    template_name = 'tools/encode.html'


class PprintJSONView(TemplateView):
    template_name = 'tools/pprint.html'


class DateParseView(TemplateView):
    template_name = 'tools/date_parse.html'

    def get_context_data(self, **kwargs):
        kwargs['strftime'] = (('%a', 'Weekday as locale’s abbreviated name.', 'Mon'),
                              ('%A', 'Weekday as locale’s full name.', 'Monday'),
                              ('%w', 'Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.', '1'),
                              ('%d', 'Day of the month as a zero-padded decimal number.', '30'),
                              ('%-d', 'Day of the month as a decimal number. (Platform specific)', '30'),
                              ('%b', 'Month as locale’s abbreviated name.', 'Sep'),
                              ('%B', 'Month as locale’s full name.', 'September'),
                              ('%m', 'Month as a zero-padded decimal number.', '09'),
                              ('%-m', 'Month as a decimal number. (Platform specific)', '9'),
                              ('%y', 'Year without century as a zero-padded decimal number.', '13'),
                              ('%Y', 'Year with century as a decimal number.', '2013'),
                              ('%H', 'Hour (24-hour clock) as a zero-padded decimal number.', '07'),
                              ('%-H', 'Hour (24-hour clock) as a decimal number. (Platform specific)', '7'),
                              ('%I', 'Hour (12-hour clock) as a zero-padded decimal number.', '07'),
                              ('%-I,', 'Hour (12-hour clock) as a decimal number. (Platform specific)', '7'),
                              ('%p', 'Locale’s equivalent of either AM or PM.', 'AM'),
                              ('%M', 'Minute as a zero-padded decimal number.', '06'),
                              ('%-M,', 'Minute as a decimal number. (Platform specific)', '6'),
                              ('%S', 'Second as a zero-padded decimal number.', '05'),
                              ('%-S', 'Second as a decimal number. (Platform specific)', '5'),
                              ('%f', 'Microsecond as a decimal number, zero-padded on the left.', '000000'),
                              ('%z', 'UTC offset in the form +HHMM or -HHMM (empty string if the the object is naive).',
                               ''),
                              ('%Z', 'Time zone name (empty string if the object is naive).', ''),
                              ('%j', 'Day of the year as a zero-padded decimal number.', '273'),
                              ('%-j', 'Day of the year as a decimal number. (Platform specific)', '273'),
                              ('%U',
                               'Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.',
                               '39'),
                              ('%W',
                               'Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.',
                               '39'),
                              ('%c', 'Locale’s appropriate date and time representation.', 'Mon Sep 30 07:06:05 2013'),
                              ('%x', 'Locale’s appropriate date representation.', '09/30/13'),
                              ('%X', 'Locale’s appropriate time representation.', '07:06:05'),
                              ('%%', 'A literal "%" character.', '%'))
        return kwargs


class EncodeDecodeAPIView(views.APIView):
    permission_classes = []

    def get(self, request):
        to_encode = request.query_params.get('to_encode')
        to_decode = request.query_params.get('to_decode')
        encoded = quote_plus(to_encode) if to_encode else ''
        decoded = unquote_plus(to_decode) if to_decode else ''
        response = {
            'encoded': encoded,
            'decoded': decoded
        }
        return Response(response)


class PprintJSONAPIView(views.APIView):
    permission_classes = []

    def get(self, request):
        to_pprint = request.query_params.get('to_pprint')
        if not to_pprint:
            return Response({
                'formatted': ''})
        try:
            if to_pprint[0] in ["'", '"'] and to_pprint[-1] in ['"', "'"]:
                to_pprint = to_pprint[1:-1]
            formatted = ast.literal_eval(to_pprint)
            formatted = json.dumps(formatted, indent=4, sort_keys=True)
        except (SyntaxError, ValueError):
            formatted = 'Malformed input :('
        response = {
            'formatted': formatted}
        return Response(response)


class DateParseAPIView(views.APIView):
    permission_classes = []

    def get(self, request):
        to_parse = urllib.parse.unquote(request.query_params.get('to_parse', ''))  # parse a datetime from string
        to_format = request.query_params.get('to_format', '')  # Format datetime as strftime
        try:
            if to_parse.strip().lower() in ['now', 'now()']:
                to_parse = timezone.now().isoformat()
            parsed = parser.parse(to_parse)
            if not parsed.tzinfo:
                parsed = pytz.utc.localize(parsed)
            formatted = parsed.strftime(to_format)
            unix = int(parsed.timestamp())
            parsed = parsed.replace(microsecond=0).isoformat()
        except ValueError:
            try:
                parsed = pytz.utc.localize(datetime.datetime.utcfromtimestamp(float(to_parse)))
                formatted = parsed.strftime(to_format)
                unix = parsed.timestamp()
                parsed = parsed.isoformat()
            except ValueError:
                parsed = ''
                formatted = ''
                unix = ''

        response = {
            'parsed': parsed,
            'formatted': formatted,
            'unix': unix
        }
        return Response(response)
