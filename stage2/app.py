from flask import Flask,jsonify
from flask_restful import Api

from flask_jwt_extended import JWTManager
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from resources.user import UserRegister,User,UserLogin,TokenRefresh

app = Flask(__name__)

app.secret_key = 'this must be a secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(app)
jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):

    if identity == 1:
        return {'is_admin':True}
    return {'is_admin':False}


@jwt.expired_token_loader
def token_expired_callback():
    return jsonify({'message':'Token is expired.',
                    'error':'token_expired'
                  })

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({'message':'Provided token is invalid',
                    'error':'invalid_token'
                  })

@jwt.needs_fresh_token_loader
def fresh_token_callback():
    return jsonify({'message':'Fresh token is required.',
                    'error':'fresh_token_required'
                  })

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({'message':'Token is missing.',
                    'error':'unauthorized_token'
                  })

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({'message':'Token is revoked.',
                    'error':'revoked_token'
                  })


api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
api.add_resource(TokenRefresh,'/refresh')


@app.before_first_request
def create_table():
    db.create_all()



if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True)
