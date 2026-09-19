"""Fetch fine dust levels using the GPT-4o Search Preview model.

This script sends a structured prompt to the OpenAI Responses API so that the
GPT-4o Search Preview model performs a live web search restricted to Naver and
returns the current PM10/PM2.5 readings for the requested Korean location.

Usage:
    export OPENAI_API_KEY="sk-..."
    python gpt4o_search_air_quality.py --location "영등포구 여의도동"

An optional ``--model`` flag lets you override the default model name if
OpenAI releases a newer Search Preview variant. The script normalises the
returned JSON payload and prints it to stdout.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any, Dict

from openai import OpenAI

# Default model requested by the user. You can override it by setting the
# environment variable ``OPENAI_GPT4O_SEARCH_MODEL`` or by using the ``--model``
# CLI flag when running this script.
DEFAULT_MODEL = os.getenv("OPENAI_GPT4O_SEARCH_MODEL", "gpt-4o-search-preview")

SYSTEM_PROMPT = """\
당신은 신뢰성 높은 한국어 웹 리서처입니다.
반드시 naver.com(하위 도메인 포함: weather.naver.com 등)의 페이지에서만 사실을 인용하세요.
검색어는 한국어로 사용하고, 목표 지역은 '영등포구 여의도동'입니다.
원문 페이지에서 '미세먼지(PM10)'와 '초미세먼지(PM2.5)'의 현재 수치와 등급(좋음/보통/나쁨 등), 단위(㎍/㎥), 관측 시각을 추출하세요.
가장 구체적인 행정동(여의도동) 기준이 우선이며, 불가하면 '영등포구' 수준을 사용하세요.
반드시 아래 JSON 스키마만 출력하세요(추가 텍스트 금지).

{
  "pm10_value": <number or null>,
  "pm10_grade": "<string or null>",
  "pm25_value": <number or null>,
  "pm25_grade": "<string or null>",
  "unit": "<string or null>",
  "observed_at": "<string or null>",
  "source_url": "<string>",
  "source_title": "<string>"
}

가능하면 값을 모두 채우되, 원문에 없는 항목은 null로 두세요.
"""

USER_PROMPT_TEMPLATE = """\
다음을 수행:
1) naver.com 도메인에서만 검색/열람.
2) '{loc} 미세먼지' 또는 '{loc} 초미세먼지' 등 한국어 쿼리 사용.
3) 가장 신뢰되는 네이버 공식/날씨 페이지를 열람하여 현재 수치를 파싱.
4) 지정된 JSON만 반환(불필요한 설명 금지).
"""

EXPECTED_KEYS = [
    "pm10_value",
    "pm10_grade",
    "pm25_value",
    "pm25_grade",
    "unit",
    "observed_at",
    "source_url",
    "source_title",
]


def _strip_code_fence(text: str) -> str:
    """Remove optional JSON code fences from the model output."""

    match = re.match(r"^\s*```(?:json)?\s*([\s\S]*?)\s*```\s*$", text.strip(), re.IGNORECASE)
    return match.group(1).strip() if match else text.strip()


def _extract_output_text(response: Any) -> str:
    """Best-effort conversion of the Responses API payload into plain text."""

    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    # Fallback: collect textual content from the response structure.
    output_chunks = getattr(response, "output", [])
    pieces = []
    for chunk in output_chunks:
        if not isinstance(chunk, dict):
            continue
        content = chunk.get("content")
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "output_text":
                    text = item.get("text")
                    if isinstance(text, str):
                        pieces.append(text)
        elif isinstance(content, str):
            pieces.append(content)
    return "".join(pieces)


def fetch_air_quality_from_naver(
    client: OpenAI,
    location: str = "영등포구 여의도동",
    model: str = DEFAULT_MODEL,
) -> Dict[str, Any]:
    """Use the GPT-4o Search Preview model to gather air quality data."""

    response = client.responses.create(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(loc=location)},
        ],
    )

    raw_text = _extract_output_text(response)
    raw_text = _strip_code_fence(raw_text)

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        data = {key: None for key in EXPECTED_KEYS}
        data["_raw"] = raw_text

    for key in EXPECTED_KEYS:
        data.setdefault(key, None)

    return data


def build_client() -> OpenAI:
    """Create an OpenAI client, ensuring the API key is present."""

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
    return OpenAI(api_key=api_key)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch current PM10/PM2.5 readings using GPT-4o Search Preview",
    )
    parser.add_argument(
        "--location",
        default="영등포구 여의도동",
        help="검색할 행정동 이름 (기본값: 영등포구 여의도동)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=(
            "사용할 GPT 모델 이름 (기본값: %(default)s). "
            "Search Preview 계열 모델 문자열을 입력하세요."
        ),
    )
    args = parser.parse_args()

    client = build_client()
    result = fetch_air_quality_from_naver(client, location=args.location, model=args.model)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
