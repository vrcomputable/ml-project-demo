# Pull python base image
FROM python:3.11.11

# Add requirements.txt file
ADD requirements.txt .

# Update pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt
RUN rm requirements.txt

# Add application file
ADD app/model/*.pkl app/model/.
ADD app/main.py app/.

# Expose port where your application will be running
EXPOSE 7860

# Start application
CMD ["python", "app/main.py"]