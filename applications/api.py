# from flask_restful import Resource, Api
# from applications.database import db
# from applications.models import *
# from flask import current_app as app
#
# api = Api(app)
#
#
# def post(username):
#     """
#     Create a user
#     ---
#     """
#     # userinfo = db.session.query(User).filter(User.username == username).first()
#     #
#     # if userinfo:
#     #     return {"user_id": userinfo.user_id, "username": userinfo.username}
#     # else:
#     #     return {}, 404
#
#
# class UserAPI(Resource):
#     def get(self, username):
#         """
#         Get a user
#         ---
#         """
#         # userinfo = db.session.query(User).filter(User.username == username).first()
#         #
#         # if userinfo:
#         #     return {"user_id": userinfo.user_id, "username": userinfo.username}
#         # else:
#         #     return {}, 404
#
#     def put(self):
#         """
#         Update a user
#         ---
#         """
#
#     def delete(self):
#         """
#         Delete a user
#         ---
#         """
#
#
# # api.add_resource(UserAPI, '/profile/<string:username>')
