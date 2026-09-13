# Scrape and Analyze Job Requirements (kariyer.net)

Portfolio project that scrapes job ads from **[kariyer.net](https://www.kariyer.net)**, a major Turkish job board, and stores structured fields for later analysis of hiring requirements.

Despite the repository name, the scraper walks **many industry sectors** on the site (IT, finance, retail, education, and others), not only “Data Analyst” postings. The exported Excel files are useful as a broad job-market dataset.

## What’s included

| File | Description |
|------|-------------|
| `web_scraping_job_vacancies.py` | Selenium + BeautifulSoup scraper (written for Google Colab) |
| `job_listings.xlsx` | Collected ad URLs (~28,175 listings) |
| `job_final.xlsx` | Detailed fields scraped from each ad page |
| `All text to turkish Final.xlsx` | Extra export with text normalized toward Turkish |

At scrape time the run produced about **28,175** rows.

## Scraped fields (detail pages)

Examples of columns captured into `job_final.xlsx`:

- Ad link, position title, company  
- City / region  
- Work model and work type  
- Position level, department, sectors  
- Benefits / criteria  
- Experience, education, languages, and related requirements  

## How the scraper works

1. Loop over kariyer.net sector codes  
2. Paginate listing pages (`is-ilanlari`) and collect ad URLs  
3. Open each ad page and parse the detail HTML  
4. Append rows to Excel with Pandas  

The script uses **headless Chrome** via Selenium and was set up for **Google Colab** (`chromium-chromedriver`, `google.colab.files`).

## Tech stack

Python, Selenium, BeautifulSoup, Requests, Pandas, tqdm, Google Colab (original environment)

## How to run

1. Prefer Google Colab, or install Chrome + a matching ChromeDriver locally.  
2. Install dependencies:

```bash
pip install selenium beautifulsoup4 requests pandas tqdm openpyxl
```

3. Update driver / output paths if you are not on Colab (`/content/...`).  
4. Run `web_scraping_job_vacancies.py`.  

Website markup changes often; selectors may need refresh before a new full scrape.

## Notes

- Be respectful of kariyer.net’s terms of use and rate limits.  
- This repo currently focuses on **scraping and data dumps**. Deeper skill/requirement analysis would be a follow-on notebook on top of `job_final.xlsx`.  
- Some column labels in the Excel exports still contain typos from the original scrape (`Benfits`, etc.).
