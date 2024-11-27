# Problem Dev 1

This problem includes two web applications, `portal_a` and `portal_b`, which 
together create the CTF challenge. Each portal has unique functionalities and 
is designed to run together on single docker container.

Solution approach:
1. **Portal-A**:
    - Any email other than admin does not have MFA enabled. 
    So, login as a non-admin using any email. XOR between 
    the unique two strings in the OTP page logs in to the portal
    - 10 boxes are provided and only one box has the right reward.
      Each box has a hidden value which can be decoded as Base64 decode and 
      Base 64 decode and JWT decode. The final JWT string has the 'admin' 
      value set to true.
    - After the right box is chosen, the MFA password of the admin is provided
    - Login in as admin and the invite token to the 2nd portal is provided.
      
2. **Portal-B**
    - Make a GET request to the Portal B using the 'token' value as the value 
      gound from portal A
    - The user will be provided access to the portal as admin. But only super 
      admin can retrieve the flag.
    - To become a super admin, decode the session cookie using flask-unsign, 
      make the super_admin=True and sign it using key that is bruteforced 
      with any common wordlist. The actual key is 'iloveyou'
    - Using the cracked cookie, make a request to the portal and 
      the flag is rewarded.


Steps to run the container,

Build the container:
docker build -t sgopara2 .
docker run -p 5002:5002 -p 5003:5003 sgopara2

After building and running the docker container, they can be access via:
portal_a => http://127.0.0.1:5002
portal_b => http://127.0.0.1:5003


## Directory Structure

