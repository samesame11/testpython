from django.shortcuts import render
import urllib.request
import json
import numpy as np

def task3():
    output = []
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    api_key = 'AIzaSyB2gn6769SxUiUsyAAReGKN0_JVCTzPxTs'
    # origin =input('Where are you?: ').replace(' ','+')
    origin = "SCG Bangsue"
    origin = origin.replace(' ','+')
    destination = "Central World Bangkok"
    destination = destination.replace(' ','+')
    # destination=input('Where do you want to do?: ').replace(' ','+')
    nav_request ='origin={}&destination={}&key={}'.format(origin,destination,api_key)
    request = endpoint + nav_request
    response = urllib.request.urlopen(request).read()
    directions = json.loads(response)
    routes = directions['routes']
    legs = routes[0]['legs']
    # print(legs)
    ways = legs[0]['steps']
    distance = (legs[0]['distance']['text'])
    duration = (legs[0]['duration']['text'])
    goby = (ways[0]['travel_mode'])
    output.append(distance)
    output.append(duration)
    output.append(goby)
    return output

# Calculate diff between inputs
def calculate_diff(input):
    output = []
    for i in range(len(input) - 1):
        diff = input[i+1] - input[i]
        output.append(diff)
    return  output

# Find range of known inputs
def find_range(input):
    found_start_flag = False
    output = []
    for i in range(len(input)):
        if input[i] is not None and found_start_flag == False:
            found_start_flag = True
            output.append(i)
        elif input[i] is None and found_start_flag == True:
            output.append(i - 1)
            break
    return output

# Fill static inputs compares to the length of the input
def fill_static_arr(input, static_arr):
    r = find_range(input)
    for i in range(0, r[0]):
        static_arr.insert(0, static_arr[0] - 2)
    for i in range(r[1], len(input) - 1):
        static_arr.append(static_arr[i - 1] + 2)
    return static_arr


# Calculate the series
def calculate_series(input, static_arr):
    r = find_range(input)
    print(static_arr)
    for i in range(r[0] -1 , -1 , -1):
        input[i] = input[i + 1] - static_arr[i]
    for i in range(r[1] + 1, len(input)):
        input[i] = input[i - 1] + static_arr[i-1]
    return input


def task2():

    # declares vars
    x,y,z = None, None, None
    input = [x,y,5,9,15,23,z]
    # find known inputs
    r = find_range(input)
    known_input =  input[r[0]: r[1] + 1]


    n = []
    while np.allclose(known_input, known_input[0]) == False:
        diff_input = calculate_diff(known_input)
        n.append(diff_input)
        known_input = diff_input

    static_arr = fill_static_arr(input, n[0])
    calculate_series(input, static_arr)
    return input

def task1():
    a = 21
    for b in range(-50, 51, 1):
        for c in range(-50, 51, 1):
            if a + b == 23 and a + c == -21:
                text = "B: "+str(b)+' C: '+str(c)
                return text


# Create your views here.
def mainpage(request):
    result = task3()
    return render(request,'index.html'
    ,{
        'distance': result[0],
        'duration': result[1],
        'goby': result[2],
        'answer1': task1(),
        'answer2': task2(),
    })