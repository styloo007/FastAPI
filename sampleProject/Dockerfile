# Use Python 3.10.6
FROM python:3.10.6

# Set Working Directory
WORKDIR /app

# Copy Requirements Text file
COPY requirements.txt .

# Install System Dependencies
RUN pip install -r requirements.txt

# Copy Rest of the application code
COPY . .

# Expose Port
EXPOSE 8000

# Command to Run the Application
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]