from django.db import models
import re
from django.http.response import JsonResponse
from rest_framework import status
    
MODELS = (("Lightweight", "Lightweight"), ("Middleweight", "Middleweight"), ("Cruiserweight", "Cruiserweight"),
    ("Heavyweight", "Heavyweight"))
STATE =  (("IDLE", "IDLE"), ("LOADING", "LOADING"), ("LOADED", "LOADED"),
    ("DELIVERING", "DELIVERING"), ("DELIVERED", "DELIVERED"), ("RETURNING", "RETURNING"))




class Producto(models.Model):
    

    nombre = models.CharField("Name", max_length=50, blank=False, null=False)
    precio = models.FloatField("Weight")
    descripcion = models.CharField("Code", max_length=100, blank=False, null=False)
    image = models.CharField("Image", max_length=10000000,blank=False, null=False)
    
    def __nuevo__(nombre, precio, descripcion, image):
        aux = Producto()
        aux.nombre = nombre
        aux.precio = precio
        aux.descripcion = descripcion
        aux.image = image
        aux.save()

#Producto.__new__ ("frijoles", 300, "Granos", "XXXXXXXXXXXXXXXXXXXXX")      

class Medication(models.Model):
    

    name = models.CharField("Name", max_length=50, blank=False, null=False)
    weight = models.FloatField("Weight")
    code = models.CharField("Code", max_length=100, blank=False, null=False)
    image = models.CharField("Image", max_length=10000000,blank=False, null=False)

    def __validate__(self):
        exLetterNumberScriptUndersocre = "^[0-9a-zA-Z_-]*$"
        exLetterUpNumberUnderscore = "^[0-9A-Z_]*$"
        valid = True
        messageError = ""
        if re.match(exLetterNumberScriptUndersocre, self.pk["name"]) == None:
            valid = False
            messageError += " The medications name allowed only letters, numbers, '-' and '_'."
        if re.match(exLetterUpNumberUnderscore, self.pk["code"]) == None:
            valid = False
            messageError += " The code allowed only upper case letters, underscore and numbers."
        if valid:
            return JsonResponse({"data": "Data is OK"}, status=status.HTTP_200_OK)
        else:
             return  JsonResponse({"error":messageError}, status=status.HTTP_400_BAD_REQUEST)

class Drone(models.Model):
    
    serialNumber = models.CharField("Serial number", unique=True, max_length=100, blank=False, null=False)
    model = models.CharField("Model", max_length=50, choices=MODELS)
    medicationLoad = models.ManyToManyField(Medication, blank=True)
    weightLimit = models.FloatField("Weigh limit", blank=True, null=True)
    battery = models.IntegerField("Battery", blank=False, null=False)
    state = models.CharField("State",default="IDLE", max_length=50, choices=STATE)
    
    def __validate__(self):
        exLen = "^(.){1,100}$"
        valid = True
        messageError = ""
        
        if re.match(exLen, self.pk["serialNumber"].strip()) == None:
            messageError += " The serial number only permits 100 characters max and can't be empty."
            valid = False
        if self.pk["weightLimit"] > 500 or self.pk["weightLimit"] < 0:
            messageError += f" The actual weigh is {self.pk['weightLimit']} and weight can't be bigger than 500gr or smaller than 0."
            valid = False
        if self.pk["battery"] > 100 or self.pk["battery"] < 0:
            messageError += " The battery percent can't be bigger than 100 or smaller than 0."
            valid = False
        if not self.pk["model"] in ["Lightweight", "Middleweight", "Cruiserweight", "Heavyweight"]:
            messageError += " Model most be one of the next four models: Lightweight, Middleweight, Cruiserweight and Heavyweight."
            valid = False
        if not self.pk["state"] in ["IDLE", "LOADING", "LOADED", "DELIVERING", "DELIVERED", "RETURNING"]:
            messageError += " State most be one of the next six models: IDLE, LOADING, LOADED, DELIVERING, DELIVERED and RETURNING."
            valid = False
        if  self.pk["state"] == "LOADING" and self.pk["battery"] < 25:
            messageError += " Drones can't be LOADING if the battery level is below 25%."
            valid = False
        if  calculateWeight(self.pk["medicationLoad"]) > self.pk["weightLimit"]:
            messageError += f" Total weight most be under weidhtLimit({self.pk['weightLimit']}) ."
            valid = False
        if valid:
            return JsonResponse({"data": "Data is OK"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": messageError}, status=status.HTTP_400_BAD_REQUEST)


def calculateWeight(medicationsIds):
    weight = 0
    for id in medicationsIds:
        weight += Medication.objects.get(id=id).weight
    return weight
   
