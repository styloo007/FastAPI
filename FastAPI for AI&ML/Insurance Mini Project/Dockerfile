# Use Python 3.10.6
FROM python:3.10.6-slim

# Set working directory
WORKDIR /app

# Copy Requirements Text File
COPY requirements.txt .

# Install Python Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the other code files
COPY . .

# Expose Port
EXPOSE 8000 8501

# Run the Application
CMD uvicorn apiEndpoint:app --host 0.0.0.0 --port 8000 & streamlit run frontend.py --server.address 0.0.0.0 --server.port 8501
