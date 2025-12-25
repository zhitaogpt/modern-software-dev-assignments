from mcp.server.fastmcp import FastMCP
from week3.server.tools import hn, kalshi

# Initialize the MCP Server
mcp = FastMCP("Week3-Toolkit")

# --- Register Hacker News Tools ---

@mcp.tool()
async def hn_get_hot_stories(hours: int = 24, min_points: int = 50, limit: int = 20) -> str:
    """
    Get trending stories from Hacker News from the last N hours.
    
    Args:
        hours: How many hours to look back (default: 24)
        min_points: Minimum points threshold to filter noise (default: 50)
        limit: Max number of stories to return (default: 20)
    """
    return await hn.fetch_hot_stories(hours, min_points, limit)

@mcp.tool()
async def hn_get_story_details(story_id: str) -> str:
    """
    Get details and top comments for a specific Hacker News story.
    Use this when a story's title is vague or you need community insights.
    
    Args:
        story_id: The ID of the story (found in the 'id' field from get_hot_stories)
    """
    return await hn.fetch_story_details(story_id)

# --- Register Kalshi (Prediction Market) Tools ---

@mcp.tool()
async def kalshi_search(query: str = "", limit: int = 10) -> str:
    """
    Search for prediction markets on Kalshi.
    Use this to check odds/probabilities on real-world events (Economics, Politics, Climate).
    
    Args:
        query: Keywords to search for (e.g., "Fed", "Rate", "Trump"). If empty, returns trending markets.
    """
    return await kalshi.search_markets(query, limit)

@mcp.tool()
async def kalshi_details(ticker: str) -> str:
    """
    Get full details for a specific Kalshi market ticker.
    """
    return await kalshi.get_market_details(ticker)



# --- Define Prompts ---

@mcp.prompt()
def summarize_hn_trends():
    """
    Generates a high-quality briefing of the latest tech trends from Hacker News.
    """
    return (
        "你是一名资深的技术趋势分析师。你的任务是根据 Hacker News 的实时数据生成一份高质量的《技术动态简报》。\n\n"
        "工作流程建议：\n"
        "1. 调用 `hn_get_hot_stories` 获取过去 24 小时的热门文章（建议 min_points=60）。\n"
        "2. 浏览标题。对于那些听起来非常重大（如大型收购、重大发布、突破性技术）的文章：\n"
        "   - **强烈建议** 调用你原生的 `web_fetch` 工具直接读取文章 URL 的正文内容。\n"
        "   - 同时可以调用 `hn_get_story_details` 查看 HN 社区的评论，了解业界反馈。\n"
        "3. 将信息归类为“重大新闻”、“技术突破”、“社区热点”等主题。\n"
        "4. **严禁仅根据标题猜测内容**。请基于读取到的网页正文或深度评论进行总结。\n"
        "5. 最终简报应包含：核心事件描述、为什么这很重要、以及社区的典型观点。\n"
        "6. 请用中文回复，风格应客观、专业且精炼。"
    )

if __name__ == "__main__":
    mcp.run()
