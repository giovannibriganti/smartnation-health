# Use an official Python runtime as a parent image
FROM mongo:latest

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port for the FastAPI application
EXPOSE 8000

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add wait-for-it.sh to the container
#ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /app/wait-for-it.sh
#RUN chmod +x /app/wait-for-it.sh

# CMD ["./wait-for-it.sh", "127.0.0.1:11434", "--", "python", "mistral_api.py"]
# Start MongoDB
CMD ["uvicorn", "nosql.app.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

