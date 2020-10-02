# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import requests


def get_token(client_id, client_secret):
    url = 'https://connect-api.cloud.huawei.com/api/oauth2/v1/token'
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, json=body)
    if response.status_code == 200:
        json = response.json()
        return json['access_token']
    else:
        print('token: ' + str(response.status_code) + ': ' + response.reason)


def get_upload_url(access_token, client_id, app_id):
    url = 'https://connect-api.cloud.huawei.com/api/publish/v2/upload-url'
    params = {
        'appId': app_id,
        'suffix': 'apk'
    }
    headers = {
        'client_id': client_id,
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        json = response.json()
        return json['uploadUrl'], json['authCode']
    else:
        print('upload-url: ' + str(response.status_code) + ': ' + response.reason)


def upload_file(upload_url, auth_code, path_file, access_token, client_id, app_id):
    headers = {
        "accept": "application/json"
    }
    body = {
        'authCode': auth_code,
        'fileCount': '1'
    }
    with open(path_file, 'rb') as f:
        response = requests.post(upload_url, files={'file_name': f}, data=body, headers=headers)
        if response.status_code == 200:
            json = response.json()
            fileInfoList = json['result']['UploadFileRsp']['fileInfoList'][0]
            update_app_file_info(file_url=fileInfoList['fileDestUlr'],
                                 file_size=fileInfoList['size'],
                                 client_id=client_id,
                                 access_token=access_token,
                                 app_id=app_id)
        else:
            print('upload-file: ' + str(response.status_code) + ': ' + response.reason)


def update_app_file_info(file_url, file_size, client_id, access_token, app_id):
    url = 'https://connect-api.cloud.huawei.com/api/publish/v2/app-file-info'
    headers = {
        'client_id': client_id,
        'Authorization': 'Bearer ' + access_token
    }
    body = {
        'fileType': 5,
        'files': [{
            'fileName': 'this_is_a_new.apk',
            'fileDestUrl': file_url,
            'size': file_size
        }]
    }
    params = {
        'appId': app_id
    }
    response = requests.put(url, headers=headers, json=body, params=params)
    if response.status_code == 200:
        json = response.json()
        pkgVersion = json['pkgVersion'][0]
        msg = json['ret']['msg']
        code = json['ret']['code']
        print str(pkgVersion) + ', ' + msg + ', ' + str(code)
    else:
        print('app-file-info: ' + str(response.status_code) + ': ' + response.reason)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app_id = '102297755'
    client_id = '428480937370584064'
    client_secret = '89B14190595D0785516119D613E704B0E73EF9EC6B9503CFBC8A0C2217048DE5'
    access_token = get_token(client_id=client_id,
                             client_secret=client_secret)
    upload_url, auth_code = get_upload_url(access_token=access_token,
                                           client_id=client_id,
                                           app_id=app_id)
    upload_file(upload_url=upload_url,
                auth_code=auth_code,
                path_file='/Users/alvarez/Developer/facts-android/app/release/this_is_a_new.apk',
                access_token=access_token,
                client_id=client_id,
                app_id=app_id)
