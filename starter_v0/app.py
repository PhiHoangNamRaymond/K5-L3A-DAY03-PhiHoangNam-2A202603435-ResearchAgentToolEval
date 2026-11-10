from __future__ import annotations

import os

import streamlit as st

from chat import ARTIFACTS_DIR, run_model_tool_loop, trim_history
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools


@st.cache_resource
def load_agent():
    prompt = (ARTIFACTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    declarations = load_tool_declarations(ARTIFACTS_DIR / "tools.yaml")
    provider_name = os.getenv("LAB_UI_PROVIDER", "openrouter")
    default_model = "recursive/flint-v1.0:free" if provider_name == "openrouter" else None
    model = os.getenv("LAB_UI_MODEL") or default_model
    return prompt, to_openai_tools(declarations), make_provider(provider_name), provider_name, model


def show_tool_activity(events):
    if events:
        with st.expander("Hoạt động của công cụ"):
            for event in events:
                result = event.get("result", {})
                st.code(event["tool"], language=None)
                if "error" in result:
                    st.warning(result.get("message") or result["error"])
                elif "items" in result:
                    for item in result["items"]:
                        if item.get("url"):
                            st.text(item["url"])


def main():
    st.set_page_config(page_title="Research Agent Lab", page_icon="🔎")
    st.title("Research Agent Lab")
    st.caption("Tra cứu nguồn, đọc policy mẫu và trích đường dẫn từ văn bản.")
    with st.sidebar:
        st.subheader("Thử một câu hỏi")
        st.markdown(
            "- Trích các URL trong đoạn sau: https://example.org/a và https://example.org/b.\n"
            "- Theo policy nội bộ, có cần xác nhận trước khi đăng Telegram không?\n"
            "- Tóm tắt 5 bài đăng mới nhất giúp mình."
        )
        if st.button("Bắt đầu hội thoại mới"):
            st.session_state.turns = []

    turns = st.session_state.setdefault("turns", [])
    for turn in turns:
        with st.chat_message(turn["role"]):
            st.markdown(turn["content"])
            show_tool_activity(turn.get("tool_events", []))

    user_text = st.chat_input("Nhập yêu cầu nghiên cứu", max_chars=2500)
    if not user_text:
        return

    prompt, tools, provider, provider_name, model = load_agent()
    if provider_name == "openrouter" and not (model or "").endswith(":free"):
        st.error("UI OpenRouter dùng model có hậu tố :free.")
        return

    user = {"role": "user", "content": user_text}
    history = [{"role": turn["role"], "content": turn["content"]} for turn in turns]
    messages = [{"role": "system", "content": prompt}, *trim_history(history, 5), user]
    turns.append(user)
    with st.chat_message("user"):
        st.markdown(user_text)
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý…"):
            try:
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=tools,
                    model=model,
                    max_tool_rounds=3,
                    allow_external_actions=False,
                )
                answer = result["assistant_text"] or "Model chưa trả nội dung."
                events = result["tool_events"]
            except Exception as exc:
                status = getattr(exc, "status_code", None)
                label = f"HTTP {status}" if status else type(exc).__name__
                answer, events = f"Provider báo lỗi {label}. Hãy thử lại sau.", []
        st.markdown(answer)
        show_tool_activity(events)
    turns.append({"role": "assistant", "content": answer, "tool_events": events})


if __name__ == "__main__":
    main()
