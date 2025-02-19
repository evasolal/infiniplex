# InfiniPlex Assignment

### Steps to run the program:

1. Make sure Docker is installed on your machine


2. Clone this repository:
<code> git clone https://github.com/evasolal/infiniplex.git </code>

3. Navigate to the project directory:
<code> cd infiniplex </code>

4. Build the Docker image:
<code> docker build -t infiniplex-app . </code>

5. Run the Docker container:
<code> docker run -p 8000:8000 infiniplex-app </code>

6. Access the application at <code> http://localhost:8000/upload_csv </code>
