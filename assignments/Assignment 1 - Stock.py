#Joe Helped with the dailyLog() function

import sqlite3
import datetime

currentDT = datetime.datetime.now()
date = str(currentDT.day)+'-'+str(currentDT.month)+'-'+str(currentDT.year)
time=  str(currentDT.hour)+':'+str(currentDT.minute)+':'+str(currentDT.second)
cxn = sqlite3.connect("Stock.db")
#Note : If database gets locked inadvertently, try unlocking it, or running the program with a different database name.
#       Deleting the original database would work too.

#Drop Table 
cxn.execute("DROP TABLE IF EXISTS USER")
cxn.execute("DROP TABLE IF EXISTS TICKERS")
cxn.execute("DROP TABLE IF EXISTS TRANS")
cxn.execute("DROP TABLE IF EXISTS DAILY_LOG")

#Creating Table
cxn.execute("CREATE TABLE USER(NAME VARCHAR(20), ID INTEGER PRIMARY KEY)")
cxn.execute("CREATE TABLE TICKERS(TICKERS VARCHAR(8) PRIMARY KEY)")
cxn.execute("""CREATE TABLE TRANS(
                                SELLER VARCHAR(20),
                                BUYER VARCHAR(20),
                                TICKERS VARCHAR(4),
                                PRICE INTEGER, 
                                DATE VARCHAR(10),
                                TIME VARCHAR(10),
                                FOREIGN KEY(SELLER) REFERENCES USER(ID), 
                                FOREIGN KEY(BUYER) REFERENCES USER(ID), 
                                FOREIGN KEY(TICKERS) REFERENCES TICKERS(TICKERS))""")
cxn.execute("CREATE TABLE DAILY_LOG(TICKERS VARCHAR(4), OPEN_PRICE INTEGER, CLOSE_PRICE INTEGER,DATE VARCHAR(10), HIGH INTEGER, LOW INTEGER)")

#Inserting Values into User.
#Inserting Values into Tickers
cxn.execute("INSERT INTO USER VALUES ('A',1)")
cxn.execute("INSERT INTO USER VALUES ('B',2)")
cxn.execute("INSERT INTO USER VALUES ('C',3)")
cxn.execute("INSERT INTO TICKERS VALUES ('SENSEX')")
cxn.execute("INSERT INTO TICKERS VALUES ('NIFTY')")
cxn.execute("INSERT INTO TICKERS VALUES ('GOOGLE')")
cxn.commit()

#Creation of cursor
cur = cxn.cursor()

'''
#Get tickers      
def getTickers(c):
    l=[]
    for row in c.execute('SELECT * FROM TICKERS'):
        l.append((str(row)))   
    for i in range(len(l)):
        l[i]=l[i].strip("'(',')','\'',',']")
    return l
'''

#Validating the User Input
def validateName(cur,tName,Name,TABLE):
 
        cur.execute("SELECT {0} FROM {2} WHERE {0}='{1}'".format(tName,Name,TABLE))
        x=cur.fetchone()
        if x:
             return True
        else:
             return False

#Updating the daily log
def day(cur,cxn):
    cur.execute("DELETE FROM DAILY_LOG")
    cur.execute("SELECT TICKERS FROM TICKERS")
    allTicks = cur.fetchall()
    for i in allTicks:
        print(i)
        cur.execute("SELECT PRICE FROM TRANS WHERE TICKERS = '{0}'".format(i[0]))
        allPrices = cur.fetchall()
        print((allPrices))
        a=[]
        if allPrices:
            for k in range(len(allPrices)):
                a.append(allPrices[k])
            high = max(a)
            low = min(a)
            openPrice = a[0]
            closePrice = a[-1]
            cur.execute("INSERT INTO DAILY_LOG VALUES('{0}','{1}','{2}','{3}','{4}','{5}')".format(i[0],openPrice[0],closePrice[0],date,high[0],low[0]))
            cxn.commit()        

#For making a trade:
def makeTrade():
    flags = True
    while flags:
        #Seller Name Validation
        sName = input("Enter the seller's name :")
        if validateName(cur,"NAME",sName,"USER"):
            pass
        else:
            print("Invalid Data.")
            break
        
        #Buyer Name Validation
        bName = input("Enter the buyer's name :")
        if sName == bName:
            print("Invalid Data.")
            break
        elif validateName(cur,"NAME",bName,"USER"):
            pass
        else:
            print("Invalid Data.")
            break
        
        #Ticker Validation
        ticker = input("Enter the ticker's name :")
        if validateName(cur,"TICKERS",ticker,"TICKERS"):
            pass
        else:
            break
        
        price = (input("Enter price :"))
        cxn.execute("INSERT INTO TRANS VALUES ('{0}','{1}','{2}',{3},'{4}','{5}')".format(sName,bName,ticker,price,date,time))
        cxn.commit()
        if(input("Do you want to quit?")):
            flags = False
        
makeTrade()
day(cur,cxn)

    
    
    
    
    
    