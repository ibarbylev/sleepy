# sleepy


### IMPORTANT!!!
For run shell in PyCharm Python Console must do next:
```
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()
```
In other words, it's the same as running ```python manage.py shell```  in the terminal window, but only MUCH MORE convenient!))) 

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
                      --> create new client add return {'id': 'client_id'}
   3. If not (date_min < birthdate < date_max and date_min < createdAt < date_max)
                      --> return "Error of data validation!!!"

2. DELETE OLD CLIENT INFORMATION (PUT request to url 'api/delete-sleeps/client_id' with JSON)

        required fields:
    {
        "client_name": "John Smith",
        "createdAt": "2022-04-04T03:07:34+03:00",
    })
    1. If client.name == client_name and client.pk == client_id 
                       --> delete all sleeps (and segments) for current client
    2. Otherwise --> return "Error in name for client.id={pk}"

3. ADD SLEEPS TO CLIENT (PUT request to url 'api/add-sleeps/client_id' with JSON)

        required fields:
    {
        "client_name": "John Smith",
        "createdAt": "2022-04-04T03:07:34+03:00",
        "sleeps": ALL INFORMATION ABOUT THE CLIENT!!!
    })
   1. If client.name == client_name and client.pk == client_id 
      1. if client.sleeps is empty --> add all sleeps (and segments) for current client
      2. Otherwise --> return "Mistake! You must clear old data before uploading new ones!"
   2. Otherwise --> return "Client not found!"
   
4. GET LIST OF CONSULTANTS (GET request to url 'api/consultants')
    IMPORTANT! The consultant must be: enable=True
