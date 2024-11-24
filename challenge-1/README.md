# Problem Dev 1

This problem includes two web applications, `portal_a` and `portal_b`, which 
together create the CTF challenge. Each portal has unique functionalities and 
is designed to run together on single docker container.

Steps to run the container,

Build the container:
docker build -t sgopara2 .
docker run -p 5002:5002 -p 5003:5003 sgopara2

After building and running the docker container, they can be access via:
portal_a => http://127.0.0.1:5002
portal_b => http://127.0.0.1:5003


## Directory Structure

