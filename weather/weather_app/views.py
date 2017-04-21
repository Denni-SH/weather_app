from django.shortcuts import render
import requests
from .models import Information
from django.http import Http404

def index(request):
    return render(request, 'weather_app/input.html')

def output(request):
    form = {}
    if request.POST:
        form['city'] = request.POST.get('city')
    s_city = str(form['city'])
    w_date = []
    w_temp = []
    w_desc = []
    if Information.objects.filter(city=s_city).exists():
        db_data = []
        db_data.append(Information.objects.filter(city=s_city).all().values_list())
        for j in db_data:
            for i in j:
                w_date.append(i[2])
                w_temp.append(i[3])
                w_desc.append(i[4])
    else:
        appid = "4b6b4c326521b37ef3e934995fffd90a"
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
            data = res.json()
            for i in data['list']:
                w_date.append(i['dt_txt'])
                w_temp.append('{0:+3.0f}'.format(i['main']['temp']))
                w_desc.append(i['weather'][0]['description'])
            for i in range(len(w_date)):
                save_info = Information(city=s_city, date=w_date[i], temperature=w_temp[i], description=w_desc[i])
                save_info.save()
            w_data = [w_date, w_temp, w_desc]
            w_data = zip(*w_data)
        except Exception as e:
            raise Http404("No cities matches the given query.")
    return render(request, 'weather_app/output.html',
                  {'form': form, 'w_data': w_data})

