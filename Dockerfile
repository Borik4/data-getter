FROM python:3.8-slim

# Create and set the working directory to /app
WORKDIR /app

# Copy only the requirements file to the container at /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Run the application
CMD ["python", "main.py"]
