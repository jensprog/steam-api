# API Design Assignment

## Project Name

**Steam Games Archive API**

## Objective

Design and develop a robust, well-documented API (REST or GraphQL) that allows users to retrieve and manage information from a dataset of your choice. The API must include JWT authentication, automated testing via Postman/Newman in a CI/CD pipeline, and be publicly deployed.

Choose a dataset (10000+ data points) that interests you — it should include at least one primary CRUD resource and two additional read-only resources. Sources like [Kaggle](https://www.kaggle.com/datasets), public APIs, or CSV files work well. Pick something you find interesting, as you will reuse this API in the next assignment (WT dashboard).

_Describe your API in a few sentences: what dataset does it serve, what are its main resources, and what can users do with it?_

- The dataset contains the games from the gaming platform Steam, the largest platform for PC.
- The main resource is Games, authenticated users can use CRUD operations.
- The second and third resources are Developers & Genres, those resources are only read-only (GET) and doesn't require authentication.

**Download the dataset from [kaggle](https://www.kaggle.com/datasets/fronkongames/steam-games-dataset)**

You will need to have an account on kaggle.com to download datasets.

### Prerequisites

1. Create a Kaggle account at [kaggle.com](https://kaggle.com)
2. Go to Account -> Create new API Token to download `kaggle.json`

### Installation & Download

**Linux/Ubuntu:**

```bash
sudo apt update
sudo apt install pipx
pipx ensurepath
source ~/.bashrc
pipx install kaggle
```

**macOS:**

```bash
brew install pipx
pipx ensurepath
source ~/.zshrc
pipx install kaggle
```

**Windows:**

```powershell
pip install kaggle
```

### Configure Kaggle API Credentials

After downloading kaggle.json, move it to the correct location:
**Linux/MacOS**:

```bash
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json
```

**Windows**:

```powershell
mkdir $HOME\.kaggle
move $HOME\Downloads\kaggle.json $HOME\.kaggle\
```

### Verify Kaggle CLI setup

```bash
kaggle datasets list
```

### Download Dataset

```bash
kaggle datasets download fronkongames/steam-games-dataset -p data/ --unzip
```

This will download:

- `data/games.csv`
- `data/games.json`

### Recommended File

My recommendation is to use the games.json file instead of the csv file. Json file is more reliable and has a better structure.

### Alternative installation & download

You can also download manually from the Kaggle website and extract to the data/ folder.

## Database Setup

### Running the Seed Script

To populate the database with sample data:

```bash
# Activate virtual environment
source venv/bin/activate

# Run the seed script
python app/seed/steamgames.py
```

This will load 15.000 games with their associated developers and genres from the Steam games dataset.

To clear the database before re-seeding:

```bash
python app/clearDatabase.py
```

## Implementation Type

The API is implemented using REST principles.

## Links and Testing

|                            | URL / File                            |
| -------------------------- | ------------------------------------- |
| **Production API**         | _https://cu2107.camp.lnu.se_          |
| **API Documentation**      | _https://cu2107.camp.lnu.se/docs_     |
| **Postman Collection**     | `SteamAPI.postman_collection.json`    |
| **Production Environment** | `production.postman_environment.json` |

**Examiner can verify tests in one of the following ways:**

1. **CI/CD pipeline** — check the pipeline output in GitLab for test results.
2. **Run manually** — no setup needed:
   ```
   npx newman run SteamAPI.postman_collection.json -e production.postman_environment.json --insecure
   ```

## Dataset

_Describe the dataset you chose:_

| Field                                | Description                                                     |
| ------------------------------------ | --------------------------------------------------------------- |
| **Dataset source**                   | Kaggle - Steam Games Dataset                                    |
| **Primary resource (CRUD)**          | Games (id, name, price, developer, genre, rating, release_date) |
| **Secondary resource 1 (read-only)** | Developers (id, name, games_count)                              |
| **Secondary resource 2 (read-only)** | Genres (id, name, games_count)                                  |

## Design Decisions

### Authentication

JWT is required for 3 endpoints:

- POST /games
- PUT /games/{id}
- DELETE /games/{id}

JWT authentication was a requirement for this project. The implementation follows REST principles by being stateless - each request contains all necessary authentication information.

**Implementation details:**

- Token expires after 30 minutes for security.
- Only write operations (POST, PUT, DELETE) require authentication.
- Read operations remain publicly accessible.
- Bearer token sent via Authorization header.

**Token Refresh:**
Will be implemented when frontend is going to be built.

## API Design

### HATEOAS

**1. Pagination Links (`build_pagination_links`):**

- Generates `self`, `next` and `previous` links for paginated results.
- Used in all list endpoints (/games, /developers, /genres).
- Improves navigation through large datasets.

**2. Resource Links (`build_resource_links`):**

- Creates hypermedia links for individual resources.
- `include_crud=True` for games (shows update/delete links for authenticated users).
- `include_crud=False` for read-only resources (developers/genres).

**3. Related Resource Links (serializer.py):**

- Creates domain-specific links between related resources.
- Games link to their developers and genres.
- Developers and genres link back to their games.
- Only included when `include_links=True` for performance flexibility.
- Enables full navigation between interconnected resources.

**API Discoverability Benefits:**

- Clients don't need to construct URLs manually.
- Dynamic links show available actions (CRUD operations).
- Pagination is self-documenting with next/previous links.

**Example Response:**

```json
{
  "id": 10773,
  "name": "BAFF Halloween",
  "price": 0.55,
  "developers": ["Blender Games"],
  "genres": ["Casual", "Indie"],
  "links": [
    { "rel": "self", "href": "/games/10773", "method": "GET" },
    { "rel": "update", "href": "/games/10773", "method": "PUT" },
    { "rel": "delete", "href": "/games/10773", "method": "DELETE" },
    {
      "rel": "related",
      "href": "/developers/3492",
      "method": "GET",
      "title": "Developer: Blender Games"
    },
    {
      "rel": "related",
      "href": "/genres/6",
      "method": "GET",
      "title": "Genre: Casual"
    },
    {
      "rel": "related",
      "href": "/genres/10",
      "method": "GET",
      "title": "Genre: Indie"
    }
  ]
}
```

### Resource URLs and HTTP Methods

**URL Structure:**

- `/games` - Collection endpoints.
- `/games/{id}` - Individual resource endpoints.
- `/games/{id}/price` - Sub-resource for specific data.
- `/developers` and `/genres` - Read-only collections

**HTTP Methods & Status Codes:**

| Method | Endpoint      | Purpose           | Success | Error              |
| ------ | ------------- | ----------------- | ------- | ------------------ |
| GET    | `/games`      | List games        | 200     | -                  |
| GET    | `/games/{id}` | Get specific game | 200     | 404, 422           |
| POST   | `/games`      | Create game       | 201     | 400, 422, 401      |
| PUT    | `/games/{id}` | Update game       | 200     | 400, 404, 422, 401 |
| DELETE | `/games/{id}` | Delete game       | 204     | 404, 422, 401      |

**Status Code Strategy:**

- **200** - Successful GET/PUT operations.
- **201** - Resource created successfully.
- **204** - Successful deletion (no content).
- **400** - Bad request/validation errors.
- **401** - Authentication required.
- **404** - Resource not found.
- **422** - Unprocessable Entity (invalid ID format)

### Error Handling

**Standardized Error Format:**
All errors follow a constistent JSON structure defined in `app/schemas/error.py`:

```json
{
  "status_code": 422,
  "error_code": "VALIDATION_ERROR",
  "message": "Unprocessable entity: 'id' contains semantically invalid data.",
  "details": {
    "field": "id",
    "value": -1,
    "constraint": "ID must be a positive integer"
  }
}
```

Error Categories:

- VALIDATION_ERROR - Invalid input data (400/422)
- NOT_FOUND - Resource doesn't exist (404)
- UNAUTHORIZED - Authentication required (401)
- CONFLICT - Resource conflict (409)
- DATABASE_ERROR - Server issues (500)

Reusable Error Functions (utils/errors.py):

- validation_error() - 400 for syntax errors.
- unproccessable_entity_error() - 422 for semantic errors.
- not_found_error() - 404 for missing resources.
- conflict_error() - 409 for duplicate resources.
- database\*error() - 500 for server issues.

Benefits:

- Consistent error format across all endpoints.
- Machine-readable error codes for client handling.
- Detailed context in `details` field for debugging.
- Centralized error handling prevents inconsistencies.

## Core Technologies Used

**Backend Framework:**

- **FastAPI** - Modern Python web framework with automatic OpenAPI documentation and type hints.
- **Uvicorn** - ASGI server for high-performance async handling.

**Database & ORM:**

- **PostgreSQL** - Production database via `psycopg2-binary`.
- **SQLAlchemy 2.0** - Modern ORM with async support and type safety.

**Authentication & Security:**

- **PyJWT** - JWT token generation and validation.
- **Passlib + Bcrypt** - Secure password hashing.

**Data Processing & Validation:**

- **Pydantic** - Data validation, serialization and API schema definition.
- **Pandas** - Data processing for the Steam dataset import.

**Development & Deployment:**

- **Python-multipart** - File upload support.
- **Pydantic-settings** - Configuration management.

**Why these choices:**

- FastAPI for automatic documentation and modern async Python.
- PostgreSQL for production-grade relational data storage.
- SQLAlchemy for database abstraction and migration support.
- JWT for stateless authentication fitting REST principles.

This is the first time developing in Python, most of the tech stack I researched on google and asked AI for help with recommended different frameworks and libraries.

## Reflection

The hardest part about creating the API was that I chose a new tech stack that I have never tried before. I wasn't that familiar with Python not using any curly brackets and that formatting is really important to get the code working as you would expect.

I learned new frameworks like FastAPI, SQLAlchemy for a relational database, PostgreSQL and I almost forgot (thanks to the clean code quiz I rembemered) to not mix high-level and low-level modules.
I have not tried to seed data into a database before, use the ETL process to get the data that you want, transform it, then load it into the database.

If I could go back with the knowledge I have now, I would structure my work better. I had a vision and a plan written down before hand but somewhere along the way I steered of course and that made things frustrating and I lost track of my vision for a bit. I would also recommend myself to read up on and learn more about the frameworks and libraries before hand.

## Acknowledgements

**Resource used in this API:**

- https://www.kaggle.com/datasets/fronkongames/steam-games-dataset
- https://fastapi.tiangolo.com/
- https://pandas.pydata.org/docs/
- https://www.sqlalchemy.org/
- https://docs.pydantic.dev/latest/
- https://www.youtube.com/watch?v=qw--VYLpxG4&list=LL&index=10

**Shoutout:**

- https://www.postman.com/learn/

Postman and their learning programs were great to get a better understanding on how to use Postman.

## Requirements

See [all requirements in Issues](../../issues/). Close issues as you implement them. Create additional issues for any custom functionality. See [TESTING.md](TESTING.md) for detailed testing requirements.

### Functional Requirements — Common

| Requirement                                                          | Issue                  | Status             |
| -------------------------------------------------------------------- | ---------------------- | ------------------ |
| Data acquisition — choose and document a dataset (1000+ data points) | [#1](../../issues/1)   | :white_check_mark: |
| Full CRUD for primary resource, read-only for secondary resources    | [#2](../../issues/2)   | :white_check_mark: |
| JWT authentication for write operations                              | [#3](../../issues/3)   | :white_check_mark: |
| Error handling (400, 401, 404 with consistent format)                | [#4](../../issues/4)   | :white_check_mark: |
| Filtering and pagination for large result sets                       | [#17](../../issues/17) | :white_check_mark: |

### Functional Requirements — REST

| Requirement                                                 | Issue                  | Status             |
| ----------------------------------------------------------- | ---------------------- | ------------------ |
| RESTful endpoints with proper HTTP methods and status codes | [#12](../../issues/12) | :white_check_mark: |
| HATEOAS (hypermedia links in responses)                     | [#13](../../issues/13) | :white_check_mark: |

### Non-Functional Requirements

| Requirement                                                 | Issue                  | Status               |
| ----------------------------------------------------------- | ---------------------- | -------------------- |
| API documentation (Swagger/OpenAPI or Postman)              | [#6](../../issues/6)   | :white_check_mark:   |
| Automated Postman tests (20+ test cases, success + failure) | [#7](../../issues/7)   | :white_check_mark:   |
| CI/CD pipeline running tests on every commit/MR             | [#8](../../issues/8)   | :white_check_mark:   |
| Seed script for sample data                                 | [#5](../../issues/5)   | :white_check_mark:   |
| Code quality (consistent standard, modular, documented)     | [#10](../../issues/10) | :white_check_mark:   |
| Deployed and publicly accessible                            | [#9](../../issues/9)   | :white_check_mark:   |
| Peer review reflection submitted on merge request           | [#11](../../issues/11) | :white_large_square: |

```

```
