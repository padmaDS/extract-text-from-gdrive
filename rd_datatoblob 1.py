from azure.storage.blob import BlobServiceClient
import os

base_file_path = '/content/Answer.mp3'

# Replace 'your_account_key' with your actual Azure Storage account key
account_key = ''
account_name = ''
container_name = ''

# Construct the BlobServiceClient using the account key
service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net", credential=account_key)

def upload_file(source, container_client):
    dest_blob_name = os.path.basename(source)
    print(f'Uploading {source} to {dest_blob_name}')
    with open(source, 'rb') as data:
        container_client.upload_blob(name=dest_blob_name, data=data)
    print(f'Successfully uploaded {source}')

try:
    source = base_file_path
    container_client = service_client.get_container_client(container_name)
    print(f'Connected to Azure Blob Storage container: {container_name}')
except Exception as ex:
    print('Exception during connection to Azure Blob Storage:')
    print(ex)

if __name__ == '__main__':
    try:
        upload_file(source=source, container_client=container_client)
        print('File upload completed successfully.')
    except Exception as ex:
        print('Exception during file upload:')
        print(ex)

