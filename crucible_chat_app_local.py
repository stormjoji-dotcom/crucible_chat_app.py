import random
from pathlib import Path

import streamlit as st
from openai import OpenAI


st.set_page_config(page_title="시련 인터랙션", page_icon="🎭", layout="wide")

IMAGE_ROOT = Path("images")
ABIGAIL_NAME = "아비게일 윌리엄즈"
ABIGAIL_STORY_KEY = "abigail_story"
STORY_LOG_HEIGHT = 420
FREE_CHAT_HEIGHT = 520


st.markdown(
    """
<style>
.stApp {
    background: linear-gradient(135deg, #101014 0%, #17171d 55%, #1f1a1a 100%);
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.5rem;
    max-width: 1450px;
}
.top-title {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px 24px;
    margin-bottom: 18px;
}
.top-title h1 {
    margin: 0;
    color: #f7f2ea;
    font-size: 2.4rem;
}
.top-title p {
    margin: 8px 0 0 0;
    color: #d9d0c4;
    font-size: 1rem;
}
.side-card, .status-card, .chat-header, .big-image-wrap, .story-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 16px;
    margin-bottom: 14px;
}
.affection-box {
    background: rgba(255,90,120,0.08);
    border: 1px solid rgba(255,90,120,0.18);
    border-radius: 16px;
    padding: 12px 14px;
    margin-top: 8px;
}
.tip {
    color: #d2c8bc;
    font-size: 0.9rem;
    line-height: 1.5;
}
.small-status {
    color: #efe6d8;
    font-size: 0.95rem;
    line-height: 1.7;
}
.event-box {
    background: rgba(255,215,120,0.08);
    border: 1px solid rgba(255,215,120,0.16);
    border-radius: 16px;
    padding: 12px 14px;
    margin-bottom: 12px;
    color: #f6e7ca;
}
.choice-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 14px;
    margin-top: 12px;
}
.chapter-pill {
    display: inline-block;
    margin-right: 8px;
    margin-bottom: 8px;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.84rem;
    color: #f7f2ea;
    background: rgba(255,255,255,0.08);
}
.chapter-pill.done {
    background: rgba(255,140,160,0.25);
    border: 1px solid rgba(255,140,160,0.35);
}
.chapter-pill.active {
    background: rgba(255,214,120,0.18);
    border: 1px solid rgba(255,214,120,0.28);
