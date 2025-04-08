# Pull python base image
FROM python:3.11.11

# Add requirements.txt file
ADD requirements.txt .
ADD model/ . 

# Update pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Add application file
ADD ml_gradio_deploy.py .

# Expose port where your application will be running
EXPOSE 7860

# Start application
CMD ["python", "main.py"]