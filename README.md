# EPS-Projekt

Python Protoc:
https://github.com/grpc/grpc/blob/master/tools/distrib/python/grpcio_tools/grpc_tools/protoc.py
python -m pip install grpcio-tools

protobuf compiler usage:
python -m grpc.tools.protoc --proto_path=. --python_out=. vehicledetectionmessage.proto