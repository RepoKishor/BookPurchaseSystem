import pandas as pd
import mysql.connector as connection
from datetime import date
import random
import logging


class BookPurchaseSystemOperations:

    def __init__(self):
        logging.basicConfig(filename='NewOldBookPurchase.log', level=logging.DEBUG)
        fileHandler = logging.FileHandler("NewOldBookPurchaseLogFile.log", mode='a')
        fileHandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
        fileHandler.setFormatter(formatter)
        logging.getLogger().addHandler(fileHandler)

    """
    This method takes user id as input and checks the database if there is any user id which already exists
    Returns code "0" if the user id exists and return code "1" if the user id does not exist 
    """
    def checkUserExists(self,userId):
        status = ""
        try:
            # Creating the user account in Database
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            # Checking if the entered user id already exists
            query_checkUserId = "Select * from bookpurchasesystem.userAccount where userId='%s'" % (userId)
            cursor.execute(query_checkUserId)
            df = pd.DataFrame(cursor.fetchall())
            if (df.empty):
                status = "1"
            else:
                status = "0"
        except Exception as ex:
            logging.info("Exception occured during user account creation for user id " + userId)
        return status

    """
    This method creates an user account based on the user details entered
    """
    def createUserAccountImpl(self, userAccountDict):
        status = ""
        msg =""
        try:
            status = self.checkUserExists(userAccountDict['userId'])
            if (status =="1"):
                mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
                cursor = mydb.cursor()
                # End checking
                placeholders = ', '.join(['%s'] * len(userAccountDict))
                columns = ', '.join(userAccountDict.keys())
                sql = "INSERT INTO bookpurchasesystem.userAccount ( %s ) VALUES ( %s )" % (columns, placeholders)
                cursor.execute(sql, list(userAccountDict.values()))
                mydb.commit()
                mydb.close()
                logging.info("User Account has been created " + userAccountDict['userId'])
                msg = "User Account has been created successfully"
            else:
                msg = "The userID already exists. Please enter again."
        except Exception as ex:
            logging.info("Exception occured during user account creation for user id " + userAccountDict['userId'])
            msg = "Error: Please check the details you have entered"
        return msg

    """
    This method takes user id and the book title and searches the database.
    """
    def searchBookImpl(self, userId,bktitle):
        bookDict = {}
        status = ""
        try:
            # Creating the user account in Database
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            query = "Select * from bookpurchasesystem.books"
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=['bookId','bookTitle','Edition','type','price'])
            for ind in df.index:
                if (df['bookTitle'][ind]==bktitle):
                    bookDict ={'bookId': str(df['bookId'][ind]),
                      'bookTitle' : str(df['bookTitle'][ind]),
                      'Edition' : str(df['Edition'][ind]),
                      'type' : str(df['type'][ind]),
                      'price' : str(df['price'][ind])}

            #mydb.commit()
            mydb.close()
        except Exception as ex:
            logging.info("Exception occured during user account creation for user id " + bookDict['userId'])

        return bookDict

    """
    This method allows the user to purchase the book
    """
    def purchaseBookImpl(self,userId, bookDict):
        orderid = ""
        status=""
        try:
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            paymentDict = dict(userId=userId,
                           paymentId=random.randint(100, 999),
                           paymentDate=date.today(),
                           amount=bookDict['price']
                           )
            orderDict = dict(orderId=random.randint(10000, 99999),
                         userId=userId,
                         bookId=bookDict['bookId'],
                         orderDate=date.today(),
                         price=bookDict['price'],
                         type='purchase',
                         status='order placed'
                         )
            placeholders_pmt = ', '.join(['%s'] * len(paymentDict))
            columns_pmt = ', '.join(paymentDict.keys())
            sql = "INSERT INTO bookpurchasesystem.payments ( %s ) VALUES ( %s )" % (columns_pmt, placeholders_pmt)
            cursor.execute(sql, list(paymentDict.values()))
            # Creating record to insert in the Order table
            placeholdersOrder = ', '.join(['%s'] * len(orderDict))
            columnsOrder = ', '.join(orderDict.keys())
            sql_order = "INSERT INTO bookpurchasesystem.order ( %s ) VALUES ( %s )" % (columnsOrder, placeholdersOrder)
            cursor.execute(sql_order, list(orderDict.values()))
            mydb.commit()
            mydb.close()
            # "0" is for successful purchase
            status="0"
            orderid = str(orderDict['orderId'])
        except Exception as ex:
            logging.info("DB Exception has occurred in purchasing book")
            status = "1"
        return orderid

    """
    This method takes user id and the order id as input and fetches all the order details.
    """
    def trackOrderImpl(self, userId, orderId):
        orderDtls = {}
        # fetching the order details
        try:
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            query_track = "Select * from bookpurchasesystem.order where orderId='%s'" % (orderId)
            cursor.execute(query_track)
            df = pd.DataFrame(cursor.fetchall(),
                              columns=['orderId', 'userId', 'bookId', 'orderDate', 'price', 'type', 'status'])
            for ind in df.index:
                if (str(df['orderId'][ind]) == orderId):
                    # messagebox.showinfo("Success", "The order details are " +str(df['orderId'][ind]))
                    orderDtls = dict(orderId=str(df['orderId'][ind]),
                                     orderDate= str(df['orderDate'][ind]),
                                     orderStatus= str(df['status'][ind])
                                     )
                else:
                    logging.info("We could not found the order id in our database.")
            mydb.commit()
            mydb.close()
        except Exception as ex:
            logging.debug('DB exception during tracking of order: %s' % ex)
        return orderDtls

    """
    This method allows the user to sell the old books by uploading the book details such as book title,
    book price and the edition of the book
    """
    def sellOldBookImpl(self,userid,bktitle,bkprice,bkedition):
        status =""
        bookDict = {'bookId': random.randint(1000, 9999),
                    'bookTitle': bktitle,
                    'Edition': bkedition,
                    'type': "old",
                    'price': bkprice}
        try:
            # insert records into Book table
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            # Creating the record for book in Database
            placeholders_bk = ', '.join(['%s'] * len(bookDict))
            columns_bk = ', '.join(bookDict.keys())
            sql = "INSERT INTO bookpurchasesystem.books ( %s ) VALUES ( %s )" % (columns_bk, placeholders_bk)
            cursor.execute(sql, list(bookDict.values()))
            mydb.commit()
            mydb.close()
            status ="0"
        except Exception as ex:
            logging.debug('DB exception during upload of details of the book to be sold: %s' % ex)
            status=""
        return status



    """
    This method fetches the discussions made by all the users on a particular topic.
    Input is the topic title and returns the all discussion text of all the users. 
    """

    def showTopicDiscussionImpl(self,topicTtl):
        print_topicDiscussions = ''
        # fetching the topic discussions
        try:
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            query_topic = "Select * from bookpurchasesystem.discussion where topicTitle='%s'" % (topicTtl)
            cursor.execute(query_topic)
            df = pd.DataFrame(cursor.fetchall(), columns=['topicTitle', 'userId', 'comments'])
            print_topicDiscussions += "Topic Title is :" + topicTtl + "\n"
            for ind in df.index:
                print_topicDiscussions += "By User ID:" + str(df['userId'][ind]) + "\n"
                print_topicDiscussions += "comments:" + str(df['comments'][ind]) + "\n"
            mydb.commit()
            mydb.close()
        except Exception as ex:
            logging.debug('DB exception in showTopic Discussion: %s' % ex)
        return print_topicDiscussions


    """
    This method saves the topic discussions made by the user
    """
    def saveTopicDiscussionImpl(self, topicDict):
        status =""
        try:
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            placeholders = ', '.join(['%s'] * len(topicDict))
            columns = ', '.join(topicDict.keys())
            sql = "INSERT INTO bookpurchasesystem.discussion ( %s ) VALUES ( %s )" % (columns, placeholders)
            cursor.execute(sql, list(topicDict.values()))
            mydb.commit()
            mydb.close()
            status ="0"
        except Exception as ex:
            logging.debug('DB exception during saving topic discussion: %s' % ex)
            status="1"
        return status

    """
    This method saves the user feedback on a book
    """
    def saveFeedbackImpl(self,feedbkDict):
        status=""
        try:
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            placeholders = ', '.join(['%s'] * len(feedbkDict))
            columns = ', '.join(feedbkDict.keys())
            sql = "INSERT INTO bookpurchasesystem.feedback ( %s ) VALUES ( %s )" % (columns, placeholders)
            cursor.execute(sql, list(feedbkDict.values()))
            mydb.commit()
            mydb.close()
            status = "0"
        except Exception as ex:
            logging.debug('DB exception during saving the feedback for a book: %s' % ex)
        return status

    """
    This is the method which fetches all the transaction details of a user
    """
    def historyTransactionsImpl(self,userId):
        print_records = ''
        try:
            mydb = connection.connect(host="localhost", user="root", passwd="mysql", use_pure=True)
            cursor = mydb.cursor()
            query = "select * from bookpurchasesystem.order WHERE DATE(orderDate) <= CURDATE() and userId='%s'" % (userId)
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(),
                              columns=['orderId', 'userId', 'bookId', 'orderDate', 'price', 'type', 'status'])
            for ind in df.index:
                print_records += "Order ID:" + str(df['orderId'][ind]) + "\n"
                print_records += "Book ID:" + str(df['bookId'][ind]) + "\n"
                print_records += "Order Date:" + str(df['orderDate'][ind]) + "\n"
                print_records += "Price:" + str(df['price'][ind]) + "\n"
                print_records += "Order Status:" + str(df['status'][ind]) + "\n"
                print_records += "------------------------------" + "\n"
            mydb.commit()
            mydb.close()
        except Exception as ex:
            logging.debug('DB exception while fetching the history of transaction: %s' % ex)
            print_records = ""
        return print_records

