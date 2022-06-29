# Playing with same base BPMN
Contains some "playable" BPMN-processes

Repo contains a set of BPMN-files as well as a "Camunda deployer", that deplays all the processes in the directory to Camunda. Can be run locally after cocceting to Camunda with 
```bash
kubectl port-forward svc/camunda8-zeebe-gateway 26500:26500 -n camunda8
```

Deployment through a Github action is on it's way...

## echo.bpmn
A process with two actions. One is an external worker that does nothing 
A simple GET process that echos back call parameters as a json struct
