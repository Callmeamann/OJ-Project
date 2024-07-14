# Use the official Python image from the Docker Hub as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE onlineJudge.settings

# Set the working directory in the container
WORKDIR /code_arena

# Copy the requirements.txt file into the container
COPY requirements.txt /code_arena/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install g++ and default-jdk for Java
RUN apt-get update && \
    apt-get install -y g++ default-jdk && \
    apt-get clean

# Copy the entire project into the container
COPY . /code_arena/

# Expose port 8000 for the Django app
EXPOSE 8000

# Run database migrations
RUN python manage.py migrate

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
