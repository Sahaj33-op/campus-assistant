"""
Script to load sample FAQs into the database.
Run this after starting the backend server.
"""

import asyncio
import json
from pathlib import Path
import httpx


API_URL = "http://localhost:8000"


async def load_faqs():
    """Load sample FAQs from JSON file."""
    faqs_file = Path(__file__).parent.parent / "data" / "sample_faqs.json"

    if not faqs_file.exists():
        print(f"FAQ file not found: {faqs_file}")
        return

    with open(faqs_file, "r", encoding="utf-8") as f:
        faqs = json.load(f)

    print(f"Loading {len(faqs)} FAQs...")

    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, faq in enumerate(faqs, 1):
            try:
                response = await client.post(
                    f"{API_URL}/api/v1/faqs/",
                    json=faq,
                )
                if response.status_code == 200:
                    print(f"  [{i}/{len(faqs)}] Created: {faq['question'][:50]}...")
                else:
                    print(f"  [{i}/{len(faqs)}] Failed: {response.text}")
            except Exception as e:
                print(f"  [{i}/{len(faqs)}] Error: {e}")

    print("\nDone!")


if __name__ == "__main__":
    asyncio.run(load_faqs())
