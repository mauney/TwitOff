from decouple import config
from flask import Flask, render_template, request
from .models import DB, User
from .predict import predict_user
from .twitter import add_or_update_user


def create_app():
    """Create and configure an instance of the flask application."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None):
        message = ''
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User {name} successfully added!'
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f'Error adding {name}: {e}'
            tweets = []
        return render_template('user.html', title=name, tweets=tweets,
                               message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        message = ""
        user1, user2, = sorted([request.values['user1'],
                                request.values['user2']])
        if user1 == user2:
            message = 'Cannot compare a user to themselves!'
        else:
            tweet_text = request.values['tweet_text']
            confidence = (predict_user(user1, user2, tweet_text) * 100)
            if confidence >= 50:
                message = (f'"{tweet_text}" is more likely to be said by '
                           f'{user1} than {user2}, with {confidence:.2f}% '
                           'confidence')
            else:
                message = (f'"{tweet_text}" is more likely to be said by '
                           f'{user2} than {user1}, with {100-confidence:.2f}% '
                           'confidence')
        return render_template('prediction.html', title='Predicition',
                               message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    return app
