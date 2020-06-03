from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy

database_name = "yieldifydb"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()


'''
Log
'''


class Log(db.Model):
    __tablename__ = 'logs'

    log_id = Column(Integer, primary_key=True)
    date = Column(String)
    time = Column(String)
    hash = Column(String)
    url = Column(String)
    ip = Column(String)
    user_agent_family = Column(String)
    os_family = Column(String)
    device_family = Column(String)
    device_brand = Column(String)
    device_model = Column(String)
    country = Column(String)
    city = Column(String)

    def __init__(self, log_id, date, time, user_id, url, ip, user_agent_family, os_family, device_family, device_brand,
                 device_model, country, city):
        self.log_id = log_id
        self.date = date
        self.time = time
        self.user_id = user_id
        self.url = url
        self.ip = ip
        self.user_agent_family = user_agent_family
        self.os_family = os_family
        self.device_family = device_family
        self.device_brand = device_brand
        self.device_model = device_model
        self.country = country
        self.city = city

    def format(self):
        return {
            'log_id': self.log_id,
            'date': self.date,
            'time': self.time,
            'user_id': self.user_id,
            'url': self.url,
            'ip': self.ip,
            'user_agent_family': self.user_agent_family,
            'os_family': self.os_family,
            'device_family': self.device_family,
            'device_brand': self.device_brand,
            'device_model': self.device_model,
            'country': self.country,
            'city': self.city,
        }
