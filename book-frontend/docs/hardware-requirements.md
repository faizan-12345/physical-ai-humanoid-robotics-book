# Hardware Requirements

This section outlines the recommended and minimum hardware requirements for working with the concepts and examples presented in the Humanoid Robotics Book. These requirements are based on the need to run ROS 2, Gazebo, Unity (for visualization), and NVIDIA Isaac Sim for simulation and development.

## Workstation

### Minimum Requirements

*   **CPU**: Intel Core i5 or AMD Ryzen 5 (4 cores, 8 threads)
*   **RAM**: 16 GB
*   **GPU**: Integrated graphics (Intel UHD Graphics 620 or equivalent) - *sufficient for basic ROS 2 and Gazebo usage, limited simulation complexity*
*   **Storage**: 500 GB SSD
*   **OS**: Ubuntu 20.04 LTS or Windows 10/11 (64-bit)

### Recommended Requirements

*   **CPU**: Intel Core i7/i9 or AMD Ryzen 7/9 (8+ cores, 16+ threads)
*   **RAM**: 32 GB or more
*   **GPU**: NVIDIA RTX 3060 / RTX 4060 or higher (for Isaac Sim, Unity rendering, and complex Gazebo physics) with CUDA support
*   **Storage**: 1 TB NVMe SSD (for faster loading of large simulation environments and models)
*   **OS**: Ubuntu 22.04 LTS (preferred for ROS 2 development) or Windows 10/11 (64-bit)

## Edge Kits (Robot-Side Computing)

For running parts of the AI/robotics stack directly on the robot or a nearby compute unit:

*   **Platform**: NVIDIA Jetson Orin (AGX Orin or Orin NX/Nano), NVIDIA Jetson Xavier NX, or Intel NUC (with discrete GPU if possible)
*   **RAM**: 8 GB minimum, 16 GB recommended
*   **Storage**: 64 GB eMMC/SSD minimum, 256 GB recommended
*   **Connectivity**: Wi-Fi 6 (802.11ax) or Ethernet for reliable communication with base station or cloud services.

## Robot Lab / Physical Testing Environment

*   **Space**: A dedicated, obstacle-free area of at least 3m x 3m for basic navigation and interaction tests.
*   **Sensors**: A robot platform equipped with basic sensors (e.g., LIDAR, RGB-D camera, IMU) compatible with ROS 2 (e.g., TurtleBot3, Clearpath Husky, or custom ROS-compatible platform).
*   **Network Infrastructure**: Reliable Wi-Fi access point to facilitate communication between the robot and control stations/laptops.

## Notes

*   Running NVIDIA Isaac Sim requires an NVIDIA GPU with significant VRAM (e.g., RTX 3080/4080 or better) and a compatible CUDA version.
*   The requirements for Unity depend heavily on the complexity of the scenes and the desired rendering quality.
*   These requirements are estimates based on typical usage. Actual performance may vary depending on the specific simulation environments, robot models, and complexity of the AI algorithms being run.