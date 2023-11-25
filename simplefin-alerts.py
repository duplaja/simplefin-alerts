import datetime
import time
import requests
import base64
import pickle

def send_via_apprise(apprise_url,tag,content):

    payload='body='+content+'&tag='+tag
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", apprise_url, headers=headers, data=payload)

    return None

def list_to_string(lst):
    if not lst:
        return False
    else:
        return ' '.join(map(str, lst))

def setup_function(file_name):
    setup_token = input('SimpleFin Setup Token? ')

    claim_url = base64.b64decode(setup_token)
    response = requests.post(claim_url)
    access_url = response.text

    apprise_url = input('Apprise URL? (leave blank to skip) ')

    apprise_tag = input('Apprise Tag? (leave blank to skip) ')

    data = {"access_url":access_url, "apprise_url":apprise_url, "apprise_tag":apprise_tag}
        
    with open(file_name,"wb") as  file:
        pickle.dump(data, file)
        file.close()

    return None


def main():

    file_name = "simplefin-data.pickle"

    try:

        with open(file_name,"rb") as  file:
            data = pickle.load(file)
            access_url = data["access_url"]
            apprise_url = data["apprise_url"]
            apprise_tag = data["apprise_tag"]

            file.close()
    
    except IOError:   

        access_url = ''

    if not access_url:
    
        setup_function(file_name)

        with open(file_name,"rb") as  file:
            data = pickle.load(file)
            access_url = data["access_url"]
            apprise_url = data["apprise_url"]
            apprise_tag = data["apprise_tag"]

            file.close()
        
    scheme, rest = access_url.split('//', 1)
    auth, rest = rest.split('@', 1)

    url = scheme + '//' + rest + '/accounts'
    username, password = auth.split(':', 1)

    start_datetime = datetime.date(2023, 11, 1)
    start_unixtime = int(round(time.mktime(start_datetime.timetuple())))
    end_datetime = datetime.date(2023, 11, 2)
    end_unixtime = int(round(time.mktime(end_datetime.timetuple())))

    response = requests.get(url, auth=(username, password),params={'start-date': start_unixtime, 'end-date': end_unixtime})
    data = response.json()

    errors = data['errors']

    error_string = list_to_string(errors)

    if error_string:
        print(error_string)

        if apprise_url:
            send_via_apprise(apprise_url,apprise_tag,error_string)

    else:
        print('No SimpleFin Accounts in Error State')
        if apprise_url:
            send_via_apprise(apprise_url,apprise_tag,'No SimpleFin Accounts in Error State')
    
if __name__ == "__main__":
    main()
