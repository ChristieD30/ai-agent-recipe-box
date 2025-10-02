# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir tabulate

# Create a directory for the database file with write permissions
RUN mkdir -p /data && chmod 777 /data

# Set environment variable to store the database in a persistent volume
ENV DB_PATH=/data/recipes.db

# Create an entrypoint script
RUN echo '#!/bin/bash\n\
# Initialize the database\npython /app/init_db.py\n\n# Start the application\npython /app/recipe_app.py\n' > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# Run the entrypoint script when the container launches
ENTRYPOINT ["/app/entrypoint.sh"]
