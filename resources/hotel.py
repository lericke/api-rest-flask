from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return {"Lista de hoteis": [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('nome', type=str, required=True, help="O campo nome é requirido")
    args.add_argument('estrelas', type=str, required=True, help="O campo estrelas é requirido")
    args.add_argument('diaria')
    args.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404

    @jwt_required()
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'Message': f"O hotel: '{hotel_id}' ja existe"}, 400
        dados = Hotel.args.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        try:
            hotel_objeto.save_hotel()
        except:
            return {"message": "Ocorreu um erro interno ao tentar salvar o hotel"}, 500
        return hotel_objeto.json()

    @jwt_required()
    def put(self, hotel_id):

        dados = Hotel.args.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200

        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return {"message": "Ocorreu um erro interno ao tentar salvar o hotel"}, 500
        return hotel_encontrado.json(), 201

    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': "Ocorreu um interno ao tentar deletar o Hotel"}, 500
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}, 404