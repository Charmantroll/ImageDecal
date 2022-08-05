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
            
ROBLOXSECID = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_A69CECBF652EABBDF22B27D3A4D9A60A5F4F1D772153A2DE911243D42545743444F2DB47107422A2754B77037FE7F6B64C2F76606A8CBAE754D0E476D26EA617A22A329F2C6AD5EFA94AE7346A871810FBCE5A64809E75B8D5EB641196311AA13B1DD1A3C1F7485FBCE619E5A1055045FF7208CE56ACE259AF60F693A11C6F17F21025EB3149532CD7B896C9532513C3DD76C2D51D1A02922B83AFE6063A821706F0BF4013812B94DF32B55916EFD2A3319525075F208EE61880850526CCF0951537E3E35D045EA7195FDBB60F79AEB40119B994D2BF491E2E1A01C4DB11F8486C397F32EC9DE389BC6AC00956EF5455502595C9FF69384F2A83BCC27E501A00396221FE80D7CF4EF9190BD031037737DD01C85837DA59E007563C032E25067EC9A6FA75956D20893CC9F7E5DA1A3557BEE75EE2183AC8798A085F5664A0D41B6882196322ACBE32AA5C18B999379486BEDBAEB81238E5EE3BAD5AC22DD9A12491F794AEF3B245E6D6735B5815315A9CD127A417"

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
