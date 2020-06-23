#------------------ PACKAGES USED----------------------#
import json , requests
import sqlite3
from sqlite3 import Error
from matplotlib import pyplot as plt        # Used to draw BAR GRAPH
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd                         # Used to draw TABULAR GRAPH
#%matplotlib inline
from pandas.tools.plotting import table
from pandas.tools.plotting import scatter_matrix
import urllib.request


#-----------------COUNTRY URL---------------------------#

url1 = 'https://free.currencyconverterapi.com/api/v5/countries'

r = requests.get(url1)
a= json.dumps(r.json())
#print(type(a))         # CODE FOR CHECKING PURPOSE
b = json.loads(a)
#print(type(b))         # CODE FOR CHECKING PURPOSE

#-----------------CURRENCY URL---------------------------#

url2 = 'https://free.currencyconverterapi.com/api/v5/currencies'


q = requests.get(url2, auth=('user', 'pass'))
c = json.dumps(q.json())
#print(type(c))          # CODE FOR CHECKING PURPOSE
d = json.loads(c)
#print(type(c))          # CODE FOR CHECKING PURPOSE

#------------------------------------------------------------------     DATABSE   ------------------------------------------------------------------------------------#

# Create a database in RAM
#db = sqlite3.connect(':memory:')

# Creates or opens a file called case1 with a SQLite3 DB
db = sqlite3.connect('C:/Python/Python37/Lib/sqlite3/case1.db')

# Get a cursor object
cursor = db.cursor()


#-----------------------------------------------------------------      CREATING COUNTRIES TABLE     -----------------------------------------------------------------#

cursor.execute("CREATE TABLE IF NOT EXISTS countries(alpha31  TEXT, currencyId1 TEXT , currencyName1 TEXT , currencySymbol1 TEXT , countryID1 TEXT , name1 TEXT)")
db.commit()


#-----------------------------------------------------------------      CURRENCIES COUNTRIES TABLE  ------------------------------------------------------------------#

cursor.execute("CREATE TABLE IF NOT EXISTS currencies(currencyName TEXT , currencySymbol TEXT, currencyId TEXT)")
db.commit()

cursor = db.cursor()



#-----------------------------------------------------------------      STORING IN DATABSE  ------------------------------------------------------------------#


#------------------------------------- STORING COUNTRIES TABLE

def insertingCountries():
    for id , info1 in b.items():
        #print("\n currensies:", id)
        for key1 , info2 in info1.items():
            s = []
            for key2 , info3 in info2.items():
                s.append(info2[key2])
            s = str(s).replace("[","").replace("]","").replace(",","\t")
            cursor.execute("INSERT INTO countries(alpha31, currencyId1, currencyName1, currencySymbol1 , countryID1 , name1) VALUES(?,?,?,?,?,?)", (info2["alpha3"], info2["currencyId"], info2["currencyName"], info2["currencySymbol"] , info2["id"] , info2["name"]))
            db.commit()


insertingCountries()   #CALL TO INSERT DATA 


#-------------------------------------STORING CURRENCIES TABLE

def insertingCurrencies():
    for id , info1 in d.items():
        print("\n currencies:", id)
        for key1 , info2 in info1.items():
            s = []
            for key2 , info3 in info2.items():
                s.append(info2[key2])
            s = str(s).replace("[","").replace("]","").replace(",","\t")
            if "currencySymbol" not in info2:
                cursor.execute("INSERT INTO currencies(currencyName, currencySymbol, currencyId) VALUES(?,?,?)", (info2["currencyName"], "NULL", info2["id"]))
                db.commit()
            else:
                cursor.execute("INSERT INTO currencies(currencyName, currencySymbol, currencyId) VALUES(?,?,?)", (info2["currencyName"], info2["currencySymbol"], info2["id"]))
                db.commit()

insertingCurrencies()     #CALL TO INSERT DATA COUNTRIES TABLE
        
#-----------------------------------------------------------------  CODE TO VISUALLISE DATA  -------------------------------------------------------------------------#


#------------------------------------- BAR CHART 

def draw_graph():
    try:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        number = []
        currencyID = []
        cursor.execute("SELECT COUNT(name1) , currencyId1 FROM countries GROUP BY currencyId1 ORDER BY COUNT(currencyId1) DESC limit 9")
        for rows in cursor.fetchall():
            number.append(int(rows[0]))
            currencyID.append(str(rows[1]))

        #x_axis = number
        #y_axis = currencyID
        ## necessary variables
        ind = np.arange(len(number))
        width = 0.35

        ## the bars
        rects1 = ax.bar(ind, number, width,
                    color='black',
                    error_kw=dict(elinewidth=2,ecolor='red'))
        # axes and labels
        ax.set_xlim(-width,len(ind)+width)
        ax.set_ylim(0,45)

        ax.set_ylabel('No. of Country')
        ax.set_xlabel('Currency ')
        ax.set_title('Top 9 Currencies in World')

        ax.set_xticks(ind+width)
        xtickNames = ax.set_xticklabels(currencyID)
        plt.setp(xtickNames, rotation=45, fontsize=10)
        
        plt.show()
        plt.savefig("C:/Users/MoniSingh/Desktop/cervello/barGraph.png")
    except ValueError:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        number = []
        currencyID = []
        cursor.execute("SELECT COUNT(name1) , currencyId1 FROM countries GROUP BY currencyId1 ORDER BY COUNT(currencyId1) DESC limit 9")
        for rows in cursor.fetchall():
            #print(rows[0] , " " , rows[1])             # DISPLAY ON CONSOLE
            number.append(int(rows[0]))
            currencyID.append(str(rows[1]))
            
        #x_axis = number
        #y_axis = currencyID
        ## necessary variables
        ind = np.arange(len(number))
        width = 0.50

        ## the bars
        rects1 = ax.bar(ind, number, width,
                    color='black',
                    error_kw=dict(elinewidth=2,ecolor='red'))
        # axes and labels
        ax.set_xlim(-width,len(ind)+width)
        ax.set_ylim(0,45)

        ax.set_ylabel('no. of countries')
        ax.set_xlabel('currencies id ')
        ax.set_title('top 9 currencies')

        ax.set_xticks(ind+width)
        xtickNames = ax.set_xticklabels(currencyID)
        plt.setp(xtickNames, rotation=45, fontsize=10)
        
        plt.show()
        plt.savefig("C:/Users/MoniSingh/Desktop/cervello/secondTestCase/barGraph.png")
        #plt.savefig('barGraph.png')

draw_graph()            #CALL TO SHOW BAR CHART

#------------------------------------- TABULAR CHART 


def draw_tabular():
    try:
        df = pd.read_sql_query("SELECT DISTINCT currencySymbol ,  currencyName FROM currencies  WHERE currencies.currencyId Not IN (SELECT DISTINCT countries.currencyId1 FROM countries) ", db )
        #print(df)
        ax = plt.subplot(111, frame_on=False) # no visible frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis

        table(ax, df , loc='center' )  # where df is your data frame
        plt.show()
        plt.savefig('C:/Users/MoniSingh/Desktop/cervello/tabular.png')
    except ValueError: 
        df = pd.read_sql_query("SELECT DISTINCT currencySymbol ,  currencyName FROM currencies  WHERE currencies.currencyId Not IN (SELECT DISTINCT countries.currencyId1 FROM countries) ", db)
        #print(df)          # DISPLAY ON CONSOLE
        ax = plt.subplot(111, frame_on=False) # no visible frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis

        table(ax, df , loc='center' , index = False)  # where df is our data frame
        plt.show()
        plt.savefig('C:/Users/MoniSingh/Desktop/cervello/tabular.png')
        #plt.savefig('tabular.png')
        #print("done   :) ")


draw_tabular()              #CALL TO SHOW TABULAR CHART

