# AI News Aggregator

An AI-powered news aggregator application in Python. It scrapes RSS feeds (blogs, YouTube), stores structured data, provides a CLI chat interface for querying (using OpenAI API), and sends a daily HTML email digest to configured recipients.

## Features
- Scrape and aggregate news from multiple RSS feeds (blogs, YouTube)
- Store articles/videos in a structured database (SQLite for dev, PostgreSQL for prod)
- Query news using a CLI chat interface powered by OpenAI
- Send daily HTML email digests to recipients
- Modular structure for easy extension and deployment

## Project Structure
```
app/
  scraper/   # RSS scraping logic
  db/        # Database models and access
  chat/      # Chat/AI query interface
  digest/    # Daily digest and email logic
  config/    # Configuration files
  utils/     # Utility functions
deploy/      # Deployment scripts and configs
docker/      # Docker and containerization files
main.py      # Entry point
requirements.txt
.env.example # Example environment variables
```

## Getting Started
1. Clone the repository
2. Create and activate a virtual environment:
	- `python -m venv venv`
	- Windows: `venv\Scripts\activate`
	- Linux/Mac: `source venv/bin/activate`
3. Install dependencies:
	- `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in your secrets (API keys, email credentials)
5. Run the application (to be updated as modules are implemented)

## Development
- Pre-commit hook checks code formatting and linting before each commit
- Use `black`, `flake8`, and `isort` for code quality

## Roadmap
- Implement RSS scraper
- Add database integration
- Build CLI chat interface
- Add daily digest email
- Prepare for Azure deployment

## License
MIT
