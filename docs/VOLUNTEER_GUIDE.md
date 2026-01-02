# Volunteer Maintainer's Guide

This guide is for student volunteers who will maintain the Campus Assistant chatbot after the hackathon.

## Overview

The Campus Assistant is a multilingual chatbot that helps students get answers to common questions. Your role is to:

1. Keep the FAQ database updated
2. Review conversation logs
3. Handle escalated queries
4. Upload new documents
5. Monitor system health

## Daily Routine (5-10 minutes)

### 1. Check System Health

Visit: `http://your-domain/api/v1/admin/health`

You should see:
```json
{
  "status": "healthy",
  "database": "healthy",
  "vector_db": "healthy"
}
```

If anything shows "unhealthy", contact the technical admin.

### 2. Check Pending Escalations

Visit the admin dashboard and look for "Pending Escalations". These are queries the bot couldn't answer confidently.

**To resolve an escalation:**
1. Read the conversation
2. If you can answer, add the FAQ to the database
3. Mark the escalation as "Resolved"

### 3. Quick Stats Check

Look at today's message count. If it's unusually low, something might be wrong.

## Weekly Tasks (30 minutes)

### 1. Review Top Queries

Check the analytics to see:
- What questions are asked most frequently
- Which languages are being used
- Low-confidence responses

### 2. Update FAQs

Based on common queries, add new FAQs:

**Using the API:**
```bash
curl -X POST http://localhost:8000/api/v1/faqs/ \
  -H "Content-Type: application/json" \
  -u admin:password \
  -d '{
    "question": "When is the last date for fee payment?",
    "answer": "The last date for fee payment is December 31, 2024.",
    "category": "fees",
    "keywords": ["fee", "payment", "deadline", "last date"]
  }'
```

**Tips for good FAQs:**
- Keep answers concise (2-3 sentences)
- Include relevant keywords
- Assign the right category

### 3. Upload New Documents

When new circulars or notices are released:

```bash
curl -X POST http://your-domain/api/v1/documents/upload \
  -F "file=@new_circular.pdf" \
  -F "category=admission"
```

## Categories to Use

| Category | For |
|----------|-----|
| admission | Admission procedures, eligibility, deadlines |
| fees | Fee structure, payment methods, deadlines |
| scholarship | Scholarship schemes, eligibility, applications |
| examination | Exam schedules, results, revaluation |
| hostel | Hostel facilities, fees, rules |
| library | Library timings, book borrowing |
| placement | Campus placements, companies |
| general | Everything else |

## Common Issues & Solutions

### Bot Not Responding

1. Check if the server is running: `http://your-domain/health`
2. Check the logs: `./data/logs/chatbot.log`
3. Restart the server if needed

### Wrong Answers

1. Find the FAQ that caused the wrong answer
2. Update or correct the FAQ
3. Reindex: `POST /api/v1/faqs/reindex`

### Translation Issues

- Bhashini API might be slow sometimes
- The bot automatically falls back to Google Translate
- If both fail, response will be in English

### New Document Not Working

1. Check if it was indexed: `GET /api/v1/documents/{id}`
2. If `is_indexed: false`, trigger indexing: `POST /api/v1/documents/{id}/index`

## Adding a New Language

Currently not supported through admin panel. Contact technical admin.

## Export Conversation Logs

For monthly reports:

```bash
curl "http://your-domain/api/v1/admin/conversations/export?date=2024-01-15" \
  -u admin:password \
  > conversations_jan15.json
```

## Security Notes

- Never share the admin password
- Change the default password immediately
- Don't upload documents with sensitive information
- The bot logs all conversations for improvement

## Contact

For technical issues beyond this guide:
- Technical Admin: [email]
- GitHub Issues: [link]

## Quick Reference

| Task | Endpoint | Method |
|------|----------|--------|
| Check health | /api/v1/admin/health | GET |
| View dashboard | /api/v1/admin/dashboard | GET |
| List FAQs | /api/v1/faqs/ | GET |
| Add FAQ | /api/v1/faqs/ | POST |
| Upload document | /api/v1/documents/upload | POST |
| View analytics | /api/v1/admin/analytics | GET |
| Export logs | /api/v1/admin/conversations/export | GET |
