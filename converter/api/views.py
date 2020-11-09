import csv
import json
import time
from io import StringIO
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import response, status
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.shortcuts import get_current_site


class Index(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Index, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            json_data = request.data
            csv_name = 'file_{0}.csv'.format(int(time.time()))
            generated_json = json.load(json_data['json'])

            flat = []

            def flatten(y):
                out = {}

                def flatten2(x, name=''):
                    if type(x) is dict:
                        for a in x:
                            flatten2(x[a], name + a + '_')
                    elif type(x) is list:
                        i = 0
                        for a in x:
                            flatten2(a, name + str(i) + '_')
                            i += 1
                    else:
                        out[name[:-1]] = x
                flatten2(y)
                return out

            # Loop needed to flatten multiple objects
            for i in range(len(generated_json)):
                flat.append(flatten(generated_json[i]).copy())
            key_length = []
            for j in flat:
                k = []
                for key in j:
                    k.append(key)
                key_length.append(len(k))
            highest_index = key_length.index(max(key_length))
            data_keys = []
            for data in flat[highest_index]:
                data_keys.append(data)
            updated_json = []
            for j in flat:
                values_json = {}
                for key in data_keys:
                    try:
                        values_json.update({"{0}".format(key): "{0}".format(str(j[key]))})
                    except Exception as e:
                        values_json.update({"{0}".format(key): "-11"})  # empty spaces will be filled with -11
                        # print(e)
                updated_json.append(values_json)
            csv_buffer = StringIO()
            csv_writer = csv.writer(csv_buffer)
            csv_writer.writerow(data_keys)
            for j in updated_json:
                values = []
                for key in j:
                    values.append(j[key])
                csv_writer.writerow(values)
            csv_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))
            path = default_storage.save('extracted_data/{0}'.format(csv_name), csv_file)
            full_path = "http://" + get_current_site(request).domain + settings.MEDIA_URL + path
            return response.Response({"message": full_path}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:  # Http404:
            return response.Response({"message": "Invalid code"}, status=status.HTTP_202_ACCEPTED)


