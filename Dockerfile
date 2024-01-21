# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /code
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Install Pulumi
RUN curl -fsSL https://get.pulumi.com | sh

# Add Pulumi to the PATH
ENV PATH="/root/.pulumi/bin:${PATH}"

# Copy the api_pulumi directory contents into the container at /code/api_pulumi
COPY ./api_pulumi /code/api_pulumi

# Run uvicorn when the container launches
CMD ["uvicorn", "api_pulumi.app:app", "--host", "0.0.0.0", "--port", "8000"]
