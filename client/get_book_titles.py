import logging
import sys

sys.path.insert(0, '../service')
import grpc
import libraryInventory_pb2
import libraryInventory_pb2_grpc
from inventory_client import LibraryClient

#client object: to access RPC
def searchForBookTitles(clientObj, isbn_list):
    booktitle_list = list()

    #check one by one
    for isbn in isbn_list:
        #get the whole response
        rsp = clientObj.getBookInformation(isbn)
        
        #check if we have book title or not
        if(rsp.message == "Success"):
            booktitle_list.append(rsp.book.title)
        else:
            booktitle_list.append("")
    
    return booktitle_list

if __name__ == '__main__':
    #initialization
    #logging.basicConfig()

    #create an instance of client api object with reasonable defaults to access the server
    client_instance = LibraryClient()
    #call the defined function using two hardcoded ISBNs as a parameter
    isbn_list = ['978-3-16-148410-2', '978-3-16-148410-0']
    booktitle_list = searchForBookTitles(client_instance, isbn_list)
    #print returned titles to standard output
    print(booktitle_list)