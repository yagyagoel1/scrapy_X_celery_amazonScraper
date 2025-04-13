# 🕷️ Async Distributed Amazon Scraper

An **asynchronous distributed web scraper** for Amazon that leverages:
- 🐍 Python (FastAPI, Scrapy)
- 🐋 Docker
- 🧪 Poetry (dependency management)
- 🧵 Celery (task queue)
- 🧠 Redis (broker & result backend)
- ☁️ Boto3 (for pushing scraped data to AWS S3)
- 📊 ScrapeOps (monitoring)

## 🎥 Demo & Architecture Overview

Watch the full project demo and architecture walkthrough here:  
👉 👉 [![Watch on Loom](https://imgur.com/a/zY7D5xz)](https://www.loom.com/share/9816bdf62861418bad64c80378b85e4a?sid=764afa14-4e9e-42e2-8c42-db03a75b011d)




---

## 🚀 Features

- 🔁 **Asynchronous, distributed scraping** powered by Celery
- 📦 Fully containerized using Docker
- 🛠️ Poetry for modern Python packaging & management
- 📡 FastAPI to trigger scrape jobs with keyword and page count
- 🕷️ Scrapy to crawl Amazon product pages
- 🔍 ScrapeOps integration to manage scraping at scale
- ☁️ Results automatically pushed to **Amazon S3**
- 📬 Get job status via Task ID API

---

## ⚙️ Tech Stack

| Tool        | Purpose                         |
|-------------|----------------------------------|
| FastAPI     | API server for accepting tasks   |
| Celery      | Distributed task queue           |
| Redis       | Message broker & result backend  |
| Scrapy      | Web scraping framework           |
| Boto3       | Push results to AWS S3           |
| ScrapeOps   | Scraper monitoring & rotation    |
| Poetry      | Python packaging                 |
| Docker      | Containerized deployment         |

---

## 📥 How It Works

1. **User sends POST request** to FastAPI with a keyword and number of pages.
2. FastAPI **queues a task** using Celery and Redis.
3. A **Celery worker** picks up the task asynchronously.
4. Worker **runs a Scrapy spider**, scraping Amazon products based on the keyword.
5. Once done, the results are **uploaded to S3** using `boto3`.
6. User can **check task status** using a separate endpoint with the task ID.

---

## 📦 Installation

```bash
git clone https://github.com/your-username/amazon-distributed-scraper.git
cd amazon-distributed-scraper
poetry install
```

---

## 🐳 Run with Docker

```bash
docker compose up --build
```

This spins up:
- Redis
- FastAPI server
- Celery worker

---



---

## 🧠 To Do / Roadmap

- [ ] UI dashboard for scraping jobs
- [ ] Retry failed scraping tasks
- [ ] Database to store metadata
