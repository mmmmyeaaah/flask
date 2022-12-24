from flask.views import MethodView
from auth import hash_password
from database import UserModel, Session, AdvertisementModel
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from errors import ApiException
from validate import validate, CreateUserSchema, CreateAdvertisementSchema


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            if user is None:
                raise ApiException(404, 'User not found')
            return jsonify({
                'id': user.id,
                'email': user.email
            })

    def post(self):
        user_data = validate(request.json, CreateUserSchema)
        user_data['password'] = hash_password(user_data['password'])
        with Session() as session:
            new_user = UserModel(**user_data)
            session.add(new_user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, 'email is busy')
            return jsonify({'id': new_user.id, 'email': new_user.email})

    def patch(self, user_id: int):
        user_data = request.json
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            for field, value in user_data.items():
                setattr(user, field, value)
            session.add(user)
            try:
                session.commit()
            except IntegrityError:
                raise ApiException(400, 'email is busy')
            return jsonify({'id': user.id, 'email': user.email})

    def delete(self, user_id: int):
        with Session() as session:
            user = session.query(UserModel).get(user_id)
            session.delete(user)
            session.commit()
            return jsonify({'status': 'deleted'})


class AdvertisementView(MethodView):

    def get(self, advertisement_id: int):
        with Session() as session:
            advertisement = session.query(AdvertisementModel).get(advertisement_id)
            if advertisement is None:
                raise ApiException(404, 'advertisement not found')
            return jsonify({'id': advertisement.id,
                           'tittle': advertisement.title,
                            'description': advertisement.description,
                            'user_id': advertisement.user_id
                            })

    def post(self):
        advertisement_data = validate(request.json, CreateAdvertisementSchema)
        with Session() as session:
            new_advertisement = AdvertisementModel(**advertisement_data)
            session.add(new_advertisement)
            session.commit()
            return jsonify({
                'id': new_advertisement.id,
                'title': new_advertisement.title,
                'description': new_advertisement.description,
                'user_id': new_advertisement.user_id
            })

    def patch(self, advertisement_id: int):
        advertisement_data = request.json
        with Session() as session:
            advertisement = session.query(AdvertisementModel).get(advertisement_id)
            for field, value in advertisement_data.items():
                setattr(advertisement, field, value)
            session.add(advertisement)
            session.commit()
            return jsonify({
                'id': advertisement.id,
                'title': advertisement.title,
                'description': advertisement.description,
                'user_id': advertisement.user_id
            })

    def delete(self, advertisement_id: int):
        with Session() as session:
            advertisement = session.query(AdvertisementModel).get(advertisement_id)
            session.delete(advertisement)
            session.commit()
            return jsonify({
                'status': 'deleted'
            })