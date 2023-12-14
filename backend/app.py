from flask import Flask, request
from flask_restful import Api
from api import UserListResource, UserResource, TheatreListResource, TheatreResource, ShowListResource, ShowResource, BookingListResource, BookingResource
# from models import User, Role
from models import *
from database import db 
from flask_cors import CORS
# from flask_security import Security, SQLAlchemyUserDatastore
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import workers
import redis
from task import send_mail

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/2'
app.config['REDIS_URL'] = 'redis://localhost:6379'
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 9
app.config['REDIS_HOST'] = 'localhost'
app.config['REDIS_PORT'] = 6379
app.config['REDIS_DB'] = 0


app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a secure key
jwt = JWTManager(app)

# Initialize the SQLAlchemy extension with the app
db.init_app(app)

api = Api(app)
# Initialize Celery
celery = workers.celery
celery.conf.update(
    broker_url=app.config['CELERY_BROKER_URL'],
    result_backend=app.config['CELERY_RESULT_BACKEND'],
)
celery.Task = workers.ContextTask


app.redis = redis.Redis(host=app.config["REDIS_HOST"], port=app.config["REDIS_PORT"], db=app.config["REDIS_DB"])
app.app_context().push()

# user_datastore = SQLAlchemyUserDatastore(db,User,Role)
# app.security = Security(app, user_datastore)

# Create the database tables
with app.app_context():
    # db.drop_all()
    db.create_all()

# Add the API resources to the API
api.add_resource(UserListResource, '/users') # done
api.add_resource(UserResource, '/users/<int:user_id>') # done
api.add_resource(TheatreListResource, '/theatres')   
api.add_resource(TheatreResource, '/theatres/<int:theatre_id>') 
api.add_resource(ShowListResource, '/shows')
api.add_resource(ShowResource, '/shows/<int:show_id>')
api.add_resource(BookingListResource, '/bookings')
api.add_resource(BookingResource, '/bookings/<int:booking_id>')

def addAdmin():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin')
            db.session.add(admin_role)
            db.session.commit()
        admin = User(username='admin',
                     email = 'as25822@gmail.com',
                     password = 'admin',
        )
        send_mail("Welcome Mr. Aditya Singh Your admin account has been created successfully.", "Welcome to BookMyShow", admin.email)
        admin.roles.append(admin_role)
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    addAdmin()
# app.app_context().push()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    send_mail(f'Welcome {user.username} to BookMyShow Successfully Logged in', 'Welcome to BookMyShow', user.email)
    if user and user.password == password:
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
    return {'message': 'Invalid credentials'}, 401

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected_route():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return {'message': f'Hello, {user.username}! You have access to this protected route.'}

# Search

@app.route('/search', methods=['GET'])
def search():
    data = request.args.get('data')
    if data:
        theatres = Theatre.query.filter(Theatre.name.contains(data)).all()
        shows = Show.query.filter(Show.name.contains(data)).all()
        if theatres or shows:
            return {'theatres': [{'id':theatre.id,
                                  'name':theatre.name,
                                  'location':theatre.location,
                                  'capacity':theatre.capacity} for theatre in theatres], 'shows': [{'id':show.id,
                                                                                                    'name':show.name,
                                                                                                    'rating':show.rating,
                                                                                                    'seats':show.seats,
                                                                                                    'ticket_price':show.ticket_price,
                                                                                                    'start_time':show.start_time,
                                                                                                    'end_time':show.end_time} for show in shows]}, 200
        else:
            return {'message': 'No results found'}, 404
    else:
        return {'message': 'No search data provided'}, 400

if __name__ == '__main__':
    CORS(app)
    app.run(debug=True)
