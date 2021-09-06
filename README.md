# reloc

## Overview
This system assigns static sensors and mobile devices to edge servers so that resources on edge servers would not be consumed over limitation. The goal of this system is to enable static sensors deployed at road side to deliver messages to mobile devices such as vehicles with negligible latency. The sensors and mobile devices are in publisher/subscriber relationship.  



reloc assigns static sensors to edge servers to minimize delivery delay while satisfying the following conditions

- Memory capacity allocated for a microservice on every edge server would not be exhausted
- CPU allocated for a microservice on every edge server is not over limitation would not be exhaused



The delivery delay is calculated based on the following equation [1]:

<img src="https://reloc.s3.eu-north-1.amazonaws.com/equation.png">

Briefly, the delivery delay increases when

- The mentioned resources on edge servers, namely memory and CPU is exhaused
- Clients who has relation of publish/subscribe is assigned to distant edge servers



**Note:** This repository was created as an implementation of the system proposed in this paper (https://onlinelibrary.wiley.com/doi/10.1002/nem.2173). 



[1]  Tomoya Tanaka, Tomio Kamada, Chikara Ohta, “Topic allocation method on  edge servers for latency-sensitive notification service,” International  Journal of Network Management, 17 pages (e2173), June, 2021



## Usage

### Using docker

```
docker run -d -p 8080:8080 -e HOST_IP=172.17.0.1 -e EDGE_SERVER_CAPACITY=640 camsenec/reloc
```



### Configuration

- `HOST_IP`: your docker host ip
- `EDGE_SERVER_CAPACITY`: memory capacity assigned to an microservice managed by reloc



### Simulation

https://github.com/camsenec/reloc-evaluator

1. Register edge servers
2. Register sensors (clients)
3. A "home server" is assigned to each sensors based on the pub/sub relation among the sensors
4. Resource usage of edge servers are calculated by simulation.
5. Home server is updated so that any edge server's resource is not consumed over limitation.



### Sensor distribution

Sensors connected by gray line are publishers for a same topic.
<div align="center"><img width=700px src="https://reloc.s3.eu-north-1.amazonaws.com/client_distribution.png"></div>



### Home server assignment and resource usage

<div align="center"><img width=700px src="https://reloc.s3.eu-north-1.amazonaws.com/used.png"></div>



<div align="center"><img width=700px src="https://reloc.s3.eu-north-1.amazonaws.com/cp.png"></div>






## API

### Base URL

http://<host_name>/api/v1/manager



## Client

### [POST] (/user/post) register a client

+ Attributes (multipart/formdata)

  + `x` :  x coordinate of client position (latitude)
  + `y` :  y coordinate of client position (longitude)

- Parameters (URL parameter)
  - `application_id` : id of application the client who send request is using.

- Request Example

  ```bash
  curl -XPOST -F "x=30.0" -F "y=30.0" "http://localhost:8000/api/v1/manager/user/post/?application_id=1"
  ```


+ Response (Code 200)

  + Example value

    ```json
    {
     "application_id" : 1,
     "client_id" : 1149989,
     "x" : 30,
     "y" : 30,
     "home" : 89
    }
    ```



### [PUT] (/user/update_location) Update client position

Position data of the client is updated and new home server is allocated according to the mobility of a client. 

+ Attributes (multipart/formdata)

  + `x` :  x coordinate of current client position (latitude)
  + `y` :  y coordinate of current client position (longitude)


- Parameters (URL parameter)
  - `application_id` : id of application the client is using.
  - `client_id` : id of the client who send request

- Request Example

  ```bash
  curl -XPUT -F "x=70.0" -F "y=70.0" "http://localhost:8000/api/v1/manager/user/update_location/?application_id=1&client_id=1149989"
  ```

  

+ Response (Code 200)

  + Example value

    ```json
    {
     "application_id" : 1,
     "client_id" : 1149989,
     "x" : 70,
     "y" : 70,
     "home" : 45
    }
    ```



## Edge Server

### [POST] (server /post) Register an edge server

+ Attributes (multipart/formdata)

  + `x` :  x coordinate of server position (latitude)
  + `y` :  y coordinate of server position (longitude)
  + `capacity`: The cache capacity given to the application identified by the `applicaiton_id` field

- Parameters (URL parameter)
  - `application_id` : id of application the client who send request is using.

- Request Example

  ```bash
  curl -XPOST -F "x=30.0" -F "y=30.0" -F "capacity=640" "http://localhost:8000/api/v1/manager/server/post/?application_id=1"
  ```


+ Response (Code 200)

  + Example value

    ```json
    {
      "application_id": 1,
      "server_id": 18,
      "x": 30,
      "y": 30,
      "capacity": 640,
      "used": 0,
      "connection": 0,
      "cp": 0,
      "cluster_id": 1
    }
    ```
    



## Author

Tomoya Tanaka (deepsky2221@gmail.com)
