import logging
import sys

sys.path.insert(0, '../service')


#Reference: https://www.geeksforgeeks.org/python-import-module-from-different-directory/
import grpc
import libraryInventory_pb2, libraryInventory_pb2_grpc


class LibraryClient:
    #server address,interfaces
    def __init__(self, server=libraryInventory_pb2_grpc.InventoryServiceStub):
        #address
        self.host = 'localhost'
        self.port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel("{}:{}".format(self.host, self.port))
        #linking the client and the server together
        if(server==libraryInventory_pb2_grpc.InventoryServiceStub):
            self.stub = server(self.channel)
        else:
            self.stub = server
    
    #Client function to call the rpc for CreateBookResponse
    #input bookInformation: a dictionary with a book's ISBN, title, author, publishyear, and genre
    #output: reponse from server whether it is successful or not
    def creatingBook(self, bookInformation):
        message = libraryInventory_pb2.CreateBookRequest(
            ISBN=bookInformation['ISBN'],
            title=bookInformation['title'], 
            author=bookInformation['author'], 
            publishyear=bookInformation['publishyear'], 
            genre=bookInformation['genre']
        )

        return self.stub.CreateBook(message)

    #Client function to call the rpc for GetBookResponse
    #input ISBN: a book's ISBN (string)
    #output: reponse from server whether it is successful or not and the book's information
    def getBookInformation(self, bookISBN):
        message = libraryInventory_pb2.GetBookRequest(ISBN=bookISBN)
        
        return self.stub.GetBook(message)




if __name__ == '__main__':
    logging.basicConfig()

    cli = LibraryClient()
    print(cli.getBookInformation('978-3-16-148410-2'))
    
