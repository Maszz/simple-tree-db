# Tree Data Structure Management API

## Overview

This FastAPI application provides a RESTful API for managing a tree-like data structure. It includes functionalities for creating, querying, updating, and deleting nodes within a tree. The application uses Pydantic models for request and response validation, and the tree data is managed using a `TreeDataBase` instance.

## Features

- **Create Nodes**: Add new nodes to the tree with unique identifiers.
- **Query Tree Structure**: Retrieve the entire tree or specific nodes.
- **Update Nodes**: Modify existing nodes in the tree.
- **Delete Nodes**: Remove nodes from the tree.
- **Data Persistence**: The tree data can be saved to and loaded from a file.

## Installation

To set up the project, follow these steps:

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Install the required packages:
```bash
pip install -r requirements.txt

```

## Usage

 

To run the application:

0. Seed the db 
```bash
cd ./app
python seed.py
```

1. Start the server using Uvicorn:
```
cd ./app
python main.py
```

2. The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Returns a simple greeting message.
- `GET /items/query_tree`: Retrieves the entire tree structure.
- `GET /items/`: Gets a specific node or all child nodes based on the provided node identifier.
- `POST /items`: Creates a new node in the tree.
- `POST /items/update`: Updates an existing node in the tree.
- `POST /items/delete`: Deletes a node from the tree.

## Configuration

The application's configuration is managed through environment variables and a settings class, which can be modified in the `core.config` module.

## Container

> If you are using a Docker solution, please edit the .docker.env file instead of the .env file.

1. Build the container
```bash
docker build -t masz/tree-api .
```

2. compose the container
```bash
docker compose up -d
```


