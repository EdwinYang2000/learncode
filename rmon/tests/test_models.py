from rmon.models import Server

class TestServer:
    """test Server relative function"""
    def test_save(self,db):
        assert Server.query.count() ==0
        server = Server(name='test',host='127.0.0.1')
        server.save()
        assert Server.query.count() ==1
        assert Server.query.first() ==server
    
    def test_delete(self,db,server):
        """test Server.delete function"""

        assert Server.query.count() ==1
        server.delete()
        assert Server.query.count() ==0
    def test_ping_success(self,db,server):
        """ test Server.ping function successfully"""

        def test_ping_success(self,db,server):
            """test Server.ping function ok ensure redis server monitor correct port"""
            assert server.ping() is True

        def test_ping_failed(self,db):
            """test Server.ping function failure Server.ping raise RestException"""
            server = Server(name='test',host='127.0.0.1',port=6399)
            try:
                server.ping()
            except RestException as e:
                assert e.code == 400
                assert e.message == 'redis server %s can not connected' % server.host

