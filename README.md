# sleepy

Algorithm:

1. CHECK IF CLIENT EXISTS (POST request to url 'api/is_exist/' with JSON
    {
        "id": 1,
        "client_name": "John Smith",
        "birthdate": "2022-04-04T03:07:30+03:00",
        "createdAt": "2022-04-04T03:07:34+03:00",
        "sleeps": null
    })
   1. If client with client_name and client_data_registration exists 
                      --> return 'Client ID is exist'
   2. If client_name exists, but createdAt !== client_data_registration 
                      --> create new client and return {'ID': 'client_id'}
   3. If not (date_min < birthdate < date_max and date_min < createdAt < date_max)
                      --> return "Error of data validation!!!"

2. DELETE OLD CLIENT INFORMATION (DELETE request to url 'api/is_exist/client_id' with JSON)
    {
        "id": 1,
        "client_name": "John Smith",
        "birthdate": "2022-04-04T03:07:30+03:00",
        "createdAt": "2022-04-04T03:07:34+03:00",
        "sleeps": null
    })


3. ADD SLEEPS TO CLIENT
