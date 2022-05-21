from azure.storage.blob import ContainerClient
from secret import AZURE_DATASETS_CONTAINER, AZURE_STORAGE_CONN_STRING, AZURE_STUDY_DATASETS_CONTAINER, AZURE_TRAIN_TEST_CONTAINER

class BlobDatabase:
    def upload_dataset(name, blob):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_DATASETS_CONTAINER)

            blob_client = dataset_client.get_blob_client(name)
            blob_client.upload_blob(blob)
        except Exception as e:
            raise e 
    
    def get_dataset(name):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_DATASETS_CONTAINER)

            blob_client = dataset_client.get_blob_client(name)

            return blob_client.url
        except Exception as e :
            raise e 
    
    def upload_study_dataset(name, blob):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_STUDY_DATASETS_CONTAINER)

            blob_client = dataset_client.get_blob_client(name)
            blob_client.upload_blob(blob)
        except Exception as e:
            raise e 
    
    def get_study_dataset(name):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_STUDY_DATASETS_CONTAINER)

            blob_client = dataset_client.get_blob_client(name)

            return blob_client.url
        except Exception as e :
            raise e 
    
    def delete_dataset(name):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_DATASETS_CONTAINER)

            return dataset_client.delete_blob(name)
        except Exception as e:
            raise e 
    
    def delete_study_dataset(name):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_STUDY_DATASETS_CONTAINER)

            return dataset_client.delete_blob(name)
        except Exception as e:
            raise e 
    
    def upload_train_test_dataset(name, blob):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_TRAIN_TEST_CONTAINER)

            blob_client = dataset_client.get_blob_client(name)
            blob_client.upload_blob(blob)
        except Exception as e:
            raise e 
    
    def get_train_test_dataset(name):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_TRAIN_TEST_CONTAINER)

            blob_client = dataset_client.get_blob_client(name)

            return blob_client.url
        except Exception as e :
            raise e 
    
    def delete_train_test_dataset(name):
        try:
            dataset_client = ContainerClient.from_connection_string(AZURE_STORAGE_CONN_STRING, AZURE_TRAIN_TEST_CONTAINER)

            return dataset_client.delete_blob(name)
        except Exception as e:
            raise e 