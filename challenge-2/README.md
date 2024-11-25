# Problem Dev 2

This problem includes a vulnerable binary. The objective is to bypass identify and bypass 2 stack canaries (referred  as soldiers), overflow the buffer and redirect the execution to `win()` function to retrieve the flag.

1st canary value is provided to the user at run time but the 2nd canary value is hidden from the user.

The user has to bruteforce the 2nd canary value byte-by-byte, identify the placement of both canaries in the stack to bypass and overflow the stack.

To make the challenge a little harder, the source code of the binary is not provided to the user.

Steps to run the container,

Build the container:
docker build -t sgopara2 .
docker run -p 5002:5002 -p 5003:5003 sgopara2

After building and running the docker container, they can be access via:
portal_a => http://127.0.0.1:5002
portal_b => http://127.0.0.1:5003


## Directory Structure

