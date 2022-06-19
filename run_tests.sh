# #!/bin/bash

echo 'start --- storage.tests.TestRequestAPIisExist ---'
python manage.py test storage.tests.TestRequestAPIisExist

echo 'start --- storage.tests.TestRequestAPIaddSleeps ---'
python manage.py test storage.tests.TestRequestAPIaddSleeps

