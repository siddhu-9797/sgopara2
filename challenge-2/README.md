# Problem Dev 2

This problem includes a vulnerable binary. The objective is to bypass 2 stack 
canaries (referred  as soldiers), overflow the buffer and 
redirect the execution to `castle()` function to retrieve the flag.

1st canary value is provided to the user at run time but the 2nd canary value 
is hidden from the user.

The user has to bruteforce the 2nd canary value byte-by-byte, identify the 
placement of both canaries in the stack to bypass and overflow the stack.

To make the challenge a little harder, the source code of the binary is 
not provided to the user.

##Solution Approach:

To solve this challenge, follow these steps:

1. **Analyze the Binary**:
    - ncat and run the binary:
     ```bash
     nc localhost 1337
     ```
    - Alternatively, run the binary locally by downloading from the portal
   - Use `objdump`, `readelf`, or `gdb` to locate the address of the `win()` 
     function:
     ```bash
     objdump -d vuln | grep win
     ```

2. **Understand the Vulnerability**:
   - The program has a buffer of size 64 bytes, followed by two canaries.
   - Canary 1 is leaked in the output. Canary 2 is hidden.
   - The goal is to construct a payload to overflow the buffer, replace the canary values
     with their respective values, add 10 extra bytes padding to reach the return address
     and overwrite the return address to call `win()`.
   - Here, the canary value should be identified byte-by-byte by bruteforcing every possible
     value from 0x00 to 0xff 

3. **Exploit Construction**:
   - Connect to the program using `nc`:
     ```bash
     nc localhost 1337
     ```
   - Read `Canary 1` from the program's output.
   - Build a payload:
     - Overflow the buffer with 64 bytes of junk.
     - Add `Canary 1` (4 bytes).
     - Add `Canary 2` (6 bytes).
     - Add 10 bytes of padding to align the stack.
     - Overwrite the return address with the `win()` function's address.

4. **Payload Execution**:
   - Send the payload length as the first input.
   - Send the payload as the second input.

5. **Retrieve the Flag**:
   - Once the `win()` function is executed, the program will print the flag.


Steps to run the container,

Build the container:
docker build -t sgopara2 .
docker run -p 5002:5002 -p 5003:5003 sgopara2

After building and running the docker container, they can be access via:
portal_a => http://127.0.0.1:5002
portal_b => http://127.0.0.1:5003


## Directory Structure

