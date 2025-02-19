# InfiniPlex Assignment

### Steps to run the program:

1. Make sure Docker is installed on your machine
Clone this repository:
<code> git clone https://github.com/evasolal/infiniplex.git </code>

2. Navigate to the project directory:
<code> cd infiniplex </code>

3. Build the Docker image:
<code> docker build -t my-django-app . </code>

4. Run the Docker container:
<code> docker run -p 8000:8000 my-django-app </code>

Access the application at <code> http://localhost:8000/upload_csv </code>
