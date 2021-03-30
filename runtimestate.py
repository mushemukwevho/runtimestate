"""RUNTIME STATE FOR FUNCTIONS AND CLASS METHODS

Author: Mushe Mukwevho
E-mail: mushemukwevho@gmail.com

I have created this module to monitor state,errors and performance of class methods and functions.
It can monitor methods at runtime. 

The report is optionally dumped into a json file, data.json

You can expose the report as an endpoint in your API. You will be able to analyse the integrity of your methods.

It will monitor fuctions and methods: 
their names, 
their descriptions, 
time it took for the last execution, 
average time of all combined execution, 
frequency of execution(How many times it has run), 
success rate, 
success ratio(percentage),
error generated by last execution, if any,
list of common errors being generated by the fuction and their frequency,
last date and time it was executed

Setup:
 Download or clone the script into your directory

 add... 
 
 from runtimestate import*
"""
__author__="Mushe Mukwevho"
__email__="mushemukwevho@gmail"

import json, time, datetime
from functools import wraps

RUNTIMEFILE=True  #It dumps the report into a json file

runtime_state={} #Output dictionary, contain the report
runtime_file=runtime_state

def runtime_method(func):
    
    """Runtime performance; for class methods. 'self' is required"""

    if RUNTIMEFILE:
        with open('data.json',) as json_file:
            try:
                data = json.load(json_file)
                runtime_file=data
            except:
                runtime_file=runtime_state

    @wraps(func)
    def wrapper(self,*args,**kwargs):
        name=func.__name__
        doc=func.__doc__
        filename="filename" #inspect.__file__(func)
        duration=""
        freq=0
        fail=0
        success=0
        lastdate=""
        error="none"
        #runtime_state={}
        
        freq+=1
        lastdate=str(datetime.datetime.now())
        start = time.time()

        try:
            func(self,*args,**kwargs)
            pass #run fuc

        except Exception as e:
            fail+=1
            error=str(e) #error assign

        else:
            success+=1
        end = time.time()
        duration=end-start
        success_ratio=str((success//freq)*100)+"%"
        error_info={}
        if error!='none':
            error_info[error]=error_info.get(error,0)+1

        if name not in runtime_state.keys():
            runtime_state[name]={"func_name":name,"doc":doc,"time":duration,"average_time":duration,"frequency":freq,"success":success,"fail":fail,"success_ratio":success_ratio,"error":error,"error_info":error_info,"last_date":lastdate}
            runtime_file=runtime_state
            if RUNTIMEFILE:
                with open('data.json', 'w') as outfile:
                    json.dump(runtime_file, outfile)
        
        else:
            runtime_state[name]["time"]=duration
            runtime_state[name]["frequency"]+=freq
            runtime_state[name]["average_time"]=(runtime_state[name]["average_time"]+runtime_state[name]["time"])/2
            runtime_state[name]["success"]+=success
            runtime_state[name]["success_ratio"]=str(round(((runtime_state[name]["success"]/runtime_state[name]["frequency"])*100),2))+"%"
            runtime_state[name]["fail"]+=fail
            runtime_state[name]["error"]=error
            runtime_state[name]["error_info"][error]=runtime_state[name]["error_info"].get(error,0)+1
            runtime_state[name]["last_date"]=lastdate

            #print(runtime_state) #check function
            runtime_file=runtime_state
            if RUNTIMEFILE:
                with open('data.json', 'w') as outfile:
                    json.dump(runtime_file, outfile)

    return wrapper

def runtime_function(func):
    """Runtime performance; for functions. 'self' is not required"""
    if RUNTIMEFILE:
        with open('data.json','w+') as json_file:
            try:
                data = json.load(json_file)
                runtime_file=data
            
            except:
                runtime_file=runtime_state

    @wraps(func)
    def wrapper(*args,**kwargs):
        name=func.__name__
        doc=func.__doc__
        filename="filename" #inspect.__file__(func)
        duration=""
        freq=0
        fail=0
        success=0
        lastdate=""
        error="none"
        #runtime_state={}
        
        freq+=1
        lastdate=str(datetime.datetime.now())
        start = time.time()

        try:
            func(*args,**kwargs)
            pass #run fuc

        except Exception as e:
            fail+=1
            error=str(e) #error assign

        else:
            success+=1
        end = time.time()
        duration=end-start
        success_ratio=str((success//freq)*100)+"%"
        error_info={}
        if error!='none':
            error_info[error]=error_info.get(error,0)+1

        if name not in runtime_state.keys():
            runtime_state[name]={"func_name":name,"doc":doc,"time":duration,"average_time":duration,"frequency":freq,"success":success,"fail":fail,"success_ratio":success_ratio,"error":error,"error_info":error_info,"last_date":lastdate}
            runtime_file=runtime_state
            if RUNTIMEFILE:
                with open('data.json', 'w') as outfile:
                    json.dump(runtime_file, outfile)       
        
        else:
            runtime_state[name]["time"]=duration
            runtime_state[name]["frequency"]+=freq
            runtime_state[name]["average_time"]=(runtime_state[name]["average_time"]+runtime_state[name]["time"])/2
            runtime_state[name]["success"]+=success
            runtime_state[name]["success_ratio"]=str(round(((runtime_state[name]["success"]/runtime_state[name]["frequency"])*100),2))+"%"
            runtime_state[name]["fail"]+=fail
            runtime_state[name]["error"]=error
            runtime_state[name]["error_info"][error]=runtime_state[name]["error_info"].get(error,0)+1
            runtime_state[name]["last_date"]=lastdate

            #print(runtime_state) #check function
            runtime_file=runtime_state

            if RUNTIMEFILE:
                with open('data.json', 'w') as outfile:
                    json.dump(runtime_file, outfile)
    return wrapper

