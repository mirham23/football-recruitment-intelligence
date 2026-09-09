# Football Recruitment Intelligence — Project Handover Document

## 1. Project Context

The goal is to build a **flagship football analytics portfolio project** for GitHub.

The project is intended to help demonstrate practical ability in:

* Data Science
* Data Analytics
* Machine Learning
* SQL
* Python
* Data Engineering
* FastAPI / REST API development
* Frontend development
* Docker / containerization
* CI/CD
* DevOps
* Production deployment
* Technical communication and architectural decision-making

The project should be strong enough to use as a portfolio/CV project when applying for Data Scientist, Data Analyst, ML/AI, or related roles.

The user is particularly interested in football analytics, so the project should use football data rather than a generic ML portfolio dataset.

---

# 2. Main Project Idea

## Football Recruitment Intelligence Platform

The application should function as a **football recruitment/scouting decision-support system**, rather than a generic football statistics website.

### Core question

> Given a club's recruitment requirements, which players should the club consider signing, why are they suitable, and are they potentially undervalued relative to their performance?

Example:

> Find a central midfielder aged ≤25, costing ≤€30M, with strong progressive passing, ball carrying and chance creation.

The system should return a ranked shortlist of players and explain the recommendation.

---

# 3. Important Product Positioning

The project should **NOT become a FotMob clone**.

FotMob and similar platforms primarily answer:

> "What happened / how did this player perform?"

This project should answer:

> "Who should we recruit and why?"

Therefore the focus should be:

* Player similarity
* Recruitment constraints
* Market-value estimation
* Undervalued-player detection
* Player development
* Recruitment recommendations
* Explainable recommendations

A useful positioning statement:

> **An analytics-driven football recruitment platform that identifies statistically similar, tactically suitable and potentially undervalued players using performance and market-value data.**

The project is not intended to replace football information platforms.

---

# 4. Potential Data Sources

The user has found the following datasets on Kaggle:

### Primary

1. **StatsBomb Football Data**

   * Event/performance data
   * Potentially useful for deeper player-performance analysis
   * Useful for progressive actions, passing, pressing, shooting, etc.

2. **Transfermarkt Football Data**

   * Market values
   * Transfer information
   * Useful for market-value modelling and recruitment analysis

3. **Football Player Stats 25/26**

   * Recent player performance
   * Potentially core dataset

4. **All Football Player Stats 23/24**

   * Historical player performance
   * Useful for longitudinal/development analysis

### Secondary

5. **Fantasy Premier League 26/27**

   * FPL price and fantasy performance-related information
   * Should NOT be the main purpose of the project
   * Could be used as an additional module/validation use case

6. **FIFA World Cup 2026 Dataset**

   * Potential future scouting module
   * Could identify World Cup players whose performance resembles Premier League players

7. **FIFA 2026 Player Performance**

   * Supplementary data if compatible with the main dataset

### Important

Before publishing data to GitHub, verify the licensing/usage terms of each dataset. Do not redistribute datasets if their licenses prohibit it.

---

# 5. Recommended Project Scope

The project should be developed incrementally.

Do NOT attempt to build the complete platform immediately.

## Phase 1 — Data Science MVP

Primary research question:

> **Can historical player performance statistics predict a player's transfer-market value?**

Secondary question:

> **Which players appear undervalued relative to their performance?**

Pipeline:

```text
Raw datasets
    ↓
Data cleaning
    ↓
Dataset integration
    ↓
Feature engineering
    ↓
Player performance metrics
    ↓
Market-value model
    ↓
Undervalued-player analysis
    ↓
GitHub
```

This should be the first deliverable.

---

# 6. Initial ML Approach

Do not immediately use complicated models.

Start with:

1. Baseline
2. Linear Regression
3. Random Forest
4. XGBoost

Compare their performance.

Potential metrics:

* MAE
* RMSE
* R²

Example:

| Model             | MAE | RMSE |  R² |
| ----------------- | --: | ---: | --: |
| Baseline          | ... |  ... | ... |
| Linear Regression | ... |  ... | ... |
| Random Forest     | ... |  ... | ... |
| XGBoost           | ... |  ... | ... |

Use SHAP or another explainability method to understand important features.

Potential features:

* Age
* Minutes
* Goals
* Goals/90
* Assists
* Assists/90
* xG
* xG/90
* xA
* xA/90
* Progressive passes
* Progressive carries
* Chance creation
* Defensive actions
* Position
* League
* Team
* International appearances
* Historical transfer information

The exact feature list must be determined after inspecting the actual datasets.

---

# 7. Undervalued Player Concept

After predicting expected market value:

```text
Performance data
       ↓
ML model
       ↓
Expected market value
       ↓
Compare with actual market value
```

Example:

```text
Actual market value:       €12M
Predicted market value:    €27M

Value gap:                 +€15M
```

Potential interpretation:

> The player's statistical performance is substantially higher than what the model would expect given their market value.

This should **not** automatically be described as proof that the player is objectively undervalued.

Better wording:

> "Potentially undervalued according to the model."

Market value is affected by many factors not present in the dataset.

---

# 8. Future Player Similarity System

After the ML MVP works, implement player similarity.

Possible methods:

* Cosine similarity
* K-nearest neighbors
* PCA
* Clustering
* UMAP for visualization

Example:

```text
Target Player
      ↓
Feature vector
      ↓
Similarity model
      ↓
Top 5 statistically similar players
```

Output:

| Player   | Similarity | Age | Market Value |
| -------- | ---------: | --: | -----------: |
| Player A |        94% |  24 |         €18M |
| Player B |        91% |  25 |         €22M |
| Player C |        88% |  23 |         €12M |

The system should also explain **which attributes drive the similarity**.

---

# 9. Final Recruitment Engine

Eventually create a recruitment search interface.

Example input:

```text
Position: CM
Maximum age: 25
Maximum market value: €30M
Minimum minutes: 1,000

Progressive passing: High
Ball carrying: High
Chance creation: Medium
Defensive contribution: Medium
```

Output:

```text
1. Player A
   Similarity: 94%
   Actual value: €18M
   Estimated value: €27M

2. Player B
   Similarity: 91%
   Actual value: €22M
   Estimated value: €31M

3. Player C
   Similarity: 88%
   Actual value: €12M
   Estimated value: €20M
```

The system should explain:

* Why the player matches
* Strengths
* Weaknesses
* Similarity
* Market value
* Estimated market value
* Value gap
* Data limitations

---

# 10. "Replace Player X" Feature

Potential flagship feature.

User selects a player.

Example:

> Find replacements for Player X.

The application returns:

```text
Player A — 94% similarity
Player B — 91%
Player C — 88%
Player D — 84%
Player E — 81%
```

Then show attribute-level comparison.

Example:

| Attribute           | Target | Candidate |
| ------------------- | -----: | --------: |
| Progressive passing |     92 |        89 |
| Ball carrying       |     78 |        84 |
| Defensive actions   |     95 |        73 |
| xA                  |     64 |        81 |
| Pressures           |     90 |        88 |

This provides a much stronger recruitment use case than a generic player statistics page.

---

# 11. FPL Module

FPL 26/27 should be treated as a **secondary feature**, not the central project.

Potential question:

> Do players identified as high-performing/recruitment targets also generate strong fantasy performance?

Potential output:

```text
Player A

Predicted FPL value: 8.4
Expected points: 6.8 GW⁻¹
Price: £6.5M
Value: 1.05 pts / £M

Recommendation: BUY
```

This could be added after the recruitment system is working.

---

# 12. World Cup Module

The World Cup 2026 datasets could become a future extension.

Potential feature:

## World Cup Breakout Scouting

```text
World Cup performance
        ↓
Compare against PL player database
        ↓
Player similarity model
        ↓
Identify players whose profile resembles PL players
```

This is optional and should not delay the core project.

---

# 13. Target Technical Architecture

Eventually the project should demonstrate full-stack/data engineering capability.

Recommended architecture:

```text
                    DATA SOURCES
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     StatsBomb       Transfermarkt      FPL
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
                  DATA PIPELINE
                    Python / SQL
                         │
                         ▼
                    PostgreSQL
                         │
              ┌──────────┴──────────┐
              │                     │
              ▼                     ▼
       ML / Analytics            FastAPI
       scikit-learn              REST API
       XGBoost                   OpenAPI
              │                     │
              └──────────┬──────────┘
                         ▼
                  React Frontend
                  TypeScript
                         │
                         ▼
                    Nginx
                         │
                         ▼
                     Internet
```

---

# 14. Recommended Technology Stack

| Layer               | Technology           |
| ------------------- | -------------------- |
| Language            | Python               |
| Data processing     | Pandas or Polars     |
| Database            | PostgreSQL           |
| SQL                 | PostgreSQL SQL       |
| ML                  | scikit-learn         |
| Advanced ML         | XGBoost              |
| Explainability      | SHAP                 |
| Backend             | FastAPI              |
| API documentation   | OpenAPI / Swagger    |
| Frontend            | React + TypeScript   |
| Styling             | Tailwind CSS         |
| Containerization    | Docker               |
| Local orchestration | Docker Compose       |
| Testing             | Pytest               |
| API testing         | HTTPX                |
| CI/CD               | GitHub Actions       |
| Reverse proxy       | Nginx                |
| Deployment          | VPS / cloud          |
| Monitoring          | Prometheus + Grafana |

Do not introduce technologies merely to make the project look complicated.

---

# 15. Docker Architecture

Eventually use separate containers:

```text
Docker
│
├── frontend
│     React
│
├── api
│     FastAPI
│
├── postgres
│     PostgreSQL
│
├── nginx
│     Reverse proxy
│
└── pipeline
      ETL / data processing
```

Potential future additions:

* Redis
* Celery
* Prometheus
* Grafana

But only introduce them when there is a legitimate engineering reason.

Do NOT use Kubernetes just for the sake of claiming Kubernetes experience.

---

# 16. Development vs Production

Create separate configurations.

Development:

```text
docker-compose.dev.yml
```

Production:

```text
docker-compose.prod.yml
```

Development should support:

* Hot reload
* Debug logging
* Source mounts
* Development database

Production should support:

* Optimized builds
* Environment variables
* No source-code mounts
* Health checks
* Nginx
* Production configuration

---

# 17. FastAPI API

Potential endpoints:

```text
GET  /api/v1/players
GET  /api/v1/players/{player_id}
GET  /api/v1/players/{player_id}/similar
GET  /api/v1/players/{player_id}/performance
GET  /api/v1/players/{player_id}/market-value
POST /api/v1/recruitment/search
GET  /api/v1/teams
GET  /api/v1/health
```

The main endpoint should eventually be:

```text
POST /api/v1/recruitment/search
```

Example request:

```json
{
  "position": "CM",
  "max_age": 25,
  "max_market_value": 30000000,
  "min_minutes": 1000,
  "attributes": {
    "progressive_passing": 0.8,
    "ball_carrying": 0.7,
    "chance_creation": 0.6
  }
}
```

Example response:

```json
{
  "candidates": [
    {
      "player_id": 123,
      "name": "Player A",
      "similarity": 0.94,
      "estimated_value": 27000000,
      "market_value": 18000000,
      "value_gap": 9000000
    }
  ]
}
```

---

# 18. Frontend

Eventually use React + TypeScript.

Main interface:

```text
FOOTBALL RECRUITMENT INTELLIGENCE

Recruitment Search

Position: [Central Midfielder]

Age: 18 ────────●── 25

Budget: €30M

Required Attributes:

Progressive passing   ████████░░
Ball carrying         ███████░░░
Chance creation       ██████░░░░
Defensive             █████░░░░░

[ FIND PLAYERS ]
```

Results:

```text
Player       Similarity    Value    Est. Value

Player A       94%         €18M       €27M
Player B       91%         €22M       €31M
Player C       88%         €12M       €20M
```

Player profile should show:

* Performance
* Market value
* Estimated value
* Similarity
* Strengths
* Weaknesses
* Relevant metrics
* Explanation of recommendation

---

# 19. CI/CD

GitHub Actions should eventually perform:

```text
git push
   ↓
GitHub Actions
   ↓
Lint
   ↓
Unit tests
   ↓
Integration tests
   ↓
Build Docker images
   ↓
Security scan
   ↓
Deploy
   ↓
Health check
```

Potential workflows:

```text
.github/
└── workflows/
    ├── test.yml
    ├── build.yml
    └── deploy.yml
```

This provides evidence of real DevOps capability.

---

# 20. Testing

Recommended structure:

```text
tests/
├── unit/
│   ├── test_metrics.py
│   ├── test_similarity.py
│   └── test_market_value.py
│
└── integration/
    ├── test_players_api.py
    └── test_recruitment_api.py
```

Examples:

```text
Same player similarity ≈ 1.0
Invalid age → HTTP 422
Unknown player → appropriate HTTP error
Budget filter → players above budget excluded
Database query → expected player returned
```

---

# 21. Health Checks

FastAPI:

```text
GET /health
```

Potential response:

```json
{
  "status": "healthy",
  "database": "healthy",
  "model": "loaded",
  "version": "1.2.0"
}
```

Docker should also have health checks.

---

# 22. Monitoring

Eventually:

```text
Application
     ↓
Prometheus
     ↓
Grafana
```

Monitor:

* API request count
* API latency
* HTTP errors
* CPU
* Memory
* Database connections
* Model status

This provides a credible DevOps/production story.

---

# 23. Deployment

A simple VPS deployment is sufficient.

Potential architecture:

```text
Internet
   ↓
Nginx
   ↓
React
   ↓
FastAPI
   ↓
PostgreSQL
   ↓
ML models
```

Deployment pipeline:

```text
Developer
   ↓
git push
   ↓
GitHub
   ↓
GitHub Actions
   ↓
Docker image
   ↓
Container registry
   ↓
Server
   ↓
docker compose pull
   ↓
docker compose up -d
   ↓
health check
```

---

# 24. Do NOT Build Everything at Once

This is a major project-management requirement.

The user has previously struggled with feeling that their portfolio is empty and is concerned about having relied heavily on AI coding agents.

Therefore:

**Do not ask Cursor/Claude to build the entire application immediately.**

Instead, build progressively.

---

# 25. First Milestone

The first milestone should ONLY be:

## "Can I identify potentially undervalued players?"

Scope:

```text
Dataset inspection
      ↓
Data cleaning
      ↓
Dataset joining
      ↓
Feature engineering
      ↓
Exploratory analysis
      ↓
Market-value model
      ↓
Undervalued-player analysis
      ↓
GitHub README
```

Do NOT build yet:

* React
* FastAPI
* Docker
* Kubernetes
* CI/CD
* Monitoring
* Cloud deployment

Those come later.

---

# 26. First GitHub Repository

Repository:

```text
football-recruitment-intelligence
```

Initial structure:

```text
football-recruitment-intelligence/
│
├── README.md
├── .gitignore
├── LICENSE
│
├── data/
│
├── notebooks/
│
├── src/
│
└── tests/
```

The repository should be committed immediately.

The objective is to stop having an empty GitHub portfolio.

---

# 27. Recommended First 5 Days

## Day 1 — Dataset Exploration

* Identify datasets
* Inspect schemas
* Understand columns
* Check missing values
* Check duplicates
* Determine whether player identifiers exist
* Determine how datasets can be joined

## Day 2 — Data Cleaning

* Standardize player names
* Standardize teams
* Handle missing values
* Remove duplicates
* Join datasets
* Create basic per-90 metrics

## Day 3 — Analysis

Investigate:

* Performance vs market value
* Age vs market value
* Goals/90 vs value
* xG/90 vs value
* xA/90 vs value
* Minutes vs value
* Position differences

## Day 4 — Machine Learning

Implement:

1. Baseline
2. Linear Regression
3. Random Forest
4. XGBoost

Compare them.

## Day 5 — Storytelling

Document:

```text
Problem
↓
Data
↓
Methodology
↓
Results
↓
Interesting findings
↓
Limitations
↓
Future work
```

Then push the project publicly.

---

# 28. Job Search Strategy

Do NOT wait until the entire application is finished before applying.

The project should evolve:

```text
Week 1
Data analysis
       ↓
Week 2
ML + player similarity
       ↓
Week 3
FastAPI
       ↓
Week 4
React
       ↓
Week 5
Docker
       ↓
Week 6
CI/CD + deployment
```

Apply for jobs while developing the project.

The portfolio does not need to be perfect before applying.

---

# 29. How to Use AI Coding Agents

AI coding agents such as Cursor/Claude can be used, but the user should avoid asking:

> "Build the entire football recruitment platform."

Instead:

### First prompt

> I am building a football recruitment analytics project. For now, do NOT build the API, frontend, Docker, CI/CD, or deployment. Help me inspect the datasets I provide. Identify their schemas, potential join keys, useful variables for predicting player market value, data-quality problems, and propose a data-cleaning and feature-engineering plan. Do not modify files yet. Explain your reasoning first.

Then review the response.

Only after understanding the plan:

> Implement step 1 only.

The user should be able to explain the important code and architectural decisions.

AI should accelerate development rather than replace understanding.

---

# 30. Important Learning Principle

The goal is not:

> "Can I manually write every line of code?"

The goal is:

> "Can I understand, validate, explain, debug and improve the system that I built with AI assistance?"

If an AI agent produces a large function, ask it to explain:

* What it does
* Why it is structured this way
* What assumptions it makes
* What edge cases exist
* How it could fail
* How it is tested

Do not commit code that the user cannot reasonably explain.

---

# 31. Final Portfolio Story

The eventual project should demonstrate:

```text
Raw football data
       ↓
Data engineering
       ↓
SQL / PostgreSQL
       ↓
Feature engineering
       ↓
Statistical analysis
       ↓
Machine learning
       ↓
Player similarity
       ↓
Market-value modelling
       ↓
Recruitment recommendation
       ↓
FastAPI
       ↓
React
       ↓
Docker
       ↓
CI/CD
       ↓
Production deployment
       ↓
Monitoring
```

This provides evidence that the user can work across:

**Data Science + Software Engineering + Data Engineering + DevOps.**

---

# 32. Main Success Criteria

The project is successful if a recruiter can look at it and understand:

1. **What problem is being solved**
2. **Why the problem matters**
3. **Where the data comes from**
4. **How the data was processed**
5. **Why the ML methodology was chosen**
6. **How the model was evaluated**
7. **How the recommendation is generated**
8. **How the API works**
9. **How the frontend consumes the API**
10. **How the application is containerized**
11. **How tests run**
12. **How CI/CD works**
13. **How the application is deployed**
14. **How the production system is monitored**
15. **What the limitations are**

The project should prioritize **technical depth and clear reasoning over the number of technologies used.**

---

# 33. Immediate Next Action

The next action is **NOT** to build the application.

The immediate action is:

### 1. Create the GitHub repository

`football-recruitment-intelligence`

### 2. Download/organize the available datasets

### 3. Give the coding agent the datasets

### 4. Ask the agent to inspect and propose the data architecture

### 5. Bring the agent's proposed plan back for review

### 6. Only then implement the first data-analysis milestone

The first concrete question to answer is:

> **Can the available datasets be reliably joined to create a player-season dataset containing performance metrics and market value?**

Everything else depends on that.
