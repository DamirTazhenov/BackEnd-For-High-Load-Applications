# Dockerfile for Django application

# Step 1: Use Python as a base image
FROM python:3.9-slim

# Step 2: Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 3: Set the working directory in the container
WORKDIR /app

# Step 4: Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Step 5: Install the required packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Step 6: Copy the Django project files into the container
COPY . /app/

# Step 7: Expose the port
EXPOSE 8000

# Step 8: Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
