import requests
#import json
from xmlrpc import *
import http.client
from commandeAPI import *
import time


bool=parserDemande()

if bool:
    with open('XMLAPI2.xml', 'r') as file:
        lines = file.readlines()

    page = ""
    request = open("XMLAPI2.xml","rb").read()
    tour = 0
    param = "".join(lines)
    
    try:
        c = bcolors
        response = requests.post("https://apisandbox4.or2.clust2.tbs-internet.net:1443/api-operations.php", data=request)
        rootElement = ET.fromstring(response.text)
        messageRetour = rootElement.findall(".//member[name='messageReponse']//string")[0].text 
        commande = rootElement.findall(".//member[name='refTBS']//int")[0].text 
        print((c.WARNING+"[*]:"+c.ENDC+c.OKGREEN+" {0}"+c.ENDC).format(messageRetour))
        print((c.WARNING+"[*]:"+c.ENDC+ " Numéro de la commande="+c.OKGREEN+"{0}"+c.ENDC).format(commande)) 
        
    except TimeoutError:
        print("TO")
    except ConnectionError:
        print("CO")
    except Exception as ex:
        print(ex)
        print(type(ex).__name__, ex.args)
        
     
