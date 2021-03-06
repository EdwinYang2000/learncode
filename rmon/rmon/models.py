"""rmon.model
function all model and serialize
"""

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from redis import StrictRedis, RedisError

from rmon.common.rest import RestException

from marshmallow import (Schema,fields,validate,post_load,validates_schema,ValidationError)

db = SQLAlchemy()

class Server(db.Model):
    """
    Redis Server Type
    """
    __tablename__ = 'redis_server'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64),unique=True)
    description = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Server(name=%s)>' % self.name

    def save(self):

        db.session.add(self)
        db.session.commit()

    def delete(self):

        db.session.delete(self)
        db.session.commit()

    @property
    def redis(self):
        return StrictRedis(host=self.host,port=self.port,password=self.password)

    def ping(self):
        """ examine redis server visit or not"""
        try:
            return self.redis.ping()
        except RedisError:
            raise RestException(400,'redis server %s can not connected' %self.host)
    
    def get_metrics(self):
        """get REdis server monitor info"""
        try:
            return self.redis.info()
        except RedisError:
            raise RestException(400,'redis server %s can not connected' % self.host)

class ServerSchema(Schema):
    """redis server log serilize class"""

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(2,64))
    description = fields.String(validate=validate.Length(0,512))
    host = fields.String(required=True,validate=validate.Regexp(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.d{1,3}$'))
    port = fields.Integer(validate=validate.Range(1024,65536))
    password = fields.String()
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    @validates_schema
    def validate_schema(self,data):
        """ validate if there is same name redis server"""
        if 'port' not in data:
        	data['port'] = 6379

        instance = self.context.get('instance',None)
        server = Server.query.filter_by(name=data['name']).first()
        if server is None:
            return
        if instance is not None and server !=instance:
            raise ValidationError('Reids server already exist','name')
        # create server overtime
        if instance is None and serve:
            raise ValidationError('Reids server already exist','name')




    @post_load
    def create_or_update(self,data):
        """data load ok and create Server object"""
        instance = self.context.get('instance',None)
        #create Redis Server
        if instance is None:
            return Server(**data)
        #update Server
        for key in data:
            setattr(instance,key,data[key])
        return instance
