import json
from gtts import gTTS
import os
from geopy.geocoders import Nominatim

def charger_donnees(nom_fichier):
    with open(nom_fichier, 'r') as fichier:
        donnees = json.load(fichier)
    return donnees

def obtenir_reponse_chatbot(requete_utilisateur, donnees):
    if "spd" in requete_utilisateur:
        vitesse = donnees["SPD"]
        temps = donnees["time"]
        date = temps.split("T")[0]
        return f"La vitesse du véhicule était de {vitesse} km/h à la date {date}."
    elif "batterie" in requete_utilisateur:
        attributs = json.loads(donnees["ATTRIBUTES"])
        niveau_batterie = attributs["batteryLevel"]
        temps = donnees["time"]
        date = temps.split("T")[0]
        return f"Le niveau de batterie était de {niveau_batterie} pour cent à la date {date}."
    elif "ignition" in requete_utilisateur:
        attributs = json.loads(donnees["ATTRIBUTES"])
        etat_allumage = "allumé" if attributs["ignition"] else "éteint"
        temps = donnees["time"]
        date = temps.split("T")[0]
        return f"L'allumage était {etat_allumage} à la date {date}."
    elif "position" in requete_utilisateur:
        latitude, longitude = obtenir_position(donnees)
        adresse = obtenir_adresse(latitude, longitude)
        return f"La position actuelle du véhicule est : {adresse}."
    else:
        return "Désolé, je ne peux pas répondre à cette requête."

def texte_en_discours(texte):
    tts = gTTS(text=texte, lang='fr')
    tts.save("reponse.mp3")
    os.system("start reponse.mp3")

def obtenir_position(donnees):
    latitude = donnees["LAT"]
    longitude = donnees["LON"]
    return latitude, longitude

def obtenir_adresse(latitude, longitude):
    geolocator = Nominatim(user_agent="chatbot_reverse_geocoding")
    location = geolocator.reverse((latitude, longitude), language='fr')
    return location.address if location else "Adresse non trouvée"

def principal():
    print("Bienvenue sur votre interface de chatbot !")

    données = charger_donnees("assets/cardata.json")

    first_time = True

    while True:
        if first_time:
            print("Choisissez parmi les options suivantes :")
            print("1. Vitesse du véhicule")
            print("2. Niveau de batterie")
            print("3. État de l'allumage")
            print("4. Position du véhicule")
            first_time = False

        choix_utilisateur = input("Votre choix (1-4) : ")

        if choix_utilisateur == "1":
            requete_utilisateur = "spd"
        elif choix_utilisateur == "2":
            requete_utilisateur = "batterie"
        elif choix_utilisateur == "3":
            requete_utilisateur = "ignition"
        elif choix_utilisateur == "4":
            requete_utilisateur = "position"
        else:
            print("Choix invalide. Veuillez choisir un nombre entre 1 et 4.")
            continue

        reponse_chatbot = obtenir_reponse_chatbot(requete_utilisateur.lower(), données[0])
        print("Chatbot :", reponse_chatbot)
        texte_en_discours(reponse_chatbot)


if __name__ == "__main__":
    principal()
