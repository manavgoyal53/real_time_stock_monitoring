

## Part 1: Running the Project with Docker Compose

### Prerequisites

- Docker and Docker Compose must be installed on your system.
- Ensure Redis is installed but not running on the host machine, as the application will use a Dockerized instance of Redis.

### Disabling Redis on the Host Machine

If Redis is already running on your host machine, you'll need to stop it to prevent conflicts with the Redis instance running in Docker.

### Running the Project

To run the project, simply use Docker Compose:

```bash
docker-compose up --build
```

This command will build the necessary Docker images and start the application, along with the required Redis service, if defined in your `docker-compose.yml` file.

### Shutting Down the Containers

Once you're done, you can stop and remove the running containers with the below command.

```bash
docker-compose down --volumes --remove-orphans
```

Remember this will also remove any persisting volumes and hence any db data. So you can use this command instead.

```bash
docker-compose down
```


## Part 2: Code Overview

This project implements a solver for a **Loop Puzzle**, where the goal is to form a closed loop by connecting dots on a grid. Each numbered cell in the grid specifies how many of its sides must be part of the loop. Empty cells (represented by `None`) do not impose any constraints.

The solver uses **Depth First Search (DFS)** to explore possible loops starting from an arbitrary point on the grid. It ensures that the number of edges around each numbered cell matches the cell's specified number. The algorithm skips cells that contain `None` and only checks the constraints for cells that contain numbers. The solution is complete when a valid, closed loop is formed that adheres to all constraints. If no valid loop can be found, the algorithm terminates with a message indicating failure.