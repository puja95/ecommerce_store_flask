from flask import Flask, jsonify, request
import datetime

from db_connection import *

app = Flask(__name__)


@app.route('/')
def hello():
    return "welcome"
"""
API to create product

Sample Request: 
{
    "name":"New Slim-Fit Knitted Silk T-Shirt",
"description":"TOM FORD puts as much consideration into its casualwear as its impeccably cut suits - this T-shirt is a prime example of the brand's exacting standards. Knitted from fine silk that's naturally soft and breathable, it's designed with a classic ribbed crew neck to match the cuffs and hem. The slim profile means it'll layer nicely.",
"price":200,
"colors":["Red", "Blue", "Green"],
"sizes":["small", "medium"],
"categories":[1,4]
}

Response : 
{
    "status": "Product Added successfully!",
    "statusCode": 200
}

"""


@app.route('/create_products', methods=['POST'])
def createProducts():
    req = request.get_json()

    # connecting to local db connection defined in config file
    db = get_db_conection()
    cursor = db.cursor()
    product_id = 0

    # current timestamp to be added to all tables
    created_at= datetime.datetime.now()
    # inserting name,description to product table
    try:
        sql = 'INSERT INTO product(name,description,created) VALUES("' + req['name'] + '","' + req['description'] + '","'+str(created_at)+'");'
        out = cursor.execute(sql)
        print(out, db.insert_id())
        product_id = db.insert_id()
        db.commit()
    except Exception as e:
        message = {"message":"Cannot insert into product table ","exception":str(e)}
        return message

    # inserting all combination of variants
    try:
        for eachcolor in req['colors']:
            for eachsize in req['sizes']:
                subsql = 'INSERT INTO product_variant(id,color,size,price,created) VALUES("' + str(product_id) + '","' + eachcolor + '","'+eachsize+'","'+str(req['price'])+'","'+str(created_at)+'");'
                print(subsql)
                cursor.execute(subsql)
                db.commit()

        print(sql)
        cursor.execute(sql)
    except Exception as e:
        message = {"message":"Cannot insert into product variant table ","exception":str(e)}
        return message

    # Associating category with product
    try:
        for eachcategory in req['categories']:
            subsql = 'INSERT INTO product_category_association(product_id,category_id,created) VALUES("' + str(product_id) + '","' +str(eachcategory)+'","'+str(created_at)+'");'
            print(subsql)
            cursor.execute(subsql)
            db.commit()

        print(sql)
        cursor.execute(sql)
    except Exception as e:
        message = {"message": "Cannot insert into product category association table ", "exception": str(e)}
        return message

    return jsonify({"status": "Product Added successfully!","statusCode" : 200})

"""
API to fetch product details 

Sample Request :
{
    "id" : 50
}


Response : 
{
    "categories": [
        "Clothing",
        "Dresses"
    ],
    "color": [
        "Red",
        "Blue",
        "Green"
    ],
    "created_on": "Sat, 26 Sep 2020 18:43:39 GMT",
    "description": "TOM FORD puts as much consideration into its casualwear as its impeccably cut suits - this T-shirt is a prime example of the brand's exacting standards. Knitted from fine silk that's naturally soft and breathable, it's designed with a classic ribbed crew neck to match the cuffs and hem. The slim profile means it'll layer nicely.",
    "id": 50,
    "name": "New Slim-Fit Knitted Silk T-Shirt",
    "size": [
        "small",
        "medium"
    ]
}
"""
@app.route('/get_products',methods=['POST'])
def getProducts():
    req=request.get_json()
    print("product id---",req)
    product_details={}
    try :
        # connecting to local db connection defined in config file
        db = get_db_conection()
        cursor = db.cursor()

        # fetching details from product table
        sql="select * from product where id='"+str(req['id'])+"';"
        cursor.execute(sql)
        records=cursor.fetchall()
        product_id=records[0][0]
        product_details['id']=product_id
        product_details['name']=records[0][1]
        product_details['description'] = records[0][2]
        product_details['created_on'] = records[0][3]

        # fetching color list
        sql_variant ="select distinct color from product_variant where id='"+str(product_id)+"';"
        cursor.execute(sql_variant)
        records=cursor.fetchall()
        color=[]
        for eachcolor in records :
            color.append(eachcolor[0])
        product_details['color']=color

        # fetching size list
        sql_size = "select distinct size from product_variant where id='" + str(product_id) + "';"
        cursor.execute(sql_size)
        records = cursor.fetchall()
        size = []
        for eachsize in records:
            size.append(eachsize[0])
        product_details['size'] = size

        #Fetching category names , joining tables
        sql_category = "select distinct category_id,name from product_category_association join category on product_category_association.category_id = category.id where product_id='" + str(product_id) + "';"
        cursor.execute(sql_category)
        records = cursor.fetchall()
        category = []
        for eachcategory in records:
            category.append(eachcategory[1])
        product_details['categories'] = category

    except Exception as e:
        message ={"message" : "Unable to fetch product details","exception" : str(e)}
        return message
    return jsonify(product_details)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
