from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=639bc8c4220f54f6449098390817fe1a'
    
    if request.method=='POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city=form.cleaned_data['name']
            existing_city_count= City.objects.filter(name=new_city).count()
            if existing_city_count==0:
                r=requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    err_msg='City does not exist'
            else:
                err_msg='City already exists in the database'
            
            
    form = CityForm()        
    cities=City.objects.all()
    weather_data=[]
    for city in cities:
        r=requests.get(url.format(city)).json()
        city_weather={
        'city': city.name,
        'temperature':r['main']['temp'],
        'description':r['weather'][0]['description'],
        'icon':r['weather'][0]['icon'],
        
        }
        weather_data.append(city_weather)
    context={'weather_data':weather_data, 'form':form}
    return render(request, 'weathers/weather.html', context)

