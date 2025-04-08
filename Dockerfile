# Pull python base image
FROM python:3.11.11

# Add requirements.txt file
ADD requirements.txt .

# Update pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt


# Add application file
ADD model/ model/rfc_model.pkl .
ADD ml_gradio_deploy.py .

# Expose port where your application will be running
EXPOSE 7860

# Start application
CMD ["python", "ml_gradio_deploy.py"]