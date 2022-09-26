#Crearemos un restapi en python para roblox, La api lo que hara es descargar una imagen con la url y subirla a roblox como id y retornar el id del decal


import imp
import requests
import os
from bs4 import BeautifulSoup
from time import sleep
import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#from nudenet import NudeClassifier
#import cv2
import sys

#numsxd = NudeClassifier()

class DecalClass():
    def __init__(self, cookie, location, name):
        self.goose = requests.Session()
        self.goose.cookies.update({
            '.ROBLOSECURITY': cookie #set .ROBLOSECURITY cookie for authentication
        })
        self.goose.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134", #might as well use a User Agent
        })
        self.location = location
        self.name = name
    def getToken(self): #get verification token function
        homeurl= 'https://www.roblox.com/build/upload' #this is the upload endpoint
        response = self.goose.get(homeurl, verify=False)
        try:
            soup = BeautifulSoup(response.text, "lxml")
            veri = soup.find("input", {"name" : "__RequestVerificationToken"}).attrs["value"] #parse out the verification token from the HTML
        except NameError:
            print(NameError)
            return False
        return veri
    def upload(self):
        files = {'file': ('lol.png', open(self.location, 'rb'), 'image/png')} #add our image as files data
        data = {
            '__RequestVerificationToken': self.getToken(),
            'assetTypeId': '13', #we use assetTypeId '13' because 13 is the id for Decals
            'isOggUploadEnabled': 'True',
            'isTgaUploadEnabled': 'True',
            
            'onVerificationPage': "False",
            "captchaEnabled": "True",
            'name': self.name
        }
        try:
            response = self.goose.post('https://www.roblox.com/build/upload', files=files, data=data) #make the request
        except:
            print("error is making request")
            
ROBLOXSECID = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_5CE23EA58228E03BA615BEECC5AC145184C69187EEC622044908324E1B0EF235A12726CDA81EC1B475C5E6ED990553EA0FE333D04D074885DACAB0BBA555C06809F4A7F98D04A6714082A0466E95F31596CF0CB34FE95691BB900767F2B4FFA4BEEB01495485A80C301412DD940DE05BBB3224B15285C69F7D6BA3FA2FE25A37EC3E9A74BB4C65B055CF2AFEA07C83762E91F8706321B075F23DF30AEF4DFE7513E24BFB7D2B8523C5372B72471255D75EEE63943FC45462AB1AA6B06E30F642A08638AF7470F2C9A9721E2FFAE461951DCB1A12D926591433CA787ED3CE02DAA1F51DD8BE2427B02ABA0DB52C283701AED5063C13C085B3CC8D9841AACC5A307F005359EC6C5673B1B3D080FD249A903B14BA4007524B6482FAA7C883D8C67D8DCC0FBB8720B9852773EE338FB355820FCED82C01B4C987F62DC89884BA290AFED19E9460B8C0CE4E34CE55303859E8A9E475407A02A68B327D287C7203BD73C253F8B0248F3925761A3B357AB7D3054E6666AA"

def DescargarImagen(url):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open("lol.png", 'wb') as f:
                f.write(r.content)


        return True
    except:
        return     


#importamos Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Hello World"

@app.route('/upload', methods=['GET'])
def upload():
    url = request.args.get('url')
    name = request.args.get('name')
    if DescargarImagen(url):
        #quetanseguro = numsxd.classify("lol.png")

        #print(quetanseguro["lol.png"]["safe"])
        


        #if quetanseguro['lol.png']['safe'] > 0.5:
        decal = DecalClass(ROBLOXSECID, "lol.png", name)
        decal.upload()
        
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(debug=True)
