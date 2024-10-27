#import promptAutomation
import pickle
from promptAutomation import primary, checkAnswers
from typing import Union
from fastapi import FastAPI, HTTPException 
from pydantic import BaseModel 
app = FastAPI()
try:
    with open('apikey.txt', 'rb') as file:
       apiKeyGlobal = pickle.load(file)
except:
    print("Warning: The API key has not been set. Make a PUT request in the form /SETAPIKEY/<apikey>, and reset the program.")
class URL(BaseModel):
    #used to pass the url from the front end 
    urlString: str
    userTopic: str 
class returnSummary:
    def __init__(self):
        self.data = str
initSummary = returnSummary()
@app.post("/url")
def create_summary(item: URL):
    print("Got URL:: " + item.urlString)
    rtval = primary(item.urlString, apiKeyGlobal, item.userTopic)
    #print (rtval) 
    returnSummary.data=rtval
    print(returnSummary.data)
@app.get("/resp/{param1}/{param2}/{param3}")
def getAnswer(param1: str, param2: str, param3: str):
   return checkAnswers(apiKeyGlobal, returnSummary.data, param1, param2, param3)
@app.post("/SETAPIKEY/{apikey}")
def setapikey(apikey: str):
    with open('apikey.txt', 'wb') as file:
        pickle.dump(apikey, file)
        apiKeyGlobal = apikey


    


