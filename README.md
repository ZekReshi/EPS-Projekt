# EPS-Projekt

## Before starting this program
Install Python 3.7.9 or higher (tested using Python 3.7.9).
Install all dependencies referenced in requirements.txt with a package manager of your choice. (e.g. pip install -r requirements.txt).

### Protobuf
Python Protoc:
https://github.com/grpc/grpc/blob/master/tools/distrib/python/grpcio_tools/grpc_tools/protoc.py
python -m pip install grpcio-tools

protobuf compiler usage:
python -m grpc.tools.protoc --proto_path=. --python_out=. vehicledetectionmessage.proto

## Execution
Launch the program by executing start.py inside the project root directory and one of the following arguments:
* camera
* blink
* sound