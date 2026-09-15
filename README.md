# Invoice Processing Automation

**Pattern:** Evaluator-Optimizer

Automated invoice intake that extracts data from PDFs and scanned images, validates it against expected vendor ranges, and flags exceptions for human review instead of approving everything blindly.

## Problem

Manual invoice processing means someone opens every invoice, keys in vendor and amount by hand, and eyeballs whether the numbers look right — slow, error-prone, and impossible to scale past a handful of invoices a day.

## Build

An n8n workflow triggered by webhook, with a mimeType-based router splitting PDFs from scanned images. Images are sent to a self-hosted OCR service (Flask + pytesseract) reachable through a persistent Cloudflare Tunnel, so n8n can call it without exposing any infrastructure publicly. Extracted data is parsed into structured fields, then run through the Evaluator-Optimizer pattern: a rule-based evaluator checks the amount against expected vendor ranges, looping back for re-extraction or flagging for human review on failure rather than approving automatically. Every invoice lands in one of two Postgres tables — a full, queryable record of what came in and what happened to it.

## Outcome

Manual data entry disappears for invoices that fall within range, and the ones that don't get flagged instead of quietly approved or lost in an inbox.

## Reliability Notes

This project is a clean example of the full ladder in one build: input validation on extracted data, a defined error/retry path when evaluation fails, and human fallback for anything the evaluator can't confidently approve.

## Stack

n8n, Python, self-hosted Flask + pytesseract OCR, Cloudflare Tunnel, Postgres

## Status

Complete.
