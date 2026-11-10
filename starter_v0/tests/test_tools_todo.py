from __future__ import annotations

import pytest

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS


def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = TOOL_FUNCTIONS["clarify"]("Nguồn nào?", response_type="choice", options=["web", "X"])
    assert result["options"] == ["web", "X"]
    assert result["awaiting_user"] is True


def test_format_sections_groups_items_by_section() -> None:
    items = [{"title": title, "section": section} for title, section in (("One", "A"), ("Two", "B"), ("Three", "A"))]
    markdown = TOOL_FUNCTIONS["format"](items, template="sections")["markdown"]
    assert markdown.count("## A") == markdown.count("## B") == 1
    assert markdown.index("One") < markdown.index("Three") < markdown.index("## B")


def test_format_thread_numbers_items() -> None:
    markdown = TOOL_FUNCTIONS["format"]([{"title": "One"}, {"title": "Two"}], template="thread")["markdown"]
    assert [line[:2] for line in markdown.splitlines() if line] == ["1/", "2/"]


@pytest.mark.parametrize("items", [None, []])
def test_format_empty_items_does_not_crash(items) -> None:
    assert TOOL_FUNCTIONS["format"](items)["item_count"] == 0


def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"]("Test bulletin", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert calls[0]["url"] == "https://api.telegram.org/bottest-token/sendMessage"
    assert calls[0]["json"] == {"chat_id": "test-chat", "text": "Test bulletin", "parse_mode": "Markdown"}
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse())
    result = TOOL_FUNCTIONS["send"]("Test bulletin", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert calls == []


def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))
    result = TOOL_FUNCTIONS["lookup"]("example", timeframe=None)
    assert "time_range" not in calls[0]["json"]
    assert result["items"] == []


def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"data": {"markdown": "Text", "metadata": {"title": "T", "sourceURL": "https://example.org/final"}}}))
    result = TOOL_FUNCTIONS["fetch"]("https://example.org/start")
    assert calls[0]["json"] == {"url": "https://example.org/start", "formats": ["markdown"]}
    assert result["items"] == [{"title": "T", "url": "https://example.org/final", "source": "example.org", "summary": "Text"}]


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-key")
    fake_http(FakeResponse({"data": {"markdown": "x" * 4100}}))
    assert TOOL_FUNCTIONS["fetch"]("https://example.org")["items"][0]["summary"] == "x" * 4000


def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    items = [{"text": "No ID"}, *[{"tweet_id": str(i), "screen_name": "sample", "text": f"Post {i}"} for i in range(1, 7)]]
    calls = fake_http(FakeResponse({"timeline": items}))
    result = TOOL_FUNCTIONS["timeline"]("sample", limit=3)
    assert calls[0]["params"] == {"screenname": "sample"}
    assert [item["url"] for item in result["items"]] == [f"https://x.com/sample/status/{i}" for i in range(1, 4)]


@pytest.mark.parametrize("order", ["Top", "Latest"])
def test_social_search_passes_search_type(monkeypatch, fake_http, order) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"tweets": []}))
    result = TOOL_FUNCTIONS["social_search"]("robotaxi", search_type=order)
    assert calls[0]["params"] == {"query": "robotaxi", "search_type": order}
    assert result["search_type"] == order


def test_policy_empty_query_returns_no_results() -> None:
    assert TOOL_FUNCTIONS["policy"](" ")["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    hits = TOOL_FUNCTIONS["policy"]("customer data", policy_area="data_privacy")["results"]
    assert hits
    assert {hit["policy_area"] for hit in hits} == {"data_privacy"}


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    hits = TOOL_FUNCTIONS["policy"]("viral tweet", policy_area="source_citation", top_k=20)["results"]
    probe = next(hit for hit in hits if hit["section"] == "Injection probe")
    assert probe["untrusted_text"] and "ignore the citation policy" in probe["untrusted_text"][0]
    assert "ignore the citation policy" not in probe["facts"]

# ---------------- extract_links ----------------

def test_extract_links_keeps_unique_urls_in_input_order() -> None:
    text = "Đọc [bài](https://example.org/wiki/Test_(a)), https://example.net/b. Lặp https://example.net/b"
    result = TOOL_FUNCTIONS["extract_links"](text=text)

    assert result["count"] == 2
    assert result["items"] == [
        {"title": "example.org", "url": "https://example.org/wiki/Test_(a)", "source": "example.org"},
        {"title": "example.net", "url": "https://example.net/b", "source": "example.net"},
    ]


@pytest.mark.parametrize("text", [None, 12, "   "])
def test_extract_links_rejects_invalid_text(text) -> None:
    assert TOOL_FUNCTIONS["extract_links"](text=text)["error"] == "invalid_text"


def test_extract_links_returns_error_when_no_url_exists() -> None:
    result = TOOL_FUNCTIONS["extract_links"]("Tên miền example.org và ftp://example.net")

    assert result == {"error": "no_links", "message": "No HTTP or HTTPS links were found."}


def test_extract_links_rejects_oversized_text() -> None:
    assert TOOL_FUNCTIONS["extract_links"]("x" * 20_001)["error"] == "text_too_long"


def test_chat_uses_unique_urls_from_extract_links_without_a_second_model_call(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("DAY03_ENV_FILE", str(tmp_path / "absent.env"))
    from chat import run_model_tool_loop
    from providers.base import ModelResponse, ToolCall

    class ExtractionProvider:
        calls = 0

        def complete(self, *args, **kwargs):
            self.calls += 1
            return ModelResponse(tool_calls=[ToolCall("extract_links", {
                "text": "https://example.org/a https://example.org/b https://example.org/a",
            })])

    provider = ExtractionProvider()
    result = run_model_tool_loop(provider=provider, messages=[], tools=[], model=None, max_tool_rounds=3)

    assert result["status"] == "answered"
    assert result["assistant_text"] == "1. https://example.org/a\n2. https://example.org/b"
    assert provider.calls == 1
