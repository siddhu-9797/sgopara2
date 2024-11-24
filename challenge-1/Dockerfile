FROM python:3.12.7

# Set a working directory for the container
WORKDIR /app

# Copy the files for both applications
COPY app/portal_a /app/portal_a
COPY app/portal_b /app/portal_b

# Install dependencies for both applications
COPY app/portal_a/requirements.txt /app/portal_a/requirements.txt
COPY app/portal_b/requirements.txt /app/portal_b/requirements.txt
RUN pip install -r /app/portal_a/requirements.txt
RUN pip install -r /app/portal_b/requirements.txt

# Expose both ports (5000 for portal_a and 5001 for portal_b)
EXPOSE 5002 5003
# PUBLISH 5002 AS portal1
# PUBLISH 5003 AS portal2

RUN mkdir /challenge && chmod 700 /challenge
RUN echo "{\"flag\":\"FLAG{Super_Admin_Access_Granted}\"}" > /challenge/metadata.json


# Command to run both apps concurrently
CMD ["sh", "-c", "python /app/portal_a/app.py & python /app/portal_b/app.py"]
