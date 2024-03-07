#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Tiago Silva Leite
# Version 1.3.2

# Create 2 items on host zabbix server, set variables to endpoints zabbix and ansible
# <ITEMID>, # Stdout Last Jobs
# <ITEMID>  # Status Last Job

# Schedule Jobs /5m
# */5 * * * * python3  /path/<script>.py


import requests,os,json,socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

host = socket.gethostname()
ip = socket.gethostbyname(host)
host_ansible = "<hostname_ansible"

def history_clear_data():

    # Zabbix Configuration
    zabbix_url  = '<ENDPOINT_ZABBIX>'
    username   = '<USERNAME>'
    password   = 'PASSWORD'

    # Create a session with custom SSL verification settings
    session = requests.Session()
    session.verify = False  # Disable SSL certificate verification

    auth_payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": username,
            "password": password,
        },
        "id": 1,
    }

    try:
        response = session.post(zabbix_url, data=json.dumps(auth_payload), headers={"Content-Type": "application/json"})
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        exit()

    # Parse the response
    auth_result = response.json()

    if "result" in auth_result:

        auth_token = auth_result["result"]
        print(f"Authentication successful. Auth token: {auth_token}")


        # Clear History Item API Zabbix - Request Json
        history_clear_data = {
        "jsonrpc": "2.0",
        "method": "history.clear",
        "params": [
            <ITEMID>, # Stdout Last Jobs
            <ITEMID>  # Status Last Job
        ],
        'auth': auth_token,
        'id': 2,
        }

        response = session.post(zabbix_url, data=json.dumps(history_clear_data), headers={'Content-Type': 'application/json'})
        result = response.json()

        if 'result' in result and result['result']:
            print('History cleared successfully.')
        else:
            print('Failed to clear history. Check the item ID and try again.')
    else:
        print('Authentication failed. Check your credentials.')


def get_last_jobs():

    ZBX_SENDER = '/usr/bin/zabbix_sender'
    tower_base_url = "<ENDPOINT_ANSIBLE>/api/v2/"
    tower_username = "<USERNAME>"
    tower_password = "<PASSWORD>"

    last_job_url = tower_base_url + "jobs/?order_by=-finished&page_size=1"

    session = requests.Session()
    session.auth = (tower_username, tower_password)
    session.verify = False

    response = session.get(last_job_url)

    if response.status_code == 200:
        data = response.json()
        if data.get('count', 0) > 0:
            last_job = data['results'][0]

            if str(last_job['status']) == "Failed":

                # Run function history_clear_data for clear history ITEM ID API ZABBIX
                history_clear_data()

                job_id       =    "Last Job ID: "           + str (last_job['id'])
                job_name     =    "Last Job Name: "         + str (last_job['name'])
                job_started  =    "Last Job Started: "      + str (last_job['started'])
                job_finished =    "Last Job finished: "     + str (last_job['finished'])
                job_type     =    "Last Job Type: "         + str (last_job['type'])
                job_playbook =    "Last Job Playbook: "     + str (last_job['playbook'])
                job_status   =    "Last Job Status: "       + str (last_job['status'])
                job_description = "Last Job Description: "  + str (last_job['description'])

                url_stdout = tower_base_url + "jobs/" + str(last_job['id']) +"/stdout/?format=txt"
                s = requests.Session()
                s.auth = (tower_username, tower_password)
                s.verify = False
                s.headers.update({'Content-Type': 'text/plain; utf-8'})
                response = s.get(url_stdout)

                if response.status_code == 200:

                    msg_stdout=response.text
                    l = "--------------------------------------------------------------------------------------------------------------"
                    msg = (job_id + "\n" + job_name + "\n" + job_started + "\n" + job_finished + "\n" + job_status + "\n" + job_playbook + "\n" + job_description + "\n\n" + str(l) + "\n" + str(msg_stdout))
#                    print(msg)

                    # Send Details Failed Job
                    cmd = ZBX_SENDER + " -z " + ip + " -p 10051 " + " -s " + host_ansible  + " -k " + "jobs.details"  +  " -o \"" +  str(msg) +"\""
                    os.system(cmd)

                    # Send trap
                    cmd = ZBX_SENDER + " -z " + ip + " -p 10051 " + " -s " + host_ansible  + " -k " + "jobs.status"  +  " -o \"" +  "0"  +"\""
                    os.system(cmd)
                else:
                    print(f'Request failed with status code {response.status_code}')

            elif str(last_job['status']) != "Failed":

                    history_clear_data()
                    # Send trap
                    cmd = ZBX_SENDER + " -z " + ip + " -p 10051 " + " -s " + host_ansible  + " -k " + "jobs.status"  +  " -o \"" +  "1"  +"\""
                    os.system(cmd)

            else:
                # Run function history_clear_data for clear history ITEM ID API ZABBIX
                history_clear_data()
                cmd = ZBX_SENDER + " -z " + ip + " -p 10051 " + " -s " + host_ansible  + " -k " + "jobs.status"  +  " -o \"" + "1"  +"\""
                os.system(cmd)

        else:
            print("No jobs found.")
    else:
        print(f"Failed to retrieve job status. Status code: {response.status_code}")
        print(response.text)

    session.close()

get_last_jobs()
#history_clear_data()