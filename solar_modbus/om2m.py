import requests
import json
import os

def get_credentials():
    """Get credentials from environment variables."""
    return {
        'username': os.getenv('DEV_USERNAME', ''),
        'password': os.getenv('DEV_PASSWORD', '')
    }

def create_cin(uri_cnt, value, cin_labels=["AE-SL", "SL-VN02-00", "V1.0.1", "SL-V1.0.1"], data_format="json", credentials=None):
    """
    Create a Content Instance (cin) in the specified container (cnt) URI.

    Args:
        uri_cnt (str): The URI of the container where the content instance will be created.
        value (str): The value to be stored in the content instance.
        cin_labels (list, optional): A list of labels to be associated with the content instance. Defaults to ["AE-SL", "SL-VN02-00", "V1.0.1", "SL-V1.0.1"].
        data_format (str, optional): The format of the data to be sent. Defaults to "json".
        credentials (dict, optional): A dictionary containing 'username' and 'password' for authentication. If None, credentials will be fetched using get_credentials().

    Returns:
        None

    Raises:
        TypeError: If there is an issue with the data format during the POST request.

    Prints:
        The HTTP status code and response content of the POST request.
    """
    if credentials is None:
        credentials = get_credentials()

    headers = {
        'X-M2M-Origin': f'{credentials["username"]}:{credentials["password"]}',
        'Content-type': f'application/{data_format};ty=4'
    }
    body = {
        "m2m:cin": {
            "con": "{}".format(value),
            "lbl": cin_labels,
            "cnf": "text"
        }
    }
    try:
        response = requests.post(uri_cnt, json=body, headers=headers)
    except TypeError:
        response = requests.post(uri_cnt, data=json.dumps(body), headers=headers)
    print('Return code : {}'.format(response.status_code))
    print('Return Content : {}'.format(response.text))

if __name__ == "__main__":
    _url = os.getenv('OM2M_URL', 'http://dev-onem2m.iiit.ac.in:443/~/in-cse/in-name/AE-EM/EM-CR-SB00-02/Data')
    data = "something"
    create_cin(_url, data)