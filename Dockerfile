# Use an official MySQL runtime as a parent image
FROM mysql:latest

# Environment variables
ENV MYSQL_ROOT_PASSWORD=root_password
ENV MYSQL_DATABASE=your_database
ENV MYSQL_USER=your_username
ENV MYSQL_PASSWORD=your_password

# Optionally, you can customize additional MySQL configurations here

# Expose the MySQL port
EXPOSE 3306
