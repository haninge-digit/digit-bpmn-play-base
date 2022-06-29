import logging
import os
import grpc
from zeebe_grpc import gateway_pb2, gateway_pb2_grpc

ZEEBE_ADDRESS = os.getenv('ZEEBE_ADDRESS',"localhost:26500")

def deployToCamunda():
    with grpc.insecure_channel(ZEEBE_ADDRESS) as channel:
        stub = gateway_pb2_grpc.GatewayStub(channel)
        for f in os.listdir():      # Don't traverse the directory for the moment
            if ".bpmn" in f:
                logging.info(f"Trying to deploy {f} to Camunda")
                with open(f, "rb") as process_definition_file:
                    process_definition = process_definition_file.read()
                    process = gateway_pb2.Resource(name=f,content=process_definition)
                    response = stub.DeployResource(gateway_pb2.DeployResourceRequest(resources=[process]))
                    logging.info(f"Deployed BPMN process {response.deployments[0].process.bpmnProcessId} as version {response.deployments[0].process.version}")

if __name__ == '__main__':
    if os.getenv('DEBUG','false') == "true": # Debug requested
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(message)s")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")     # Default logging level

    logging.info(f"Starting deployToCamunda")
    deployToCamunda()
