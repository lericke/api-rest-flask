from flask_restful import Resource
from models.usuario import UserModel

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': "Ocorreu um interno ao tentar deletar o Usuario."}, 500
        return {'message': 'User not found.'}, 404