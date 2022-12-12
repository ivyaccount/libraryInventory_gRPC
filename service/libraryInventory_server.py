from concurrent import futures
import logging

import grpc
import libraryInventory_pb2
import libraryInventory_pb2_grpc

#three existing book
book1 = libraryInventory_pb2.Book(ISBN='978-3-16-148410-0', title='Book A', author='Sherry', publishyear=1998, genre=0)
book2 = libraryInventory_pb2.Book(ISBN='978-3-16-148410-1', title='Book B', author='Mary', publishyear=1999, genre=1)
book3 = libraryInventory_pb2.Book(ISBN='978-3-16-148410-2', title='Book C', author='Larry', publishyear=1998, genre=0)
#main inventory
Books = {'978-3-16-148410-0':book1, '978-3-16-148410-1':book2, '978-3-16-148410-2':book3}


class InventoryService(libraryInventory_pb2_grpc.InventoryServiceServicer):

    def CreateBook(self, request, context):
        #not distincet isbn
        if request.ISBN in Books:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Fail to update library')
            return libraryInventory_pb2.CreateBookResponse('Fail: Missing input ISBN')

        try:
            newbook = libraryInventory_pb2.Book(
                ISBN=request.ISBN, 
                title=request.title, 
                author=request.author, 
                publishyear=request.publishyear, 
                genre=request.genre
            )

            Books[request.ISBN] = newbook
            return libraryInventory_pb2.CreateBookResponse(message='Success')
        except:
            return libraryInventory_pb2.CreateBookResponse(message='Fail: Missing input field')


    def GetBook(self, request, context):
        #no isbn
        if len(request.ISBN) < 1:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Fail to read input')
            return libraryInventory_pb2.GetBookResponse(message='Fail: Missing input ISBN')
        
        #found book
        if request.ISBN in Books:
            result_book = Books[request.ISBN]
            
            return libraryInventory_pb2.GetBookResponse(message='Success', book=result_book)
        
        context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details('Fail to get book')
        return libraryInventory_pb2.GetBookResponse(message='Fail: Cannot find book') 
        

        


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    libraryInventory_pb2_grpc.add_InventoryServiceServicer_to_server(InventoryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    print("Server starts!\n")
    serve()