# Use an official Python runtime as a parent image
FROM python:3.10-slim


# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Change working directory to mysite
WORKDIR /app/mysite

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port that the Django app runs on
EXPOSE 80

# Start the Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]