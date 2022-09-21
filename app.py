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
            
ROBLOXSECID = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_965BD299E46EEFFCCF67B8EBAFB52469F25FA8DBF1B091225D90EA05314BF2202A3C38377960475CBAEBB8BF0A918E350029FE85F0A19ACEA87D97F85053D59DD001DB8DFF0773810F53987C0783DDBE51AD370BC7F2C056AC67994BB914E39DDF03424F5A8B7E4EB5C4BA3FBE5CC86A5026FC9EEED84B15019C8B7D9C1BC3DFB4BDDA8BFC8AE3797CB43ADE7BE999FDC930F2015DC3155EB294072A75C06563F7A9C756CAEE96E28395ED7EB1412FB47C7B488EDE2AEA313A53804D6CE5DCAE5F8922C1920F89F2C964222452AE5EE2F3A2A36FB6FD295A7C4075438AD4EBE7CE41A0B0A57F1E236020FCB65ED2B1C76967E5F5EE39633DA542489D1B72AC86AF74BC87ACD6EC09052285D71E9B74DA3DB070B4DA6B11E2A22DB803E66E84C39C32CDAB36B546EA17D2D76F54C21B53410FD39930084B72ACB5BB5A1239EC23C834B347FA0BF4EC541C48299E775889FF0CA3B6D2AD45E364038535C43D9617799E0A015F25A39B831573A3E96234AF67FF60966EB70D15E108A255EF46991F8335458C"

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
