# Recommendation Service

This service provides personalized product recommendations based on user preferences, product similarities, and sentiment analysis of reviews.

## Features

- Personalized user recommendations leveraging collaborative filtering
- Similar product recommendations using content-based filtering
- Sentiment-based recommendations using review analysis
- Popular product recommendations based on user interactions
- User preference insights
- Product recommendation reasoning

## Architecture

The recommendation service integrates with other microservices in the e-commerce ecosystem:

- Product Service: Provides product information
- User Service: Provides user preference data
- Review Service: Provides user reviews and ratings
- Sentiment Service: Provides sentiment analysis of reviews

## API Endpoints

### Core Recommendation Endpoints

- `GET /api/recommendations/user/<user_id>`: Get personalized recommendations for a user
- `GET /api/recommendations/product/<product_id>/similar`: Get similar products
- `GET /api/recommendations/sentiment`: Get recommendations based on sentiment analysis
- `GET /api/recommendations/popular`: Get popular products
- `GET /api/recommendations/sentiment-based`: Get sentiment-focused recommendations for a user

### Analytics and Insights

- `GET /api/insights/user/<user_id>/preferences`: Get user preference insights
- `GET /api/insights/product/<product_id>/recommendation-reasons`: Get reasons for product recommendations

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose (optional)
- Redis (for caching)

### Environment Variables

Copy the example environment file and modify as needed:

```bash
cp .env.example .env
```

See `.env.example` for a list of available configuration options.

### Installation

#### Local Development

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the service:

```bash
python -m src.app
```

#### Docker

1. Build and run using Docker Compose:

```bash
docker-compose up --build
```

## Testing

Run the test suite:

```bash
pytest
```

Generate a coverage report:

```bash
pytest --cov=src tests/
```

## Example Usage

### Get personalized recommendations for a user

```bash
curl -X GET "http://localhost:5002/api/recommendations/user/123?limit=5&include_sentiment=true"
```

### Get similar products

```bash
curl -X GET "http://localhost:5002/api/recommendations/product/456/similar?limit=5"
```

### Get sentiment-based recommendations

```bash
curl -X GET "http://localhost:5002/api/recommendations/sentiment?category=electronics&limit=10"
```

## Documentation

For more detailed API documentation, run the service and visit:

```
http://localhost:5002/api/docs
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project. 