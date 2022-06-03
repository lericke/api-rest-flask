from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

args = reqparse.RequestParser()
args.add_argument('login', type=str, required=True, help="O campo 'Login' não pode ser deixado em branco")
args.add_argument('senha', type=str, required=True, help="O campo 'Senha' não pode ser deixado em branco")

class User(Resource): # /usuario/{user_id}

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required()
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

        dados = args.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {f"Message": "O login '{login}' ja existe."}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'Usuario criado com sucesso.'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = args.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(identity=user.user_id)
            return {'message': token_de_acesso}, 200
        return {'message': 'Usuario ou senha invalido'}, 401

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT Token Identifier
        BLACKLIST.add(jwt_id)
        return {'message': 'Logout feito com sucesso!'}
