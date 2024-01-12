# azure_data_api_server


## Install ODBC driver
https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline


## How to run appService
https://medium.com/bb-tutorials-and-thoughts/how-to-run-and-deploy-python-rest-api-on-azure-app-services-5d80dbcd370f


## How to run odbc with python
https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-python-quickstart?view=azuresql&tabs=mac-linux%2Csql-auth


## to deploy the docker to azure cloud. First build the image in azure registry.
'''
az acr build --image azure_data_api_server:v1 \
  --registry cpdataapiserver \
  --file Dockerfile .
'''

