# Source Policy

## Preferred Sources

Prefer sources that are durable, reputable, and license-aware:

- Open educational resources such as OpenStax, MIT OpenCourseWare, LibreTexts, and university course notes with clear reuse terms.
- Official curriculum or standards pages when aligning to a course.
- Primary documentation for tool/API behavior.
- Locally curated notes or assessments already in the repo.

Avoid using homework-solution farms, copied answer banks, and pages with unclear provenance as generation sources.

## Attribution And Licensing

When outside sources materially shape content:

- Keep source URLs in working notes or final response.
- Prefer paraphrased, original questions and explanations.
- Attribute adapted content when the source license requires it.
- Record license, source title, source URL, and access date for corpus entries.

Use Creative Commons-style attribution habits even when only citing for transparency: title, author or organization, source URL, license, and changes if adapted.

## Browsing vs Corpus

Use browsing for one-off question creation, quick verification, and current facts.

Build a corpus when agents will repeatedly draw from the same source set. The corpus should store:

- `source_id`
- `title`
- `publisher`
- `url`
- `license`
- `retrieved_at`
- `topic_tags`
- `course_tags`
- `allowed_use`
- `content_hash`
- chunked text or embeddings if allowed

Refresh periodically only after checking source terms and robots directives. Keep refresh logs and do not silently replace active assessment content without review.

## Scraping Guardrails

- Respect `robots.txt` and site terms.
- Do not scrape paywalled, login-gated, or restricted content.
- Rate-limit requests and identify the project if a crawler is built.
- Prefer official APIs, downloads, GitHub repositories, or published OER export formats over page scraping.
- Store only what the license permits.

## Assessment Generation Guardrails

- Use sources for topic coverage and correctness, not direct cloning.
- Vary numbers, contexts, wording, and solution paths.
- Include enough explanation that the learner can diagnose the mistake.
- Keep answers machine-checkable when possible.
- For symbolic calculus questions, verify by differentiating the expected answer.
