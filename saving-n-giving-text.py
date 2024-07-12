import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# Replace with your credentials JSON file path
credentials_file = 'cmodemo-37fe59a38620.json'

# Replace with your file path (e.g., image with Telugu text)
file_path = r'gray_image_2290.jpg'

def authenticate():
    scopes = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/documents']
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file, scopes=scopes)
    return build('drive', 'v3', credentials=credentials), build('docs', 'v1', credentials=credentials)

def upload_file_to_drive(drive_service, file_path):
    file_metadata = {
        'name': 'Image_with_telugu_text.png'  # Replace with desired file name in Google Drive
    }
    media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype='image/png')
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"Uploaded image with ID: {file.get('id')}")
    return file.get('id')

def convert_file_to_google_docs(drive_service, docs_service, file_id):
    try:
        # Convert the file to a Google Docs document
        metadata = {
            'parents': ['root'],  # Replace with the ID of the parent folder if needed
            'name': 'Google_Docs_from_File',
            'mimeType': 'application/vnd.google-apps.document',
            'contentHints': {
                'thumbnail': {
                    'image': {
                        'imageId': file_id
                    }
                }
            }
        }
        doc = drive_service.files().copy(fileId=file_id, body=metadata).execute()
        doc_id = doc.get('id')

        # Retrieve text content from the Google Docs document
        doc_content = docs_service.documents().get(documentId=doc_id).execute()
        text_content = ""
        for content in doc_content.get('body').get('content'):
            if 'paragraph' in content:
                for element in content['paragraph']['elements']:
                    if 'textRun' in element:
                        text_content += element['textRun']['content']

        # Save text content to a file or process it further
        with open('strip_text.txt', 'w', encoding='utf-8') as f:
            f.write(text_content)

        print(f"Extracted text saved to strip_text.txt")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    drive_service, docs_service = authenticate()

    # Upload file to Google Drive
    file_id = upload_file_to_drive(drive_service, file_path)

    # Convert file to Google Docs document and extract text
    convert_file_to_google_docs(drive_service, docs_service, file_id)

if __name__ == '__main__':
    main()
