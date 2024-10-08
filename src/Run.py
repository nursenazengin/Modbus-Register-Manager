from flask import Flask
from accessPointService import accessPointBlueprint
from mainService import mainBlueprint
from postgreService.databaseService import app as db_app

app = Flask(__name__)

# Blueprint'leri kaydet
app.register_blueprint(accessPointBlueprint)
app.register_blueprint(mainBlueprint)


if __name__ == '__main__':
    app.run(port=5000, debug=True)  
