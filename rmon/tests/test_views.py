import json
from flask import url_for

from rmon.models import Server

class TestServerList:
    """test Redis Server List API"""

    endpoint = 'api.server_list'
    def test_get_servers(self,server,client):
        """get Redis Server List"""
        resp = client.get(url_for(self.endpoint))
        #RestView base class will define HTTP head Content-Type as json
        assert resp.headers['Content-Type']=='application/json; charset=utf-8'

        assert resp.status_code == 200
        servers = resp.json

        assert len(servers) == 1
        h= servers[0]
        assert h['name'] == server.name
        assert h['description'] == server.description
        assert h['host'] == server.host
        assert h['port'] == server.port
        assert 'updated_at' in h
        assert 'created_at' in h

    def test_create_server_success(self,db,client):
        """test create Redis Server ok"""

        pass

    def test_create_server_failed_with_invalid_host(self, db, client):
        """useless redis address lead to failure of REdis Server Create"""
        pass

    def test_create_server_failed_with_duplicate_server(self,server,client):
        """create duplicate server failure"""
        pass

class TestServerDetail:
    """test redis server detail api"""
    endpoint = 'api.server_detail'
    def test_get_server_success(self,server,client):
        """Test get Redis server detail"""
        pass
    
    def test_get_server_failed(self,db,client):
        """get non-exist Redis Server detail failure"""
        pass
    
    def test_update_server_success(self,server,client):
        """update Redis server successfully"""
        pass
    
    def test_update_server_success_with_duplicate_server(self, server,client):
        """ pdate server name as other same server failure"""
        pass

    def test_delete_success(self,server,client):
        """ delete redis server successfully"""
        pas

    def test_delete_failed_with_host_not_exist(self,db,client):
        """delete non-existance Reids Server failure"""
        pass

