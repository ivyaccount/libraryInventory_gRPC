from unittest.mock import MagicMock, Mock
import unittest
import sys

sys.path.insert(0, '../service')

#Reference: https://www.geeksforgeeks.org/python-import-module-from-different-directory/
import grpc
import libraryInventory_pb2, libraryInventory_pb2_grpc
import get_book_titles
from inventory_client import LibraryClient
from libraryInventory_server import InventoryService

class BookUnitTest(unittest.TestCase):
    def mockSettings(self):
        #mockresponse
        mockbook = libraryInventory_pb2.Book(ISBN='978-3-16-148410-2', title='Book C', author='Larry', publishyear=1998, genre=0)
        mockRsp = libraryInventory_pb2.GetBookResponse(message='Success', book=mockbook)

        #configure mock server
        mockserver = libraryInventory_pb2_grpc.InventoryServiceStub(grpc.insecure_channel(''))
        mockserver.GetBook = MagicMock(return_value=mockRsp)

        return mockserver
   
    def testWithMockServer(self):
        #setting up mock
        #libServerMock = mockSettings()
        #mockresponse
        mockbook = libraryInventory_pb2.Book(ISBN='978-3-16-148410-2', title='Book C', author='Larry', publishyear=1998, genre=0)
        mockRsp = libraryInventory_pb2.GetBookResponse(message='Success', book=mockbook)

        #configure mock server
        libServerMock = Mock()
        libServerMock.GetBook.return_value = mockRsp
        #pass the newly created mock object as a client API accessor
        cli = LibraryClient(libServerMock)

        #run function
        bookISBN = '978-3-16-148410-2'
        isbn_list = [bookISBN] * 2
        actuallist = get_book_titles.searchForBookTitles(cli, isbn_list)

        #verify assertion
        #libServerMock.GetBook.assert_called_with(bookISBN)
        test = unittest.TestCase()
        test.assertListEqual(actuallist, ['Book C', 'Book C'])

    def testWithServer(self):
        #create an instance of client api object with reasonable defaults to access the server
        client_instance = LibraryClient()
        #call the defined function using two hardcoded ISBNs as a parameter
        isbn_list = ['978-3-16-148410-2', '978-3-16-148410-0']
        booktitle_list = get_book_titles.searchForBookTitles(client_instance, isbn_list)

        #assert result equal
        test = unittest.TestCase()
        test.assertListEqual(booktitle_list, ['Book C', 'Book A'])

if __name__ == '__main__':
    unittest.main()
    