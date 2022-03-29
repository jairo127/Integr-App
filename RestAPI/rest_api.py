from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

# apispec via OpenAPI
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from flask_swagger_ui import get_swaggerui_blueprint

import db_connection as db

app = Flask(__name__)
CORS(app)

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
    commentaires = db.get_all_comments(connection)
    return jsonify([elem for elem in commentaires.values()]), 200

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
        - name: contenu
          in: json body
          type: string
          required: false
          description: Contenu du commentaire
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
    code, data = parse_commentaire(inp_data)

    if code == 200:
      inserted = db.insert_comment(connection, data)

      if inserted:
        return {"response": f"Comment # {data['id']} was created"}, 201
      else:
        return {"response": "Id already exists"}, 400

    else:
        return {"response": "Invalid comment"}, 400

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
        return {"response": "Bad Id format"}, 400

    deleted = db.delete_comment(connection, val)

    if deleted:
      return {"response": f"Comment # {val} was deleted."}, 200
    else:
      return {"response": "Id does not exist."}, 404

##################################################################################
# CREATION SWAGGER
# APISpec
spec = APISpec(
    title="ISIBlog API",
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
    SWAGGER_URL, API_URL, config={"app_name": "ISIBlog API Documentation"}
)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
# FIN CREATION SWAGGER
##################################################################################


def parse_commentaire(json_inp):

    keys = ["auteur", "dateCreation", "id", "titre", "contenu"]

    for key in json_inp.keys():
        if key not in keys:
            return 400, None

    data = {"auteur": "Anonyme", "dateCreation": "", "id": "", "titre": "Inconnu", "contenu": "(Vide)"}

    if "auteur" in json_inp.keys():
        data["auteur"] = json_inp["auteur"]  # ajouter #str() ici ???

    if "titre" in json_inp.keys():
        data["titre"] = json_inp["titre"]

    if "contenu" in json_inp.keys():
        data["contenu"] = json_inp["contenu"]

    if "id" in json_inp.keys():  # Ne vérifie pas si l'id est déjà dans commentaires
        if type(json_inp["id"]) != int:
            return 400, None
        data["id"] = json_inp["id"]
    else:
        data["id"] = int(db.get_last_id(connection))

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

if __name__ == "__main__":
    connection = db.mysql_connect()
    app.run()

