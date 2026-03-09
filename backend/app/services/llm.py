import os
import time
import json
import logging
from anthropic import Anthropic
from openai import OpenAI
from app.schemas.diary import DiaryStructured

logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

_MAX_RETRIES = 3
_RETRY_BASE_DELAY = 1.0  # seconds


def _retry(func, *args, **kwargs):
    """Exponential backoff retry wrapper (max 3 attempts)."""
    for attempt in range(_MAX_RETRIES):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if attempt == _MAX_RETRIES - 1:
                raise
            delay = _RETRY_BASE_DELAY * (2 ** attempt)
            logger.warning("Attempt %d failed: %s. Retrying in %.1fs...", attempt + 1, e, delay)
            time.sleep(delay)


def structure_diary(content: str) -> dict:
    """OpenAI로 일기 내용을 구조화된 데이터로 변환."""

    def _call():
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a journaling assistant. Analyze the diary entry and return a JSON object "
                        "with these exact fields:\n"
                        "- mood (string): overall emotional tone in English (e.g. happy, anxious, grateful)\n"
                        "- mood_score (integer): 1 (very negative) to 10 (very positive)\n"
                        "- tags (array of strings): key topics or themes, max 5\n"
                        "- summary (string): one-sentence summary\n"
                        "- key_events (array of strings): notable events or thoughts mentioned, max 5\n"
                        "Respond only with valid JSON."
                    ),
                },
                {"role": "user", "content": content},
            ],
        )
        raw = response.choices[0].message.content
        parsed = DiaryStructured.model_validate_json(raw)
        return parsed.model_dump()

    return _retry(_call)


def generate_reflection(content: str, structured: dict) -> str:
    """GPT-4o-mini로 일기에 대한 반성적 리플렉션 생성. (Claude 크레딧 충전 후 교체 예정)"""

    def _call():
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "너는 공감 능력이 뛰어난 일기 코치야. 사용자의 일기를 읽고 따뜻하고 통찰력 있는 리플렉션을 2~3문장으로 작성해줘. 질문 형식으로 마무리해도 좋아.",
                },
                {
                    "role": "user",
                    "content": (
                        f"다음은 사용자의 일기야:\n\n{content}\n\n"
                        f"감정 분석: mood={structured['mood']} ({structured['mood_score']}/10), "
                        f"tags={structured['tags']}"
                    ),
                },
            ],
            max_tokens=512,
        )
        return response.choices[0].message.content

    return _retry(_call)
