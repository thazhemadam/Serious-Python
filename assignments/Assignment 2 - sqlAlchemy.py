
#Derived from Rahul Koushik PES1201700121's file in concordance with the sqlAlchemy library imported.


#STEPS TO USE:

#1. CREATE USERS (MIN 2)  --- OPTION 1
#2. CREATE STOCKPRICES (MIN 1) --- OPTION 2
#3. GIVE STOCKS --- OPTION 9 (AS WE ARE CONSIDERING ONLY TRADING GIVE INITIAL STOCKS TO SOME USERS)
#4. CHECK USER TABLE, STOCK TABLE, PORTFOLIO TABLES
#5. TRADE STOCKS BETWEEN USERS ---- OPTION 3
#6. RECORDED IN RECORD TABLE AND PORTFOLIOS UPDATED

from sqlalchemy import Column,Integer, String, Float,Date, create_engine, exc, orm, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine=create_engine("sqlite:///ex2.db")
engine.connect()
session= sessionmaker(bind=engine)()

meta = MetaData()
stock = Table(
	'stock', meta, 
	Column('name', String(10), primary_key = True),	
	Column('date', Date, primary_key=True), 
	Column('hp', Float), 
	Column('lp', Float),
	Column('bp', Float),
	Column('ep', Float),
)

portfolio=Table(
	'portfolio', meta, 
	Column('pfname', String(10), primary_key = True),	
	Column('stk', String(10), primary_key=True), 
	Column('no', Integer), 
)


record=Table(
	'record', meta, 
	Column('selname', String(10), primary_key = True),	
	Column('stk', String(10), primary_key=True), 
	Column('no', Integer),
	Column('price', Float), 
	Column('date', Date), 
)


users = Table(
   'users', meta, 
   Column('usname', String(10), primary_key = True), 
)

meta.create_all(engine)



Base=declarative_base()
class Stock(Base):
	__tablename__="stock"
	name=Column(String(10), primary_key=True)
	date=Column(Date, primary_key=True)
	hp=Column(Float)
	lp=Column(Float)
	bp=Column(Float)
	ep=Column(Float)
	def __init__(self,name,date,hp,lp,bp,ep):
		self.name= name
		self.date= date
		self.hp= hp
		self.lp= lp
		self.bp= bp
		self.ep= ep
	def __str__(self):
		return self.name+"|"+str(self.date)+"|"+str(self.hp)+"|"+str(self.lp)+"|"+str(self.bp)+"|"+str(self.ep)


class Users(Base):
	__tablename__="users"
	usname=Column(String(10), primary_key=True)
	def __init__(self,usname):
		self.usname= usname
	def __str__(self):
		return self.usname


class Portfolio(Base):
	__tablename__="portfolio"
	pfname=Column(String(10), primary_key=True)
	stk=Column(String(10), primary_key=True)	
	no=Column(Float)
	def __init__(self,pfname,stk,no):
		self.pfname= pfname
		self.stk= stk
		self.no=no
	def __str__(self):
		return self.pfname+"|"+self.stk+"|"+str(self.no)


class Record(Base):
	__tablename__="record"
	selname=Column(String(10), primary_key=True)
	stk=Column(String(10), primary_key=True)	
	no=Column(Integer)
	price=Column(Float)
	date=Column(Date)
	def __init__(self,selname,stk,no,price,date):
		self.selname= selname
		self.stk= stk
		self.no= no
		self.price= price
		self.date= date
	def __str__(self):
		return self.selname+"|"+self.stk+"|"+str(self.no)+"|"+str(self.price)+"|"+str(self.date)


def adduser():
	print("Enter User Name")
	usname=input()
	userrow = Users(usname)
	session.add(userrow)
	try:
		session.commit()
	except:
		print("Already present in table")
		session.rollback()





import datetime
def addstock():
	print("Enter Stock Name")
	stkname=input()
	print("Enter Day")
	day=int(input())
	print("Enter Month")
	mon=int(input())
	print("Enter Year")
	yr=int(input())	
	dt=datetime.datetime(yr,mon,day)
	print("Enter Highest Price")
	hp=float(input())
	print("Enter Lowest Price")
	lp=float(input())
	print("Enter Base Price")
	bp=float(input())
	print("Enter Ending Price")
	ep=float(input())
	stockrow=Stock(stkname,dt,hp,lp,bp,ep)
	session.add(stockrow)
	try:
		session.commit()
	except:
		print("Already present in table")
		session.rollback()
def sell():
	flag=0
	while(flag==0):
		print("Enter Seller Name")
		seller=input()
		print("Enter Buyer Name")		
		buyer=input()
		print("Enter Stock")		
		stkname=input()
		print("Enter Number")		
		no=int(input())				
		print("Enter Price")		
		price=float(input())
		print("Enter Day")
		day=int(input())
		print("Enter Month")
		mon=int(input())
		print("Enter Year")
		yr=int(input())	
		dt=datetime.date(yr,mon,day)
		result=[r for r in session.query(Stock).all()]
		#Checking if selling price greater than lowest and lesser than highest price for the day		
		xlp=-100000
		yhp=100000		
		for i in result:
			if(i.date==dt and i.name==stkname):
				xlp=i.lp
				yhp=i.hp
				break
		if price < xlp or price > yhp :
			print("Wrong Price")
			break;
		result=[r for r in session.query(Portfolio).all()]
		#Checking if sellers portfolio has enough stocks		
		for i in result:
			if(i.pfname==seller and i.stk==stkname):
				sellerobj=i		
				nos=i.no
				break

		if no >nos:
			print("No sufficient stocks")
			break
		result=[r for r in session.query(Portfolio).all()]
		#To Check if buyer already had some stocks
		exist=False
		for i in result:
			if(i.pfname==buyer and i.stk==stkname):
				buyerobj=i
				exist=True
				break
		
		stockrow=Record(seller,stkname,no,price,dt)
		session.add(stockrow)
		session.commit()


		setattr(sellerobj,'no', sellerobj.no-no)
		session.commit()
		
		if(exist==True):  #You need to update buyers stocks
			setattr(buyerobj,'no', buyerobj.no+no)
		else:		
			stockrow=Portfolio(buyer,stkname,no)
			session.add(stockrow)
			try:
				session.commit()
			except:
				print("Try Again")
				session.rollback()
		flag=1

def dispuser():
	result=[r for r in session.query(Users).all()]
	for i in result:
		print(i)

def dispstock():
	result=[r for r in session.query(Stock).all()]
	for i in result:
		print(i)


def dispport():
	result=[r for r in session.query(Portfolio).all()]
	for i in result:
		print(i)

def disprecord():
	result=[r for r in session.query(Record).all()]
	for i in result:
		print(i)

def highest():
	print("Enter Stock")
	stk=input()	
	print("LOWER BOUND")
	print("Enter Day")
	day=int(input())
	print("Enter Month")
	mon=int(input())
	print("Enter Year")
	yr=int(input())	
	dt1=datetime.date(yr,mon,day)
	print("UPPER BOUND")
	print("Enter Day")
	day=int(input())
	print("Enter Month")
	mon=int(input())
	print("Enter Year")
	yr=int(input())	
	dt2=datetime.date(yr,mon,day)
	result=[r for r in session.query(Stock).all()]
	listprices=[]
	for i in result:
		if i.date>dt1 and i.date<dt2:
			listprices.append(i.hp)
	print("MAXIMUM PRICE IS:",max(listprices))
	
#This function is just to initialize stocks for some people as we assume theres no bank and only trading between users
def give():
	print("Enter Name")
	name=input()
	print("Enter Stock")
	stks=input()
	print("Enter Number")
	nos=int(input())
	result=[r for r in session.query(Portfolio).all()]
	exist=False
	#Check if already has some stocks
	for i in result:
		if(i.pfname==name and i.stk==stks):
			exist=True
			break
	if(exist==False):  #You need to update buyers stocks
		stockrow=Portfolio(name,stks,nos)
		session.add(stockrow)
		try:
			session.commit()
		except:
			print("Try again")
			session.rollback()

while True:
	print("1: Add User\n2: Add Stock Prices\n3: Sell Stock\n4: Display User\n5: Display Stock\n6: Display Portfolios\n7: Display Records\n8: Highest and Lowest\n9: Give Stocks\n10: Exit")
	ans=int(input())
	if(ans==1):
		adduser()
	elif(ans==2):
		addstock()
	elif(ans==3):
		sell()
	elif(ans==4):
		dispuser()
	elif(ans==5):
		dispstock()
	elif(ans==6):
		dispport()
	elif(ans==7):
		disprecord()
	elif(ans==8):
		highest()
	elif(ans==9):
		give()
	else:
		break

