from django.shortcuts import render
import requests
from datetime import datetime
import pytz

# Create your views here.
def index(request):
    city = 'london'
    
    if request.method == "POST":
        city = request.POST["city"]
    
    #openweather current weather api
    url_openweather = 'http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid=36b3749f521696ac27ab0367a0ad9faa'
    openweather = requests.get(url_openweather).json()

    latitude = openweather['coord']['lat']
    longitude = openweather['coord']['lon']
    country = openweather['sys']['country']
    temp =  int((openweather['main']['temp'])-273.15)
    condition = openweather['weather'][0]['main']
    icon_current = openweather['weather'][0]['icon']
    wind = openweather['wind']['speed']
    high = int((openweather['main']['temp_max'])-273.15)
    low = int((openweather['main']['temp_min'])-273.15)
    sunrise_timestamp = openweather['sys']['sunrise']
    time_sunrise = datetime.fromtimestamp(sunrise_timestamp)
    sunrise = time_sunrise.strftime("%I:%M")
    sunset_timestamp = openweather['sys']['sunset']
    time_sunset = datetime.fromtimestamp(sunset_timestamp)
    sunset = time_sunset.strftime("%I:%M")
    humidity = openweather['main']['humidity']

    #weatherbit forcast api
    url_weatherbit = 'https://api.weatherbit.io/v2.0/forecast/hourly?city='+city+'&key=9e6c6356556440ac9c492455185ab904&hours=24'
    weatherbit = requests.get(url_weatherbit).json()

    # icon = []
    # for i in range(1, 8):
    #     ele = weatherbit['data'][i]['weather']['icon']
    #     icon.append(ele)
    # description = []
    # for i in range(1, 8):
    #     ele = weatherbit['data'][i]['weather']['description']
    #     description.append(ele)
    # temperature = []
    # for i in range(1, 8):
    #     ele = weatherbit['data'][i]['temp']
    #     temperature.append(ele)

    # forcast_time = {'1pm' : ['1pm',icon[0],description[0],temperature[0]],
    #             '2pm' : ['2pm',icon[1],description[1],temperature[1]],
    #             '3pm' : ['3pm',icon[2],description[2],temperature[2]],
    #             '4pm' : ['4pm',icon[3],description[3],temperature[3]],
    #             '5pm' : ['5pm',icon[4],description[4],temperature[4]],
    #             '6pm' : ['6pm',icon[5],description[5],temperature[5]],
    #             '7pm' : ['7pm',icon[6],description[6],temperature[6]],
    #     }   
    
    #openweather onecall api
    url_onecall = 'https://api.openweathermap.org/data/2.5/onecall?lat='+str(latitude)+'&lon='+str(longitude)+'&exclude=daily&appid=36b3749f521696ac27ab0367a0ad9faa'
    onecall = requests.get(url_onecall).json()

    ST = pytz.timezone(onecall['timezone'])
    date_time = str(datetime.now(ST))
    # time = date_time[11:19]
    hh = int(date_time[11:13])
    mm = date_time[14:16]

    months = {
        1 : 'January',
        2 : 'February',
        3 : 'March',
        4 : 'April',
        5 : 'May',
        6 : 'June',
        7 : 'July',
        8 : 'August',
        9 : 'September',
        10 : 'October',
        11 :  'November',
        12 : 'December',
    }
    DD=date_time[8:10]
    MM=int(date_time[5:7])

    icon = []
    for i in range(1, 8):
        ele = onecall['hourly'][i]['weather'][0]['icon']
        icon.append(ele)
    description = []
    for i in range(1, 8):
        ele = onecall['hourly'][i]['weather'][0]['description']
        description.append(ele)
    temperature = []
    for i in range(1, 8):
        ele = int(onecall['hourly'][i]['temp']-273.15)
        temperature.append(ele)

    forcast_time = {'1pm' : [str(hh)+':'+str(mm),icon[0],description[0],temperature[0]],
                '2pm' : [str(hh+1)+':'+str(mm),icon[1],description[1],temperature[1]],
                '3pm' : [str(hh+2)+':'+str(mm),icon[2],description[2],temperature[2]],
                '4pm' : [str(hh+3)+':'+str(mm),icon[3],description[3],temperature[3]],
                '5pm' : [str(hh+4)+':'+str(mm),icon[4],description[4],temperature[4]],
                '6pm' : [str(hh+5)+':'+str(mm),icon[5],description[5],temperature[5]],
                '7pm' : [str(hh+6)+':'+str(mm),icon[6],description[6],temperature[6]],
        }   

    #context
    context = {
        'city': city,
        'country' : country,
        'temp' : temp,
        'condition' :condition,
        'icon_current' : icon_current,
        'wind' : wind,
        'high' : high,
        'low' : low,
        'sunrise' : sunrise,
        'sunset' : sunset,
        'humidity' : humidity,
        'forcast_time' : forcast_time,
        'icon' : icon,
        'hh' : hh,
        'mm' : mm,
        'DD' : DD,
        'MM' : months[MM],
    }
    return render(request,'index.html',context)