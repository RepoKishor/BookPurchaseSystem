from tkinter import *
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox
import pandas as pd
import re
from PIL import ImageTk, Image
from BookPurchaseSystemImpl import BookPurchaseSystemOperations

root = Tk()
root.title("New book and Old book purchase system")
my_img= ImageTk.PhotoImage(Image.open('E:/Personal/iNeuron/BookPurchaseSystem/ineuron-logo.png'))
my_label = Label(image=my_img)
my_label.pack()
#root.iconbitmap('E:/Personal/iNeuron/BookPurchaseSystem/ineuron.gif')
root.geometry("500x500")
# create a main frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)
# Create a Canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)
# Add a scrollbar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)
# Configure the canvas
my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))
# Create another Frame INSIDE the canvas
second_frame = Frame(my_canvas)
# add a new frame to a window in the canvas
my_canvas.create_window((0, 0), window=second_frame, anchor="nw")


# Variables capturing the user entry
ua = StringVar()
uname = StringVar()
mob = StringVar()
email = StringVar()
title = StringVar()
ua_track = StringVar()
ua_search = StringVar()
oid = StringVar()
uid_sell= StringVar()
title_sell = StringVar()
edition_sell = StringVar()
price_sell = StringVar()
uid_history = StringVar()
uid_fdbk = StringVar()
book_ttl = StringVar()
fdbk = StringVar()
uid_topic = StringVar()
topic_ttl = StringVar()
comment_topic = StringVar()
topic_ttl_discussion = StringVar()
df = pd.DataFrame()  # this is a temporary variable to hold dataframes
# End of the variables



#### This method searches the books in the databse and shows the message whether the book is available or not ###
### If the book is available it allows the user to purchase the same ###
def searchBook():
    userId = ua_search.get()
    bktitle = title.get()
    bookDict = {}
    if bktitle == "":
        messagebox.showwarning("Caution", "Please enter book title to search")
        return
    bpsystemImpl = BookPurchaseSystemOperations()
    bookDict  = bpsystemImpl.searchBookImpl(userId,bktitle)
    if len(bookDict) == 0:
        messagebox.showwarning("Caution", "Sorry, The book you have searched is not available.")
    else:
        messagebox.showinfo("Success", "The book is available to buy, price is Rs." + bookDict['price']+"\n"+ "Please press Ok to buy the book now")
        orderid = bpsystemImpl.purchaseBookImpl(userId,bookDict)
        if orderid !="":
            messagebox.showinfo("Success", "Your order id is "+ orderid)
        else:
            messagebox.showerror("Failure", "Your order as not placed. Please check and try again")


#### This method checks if the entered email id is valid or now #####
def checkValidEmail(emailid):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, emailid)):
        return True
    else:
        return False
### END  ###

### This method creates a user account based on the data furnished by the user ###

def createUserAccount():
    userId = ua.get()
    userName = uname.get()
    mobileNo = mob.get()
    emailId = email.get()
    if userId == "":
        messagebox.showwarning("Caution", "Please enter userID")
        raise Exception('The User id is not entered')
    elif (not userId.isnumeric()):
        messagebox.showwarning("Caution", "Please enter a numerical userID")
    elif (len(userId) != 15):
        messagebox.showwarning("Caution", "You can enter a maximum of 15 digit long user ID")
    else:
        messagebox.showinfo("Success", "We will check the UserId availability. Please press Ok")

    if (not mobileNo.isnumeric()):
        messagebox.showwarning("Caution", "Please enter 10 digit valid mobile number")
        return

    if (not checkValidEmail(emailId)):
        messagebox.showerror("Caution", "Please enter a valid email id")
        return
    userAccountDict = dict(userId=ua.get(),
                               customerName=uname.get(),
                               phone=mob.get(),
                               emailId=email.get()
                           )
    bpsystemImpl = BookPurchaseSystemOperations()
    status = bpsystemImpl.createUserAccountImpl(userAccountDict)
    messagebox.showinfo("Info", status)

# End of createAccount

### This method extracts the order details of the order id for the user to track ###

def trackOrder():
    userid = ua_track.get()
    orderid = oid.get()
    orderdtls={}
    bpsystemImpl = BookPurchaseSystemOperations()
    orderdtls = bpsystemImpl.trackOrderImpl(userid,orderid)
    if (len(orderdtls) != 0):
        # messagebox.showinfo("Success", "The order details are " +str(df['orderId'][ind]))
        windowTrack = Tk()
        windowTrack.title("Your Order details are ")
        windowTrack.geometry('350x200')
        txt = scrolledtext.ScrolledText(windowTrack, width=60, height=10)
        txt.grid(column=0, row=0)
        txt.insert(INSERT, 'Order ID is ' + str(orderdtls['orderId']) + "\n"+ "Order Date is " + str(
            orderdtls['orderDate']) + "\n" + "Order Status is " + str(orderdtls['orderStatus']))
        windowTrack.mainloop()
    else:
        messagebox.showinfo("failure", "We could not found the order id in our database.")
### End  ###

### This method uploads the old book details to be resold ###
def sellBook():
    userid = uid_sell.get()
    bktitle = title_sell.get()
    bkprice = price_sell.get()
    bkedition = edition_sell.get()
    status= ""
    if bktitle == "":
        messagebox.showwarning("Caution", "Please book title to upload and sell")
    else:
        messagebox.showinfo("Success", "Book title to be sold is : " + bktitle)

    bpsystemImpl = BookPurchaseSystemOperations()
    status = bpsystemImpl.sellOldBookImpl(userid,bktitle,bkprice,bkedition)
    if status =="0":
        messagebox.showinfo("Success", "Your Book title to be sold has been successully uploaded")
    else:
        messagebox.showinfo("Failed", "Error in uploading the book to be sold ")

# End

### This method lists the details of all the transactions done by a user ###
def histTransactions():
    userId = uid_history.get()
    transhistory=""
    bpsystemImpl = BookPurchaseSystemOperations()
    transhistory = bpsystemImpl.historyTransactionsImpl(userId)
    if(transhistory != ""):
        windowTrack = Tk()
        windowTrack.title("--Your Transaction History-- ")
        windowTrack.geometry('350x200')
        txt = scrolledtext.ScrolledText(windowTrack, width=40, height=10)
        txt.grid(column=0, row=0)
        txt.insert(INSERT, transhistory)
        windowTrack.mainloop()
    else:
        messagebox.showwarning("Warning", "You have not yet done any transaction with us.")
# End of histroy of transactions

## Save feedback for a particular book
def saveFeedback():
    userid = uid_fdbk.get()
    bkTtle = book_ttl.get()
    feedbk = fdbk.get()

    if feedbk == "":
        messagebox.showwarning("Caution", "Please enter some feedback on the book")

    feedbkDict = dict(bookTitle=bkTtle,
                      userId=userid,
                      feedbackTxt=feedbk
                      )
    # Creating the user account in Database
    bpsystemImpl = BookPurchaseSystemOperations()
    status = bpsystemImpl.saveFeedbackImpl(feedbkDict)
    print("status-- "+status)
    if status == "0":
        messagebox.showinfo("Success", " Thank you for your feedback. This helps us to improve.")
    else:
        messagebox.showerror("Failed", "Failed to save your feedback. Please try again.")
# End Save Feedback

# This method saves the discussion for a topic
def saveTopicDiscussion():
    userid = uid_topic.get()
    topicTtl = topic_ttl.get()
    comment = comment_topic.get()
    status=""
    if topicTtl == "":
        messagebox.showwarning("Caution", "Please enter the topic title you want to discuss")
    # else:
    #     messagebox.showinfo("Success", "Topic title is : " + topicTtl)

    topicDict = dict(topicTitle=topicTtl,
                     userId=userid,
                     comments=comment
                     )
    bpsystemImpl = BookPurchaseSystemOperations()
    status = bpsystemImpl.saveTopicDiscussionImpl(topicDict)
    print("status-- "+status)
    if status == "0":
        messagebox.showinfo("Success", "Your discussion has been saved successfully")
    else:
        messagebox.showerror("Failed", "Failed to save your discussion, Try again later")
# End

# This method allows the discussions posted by all the users on a particular topic
def showTopicDiscussion():
    userid = ua.get()
    topicTtl = topic_ttl_discussion.get()
    if topicTtl == "":
        messagebox.showwarning("Caution", "Please enter the topic title you want to see")
    # else:
    #     messagebox.showinfo("Success", "Topic title is : " + topicTtl)
    bpsystemImpl = BookPurchaseSystemOperations()
    print_topicDiscussions = bpsystemImpl.showTopicDiscussionImpl(topicTtl)
    if print_topicDiscussions !='':
        windowTrack = Tk()
        windowTrack.title("--Discussion for the Topic-- ")
        windowTrack.geometry('350x200')
        txt = scrolledtext.ScrolledText(windowTrack, width=60, height=10)
        txt.grid(column=0, row=0)
        txt.insert(INSERT, print_topicDiscussions)
        windowTrack.mainloop()
    else:
        messagebox.showwarning("Caution", "There is no discussion on this topic")




##### Preparing the GUI for various functions of the API ######

heading_label = Label(second_frame, text="WELCOME TO THE NEW AND OLD BOOK PURCHASE SYSTEM", font=("Calibri", 25)).grid(row=1, column=3)
label = Label(second_frame, text="Please enter your userID", font=("Calibri", 15)).grid(row=2, column=2)
eCreateAcct = Entry(second_frame, font=("Calibri", 15), textvariable=ua).grid(row=2, column=3)
labeluserName = Label(second_frame, text="user name", font=("Calibri", 15)).grid(row=3, column=2)
enteruserName = Entry(second_frame, font=("Calibri", 15), textvariable=uname).grid(row=3, column=3)
labelMobNo = Label(second_frame, text="Mobile no", font=("Calibri", 15)).grid(row=4, column=2)
enterMobNo = Entry(second_frame, font=("Calibri", 15), textvariable=mob).grid(row=4, column=3)
labelEmail = Label(second_frame, text="Email id", font=("Calibri", 15)).grid(row=5, column=2)
enterEmail = Entry(second_frame, font=("Calibri", 15), textvariable=email).grid(row=5, column=3)
btn_createAcct = Button(second_frame, text="Create Account", font=("Calibri", 15), command=createUserAccount).grid(row=6, column=3)

# on click of search button let the user enter the userid and purchase
lblSearch = Label(second_frame, text="Search the book you want to purchase", font=("Calibri", 15)).grid(row=7, column=3)
labelsearchuid = Label(second_frame, text="user id", font=("Calibri", 15)).grid(row=8, column=2)
entersearchuid = Entry(second_frame, font=("Calibri", 15), textvariable=ua_search).grid(row=8, column=3)

labelSearch = Label(second_frame, text="Book Title", font=("Calibri", 15)).grid(row=9, column=2)
enterBook = Entry(second_frame, font=("Calibri", 15), textvariable=title).grid(row=9, column=3)
#btn_Search = Button(second_frame, text="Search", command=searchBook).grid(row=9, column=4)
btn_purchase = Button(second_frame, text="Search and Purchase", font=("Calibri", 15), command=searchBook).grid(row=10, column=3)
# Track order now
label_trackorder = Label(second_frame, text="Track your order now", font=("Calibri", 20)).grid(row=11, column=3)
labeluid = Label(second_frame, text="user id", font=("Calibri", 15)).grid(row=12, column=2)
enteruid = Entry(second_frame, font=("Calibri", 15), textvariable=ua_track).grid(row=12, column=3)

labelorderid = Label(second_frame, text="Order id", font=("Calibri", 15)).grid(row=13, column=2)
enterorderid = Entry(second_frame, font=("Calibri", 15), textvariable=oid).grid(row=13, column=3)

btn_TrackOrder = Button(second_frame, text="Track", font=("Calibri", 15), command=trackOrder).grid(row=14, column=3)

label_uploadtosell = Label(second_frame, text="Upload a book to sell", font=("Calibri", 20)).grid(row=15, column=3)

entuid_lbl = Label(second_frame, text="User id", font=("Calibri", 15)).grid(row=16, column=2)
entuid = Entry(second_frame, font=("Calibri", 15), textvariable=uid_sell).grid(row=16, column=3)

labelbkTitle = Label(second_frame, text="Book Title", font=("Calibri", 15)).grid(row=17, column=2)
enterBookTitle = Entry(second_frame, font=("Calibri", 15), textvariable=title_sell).grid(row=17, column=3)

labelbkedition = Label(second_frame, text="Edition", font=("Calibri", 15)).grid(row=18, column=2)
enterBookEdition = Entry(second_frame, font=("Calibri", 15), textvariable=edition_sell).grid(row=18, column=3)

lblprice_sell = Label(second_frame, text="Price", font=("Calibri", 15)).grid(row=19, column=2)
entprice_sell = Entry(second_frame, font=("Calibri", 15), textvariable=price_sell).grid(row=19, column=3)

btn_sellBook = Button(second_frame, text="Upload", font=("Calibri", 15), command=sellBook).grid(row=20, column=3)

# Allow the user to track the history of transactions
lbl_trackHistory = Label(second_frame, text="My transaction History", font=("Calibri", 20)).grid(row=21, column=3)

luid_hist = Label(second_frame, text="User id", font=("Calibri", 15)).grid(row=22, column=2)
entuid_hist = Entry(second_frame, font=("Calibri", 15), textvariable=uid_history).grid(row=22, column=3)

btn_myTrans = Button(second_frame, text="Track history", font=("Calibri", 15), command=histTransactions).grid(row=23,column=3)
# Allow the user to provide Feedback for each book

lbl_fdbk = Label(second_frame, text="Provide Feedback for a book", font=("Calibri", 20)).grid(row=24, column=3)

luid_fdbk = Label(second_frame, text="User id", font=("Calibri", 15)).grid(row=25, column=2)
entuid_fdbk = Entry(second_frame, font=("Calibri", 15), textvariable=uid_fdbk).grid(row=25, column=3)

lbook_ttl = Label(second_frame, text="Book Title", font=("Calibri", 15)).grid(row=26, column=2)
entbook_ttl = Entry(second_frame, font=("Calibri", 15), textvariable=book_ttl).grid(row=26, column=3)

lbook_fdbk = Label(second_frame, text="Feedback", font=("Calibri", 15)).grid(row=27, column=2)
entbook_fdbk = Entry(second_frame, font=("Calibri", 15), textvariable=fdbk).grid(row=27, column=3)

btn_fdbk = Button(second_frame, text="Save", font=("Calibri", 15), command=saveFeedback).grid(row=28, column=3)
# Allow the user to discuss any topic among other users

lbl_topic = Label(second_frame, text="Discuss a topic", font=("Calibri", 20)).grid(row=29, column=3)

luid_topic = Label(second_frame, text="User id", font=("Calibri", 15)).grid(row=30, column=2)
entuid_topic = Entry(second_frame, font=("Calibri", 15), textvariable=uid_topic).grid(row=30, column=3)
ltopic_ttl = Label(second_frame, text="Topic", font=("Calibri", 15)).grid(row=31, column=2)
enttopic_ttl = Entry(second_frame, font=("Calibri", 15), textvariable=topic_ttl).grid(row=31, column=3)

ltopic_cmt = Label(second_frame, text="Comment", font=("Calibri", 15)).grid(row=32, column=2)
entbook_cmt = Entry(second_frame, font=("Calibri", 15), textvariable=comment_topic).grid(row=32, column=3)
btn_comment = Button(second_frame, text="Save", font=("Calibri", 15), command=saveTopicDiscussion).grid(row=33,
                                                                                                        column=3)

ltopic_ttl_discuss = Label(second_frame, text="Topic", font=("Calibri", 15)).grid(row=34, column=2)
enttopic_ttl_discuss = Entry(second_frame, font=("Calibri", 15), textvariable=topic_ttl_discussion).grid(row=34,
                                                                                                         column=3)
btn_comment_discuss = Button(second_frame, text="ShowTopics", font=("Calibri", 15), command=showTopicDiscussion).grid(
    row=35, column=3)

#### END

root.mainloop()