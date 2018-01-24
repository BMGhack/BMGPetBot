# Help shelter pets find a home.
This is based on/inspired by the Code For America cutepets project: https://github.com/codeforamerica/CutePets

It is different in that it is in Python, pulls data from the city of Bloomington, Indiana's 'adoptable animals' site, and includes some code to assist with deploying as an AWS Lambda Function.
## To run it:
* Use Python 3
* Install the modules in the requirements.txt file (virtualenvs are good here):
`pip install --no-cache-dir -r requirements.txt`
* You also need a 'config.py' file containing all your API secrets & keys
* Deploy as per the README.md in the 'lambda_deploy' subdirectory