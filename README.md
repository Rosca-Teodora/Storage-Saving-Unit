# Storage Saving Unit

This is a college project designed to mimic the memory allocation processes of a minimal operating system. It implements a fundamental file system that manages storage space by allocating, retrieving, freeing, and organizing data memory blocks. The entire logic is written in 32-bit x86 Assembly and relies on standard C library functions (`printf`, `scanf`) for input/output operations.

## 🗂️ Project Structure

The project explores memory management in two distinct spatial dimensions, separated into two main source files:

* **`UnidimensionalSpace.s`**: Manages a continuous, 1D memory array of 1024 bytes. Space is allocated in blocks (8 bytes per block). It handles linear contiguous memory allocation and defragmentation.
* **`BidimensionalSpace.s`**: Manages a 2D memory grid (1024 x 1024, equating to 1MB of memory). It implements row-by-row allocation, calculating block positions across lines and columns, and moving elements during defragmentation using an auxiliary memory matrix.

## ⚙️ Supported Operations

The system processes a sequence of operations required for a healthy file system. The operations are triggered by entering specific numerical codes:

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

## 🚀 How to Build and Run

Since the code is written in 32-bit x86 Assembly and uses standard C functions, you will need `gcc` with multilib support to compile it on a modern 64-bit Linux system.

### Prerequisites
If you are on a 64-bit Debian/Ubuntu system, install the necessary 32-bit libraries:
```bash
sudo apt-get install gcc-multilib
```

### Compilation 

#### Compile the 1D space program
```bash
gcc -m32 -no-pie UnidimensionalSpace.s -o uni_space
```

#### Compile the 2D space program
```bash
gcc -m32 -no-pie BidimensionalSpace.s -o bi_space
```

### Execution 
```bash
./uni_space
# or
./bi_space
```
