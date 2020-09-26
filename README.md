# ecommerce_store_flask
Create and Get product details.

Use Case : 
E-Commerce Store Application. 
Products can have various colors and sizes and categories.
It will help in filtering of products based on above conditions. 


API details.
 /create_products : Creates products, generates product variant and category association.
 
 Sample Request: 
```{
    "name":"New Slim-Fit Knitted Silk T-Shirt",
    "description":"TOM FORD puts as much consideration into its casualwear as its impeccably cut suits - this T-shirt is a prime example of the brand's exacting    standards. Knitted from fine silk that's naturally soft and breathable, it's designed with a classic ribbed crew neck to match the cuffs and hem. The slim profile means it'll layer nicely.",
    "price":200,
    "colors":["Red", "Blue", "Green"],
    "sizes":["small", "medium"],
    "categories":[1,4]
}
```

Response : 
```
{
    "status": "Product Added successfully!",
    "statusCode": 200
}
```

/get_products - Get product details according to product id.

Sample Request :

```{
    "id" : 50
}
```


Response : 

```{
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
```






