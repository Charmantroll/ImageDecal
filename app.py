#Crearemos un restapi en python para roblox, La api lo que hara es descargar una imagen con la url y subirla a roblox como id y retornar el id del decal


import imp
import requests
import os
from bs4 import BeautifulSoup
from time import sleep
import urllib3; urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from nudenet import NudeClassifier
import cv2
import sys

numsxd = NudeClassifier()

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
            
ROBLOXSECID = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_7F2D6455F0C5C309320EF82B365E600ACCFD210345EC53E948FEE52D448BED939932080CD0017C50693A3E35F61F11B3295F71F0A8EC90836A72D616F1EB2D8E83A3C20D0E7328F03DC300C59CE948CB7B918170ED32A714B20236BC7E014FBF90839310F2415F53FCB25D1B6E415095906D30F395227908A13B0D1CC0095D0A8A96A0E40D99543132BF81D6CC540E1E7FD7D911FC373057E59A7CFE84F7346EAE03999550868460AA03450EA96FD95DD4A028AC19F5D7EB3F6927AB01B12D2B163EF07088ADE50689B546C185E484AE6EA50AB19913AD52077F4D66D86C019CED5E70FB7FBEE10C521ED899F1BD9373BDB57DD97806027614B6D4DA13BF245A7CBFC7E6D75A1B1DA4FCC2FB8B320071C1F6ADFEB367A2E6B1ABC66C0EAC4FCFA9E2CC7BB7B22D02DBEC2C4E8F969F3C3569AFC51FC81A6BF95820C0A690B3B62A59B70DB11EAF202429EE35531D27EF184D21AA679A443352DF23CD0F5464BECFA73DCD74936A3DE8AB4AB95CF34279BE5AA975"

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
        quetanseguro = numsxd.classify("lol.png")

        print(quetanseguro["lol.png"]["safe"])
        


        if quetanseguro['lol.png']['safe'] > 0.5:
            decal = DecalClass(ROBLOXSECID, "lol.png", name)
            decal.upload()
        
            return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"})

if __name__ == '__main__':
    app.run(debug=True)