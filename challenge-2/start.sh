#!/bin/bash

# Start the vuln binary as a network service
exec socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"/home/ctf/vuln",stderr
