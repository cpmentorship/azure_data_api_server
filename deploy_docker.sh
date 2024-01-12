az acr build --image azure_data_api_server:v1 \
  --registry cpdataapiserver \
  --file Dockerfile .