from flask_restful import Api, Resource, reqparse
from task import send_mail, send_csv_mail
from models import db, User, Theatre, Show, Role, Booking
from flask_jwt_extended import jwt_required
from datetime import datetime

# Parser for request data
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
user_parser.add_argument('email', type=str, required=True, help='Email cannot be blank')
user_parser.add_argument('password', type=str, required=True, help='Password cannot be blank')
theatre_parser = reqparse.RequestParser()
theatre_parser.add_argument('name', type=str, required=True, help='Theatre name cannot be blank')
theatre_parser.add_argument('location', type=str, required=True, help='Theatre location cannot be blank')
theatre_parser.add_argument('capacity', type=int, required=True, help='Theatre capacity cannot be blank')
show_parser = reqparse.RequestParser()
show_parser.add_argument('name', type=str, required=True, help='Show name cannot be blank')
show_parser.add_argument('rating', type=float, required=True, help='Show rating cannot be blank')
show_parser.add_argument('ticket_price', type=float, required=True, help='Show ticket price cannot be blank')
show_parser.add_argument('start_time', type=str, required=True, help='Show start time cannot be blank')
show_parser.add_argument('end_time', type=str, required=True, help='Show end time cannot be blank')
show_parser.add_argument('theatre_id', type=int, required=True, help='Theatre ID cannot be blank')
booking_parser = reqparse.RequestParser()
booking_parser.add_argument('show_id', type=int, required=False, help='Show ID cannot be blank')
booking_parser.add_argument('user_id', type=int, required=False, help='User ID cannot be blank')
booking_parser.add_argument('seats', type=int, required=True, help='Number of seats cannot be blank')





# User resource for CRUD operations
class UserResource(Resource):
    # @jwt_required
    def get(self, user_id):
        user = User.query.get(user_id)
        roles = [role.name for role in user.roles]
        if user:
            return {'id': user.id, 'username': user.username, 'email': user.email, 'role':roles}, 200
        return {'message': 'User not found'}, 404

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            args = user_parser.parse_args()
            user.username = args['username']
            user.email = args['email']
            user.password = args['password']
            db.session.commit()
            return {'message': 'User updated successfully'}, 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        return {'message': 'User not found'}, 404

# UserList resource for listing all users and creating new users
class UserListResource(Resource):
    # @jwt_required
    def get(self):
        users = User.query.all()
        user_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return user_list, 200

    def post(self):
        # try:
        args = user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user:
            return {'message': 'User already exists'}, 400
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            user_role = Role(name='user')
            db.session.add(user_role)
            db.session.commit()
        new_user = User(username=args['username'],
                        email=args['email'],
                        password=args['password'],
        )
        new_user.roles.append(user_role)
        db.session.add(new_user)
        db.session.commit()
        send_mail(f'Welcome to BookMyShow, Your registration successfully done, click here to login <a href="http://localhost:8080/login">Login</a>', 'Welcome to BookMyShow', new_user.email)
        return {'message': 'User created successfully'}, 201
        # except Exception as e:
        #     db.session.rollback()
        #     print("Erorr: ", e)
        #     return {'message': f'An error occurred: {str(e)}'}, 400
        
#Theatre resource for CRUD operations
class TheatreResource(Resource):
    def get(self, theatre_id):
        theatre = Theatre.query.get(theatre_id)
        if theatre:
            return {'id': theatre.id, 'name': theatre.name, 'location': theatre.location, 'capacity': theatre.capacity}, 200
        return {'message': 'Theatre not found'}, 404
    
    def put(self, theatre_id):
        theatre = Theatre.query.get(theatre_id)
        if theatre:
            args = theatre_parser.parse_args()
            theatre.name = args['name']
            theatre.location = args['location']
            theatre.capacity = args['capacity']
            db.session.commit()
            return {'message': 'Theatre updated successfully'}, 200
        return {'message': 'Theatre not found'}, 404
    
    def delete(self, theatre_id):
        theatre = Theatre.query.get(theatre_id)
        if theatre:
            shows = Show.query.all()
            for show in shows:
                for show_theatre in show.theatres:
                    if theatre.id == show_theatre.id:
                        show.theatres.remove(theatre)
            db.session.delete(theatre)
            db.session.commit()
            return {'message': 'Theatre deleted successfully'}, 200
        return {'message': 'Theatre not found'}, 404
    
#TheatreList resource for listing all theatres and creating new theatres

class TheatreListResource(Resource):
    def get(self):
        theatres = Theatre.query.all()
        theatre_list = [{'id': theatre.id, 'name': theatre.name, 'location': theatre.location, 'capacity': theatre.capacity} for theatre in theatres]
        return theatre_list, 200
    
    def post(self):
        try:
            args = theatre_parser.parse_args()
            new_theatre = Theatre(name=args['name'], location=args['location'], capacity=args['capacity'])
            db.session.add(new_theatre)
            db.session.commit()
            return {'message': 'Theatre created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            print("Error: ", e)
            return {'message': f'An error occurred: {str(e)}'}, 400
        
#Show resource for CRUD operations
class ShowResource(Resource):
    def get(self, show_id):
        show = Show.query.get(show_id)
        if show:
            return {'id': show.id, 
                    'name': show.name, 
                    'rating': show.rating, 
                    'seats':show.seats, 
                    'ticket_price': show.ticket_price, 
                    'start_time': show.start_time, 
                    'end_time': show.end_time, 
                    'theatres':[
                        {'id': theatre.id, 
                         'name': theatre.name, 
                         'location': theatre.location, 
                         'capacity': theatre.capacity} 
                         for theatre in show.theatres
                    ]}, 200
        return {'message': 'Show not found'}, 404
    
    def put(self, show_id):
        show = Show.query.get(show_id)
        if show:
            args = show_parser.parse_args()
            show.name = args['name']
            show.rating = args['rating']
            show.seats = Theatre.query.get(args['theatre_id']).capacity
            show.ticket_price = args['ticket_price']
            show.start_time = args['start_time']
            show.end_time = args['end_time']
            if args['theatre_id'] not in [theatre.id for theatre in show.theatres]:
                show.theatres.append(Theatre.query.get(args['theatre_id']))
            else:
                db.session.commit()
                return {'message': 'Theatre already mapped and updated'}, 200
            db.session.commit()
            return {'message': 'Show updated successfully'}, 200
        return {'message': 'Show not found'}, 404
    
    def delete(self, show_id):
        show = Show.query.get(show_id)
        if show:
            db.session.delete(show)
            db.session.commit()
            return {'message': 'Show deleted successfully'}, 200
    
#ShowList resource for listing all shows and creating new shows

class ShowListResource(Resource):
    def get(self):
        shows = Show.query.all()
        show_list = [{'id': show.id, 
                      'name': show.name, 
                      'rating': show.rating, 
                      'seats':show.seats, 
                      'ticket_price': show.ticket_price, 
                      'start_time': show.start_time, 
                      'end_time': show.end_time, 
                      'theatres':[
                          {'id': theatre.id, 
                           'name': theatre.name, 
                           'location': theatre.location, 
                           'capacity': theatre.capacity} 
                           for theatre in show.theatres
                      ]} for show in shows]
        return show_list, 200

    
    def post(self):
        # try:
        args = show_parser.parse_args()
        show = Show.query.filter_by(name=args['name']).first()
        if show:
            return {'message': 'Show already exists'}, 400
        theatres = Theatre.query.all()
        theatre_ids = [theatre.id for theatre in theatres]
        if args['theatre_id'] not in theatre_ids:
            return {'message': 'Theatre not found'}, 404
        theatre = Theatre.query.get(args['theatre_id'])
        new_show = Show(name=args['name'], 
                        rating=args['rating'], 
                        seats=theatre.capacity,
                        ticket_price=args['ticket_price'], 
                        start_time=args['start_time'], 
                        end_time=args['end_time'])
        new_show.theatres.append(Theatre.query.get(args['theatre_id']))
        db.session.add(new_show)
        db.session.commit()
        return {'message': 'Show created successfully'}, 201
        # except:
        #     db.session.rollback()
        #     return {'message': 'An error occurred'}, 400
    
class BookingResource(Resource):
    def get(self, booking_id):
        booking = Booking.query.get(booking_id)
        user = User.query.get(booking.user_id)
        show = Show.query.get(booking.show_id)
        booking_details = {'id': booking.id,
                            'user':{
                                'id':user.id,
                                'username': user.username,
                                'email': user.email
                            },
                            'show':{
                                'id': show.id,
                                'name': show.name,
                                'rating': show.rating,
                                'seats': show.seats,
                                'ticket_price': show.ticket_price,
                                'start_time': show.start_time,
                                'end_time': show.end_time
                            },
                            'seats': booking.seats,
                            'total_price': booking.total_price,
                            'booking_time': booking.booking_time,
                        }
        return booking_details, 200
    
    def put(self, booking_id):
        booking = Booking.query.get(booking_id)
        show = Show.query.get(booking.show_id)
        if booking:
            args = booking_parser.parse_args()
            curr_seats = booking.seats
            booking.seats = args['seats']
            updated_seats = booking.seats-curr_seats
            show.seats += updated_seats
            booking.total_price = booking.seats * show.ticket_price
            db.session.commit()
            return {'message': 'Booking updated successfully'}, 200
    
    def delete(self, booking_id):
        booking = Booking.query.get(booking_id)
        if booking:
            show = Show.query.get(booking.show_id)
            show.bookings.remove(booking)
            user = User.query.get(booking.user_id)
            user.bookings.remove(booking)
            db.session.delete(booking)
            db.session.commit()
            return {'message': 'Booking deleted successfully'}, 200
        return {'message': 'Booking not found'}, 404
    
class BookingListResource(Resource):
    def get(self):
        args = booking_parser.parse_args()
        if args['user_id']:
            bookings = Booking.query.filter_by(user_id=args['user_id']).all()
            user = User.query.get(args['user_id'])            
            booking_list = [
                {
                    'id': booking.id, 
                    'user': user.username, 
                    'show_id': booking.show_id, 
                    'seats': booking.seats,
                    'booking_time': booking.booking_time,
                    'total_price': booking.total_price
                } for booking in bookings
            ]
            return booking_list, 200
        else:
            bookings = Booking.query.all()
            booking_list = [
                {
                    'id': booking.id, 
                    'user_id': booking.user_id, 
                    'show_id': booking.show_id, 
                    'seats': booking.seats,
                    'booking_time': booking.booking_time,
                    'total_price': booking.total_price
                } for booking in bookings
            ]
            return booking_list, 200
    
    def post(self):
        try:
            args = booking_parser.parse_args()
            user = User.query.get(args['user_id'])
            show = Show.query.get(args['show_id'])
            booking = Booking(user_id=args['user_id'], 
                              show_id=args['show_id'], 
                              seats=args['seats']
                              )
            booking.total_price = booking.seats * show.ticket_price
            booking.booking_time = show.start_time
            booking.timestamp = datetime.utcnow()
            user.bookings.append(booking)
            show.bookings.append(booking)
            show.seats -= booking.seats
            db.session.add(booking)
            db.session.commit()
            send_csv_mail(args['user_id'])
            return {'message': 'Booking created successfully'}, 201
        except:
            db.session.rollback()
            return {'message': 'An error occurred'}, 400