import json
import requests

def main(file_name, id_folder, file_directory):
    print(saveFile(file_name, id_folder, file_directory))
    
def getToken():
    r = requests.post(
        'https://www.googleapis.com/oauth2/v4/token',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'refresh_token',
            'client_id': readCredentials()['client_id'],
            'client_secret': readCredentials()['client_secret'],
            'refresh_token': readCredentials()['refresh_token'],
        }
    )
    data_dict = json.loads(r.text)
    return data_dict["access_token"]

def saveFile(file_name, id_folder, file_directory):
    headers = {"Authorization": "Bearer " + getToken()}
    para = {
        "name": file_name,
        "parents": [id_folder]
    }

    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open(file_directory, "rb")
    }

    url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&supportsAllDrives=true&includeItemsFromAllDrives=true"
    r = requests.post(
        url,
        headers=headers,
        files=files
    )
    return r.text

def readCredentials():
    with open("credentials.json", "r") as f:
        data = json.load(f)
    return data

def readFiles():
    with open("files.json", "r") as f:
        data = json.load(f)
    return data

if __name__ == '__main__':
    main(readFiles()['file_name'], readFiles()['id_folder'], readFiles()['file_directory'])
