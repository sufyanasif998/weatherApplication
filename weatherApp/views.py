from django.shortcuts import render
import requests
from datetime import datetime
from datetime import date, timedelta


# Create your views here.


def index(request):
    if request.method == 'POST':
        city = request.POST.get('city').capitalize()
    else:
        city = 'Dera Ghazi Khan'
   
    # URL = 'https://api.openweathermap.org/data/2.5/weather'
    # PARAMS = {'q': city, 'appid':appid, 'units':'metric'}
    # # URL1 = 'api.openweathermap.org/data/2.5/forecast?'
    # # PARAMS1 = {'q' : city, 'appid':appid, 'units': 'metric'}
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=d9c3a57526c4ee9dd8842f7dfbd66a98")
    res = r.json()
    r1 = requests.get(f'https://api.openweathermap.org/data/2.5/forecast?q={city}&units=metric&appid=d9c3a57526c4ee9dd8842f7dfbd66a98')
    weather = r1.json()
    # print(type(weather))
    descrip = res['weather'][0]['description'].capitalize()
    icon = res['weather'][0]['icon']
    print(icon)
    temp = res['main']['temp']

    #Air Conditions  
    temp_feel = res['main']['feels_like']
    real_temp_feel = round(temp_feel)
    humididty = res['main']['humidity']
    wind_speed = (res['wind']['speed'])
    clouds = (res['clouds']['all'])


    #Hourly Forecast
    mylist= []
    datelist = []
    hourly_temp = []
    for x in range(5):
        we = weather['list'][x]['weather'][0]['icon']
        curr_temp = round(weather['list'][x]['main']['temp'])
        ts = int(weather['list'][x]['dt'])
        finaltime = datetime.utcfromtimestamp(ts).strftime('%H:%M')
        print(finaltime)
        mylist.insert(x,we)
        datelist.insert(x,finaltime)
        hourly_temp.insert(x,curr_temp)

    

    
   
    # start_date = date(2023,6,9)
    start_date = date.today()
    print(start_date)
    daily_dates = []
    daily_dates1 = []
    day = []
    weeklyIcon = []
    num = 0
    now = datelist[0]

    
    for single_date in (start_date + timedelta(n) for n in range(5)):
        print(now)
        daily_dates.insert(num, single_date.strftime("%Y-%m-%d ") + now +":00")
        intDay = single_date.strftime('%A')
        if(intDay != None):
            day.insert(num, intDay)
        daily_dates1.insert(num, single_date.strftime("%Y-%m-%d") +" 21:00:00")
        num = num+1
    
  

    
    
    index = 0
    max_temp = []
    min_temp = []
    for i in range(40):
        check = daily_dates[index]
        # print(check)
        if(weather['list'][i]['dt_txt'] == check):
            max_tempRound = round(weather['list'][i]['main']['temp_max'])
            max_temp.insert(index,max_tempRound)
            weeklyIcon.insert(index,weather['list'][i]['weather'][0]['icon'])
            # min_temp.insert(index,weather['list'][i]['main']['temp_min'])
            index = index+1
            if(index == 5):
                break
    index = 0
    for i in range(40):
        check = daily_dates1[index]
        # print(check)
        if(weather['list'][i]['dt_txt'] == check):
            min_tempRound = round(weather['list'][i]['main']['temp_min'])
            min_temp.insert(index, min_tempRound)
            index = index+1
            if(index == 5):
                break
    
   
    foo = 0
    # print(icon)
    tempe = int(temp)
    # print(tempe)
    return render(request, 'index.html', {'description':descrip, 'temp':tempe, 'icon':icon , 'city': city,
    'wind_speed':wind_speed, 'temp_feel':real_temp_feel, 'clouds':clouds, 'humidity':humididty,
    'weather':mylist, 'range':range(5), 'datelist':datelist, 'foo':foo, 'hourly_temp':hourly_temp,
    'max_temp':max_temp, 'min_temp':min_temp, 'day':day, 'weeklyIcon':weeklyIcon})