import pymongo
import json
from bson.objectid import ObjectId
from pprint import pprint



client = pymongo.MongoClient('localhost', 27017)

db = client['inventorySolutions']

info = db.inventorySolutions

def menu():
    print('\nWelcome To Inventory Solutions, Your All In One Data Warehouse!\n')
    print('Menu Options: \n')
    print('[1] Add Inventory Item\n')
    print('[2] Remove Inventory Item\n')
    print('[3] Update Inventory Item\n')
    print('[4] View Current Inventory\n')
    print('[5] Check Current Statistics\n')
    print('[6] Import Inventory\n')
    print('[0] Exit The Program\n')



def option1():
    try:
        productID = int(input('\nEnter the product ID to be added into the inventory: \n'))
        productName = input('Enter the product name to be added into the inventory: \n') 
        productCount = int(input('Enter the product count to be added into the inventory: \n'))    
        productPrice = int(input('Enter the product price to be added into the inventory: \n'))    
        productDepartment = input('Enter the product department to be added into the inventory: \n')

        info.insert_one(
            {
                'productID' : productID,
                'productName': productName,
                'productCount': productCount,
                'productPrice': productPrice,
                'productDepartment': productDepartment

            })
        print(f'\nData Inserted Successfully: \nProduct ID: {productID} \nProduct Name: {productName} \nProduct Count: {productCount} \nProduct Price: {productPrice} \nProduct Department: {productDepartment} \n')
    except:
        print('\nPlease Try Again, An Unexpected Error Has Occured.\n')



def option2():
    try:
        deleteProductID = int(input("\nEnter the product ID you would like removed from the inventory: \n"))
        info.delete_many({'productID': deleteProductID})
        print(f'\nData Deleted Successfully: \nProduct ID: {deleteProductID}\n')
    except:
        print('\nPlease Try Again, An Unexpected Error Has Occured.\n')


def option3():
    try:
        updateProductID = int(input('\nEnter The Product ID You Would Like To Update: \n'))
        updateProductName = input('\nEnter Updated Product Name: \n')
        updateProductCount = int(input('\nEnter Updated Product Count: \n'))
        updateProductPrice = int(input('\nEnter Updated Product Price: \n'))
        updateProductDepartment = input('\nEnter Updated Product Department: \n')

        info.update_one(
            {'productID': updateProductID},
            {
                '$set': {
                    'productName': updateProductName,
                    'productCount': updateProductCount,
                    'productPrice': updateProductPrice,
                    'productDepartment': updateProductDepartment
                }
            },
                upsert=True
        )
        print (f'\nData Updated Successfully: \nProduct ID: {updateProductID} \nProduct Name: {updateProductName} \nProduct Count: {updateProductCount} \nProduct Price: {updateProductPrice} \nProduct Department: {updateProductDepartment}')
    except:
        print('\nPlease Try Again, An Unexpected Error Has Occured.\n')


def option4():
    print('\nYour Current Inventory: ')
    try:
        for item in info.find():
            del item['_id']
            print('\n')
            for key in item:
                print(f'{key}: {item[key]}')


    except:
        print('\nPlease Try Again, An Unexpected Error Has Occured.\n')


def option5():
    print('\nStatistical Features: \n')
    print('[1] Filter Products By Department\n')
    print('[2] Top 5 Highest Priced Products\n')
    print('[3] Lowest 5 Priced Products\n')
    print('[4] Top 5 Product Counts\n')
    print('[5] Lowest 5 Product Counts\n')
    print('[0] Exit, Go Back To Main Menu\n')

    option = int(input('\nWhich Statistical Feature Would You Like To Perform: \n'))
    try:
            if option == 1:
                print('\n\nInventory Products By Department: \n')
                count = info.aggregate(
                    [{
                        "$group" : 
                        {"_id" : "$productDepartment",
                        "Product Count" : {"$sum" : 1}
                        }
                    }]
                )
                for item in count:
                    for key in item:
                        print(f'{key}: {item[key]}')
            elif option == 2:
                print('\n\nTop 5 Highest Product Price In Inventory: ')
                for sortPriceProducts in info.find().sort('productPrice', -1).limit(5):
                    del sortPriceProducts['_id']
                    print('\n')
                    for key in sortPriceProducts:
                        print(f'{key}: {sortPriceProducts[key]}')

            elif option == 3:
                print('\n\nLowest 5 Product Price In Inventory: ')
                for sortPriceProducts in info.find().sort('productPrice', 1).limit(5):
                    del sortPriceProducts['_id']
                    print('\n')
                    for key in sortPriceProducts:
                        print(f'{key}: {sortPriceProducts[key]}')

            elif option == 4:
                print('\n\nTop 5 Highest Product Count In Inventory: ')
                for sortCountProducts in info.find().sort('productCount', -1).limit(5):
                    del sortCountProducts['_id']
                    print('\n')
                    for key in sortCountProducts:
                        print(f'{key}: {sortCountProducts[key]}')

            elif option == 5:
                print('\n\nLowest 5 Product Count In Inventory: ')
                for sortCountProducts in info.find().sort('productCount', 1).limit(5):
                    del sortCountProducts['_id']
                    print('\n')
                    for key in sortCountProducts:
                        print(f'{key}: {sortCountProducts[key]}')
            elif option == 0:
                print('Exiting Statistical Fetaures, Going Back To Main Menu.')
            else:
                print('\nPlease Try Again, An Unexpected Error Has Occured.\n')
    except:
        print('\nPlease Try Again, An Unexpected Error Has Occured.\n')

def option6():
    try:
        print('\nOpening file, processing it into the database, this may take a few minutes.\n')
        with open('bike.json') as file:
            file_data = json.load(file)
            info.insert_many(file_data)
            print('\nFile Data Uploaded Succeessfully!\n')

    except:
        print('\nPlease Try Again, An Unexpected Error Has Occured.\n')
  

menu()
option = int(input("\nEnter Your Desired Menu Option: \n"))

while option != 0:
    if option == 1:
        option1()
    elif option == 2:
        option2()
    elif option == 3:
        option3()
    elif option == 4:
        option4()
    elif option == 5:
        option5()
    elif option == 6:
        option6()
    else:
        print("\nInvalid Option, Please Try Again, Thank You.\n")
    print()
    menu()
    option = int(input('\nEnter Your Desired Menu Option: \n'))
print('\nThank You For Using Inventory Solutions, Your All In One Data Warehouse!\n')
