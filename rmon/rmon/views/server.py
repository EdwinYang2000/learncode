from flask import request, g

from rmon.common.rest import RestView
from rmon.models import Server, ServerSchema

class ServerList(RestView):
    """Redis Server list"""

    def get(self):
        """ get Redis list"""

        servers = Server.query.all()
        return ServerSchema().dump(servers,many=True).data

    def post(self):
        """create Redis server"""
        data = request.get_json()
        server, errors = ServerSchema().load(data)
        if errors:
            return errors, 400
        server.ping()
        server.save()
        return {'ok':True}, 201


class ServerDetail(RestView):
    """Redis Server List"""
    method_decorators = (ObjectMustBeExist(Server),)

    def get(self, object_id):
        """ get Redis Server Detail"""
        data, _= ServerSchema().dump(g.instance)
        return data

    def put(self, object_id):
        """update Server """
        schema = ServerSchema(contest={'instance':g.instance})
        data = request.get_json()
        server, errors = schema.load(data,partial=True)
        if errors:
            return errors, 400
        server.save()
        return {'ok':True}

    def delete(self, object_id):
        """delete redis server"""
        g.instance.delete()
        return{'ok':True},204


        
