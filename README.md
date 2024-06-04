# Access-Key-Manager

Deplyed url: https://access-key-manager-c55r.onrender.com

### Prerequisites

- Docker

### Installing and Running


1. Clone the repository:

    git clone https://github.com/KaySela/Access-Key-Manager.git
    

2. Navigate to the project directory:

    cd Access-Key-Manager
    

3. Create a .env file and set values, dont change already provided values

    ACCESS_TOKEN_LIFETIME=
    SECRET_KEY=
    DB_NAME=
    DB_USER=
    DB_PASSWORD=
    DB_HOST=db
    DB_PORT=5432
    MICRO_ADMIN_EMAIL=
    MICRO_ADMIN_PASSWORD=
    EMAIL_HOST_ADDRESS=
    EMAIL_HOST_PASSWORD=
    REDIS_HOST=redis

3. Build and run the Docker containers:
    
    docker-compose up --build -d


The application should now be running at [http://localhost:8000](http://localhost:8000)

