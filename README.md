# DB Utils

## Overview
DB Utils is a FastAPI application designed to facilitate the retrieval of similar product metadata using Qdrant for vector similarity search and Redis for metadata storage. This project is structured to provide a clean separation of concerns, with dedicated modules for database interactions and application settings.

## Features
- Fetch similar product option IDs based on a given `colorGroup_string`.
- Optionally retrieve metadata from Redis based on SKU IDs.
- Configurable database connections using environment variables.

## Project Structure
```
db-utils
├── src
│   ├── api
│   │   └── routes.py          # Defines FastAPI routes and endpoints
│   ├── db
│   │   ├── qdrant.py          # Qdrant class for similarity search
│   │   ├── redis.py           # Redis class for metadata fetching
│   │   └── __init__.py        # Initialization file for db package
│   ├── core
│   │   ├── settings.py        # Loads environment variables and configurations
│   │   └── __init__.py        # Initialization file for core package
│   ├── main.py                # Entry point of the application
│   └── __init__.py            # Initialization file for the application package
├── .env                        # Environment variables for database configurations
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd db-utils
   ```

2. Create a `.env` file in the root directory with the following structure:
   ```
   QDRANT_HOST=<your-qdrant-host>
   QDRANT_PORT=<your-qdrant-port>
   REDIS_HOST=<your-redis-host>
   REDIS_PORT=<your-redis-port>
   REDIS_PREFIX=<your-redis-prefix>
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn src.main:app --reload
   ```

## Usage
To fetch similar product metadata, send a POST request to the `/similar-products-metadata` endpoint with the following JSON body:
```json
{
  "colorGroup_string": "your_color_group_string",
  "dev": {
    "metadata": true
  }
}
```

## License
This project is licensed under the MIT License. See the LICENSE file for more details.