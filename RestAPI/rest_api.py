from flask import Flask, jsonify, request
from datetime import datetime

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

commentaires = {}


@app.route("/", methods=["GET"])
def get():
    """
    ---
    get:
      description: Permet d'obtenir tous les commentaires présents.
      responses:
        '200':
          description: Requête valide
          content:
            application/json:
              schema: CommentaireList
    """
    return jsonify([elem for elem in commentaires.values()]), 200


@app.route("/<a_id>", methods=["GET"])
def get_arg(a_id):
    """
    ---
    get:
      description: Permet d'obtenir un commentaire en particulier avec son ID.
      parameters:
        - name: a_id
          in: uri
          type: integer
          required: true
          description: ID du commentaire à obtenir.
      responses:
        '200':
          description: Requête valide
          content:
            application/json:
              schema: Commentaire
        '400':
          description: Requête non valide, Mal formatté
          content:
            application/json:
              schema: Reponse
        '404':
          description: Requête non valide, ID inexistant
          content:
            application/json:
              schema: Reponse
    """
    try:
        val = int(a_id)
    except:
        return "Bad id format. Expected integer.", 400

    if val in commentaires:
        return jsonify(commentaires[val])
    else:
        return "Id does not exist.", 404


@app.route("/", methods=["POST"])
def post():
    """
    ---
    post:
      description: Permet de créer un commentaire.
      parameters:
        - name: auteur
          in: json body
          type: string
          required: false
          description: Auteur du commentaire
        - name: dateCreation
          in: json body
          type: date
          required: false
          description: Date du commentaire (ex. 2022/03/01 10:00:00)
        - name: id
          in: json body
          type: int
          required: false
          description: ID du commentaire (auto-incrémenté si non spécifié)
        - name: titre
          in: json body
          type: string
          required: false
          description: Titre du commentaire
      responses:
        '201':
          description: Requête valide
          content:
            application/json:
              schema: Reponse
        '400':
          description: Requête non valide, champs invalides, date mal formattée...
          content:
            application/json:
              schema: Reponse
    """
    inp_data = request.get_json(force=True)
    code, data = parse_commentaire(commentaires, inp_data)

    if code == 200:
        if data["id"] in commentaires:
            return "Id already exists", 400

        commentaires[data["id"]] = data

        return f"Comment # {data['id']} was created", 201

    else:
        return "Invalid comment", 400


@app.route("/", methods=["PUT"])
def update():
    """
    ---
    put:
      description: Permet de mettre un jour un commentaire.
      parameters:
        - name: auteur
          in: json body
          type: string
          required: false
          description: Auteur du commentaire
        - name: dateCreation
          in: json body
          type: date
          required: false
          description: Date du commentaire (ex. 2022/03/01 10:00:00)
        - name: id
          in: json body
          type: int
          required: true
          description: ID du commentaire à mettre à jour
        - name: titre
          in: json body
          type: string
          required: false
          description: Titre du commentaire
      responses:
        '200':
          description: Requête valide
          content:
            application/json:
              schema: Reponse
        '400':
          description: Requête non valide, champs invalides, date mal formatté, ID inconnu...
          content:
            application/json:
              schema: Reponse
    """
    inp_data = request.get_json(force=True)
    code, data = parse_commentaire(commentaires, inp_data)  # vérif commentaire

    if code == 200:
        if "id" in inp_data:
            if inp_data["id"] not in commentaires:
                return "Id does not exists", 404
            else:
                commentaires[inp_data["id"]] = data
                return f"Comment # {inp_data['id']} was updated.", 200
        else:
            return (
                "No id specified",
                400,
            )  # choix de renvoyer une erreur au lieu d'insérer
    else:
        return "Invalid comment", 400


@app.route("/<a_id>", methods=["DELETE"])
def delete_arg(a_id):
    """
    ---
    delete:
      description: Permet de supprimer un commentaire.
      parameters:
        - name: a_id
          in: uri
          type: integer
          required: true
          description: ID du commentaire à supprimer.
      responses:
        '200':
          description: Requête valide
          content:
            application/json:
              schema: Commentaire
        '400':
          description: Requête non valide, Mal formatté
          content:
            application/json:
              schema: Reponse
        '404':
          description: Requête non valide, ID inexistant
          content:
            application/json:
              schema: Reponse
    """
    try:
        val = int(a_id)
    except:
        return "Bad Id format", 400

    if val in commentaires:
        del commentaires[val]
        return f"Comment # {val}  was deleted.", 200
    else:
        return "Id does not exist.", 404


##################################################################################
# CREATION SWAGGER
# APISpec
spec = APISpec(
    title="TP3 WSDL",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Schema definitions
class Commentaire(Schema):
    auteur = fields.String(description="Auteur du commentaire")
    dateCreation = fields.DateTime(description="Date du commentaire")
    id = fields.Int(description="ID du commentaire")
    titre = fields.Int(description="Titre du commentaire")


class CommentaireList(Schema):
    commentaires = fields.List(fields.Nested(Commentaire))


class Reponse(Schema):
    message = fields.String(
        description="Message de réponse à la requête", required=True
    )


with app.test_request_context():
    # register all swagger documented functions here
    for fn_name in app.view_functions:
        if fn_name == "static":
            continue
        print(f"Loading swagger docs for function: {fn_name}")
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


@app.route("/swagger.json")
def create_swagger_spec():
    return jsonify(spec.to_dict())


SWAGGER_URL = "/docs"
API_URL = "/swagger.json"

# Call factory function to create our blueprint
swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "TP3 WSDL"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
# FIN CREATION SWAGGER
##################################################################################


def parse_commentaire(commentaires, json_inp):

    keys = ["auteur", "dateCreation", "id", "titre"]

    for key in json_inp.keys():
        if key not in keys:
            return 400, None

    data = {"auteur": "Anonyme", "dateCreation": "", "id": "", "titre": "Inconnu"}

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


if __name__ == "__main__":
    app.run()

