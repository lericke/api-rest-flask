from flask_restful import Resource, reqparse
from models.usuario import UserModel

class User(Resource): # /usuario/{user_id}

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
            return {'message': "Usuario Deletado"}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource): # /cadastro

    def post(self):
        args = reqparse.RequestParser()
        args.add_argument('login', type=str, required=True, help="O campo 'Login' não pode ser deixado em branco")
        args.add_argument('senha', type=str, required=True, help="O campo 'Senha' não pode ser deixado em branco")
        dados = args.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {f"Message": "O login '{login}' ja existe."}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Usuario criado com sucesso.'}, 201