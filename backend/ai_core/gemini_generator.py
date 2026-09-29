from google import genai
from google.genai import types

from backend.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    MAX_DOCUMENT_CHARS,
)


class GeminiDocumentGenerator:
    """Generate AI-assisted legal-document drafts."""

    def __init__(self, api_key=None, model=None):
        self.api_key = (api_key or GEMINI_API_KEY).strip()
        self.model = (model or GEMINI_MODEL).strip()

        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def build_prompt(
        self,
        document_type,
        parties,
        terms,
        effective_date,
    ):
        term_block = "\n".join(
            f"- {term}"
            for term in terms
        ) or "- No additional terms supplied."

        return f"""You are a careful legal-document drafting assistant.

Create a professional DRAFT of a {document_type}.

Parties:
{parties}

Effective date:
{effective_date}

User-provided terms:
{term_block}

Requirements:
1. Do not invent names, addresses, amounts, dates, laws, courts, registration numbers, or material facts.
2. Preserve the user's terms.
3. Use clear professional headings and numbered clauses.
4. Include a short Document Status note saying this is an AI-assisted draft requiring review.
5. Include signature blocks where appropriate.
6. Do not claim validity in a particular jurisdiction.
7. Return plain text only, without Markdown code fences.
8. Keep the draft practical and editable.
"""

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date,
    ):
        # If no API key is configured, use demo mode.
        if not self.client:
            return self._demo_document(
                document_type,
                parties,
                terms,
                effective_date,
            ), "demo"

        prompt = self.build_prompt(
            document_type,
            parties,
            terms,
            effective_date,
        )

        last_error = None

        for attempt in range(3):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=5000,
                    ),
                )

                text = (response.text or "").strip()

                if not text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return (
                    text[:MAX_DOCUMENT_CHARS],
                    "gemini",
                )

            except Exception as e:
                last_error = e

                if attempt < 2:
                    import time
                    time.sleep(3)

        # Gemini quota / server error fallback.
        # This keeps the LegalEase demo usable even when
        # the Gemini free-tier quota is temporarily unavailable.
        return (
            self._demo_document(
                document_type,
                parties,
                terms,
                effective_date,
                fallback_reason=str(last_error),
            ),
            "demo",
        )

    @staticmethod
    def _demo_document(
        document_type,
        parties,
        terms,
        effective_date,
        fallback_reason=None,
    ):
        clauses = "\n".join(
            f"{i}. {term}"
            for i, term in enumerate(terms, 1)
        )

        if not clauses:
            clauses = "1. No additional terms were supplied."

        reason_note = ""

        if fallback_reason:
            reason_note = (
                "\n\nNote: Gemini AI was temporarily unavailable, "
                "so LegalEase generated this editable demo draft."
            )

        return f"""DRAFT {document_type.upper()}

DOCUMENT STATUS

This is an editable LegalEase draft. It requires review and finalization by qualified legal counsel before execution.{reason_note}

1. PARTIES

{parties}

2. EFFECTIVE DATE

{effective_date}

3. TERMS AND CONDITIONS

{clauses}

4. GENERAL PROVISION

The parties should review this draft and add any required jurisdiction-specific provisions before signing.

5. SIGNATURES

Party 1: ______________________________

Name: __________________________________

Date: __________________________________


Party 2: ______________________________

Name: __________________________________

Date: __________________________________
"""