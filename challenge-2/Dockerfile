# Base image with glibc 2.35+ (required for the vuln binary)
FROM ubuntu:22.04

# Install required tools
RUN apt-get update && apt-get install -y \
    socat \
    gcc-multilib \
    libc6 \
    libc6-dev \
    wget

# Create a non-root user for the challenge
RUN useradd -m ctf

# Set up the working directory
WORKDIR /home/ctf/

# Copy challenge files into the container
COPY vuln .
COPY canary1.txt .
COPY canary2.txt .
COPY flag.txt .
COPY start.sh .

# Set file permissions
RUN chmod 750 vuln \
    && chmod 440 canary1.txt canary2.txt flag.txt \
    && chmod +x start.sh \
    && chown ctf:ctf vuln canary1.txt canary2.txt flag.txt start.sh

# Expose the challenge port
EXPOSE 1337

# Start the challenge
CMD ["bash", "./start.sh"]