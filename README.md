# PolitiFact Scraper

A Python web scraper that extracts fact-check data from PolitiFact.com, including statements, verdicts, sources, dates, contexts, and category tags.

## Features

- Scrapes multiple pages of fact-checks from PolitiFact
- Extracts comprehensive data for each fact-check:
  - **Statement Originator**: Person or entity who made the statement
  - **Statement Date**: When the statement was originally made
  - **Statement**: The actual claim being fact-checked
  - **Statement Source**: Where the statement was made (e.g., "X post", "speech", "press conference")
  - **Verdict**: The fact-check rating (e.g., "true", "mostly-true", "false", "pants-fire")
  - **Tags**: Category tags (e.g., "National", "Natural Disasters", "Florida")
  - **Fact-Checker**: Name of the journalist who wrote the fact-check
  - **Fact-Check Date**: When the fact-check was published
  - **Fact-Check Analysis Link**: Direct link to the full fact-check article
- Exports data to CSV and JSON formats
- Handles multi-word names correctly (e.g., "Maria Ramirez Uribe")
- Built-in rate limiting to avoid server overload
- Progress tracking with elapsed time display
- Data filtering and categorization capabilities

## Requirements

```
beautifulsoup4
pandas
requests
```

## Installation

1. Clone or download this repository
2. Install required packages:
```bash
pip install beautifulsoup4 pandas requests
```

## Usage

### Scraping Data

1. Open `scrape-politifact-using-list.py`
2. Modify the `n` variable (line 130) to set how many pages to scrape:
   ```python
   n = 5  # Will scrape pages 1-4 (879 pages maximum available in January 2026)
   ```
3. Run the script:
   ```bash
   python src/scrape-politifact-using-list.py
   ```
4. The script will generate `politifact.csv` with all scraped data

### Data Processing and Analysis

The `src/statistics.ipynb` notebook provides various data processing capabilities:

- **Data Cleaning**: Filters out Spanish content (`PolitiFact en Español`) and flip-flop verdicts
- **Media Filtering**: Removes statements based on videos, images, or viral content
- **Category Extraction**: Creates separate datasets for 8 specific topics (Health Care, Elections, Economy, Taxes, Immigration, Education, Crime, Jobs)
- **Visualization**: Generates verdict distribution charts for each category
- **Format Conversion**: Converts CSV datasets to JSON format

To use the processing features:
```bash
jupyter notebook src/statistics.ipynb


## Output Format

The generated CSV contains the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| statement_originator | Person/entity who made the statement | Jared Moskowitz |
| statement_date | When statement was made | January 22, 2026 |
| statement | The claim being fact-checked | The Federal Emergency Management Agency's "backlog of unanswered disaster assistance applications has exploded to the largest in its history." |
| verdict | Fact-check rating | mostly-true |
| statement_source | Where statement was made | X post |
| tags | Category tags (semicolon-separated) | National; Natural Disasters; Florida |
| factchecker | Journalist who wrote the fact-check | Maria Ramirez Uribe |
| factcheck_date | When fact-check was published | January 7, 2026 |
| factcheck_analysis_link | Link to full fact-check article | https://www.politifact.com/factchecks/2026/jan/28/jared-moskowitz/FEMA-disaster-declaration-backlog-Trump/ |

## Performance

- Processing time: ~2-3 seconds per article
- Each page contains ~10 articles
- Full scrape (879 pages): Estimated 5-7 hours
- Includes 0.2-second delay between article requests

## Notes

- The scraper normalizes "barely-true" verdicts to "mostly-false" for consistency
- Articles/prepositions ("a", "an", "the", "in") are automatically removed from statement source strings
- Category tags exclude personality tags (author names)
- Correctly handles multi-word fact-checker names (e.g., "Maria Ramirez Uribe")
- Built-in progress tracking shows elapsed time after each page
- Separates statement dates (when claim was made) from fact-check dates (when published)

## Ethical Considerations

This scraper includes:
- Rate limiting (`time.sleep(0.2)`) to avoid overwhelming PolitiFact's servers
- Respectful request patterns
- Progress tracking to monitor execution

Please use responsibly and in accordance with PolitiFact's terms of service.

## Acknowledgments

This project was built upon code from [ChangyWen/PolitiFact-scraping](https://github.com/ChangyWen/PolitiFact-scraping/blob/master/scrape-politifact.py), with significant enhancements including:
- Individual article page scraping for detailed metadata
- Category tag extraction
- Statement date and context extraction
- Multi-word name handling
- Enhanced progress tracking

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
