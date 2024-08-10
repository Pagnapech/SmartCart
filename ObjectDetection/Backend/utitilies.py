from backend.models import GUITable 
from django.db import connection 

from pathlib import Path


# Fetch All specific row with the command 
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict" 
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


# Select item from productInfoTabel and insert into GUITable 
def insertIntoTable(itemDetected, productInfoTable, guiTable):
    cursor = connection.cursor()

    # Before insert new item, check the existing item in the table 
    # if it already existed, then increment "Unit" 
    # Lists of database Column 
    unit = "Unit"
    pricePerUnit = "price_per_unit"
    subtotal = "Subtotal"

    cursor.execute("SELECT {}, {} FROM {} WHERE product_name = '{}'".format(unit, pricePerUnit, guiTable, itemDetected)) 
    print("SELECT {} FROM {} WHERE product_name = '{}'".format(unit, guiTable, itemDetected))
    existed_info = dictfetchall(cursor)

    print(existed_info) 

    if (existed_info == []):
        # Select item from productInfoTable 
        # print("SELECT * FROM {} WHERE product_name = '{}'".format(productInfoTable, itemDetected))
        cursor.execute("SELECT * FROM {} WHERE product_name = '{}'".format(productInfoTable, itemDetected))
        info = dictfetchall(cursor) 
        # print(info) 

        Product_Name = info[0]["product_name"]
        Unit = info[0]["unit"]
        Price_Per_Unit = info[0]["price_per_unit"]
        Subtotal = Price_Per_Unit * Unit 

        # Insert item into GUITable 
        # Technique: using Django insert data from raw dictionary (NO INSERT INTO technique) -- check reactdjango(connect) views.py 
        # Insert into a specific GUITable 
        infoToInsert = GUITable(product_name=Product_Name, unit=Unit, price_per_unit=Price_Per_Unit, subtotal=Subtotal) 
        # Save/Add into the table 
        infoToInsert.save() 
        print("Successfully added to Table.")
    
    else:
        print(existed_info[0])
        # increment unit by 1 
        incrementByOne = existed_info[0]["unit"] + 1
        print(incrementByOne)
        # recalculate the subtotal, by using new unit 
        calculateSubtotal = round(existed_info[0]["price_per_unit"] * incrementByOne, 2)
        # update the table (unit and subtotal)
        cursor.execute("UPDATE {} SET {} = '{}', {} = '{}' WHERE product_name = '{}'".format(guiTable, unit, incrementByOne, subtotal, calculateSubtotal, itemDetected)) 


def removeFromTable(itemDetected, guiTable): 

    cursor = connection.cursor() 

    unit = "Unit"
    pricePerUnit = "price_per_unit"
    subtotal = "Subtotal"

    cursor.execute("SELECT {}, {} FROM {} WHERE product_name = '{}'".format(unit, pricePerUnit, guiTable, itemDetected)) 
    print("SELECT {} FROM {} WHERE product_name = '{}'".format(unit, guiTable, itemDetected))
    existed_info = dictfetchall(cursor)

    print(existed_info[0])

    currentUnit = existed_info[0]["unit"] 

    if(currentUnit == 1): 
        cursor.execute("DELETE FROM {} WHERE product_name = '{}'".format(guiTable, itemDetected))

    elif (currentUnit > 1):
        print("hello")
        # decrement unit by 1 
        decrementByOne = currentUnit - 1 
        calculateSubtotal = round(existed_info[0]["price_per_unit"] * decrementByOne, 2) 
        print(calculateSubtotal)
        # update the table (unit and subtotal)
        cursor.execute("UPDATE {} SET {} = '{}', {} = '{}' WHERE product_name = '{}'".format(guiTable, unit, decrementByOne, subtotal, calculateSubtotal, itemDetected)) 
        print("hello after")

    print("Successfully removed from Table.") 
    # return 

"""
Select from one table and insert into another table in the same Database schema 
Technique: using Django insert data from raw dictionary (NO INSERT INTO technique)
"""
def modifyTable():
    
    # read and write     
    filepath = "/home/kaavian/Desktop/SmartCartTwoApp_Py3.9/SmartCartTwo/connectOD_Backend"
    filename = "itemDetected.txt"
    try:
        print(Path.cwd()) # for checking the current working directory 
        # read if the file is NOT empty, then proceed with clear the text file 
        file = open("{}/{}".format(filepath, filename), "r+") # r+ is both for reading and writing 

        isEmptyString = file.read()
        
        if (isEmptyString == ""):
            print("No item here.")
        # read 
        else:
            print(isEmptyString)
            
            # split at ":"
            currentList = isEmptyString.split(":")
            print(currentList[0])
            print(currentList[1])
            print(type(currentList[1]))

            itemDetected = currentList[0]
            indicator = int(currentList[1]) 


            # if indicator = 1 => insert item to Cart 
            # if indicator = -1 => remove item from Cart 
        
        # INSERT / REMOVE from GUI Table based on the productName 
        # Add with the data sending from webcam 
        # 1: indicates inCart, -1 indicates outCart 
            productInfoTable = "backend_productinfo"
            guiTable = "backend_guitable"
            print("Before indicator check")
            if(indicator == 1):
                print("Before insert") 
                insertIntoTable(itemDetected, productInfoTable, guiTable) 
                print("after insert")
                # clear the text file with truncate
                file.truncate(0)
                emptyString = file.read()
                if (emptyString == ""): 
                    print("Successfully deleted")

            if(indicator == -1): 
                removeFromTable(itemDetected, guiTable)  
                # clear the text file with truncate
                file.truncate(0)
                emptyString = file.read()
                if (emptyString == ""): 
                    print("Successfully deleted")

        # Select the specific data with WHERE Condition (change a condition baced on the productName)
    # cursor.execute(f"SELECT * FROM {allProductTable} WHERE product_name = {productName}") 
    # # Fetch all info 
    # retrieveInfo = dictfetchall(cursor) 
        

        # emptyString = file.read()
        # if (emptyString == ""): 
        #     print("Successfully deleted")

        file.close()

    except: 
        print("Cannot open {} file".format(filename)) 
    