import logging
import os
import requests
from requests_toolbelt import MultipartEncoder
import json

CAMUNDA = os.getenv('CAMUNDA','http://camunda-server-camunda-bpm-platform:8080/engine-rest')   # This is the default

def deployToCamunda():
    for (_, _, files) in os.walk('.', topdown=True):
        for f in files:
            if ".bpmn" in f:
                # print(f)
                m = MultipartEncoder(fields={'deployment-name': f.split(".")[0], 'deployment-source': 'Digi:T Deployer', 'deploy-changed-only': 'true', f: (f, open(f, 'rb'), 'text/xml')})
                r = requests.post(f"{CAMUNDA}/deployment/create", data=m, headers={'Content-Type': m.content_type})
                pres = r.json()
                depstr = "Already " if pres['deployedProcessDefinitions'] == None else ""
                print(f"{f}: {depstr}deployed")
                # print(json.dumps(r.json(), indent=4, sort_keys=True))

if __name__ == '__main__':
    logging.info("Starting "+__name__)
    deployToCamunda()
