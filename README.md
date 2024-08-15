
# Inter-process Communication Application

## Description

This project is an inter-process communication application where multiple processes communicate with each other using the publish-subscribe messaging pattern. The application simulates a system where one process (`MotionDetector`) publishes motion messages, a second process (`SingleShotDetector`) consumes these messages and publishes detection results, and a third process (`Logger`) logs all the messages.

The application is built in Python using the `multiprocessing` module to manage the processes and pass messages between them via queues.

### Key Components

- **MotionDetector**: A process that generates motion vectors (`MotionVector`) and publishes them to a queue.
- **SingleShotDetector**: A process that consumes motion vectors and generates detection vectors (`DetectionVector`).
- **Logger**: A process that logs all vectors (both `MotionVector` and `DetectionVector`) to the console.

### Project Structure

- `inter_process_communication/`
  - `main.py`: The main script for running the application.
  - `application_business_rules/`: Contains the business logic for processing the vectors.
  - `interface_adapters/`: Contains adapters for interfacing with the core logic.
- `tests`: Contains tests

### Requirements

- Python >= 3.12
- Dependencies for tests and linter are listed in `requirements-dev.txt`

### Installation

1. **Clone the repository**:

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

### Running the Application

You can run the application using the `main.py` script. It accepts one argument, `count`, which specifies the number of `MotionVector` instances to generate and process.

```bash
python inter_process_communication/main.py 10
```

This command will start the application, generate 10 motion vectors, and process them through the system.

### Running Tests

The tests are located in the `tests` directory. To run the tests, you can use `pytest`. To ensure that the application can correctly locate the modules, you may need to set the PYTHONPATH environment variable before running the tests. This ensures that Python knows where to find the project files.

1. **Navigate to the project directory and set the PYTHONPATH**:

   ```bash
   cd inter_process_communication
   export PYTHONPATH=$(pwd)
   cd ..
   ```

2. **Install test dependencies**:

   ```bash
   pip install -r requirements-dev.txt
   ```

3. **Run the tests**:

   ```bash
   pytest tests
   ```

### Docker Setup

The project includes a `Dockerfile` and a `docker-compose.yml` file for containerization.

1. **Build the Docker image**:

   ```bash
   docker build -t inter-process-app .
   ```

2. **Run the application using Docker Compose**:

   ```bash
   COUNT=10 docker-compose up
   ```

   This command will build the Docker image (if not already built) and start the application, generating 10 motion vectors in a containerized environment.

### Additional Information

- The `MotionVector` and `DetectionVector` are dummy messages designed to simulate real-life computer vision applications, where a motion detector feeds images to a single-shot detector to detect objects like cars and bikes in a video stream.
- The `StopVector` is a special vector used to signal the end of the message stream.
