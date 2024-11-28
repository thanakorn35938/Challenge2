import torch
import time

# Check if GPU is available
if not torch.cuda.is_available():
    print("CUDA is not available. Please check your GPU setup.")
else:
    # Set the device to GPU
    device = torch.device("cuda")

    # Define the size of the matrices
    size = 10000

    # Create random matrices
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    # Warm up the GPU
    for _ in range(10):
        torch.matmul(a, b)

    # Measure the time taken for matrix multiplication
    start_time = time.time()
    for _ in range(10):
        torch.matmul(a, b)
    end_time = time.time()

    # Calculate the average time per multiplication
    avg_time = (end_time - start_time) / 10
    print(f"Average time for matrix multiplication on GPU: {avg_time:.6f} seconds")
    # Run the matrix multiplication continuously
    iteration = 0
    try:
        while True:
            torch.matmul(a, b)
            iteration += 1
            if iteration % 100 == 0:
                print(f"Iteration: {iteration}")
    except RuntimeError as e:
        print(f"RuntimeError: {e}")
    except KeyboardInterrupt:
        print("Process interrupted by user.")