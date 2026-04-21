# Storage Saving Unit

This is a college project designed to mimic the memory allocation processes of a minimal operating system. It implements a fundamental file system that manages storage space by allocating, retrieving, freeing, and organizing data memory blocks. The entire logic is written in 32-bit x86 Assembly and relies on standard C library functions (`printf`, `scanf`) for input/output operations.

## Project Structure

The project explores memory management in two distinct spatial dimensions, separated into two main source files:

* **`UnidimensionalSpace.s`**: Manages a continuous, 1D memory array of 1024 bytes. Space is allocated in blocks (8 bytes per block). It handles linear contiguous memory allocation and defragmentation.
* **`BidimensionalSpace.s`**: Manages a 2D memory grid (1024 x 1024, equating to 1MB of memory). It implements row-by-row allocation, calculating block positions across lines and columns, and moving elements during defragmentation using an auxiliary memory matrix.

## Supported Operations

The system processes a sequence of operations required for a healthy file system. The operations are triggered by entering specific numerical codes:

### Sample Input Explanation

The program first reads an integer `N`, representing the total number of top-level operations to be executed. Following this, it reads `N` sets of commands.

**Single Operations (GET, DELETE, DEFRAG):**
For most opcodes, the format is `opcode [parameters...]`.

**Batch Operation (ADD):**
The `ADD` operation (opcode `1`) is special. It reads a count for how many files to add, and then reads the data for each of those files.

For example, consider the following input:
```
3
1 2 10 100 20 50
2 10
3 20
```

Here's how it's interpreted:
1.  `3`: The program will execute 3 top-level operations.
2.  `1 2 10 100 20 50`: The first operation is `ADD` (opcode `1`).
    *   The `2` indicates that **two files** will be added in this batch.
    *   `10 100`: The first file has descriptor `10` and dimension `100`.
    *   `20 50`: The second file has descriptor `20` and dimension `50`.
3.  `2 10`: The second operation is `GET` (opcode `2`) for file descriptor `10`.
4.  `3 20`: The third operation is `DELETE` (opcode `3`) for file descriptor `20`.

The program reads these commands sequentially and processes them one by one.

1.  **ADD (Opcode: `1`)**: 
    * Allocates space for a file.
    * Requires a file descriptor (`descF`) and the size of the file (`dim`). 
    * The size is internally divided by 8 to determine the minimum number of 8-byte blocks needed (minimum 2 blocks). If space cannot be found, no allocation occurs.
2.  **GET (Opcode: `2`)**: 
    * Retrieves the exact memory coordinates of a stored file.
    * Requires the file descriptor (`descF`).
    * Outputs the starting and ending index/coordinates of the file. If the file is not found, it returns standard empty coordinates (e.g., `((0, 0), (0, 0))`).
3.  **DELETE (Opcode: `3`)**: 
    * Frees the memory blocks associated with a specific file descriptor.
    * Requires the file descriptor (`descF`).
    * Sets the previously occupied memory bytes back to `0`.
4.  **DEFRAG (Opcode: `4`)**: 
    * Organizes the memory by shifting all allocated blocks sequentially to the beginning of the memory space.
    * Eliminates empty gaps (fragmentation) created by deleted files, maximizing continuous free space for future allocations.

## How to Build and Run

This project can be built and run directly on a properly configured Linux machine or within a Docker container for a consistent, isolated environment. The Docker method is recommended to avoid potential issues with assembler versions on different host systems.


### Method 1: Running with Docker

This method uses the provided `Dockerfile` to create a consistent Ubuntu 20.04 environment, ensuring the code compiles as intended, regardless of your host system's configuration.

#### 1. Prerequisites
Ensure you have Docker installed on your system.

#### 2. Build the Docker Image
From the project's root directory, run the `docker build` command. This will create a Docker image named `storage-unit` containing the necessary environment and a copy of your code.
```bash
docker build -t storage-unit .
```

#### 3. Run an Interactive Container Session
Start a new container from the image. This command mounts your current project directory into the `/app` directory inside the container, so any changes you make to your code on your host machine will be reflected inside the container.
```bash
docker run -it --rm -v "$(pwd):/app" storage-unit bash
```
You will now have a `bash` prompt running inside the Ubuntu 20.04 container. To exit simply write the `exit` command.

#### 4. Compile and Run Inside the Container
From the container's command prompt, you can compile and run your programs just as you would locally.
```bash
# Compile the 1D space program
gcc -m32 -no-pie UnidimensionalSpace.s -o uni_space

# Run it
./uni_space

# Compile the 2D space program
gcc -m32 -no-pie BidimensionalSpace.s -o bi_space

# Run it
./bi_space
```

### Method 2: Running on a Local Linux Machine

This method requires you to have `gcc` and its 32-bit multilib libraries installed.

#### 1. Prerequisites
If you are on a 64-bit Debian/Ubuntu system, install the necessary 32-bit libraries:
```bash
sudo apt-get update
sudo apt-get install gcc-multilib
```

#### 2. Compilation 
Compile the desired program using `gcc`:
```bash
# Compile the 1D space program
gcc -m32 -no-pie UnidimensionalSpace.s -o uni_space

# Compile the 2D space program
gcc -m32 -no-pie BidimensionalSpace.s -o bi_space
```

#### 3. Execution 
Run the compiled executable. The program will wait for input from the standard input.
```bash
./uni_space
# or
./bi_space
```


## Comprehensive Test Suite

This project features a robust testing suite designed to ensure the memory allocation and file system operations are implemented correctly and reliably.

The project includes a comprehensive set of automated tests that cover a wide range of scenarios, from basic operations to complex sequences of memory manipulation. This ensures that both the `UnidimensionalSpace.s` and `BidimensionalSpace.s` implementations are fully validated for correctness and stability.

### Key Features of Our Testing Approach:

*   **Scenario-Based Validation**: Tests are organized into scenarios, each simulating a specific sequence of operations. This includes:
    *   **`add`**: Simple file allocation.
    *   **`add_get`**: Allocation followed by retrieval.
    *   **`add_delete`**: Allocation followed by deletion.
    *   **`add_get_delete`**: A full lifecycle of allocation, retrieval, and deletion.
    *   **`defragmentation`**: Scenarios that test the memory defragmentation logic.

*   **Automated Execution**: A Python script (`test.py`) automates the entire testing process. It compiles the Assembly code, runs each test case with the corresponding input, and compares the output against the expected results.

*   **Containerized Environment**: The tests are run in a containerized environment using Docker Compose (`compose.yaml`). This guarantees a consistent and reproducible testing environment, eliminating discrepancies between different development setups.

### How to Run the Tests

To run the automated tests, you can either use docker either run the Python scirpt on your own machine. Docker is recommended and there are 2 ways to do so: 

1.  **Start the Test Runner**:
    Open a terminal in the project's root directory and run the following command:
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker image, start the container, and automatically execute the `test.py` script, which runs all the test cases for both `UnidimensionalSpace.s` and `BidimensionalSpace.s`.

    The test script will print the results of each test case to the console, indicating whether the test passed or failed. This allows for quick and easy verification of the project's functionality.

    This rigorous testing methodology ensures that the project is not only a functional implementation of memory management concepts but also a reliable and well-engineered piece of software.

2. The container also includes `python3`. You can run the test suite directly from the container's prompt:
```bash
python3 test.py
```