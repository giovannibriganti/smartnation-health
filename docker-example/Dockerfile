# Use an official Python runtime as a parent image
FROM python:3.13-slim-trixie

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add wait-for-it.sh to the container
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

CMD ["./wait-for-it.sh", "127.0.0.1:11434", "--", "python", "mistral_api.py"]
