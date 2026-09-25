# Invoice Processing Automation

**Pattern:** Evaluator-Optimizer · **Stack:** n8n, Python, Flask + pytesseract OCR, Cloudflare Tunnel, PostgreSQL · **Status:** Complete (tested with sample invoices)

Reads incoming invoices from PDFs and scanned images, extracts the key fields, checks each amount against the vendor's expected range, and approves clean invoices automatically. Anything questionable is flagged for a person instead of being paid blindly.

**Property management application:** contractor and vendor invoices (plumbers, electricians, cleaners, landscapers) checked against expected amounts before approval.

---

## The problem

Manual invoice processing means someone opens every invoice, types in the vendor and amount, and eyeballs whether the numbers look right. It's slow, error-prone, and doesn't scale past a handful of invoices a day. There's also no searchable record of what came in and what happened to it.

## How it works

Webhook intake → file-type routing (PDF or image) → text extraction (direct for PDFs, OCR for images) → field parsing → range evaluation → approve, re-extract, or flag for review → log to PostgreSQL

- **Intake:** a webhook trigger, so the workflow can sit behind an upload form, an email forwarding rule, or a shared-drive watcher.
- **Routing:** a mimeType-based router sends PDFs to direct text extraction and scanned images to OCR.
- **OCR service:** a self-hosted Flask + pytesseract service, reachable through a persistent Cloudflare Tunnel, so n8n can call it without exposing any public infrastructure.
- **Parsing:** extracted text is converted into structured fields: vendor, amount, date, and line items.
- **Evaluation (Evaluator-Optimizer):** a rule-based evaluator checks the amount against the vendor's expected range. In range → approved. Out of range → loops back for re-extraction, then flags for human review if it still fails.
- **Record:** every invoice lands in one of two PostgreSQL tables, giving a full, queryable history of what was processed and what needed review.

## Workflow structure

- **Main workflow:** Invoice Intake, Extraction & Evaluation
- **External service:** OCR microservice (Flask + pytesseract), not an n8n sub-workflow

## Reliability

| Rung | How it shows up |
|---|---|
| Input validation | Extracted fields are validated before the evaluator trusts them |
| Error handling / retry | A failed evaluation loops back for re-extraction instead of passing silently |
| Logging | Every invoice is written to PostgreSQL, approved or flagged |
| Human fallback | Anything the evaluator can't confidently approve goes to a person |

## Repository contents

- n8n workflow export (JSON)
- Python OCR service (Flask + pytesseract)
- Workflow screenshots

## Running it yourself

1. Import the workflow JSON into n8n.
2. Create n8n credentials for PostgreSQL. Credentials are **not** included in the export.
3. Run the OCR service locally and expose it through your own Cloudflare Tunnel (or any HTTPS endpoint), then point the workflow's OCR request at that URL.
4. Create the two PostgreSQL tables used by the workflow.
5. Set expected amount ranges for your vendors, then send a test invoice to the webhook URL.

## Limitations

- Range checks are rule-based. New vendors need a range defined before they can be auto-approved.
- OCR accuracy depends on scan quality; low-quality images are more likely to be flagged.

---

Built by [Alex Idachaba](https://alexidachaba.com) — AI automation for property management operations.
