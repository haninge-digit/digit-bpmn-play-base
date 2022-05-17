import logging
import os
import requests
from requests_toolbelt import MultipartEncoder
import json
import grpc
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc

CAMUNDA = os.getenv('CAMUNDA','http://camunda-api-server:8080/engine-rest')   # This is the default

def deployToCamunda():
    with grpc.insecure_channel("localhost:26500") as channel:
        stub = gateway_pb2_grpc.GatewayStub(channel)
        for (_, _, files) in os.walk('.', topdown=True):
            for f in files:
                if ".bpmn" in f:
                    # print(f)
                    with open(f, "rb") as process_definition_file:
                        process_definition = process_definition_file.read()
                        process = gateway_pb2.ProcessRequestObject(name=f,definition=process_definition)
                        stub.DeployProcess(gateway_pb2.DeployProcessRequest(processes=[process]))


                    # m = MultipartEncoder(fields={'deployment-name': f.split(".")[0], 'deployment-source': 'Digi:T Deployer', 'deploy-changed-only': 'true', f: (f, open(f, 'rb'), 'text/xml')})
                    # r = requests.post(f"{CAMUNDA}/deployment/create", data=m, headers={'Content-Type': m.content_type})
                    # pres = r.json()
                    depstr = "Already " if pres['deployedProcessDefinitions'] == None else ""
                    print(f"{f}: {depstr}deployed")
                    # print(json.dumps(r.json(), indent=4, sort_keys=True))

if __name__ == '__main__':
    logging.info("Starting "+__name__)
    deployToCamunda()




    # print the topology of the zeebe cluster
    topology = stub.Topology(gateway_pb2.TopologyRequest())
    print(topology)

    # deploy a process definition
