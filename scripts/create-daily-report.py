#!/usr/bin/env python3
"""
create-daily-report.py - 生成AI日报完整版
使用MiniMax MCP WebSearch抓取24小时内AI新闻
输出结构化日报内容
"""
import subprocess, json, time, sys

MINIMAX_KEY = "sk-cp-GQOk17jk3KLWeNxjTSp5knUIpm3eYmMo11505xW-q5CgcnUIczgVfPvM54QETdCMGXKlTfsDnwp8NLmgFC3d6Ll6qz-YQE0kz3kNZhZ6GjVTC4TPwR28L0k"

def call_mcp_tool(tool_name, arguments):
    proc = subprocess.Popen(
        ["/root/.local/bin/uvx", "minimax-coding-plan-mcp", "-y"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"MINIMAX_API_KEY": MINIMAX_KEY, "MINIMAX_API_HOST": "https://api.minimaxi.com", "PATH": "/root/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin"}
    )
    proc.stdin.write((json.dumps({"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}) + "\n").encode())
    proc.stdin.flush()
    time.sleep(0.5)
    proc.stdin.write((json.dumps({"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":tool_name,"arguments":arguments}}) + "\n").encode())
    proc.stdin.flush()
    proc.stdin.close()
    time.sleep(10)
    out = proc.stdout.read().decode(errors='replace')
    for line in out.strip().split("\n"):
        if line.strip() and line.startswith("{"):
            try:
                d = json.loads(line)
                if d.get("id") == 1:
                    result = d.get("result", {})
                    content = result.get("content", [])
                    for item in content:
                        if item.get("type") == "text":
                            return item["text"]
            except: pass
    return ""

if __name__ == "__main__":
    date = sys.argv[1] if len(sys.argv) > 1 else "2026-03-21"
    print(f"正在抓取{date}的AI资讯...")
    
    results = {}
    searches = [
        ("cn", "AI模型发布新闻 今天 2026年3月"),
        ("tools", "AI工具 新功能 自动化 今天 2026年3月"),
        ("openclaw", "OpenClaw Claude AI智能体 今天 2026年3月"),
    ]
    
    for key, query in searches:
        print(f"  搜索: {query}")
        r = call_mcp_tool("web_search", {"query": query})
        results[key] = r
        print(f"  获得: {len(r)}字符")
        time.sleep(2)
    
    print("\n=== 原始数据 ===")
    for k, v in results.items():
        print(f"\n[{k}]\n{v[:500]}\n")
