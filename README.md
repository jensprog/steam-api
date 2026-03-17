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

_Describe your JWT authentication solution. Why did you choose this approach? What alternatives exist, and what are their trade-offs?_

### API Design

**REST students:**

- _How did you implement HATEOAS? How does it improve API discoverability?_
- _How did you structure your resource URLs and use HTTP methods/status codes?_

### Error Handling

_How does your API handle errors? Describe the format and consistency of your error responses._

## Core Technologies Used

_List the technologies you chose and briefly explain why:_

## Reflection

_What was hard? What did you learn? What would you do differently?_

## Acknowledgements

_Resources, attributions, or shoutouts._

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
| API documentation (Swagger/OpenAPI or Postman)              | [#6](../../issues/6)   | :white_large_square: |
| Automated Postman tests (20+ test cases, success + failure) | [#7](../../issues/7)   | :white_check_mark:   |
| CI/CD pipeline running tests on every commit/MR             | [#8](../../issues/8)   | :white_check_mark:   |
| Seed script for sample data                                 | [#5](../../issues/5)   | :white_check_mark:   |
| Code quality (consistent standard, modular, documented)     | [#10](../../issues/10) | :white_large_square: |
| Deployed and publicly accessible                            | [#9](../../issues/9)   | :white_check_mark:   |
| Peer review reflection submitted on merge request           | [#11](../../issues/11) | :white_large_square: |
