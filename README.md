# azure_data_api_server


## Install ODBC driver
https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=debian18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline


## How to run appService
https://medium.com/bb-tutorials-and-thoughts/how-to-run-and-deploy-python-rest-api-on-azure-app-services-5d80dbcd370f


## How to run odbc with python
https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-python-quickstart?view=azuresql&tabs=mac-linux%2Csql-auth


## Deploy the app_server to Azure cloud.
Please refer this for the more comprehansive steps: https://learn.microsoft.com/en-us/azure/app-service/tutorial-custom-container?tabs=azure-portal&pivots=container-linux


Here are some key steps using cli, you can do the same thing on the Azure portal:
- First build the image in azure registry.


                az acr build --image azure_data_api_server:v1 \
                --registry cpdataapiserver \
                --file Dockerfile .


- Make sure assign the correct PORT:


                az webapp config appsettings set --resource-group cpdashboard --name azure-data-api-server --settings WEBSITES_PORT=5000


## After the sucessful deployment
go to https://azure-data-api-server.azurewebsites.net/
You should see 

            Hello World!!! version 1.0

The version number should reflect your latest version you put in the code.


## API
- Home

                curl --location 'https://azure-data-api-server.azurewebsites.net//'

- Create Air Sample Table

                curl --location --request POST 'https://azure-data-api-server.azurewebsites.net//api/sgp40/create'

- add Air Sample into the table. (This is what sgp40 sensor is calling. )

                curl --location 'https://azure-data-api-server.azurewebsites.net//api/sgp40' \
                --header 'Content-Type: application/json' \
                --data '{
                    "sgp40":{
                        "device_id": "dashpi00",
                        "sample": 159,
                        "sample_time" :"2024-01-08 03:40:37"
                    }
                }'

- get all the Air Sample data. (This should be the tabulea or some other dashboard to call to retrieve the data)

                curl --location 'https://azure-data-api-server.azurewebsites.net//api/sgp40?device_id=dashpi00'

```json
[
    {
        "ID": 1,
        "device_id": "dashpi00",
        "sample": 55,
        "sample_time": "Sun, 07 Jan 2024 23:35:01 GMT"
    },
    {
        "ID": 3,
        "device_id": "dashpi00",
        "sample": 56,
        "sample_time": "Sat, 06 Jan 2024 23:35:01 GMT"
    },
    {
        "ID": 4,
        "device_id": "dashpi00",
        "sample": 57,
        "sample_time": "Sat, 06 Jan 2024 22:35:01 GMT"
    },
    {
        "ID": 6,
        "device_id": "dashpi00",
        "sample": 59,
        "sample_time": "Sat, 06 Jan 2024 21:35:01 GMT"
    },
    {
        "ID": 7,
        "device_id": "dashpi00",
        "sample": 159,
        "sample_time": "Mon, 08 Jan 2024 08:40:37 GMT"
    },
    {
        "ID": 8,
        "device_id": "dashpi00",
        "sample": 159,
        "sample_time": "Mon, 08 Jan 2024 04:40:37 GMT"
    },
    {
        "ID": 9,
        "device_id": "dashpi00",
        "sample": 159,
        "sample_time": "Mon, 08 Jan 2024 03:40:37 GMT"
    }
]
```