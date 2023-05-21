from channels.consumer import SyncConsumer
from channels.exceptions import StopConsumer

class MySyncConsumer(SyncConsumer):
    
    def websocket_connect(self,event): #this handler is called when client initially opens a connection and is about to finish handshake.
        print("websocket connected",event)
        self.send({
            'type' : 'websocket.accept'
        })

    def websocket_receive(self,event): #this handler is called when data is received  from client
        print("websocket Received...",event) 
        print("message is ", event['text'])
    
    def websocket_send(self,message):
        self.send({
            'type': 'websocket.send',
            'text': message
        })
    
    def websocket_disconnect(self,event): #this handler is called when either connection to the client is lost , either from client closing the connection , the server closing the connection or connection lost.
        print("websocket disconnecte...",event)
        raise StopConsumer()



from channels.consumer import AsyncConsumer

class MyAyncConsumer(AsyncConsumer):
    
    async def websocket_connect(self,event): #this handler is called when client initially opens a connection and is about to finish handshake.
        print("websocket connected",event)
        await self.send({
            'type' : 'websocket.accept'
        })

    async def websocket_receive(self,event): #this handler is called when data is received  from client
        print("websocket Received...",event) 
        print("message is ", event['text'])
    
    async def websocket_disconnect(self,event): #this handler is called when either connection to the client is lost , either from client closing the connection , the server closing the connection or connection lost.
        print("websocket disconnecte...",event)
        raise StopConsumer()

    