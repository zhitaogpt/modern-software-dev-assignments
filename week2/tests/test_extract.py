import os
import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


def test_llm_extract_explicit():
    """测试 LLM 对带有明确前缀的任务提取"""
    text = "TODO: Fix the login bug\nAction: Update documentation"
    items = extract_action_items_llm(text)
    
    assert isinstance(items, list)
    # 使用关键词命中逻辑，不要求 100% 字符串匹配
    assert any("login" in item.lower() for item in items)
    assert any("documentation" in item.lower() for item in items)


def test_llm_extract_natural_language():
    """测试 LLM 从自然语言对话中提取任务的能力（这是规则引擎做不到的）"""
    text = """
    We had a quick chat today. Sarah mentioned that we need to 
    prepare the slide deck by Friday. Also, can you remind 
    Bob to review the PR? We also discussed the weather.
    """
    items = extract_action_items_llm(text)
    
    assert isinstance(items, list)
    # 验证关键动作是否被捕捉
    assert any("slide" in item.lower() for item in items)
    assert any("review" in item.lower() or "pr" in item.lower() for item in items)
    # 验证无关信息（天气）是否被过滤
    assert not any("weather" in item.lower() for item in items)


def test_llm_extract_empty_or_none():
    """测试边界情况：空字符串或没有任何任务的文本"""
    # 场景 1: 完全空
    assert extract_action_items_llm("") == []
    
    # 场景 2: 只有闲聊，没有任务
    text = "The quick brown fox jumps over the lazy dog. It's a sunny day."
    items = extract_action_items_llm(text)
    assert len(items) == 0
