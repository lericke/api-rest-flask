from flask_restful import Resource, reqparse
from models.hotel import HotelModel

lista_hoteis = [
    {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
    },
    {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.34,
        'cidade': 'São Paulo'
    }
]

class Hoteis(Resource):
    def get(self):
        return {"Lista de hoteis": lista_hoteis}

class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument('nome')
    args.add_argument('estrelas')
    args.add_argument('diaria')
    args.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in lista_hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):

        dados = Hotel.args.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        lista_hoteis.append(novo_hotel)
        return novo_hotel, 201

    def put(self, hotel_id):

        dados = Hotel.args.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return hotel, 200
        lista_hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global lista_hoteis
        lista_hoteis = [hotel for hotel in lista_hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}