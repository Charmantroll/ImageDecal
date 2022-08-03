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
            
ROBLOXSECID = "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_5032B9645D624E69615E3C67C76170ADEA77F72008D4C6304208CDB0973BEC912FBEEF1940AEE78F6353101AF32C0C1D3D68678D3F9D92E272ADCA2CE54BC84DAB8B9C8B3EE42FBC3E63268197E9EBEA32AD7951902F1A126ACCF8C825B3EF59931D1F5B0D1E406FF3C5D34B0AB70CB0958AE89DA769C464F86A5132CCFA103C1B8F2CE530B54101EC4591A71E03BCF274BA6ECC4F2E180F31A12DFA1367211D5B37AD2479B7807C90C00D2D1980877BD833287B877D7AFA6D0EA273296D062F748CB19DEB589F7715BBEB9C02CE9E9989F34A5E814096E999DF15231DD157EDC22E18E9F00DEDD6BDD8AC80A0D627AB2ED029AF39072C18C6497546C349AA6C13677B6DB58D8D0D9BA71FD4F588657D1CC3B886D7E85CDF3604336A2F45CBADCAAC03318E96D90A45A2F84B55EA6104D7C699FB0DFCC4B0E2D9F2AD027D827D5A38F75ECD9318A188F5D6C5B197D3331421EDCE819A4037A3828763F3F891A90DE58D9CFBAE3F424A4C216778760B18C41B6EA2"
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
