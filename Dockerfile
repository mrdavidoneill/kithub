# Base image
FROM python:3.8.10

# Set work directory
ENV HOME=/usr/src/app/api
WORKDIR $HOME

# Create directory for static files
RUN mkdir $HOME/staticfiles

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy project
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Run starting script
RUN chmod +x ./scripts/wait-for-it.sh ./scripts/docker-entrypoint.sh
CMD ["./scripts/docker-entrypoint.sh"]
