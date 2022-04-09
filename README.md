# sleepy

Algorithm:

1. CHECK IF CLIENT EXISTS (POST request to url 'api/is_exist/' with JSON

        required fields:
    {
        "client_name": "John Smith",
        "birthdate": "2022-04-04T03:07:30+03:00",
        "createdAt": "2022-04-04T03:07:34+03:00",
    })
   1. If client with client_name and client_data_registration exists 
                      --> return 'Client ID is exist'
   2. If client_name exists, but createdAt !== client_data_registration 
                      --> create new client, add all sleeps and return {'ID': 'client_id'}
   3. If not (date_min < birthdate < date_max and date_min < createdAt < date_max)
                      --> return "Error of data validation!!!"

   4. DELETE OLD CLIENT INFORMATION (PUT request to url 'api/delete-sleeps/client_id' with JSON)

           required fields:
       {
           "id": 555,
           "client_name": "John Smith",
           "createdAt": "2022-04-04T03:07:34+03:00",
       })


3. ADD SLEEPS TO CLIENT
