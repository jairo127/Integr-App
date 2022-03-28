# coding: utf-8
from datetime import datetime


def parse_commentaire(commentaires, json_inp):

    keys = ["auteur", "dateCreation", "id", "titre"]

    for key in json_inp.keys():
        if key not in keys:
            return 400, None

    data = {"auteur": "", "dateCreation": "", "id": "", "titre": ""}

    if "auteur" in json_inp.keys():
        data["auteur"] = json_inp["auteur"]  # ajouter #str() ici ???

    if "titre" in json_inp.keys():
        data["titre"] = json_inp["titre"]

    if "id" in json_inp.keys():  # Ne vérifie pas si l'id est déjà dans commentaires
        if type(json_inp["id"]) != int:
            return 400, None
        data["id"] = json_inp["id"]
    else:
        data["id"] = gen_id(commentaires)

    # date manquante
    if "dateCreation" in json_inp:
        try:
            data["dateCreation"] = datetime.strptime(
                json_inp["dateCreation"], "%Y/%m/%d %H:%M:%S"
            )
        except ValueError:
            return 400, None
    else:
        data["dateCreation"] = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

    return 200, data


def gen_id(commentaires: dict) -> int:
    try:
        max_v = max(commentaires.keys())
    except:
        max_v = -1
    return max_v + 1

