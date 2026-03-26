"""
ResearchAgent— Autonomous Founder/CEO Research Agent
======================================================
Enhanced version for LegalSeva.org Internship Task.
Features: Multi-step reasoning, 2026-aware search, and link exploration.
"""

import os
import json
import argparse
import requests
from datetime import datetime
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "llama-3.3-70b-versatile"

memory = []
all_sources = []

def remember(role: str, content: str):
    """Add a message to the agent's internal memory."""
    memory.append({"role": role, "content": content})

def ask_groq(system_prompt: str, user_message: str, temp=0.3) -> str:
    """Core LLM Interface - Direct API call to Groq."""
    messages = [{"role": "system", "content": system_prompt}]
    messages += memory[-10:]  
    messages.append({"role": "user", "content": user_message})

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "max_tokens": 2048,
                "temperature": temp,
            },
            timeout=30,
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error contacting Groq: {str(e)}"

def web_search(query: str, max_results: int = 5) -> list:
    """Search engine tool - Updates global all_sources list."""
    print(f"  🔍 Agent Searching: {query}")
    results = []
    try:
        with DDGS() as ddgs:
            search_results = list(ddgs.text(query, max_results=max_results))
            for r in search_results:
                url = r.get("href", "")
                if url:
                    results.append({
                        "title": r.get("title", ""),
                        "url": url,
                        "snippet": r.get("body", ""),
                    })
                   
                    if url not in all_sources:
                        all_sources.append(url)
    except Exception as e:
        print(f"     ⚠️ Search Error: {e}")
    return results

def scrape_page(url: str) -> str:
    """Exploration tool - Scraping specific links for deep context."""
    print(f"  🌐 Agent Scraping Link: {url}")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
   
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
            
        text = soup.get_text(separator=" ", strip=True)
        return text[:4000] 
    except Exception as e:
        return f"Could not scrape {url}: {str(e)}"

def research_founder(founder: str) -> str:
    """Main Autonomous Pipeline with Reasoning Loop."""
    
    current_year = datetime.now().year
    system_prompt = f"""You are a Lead Research Agent. 
    Current Date: {datetime.now().strftime('%Y-%m-%d')}.
    Your goal is to build a factual, high-integrity profile of {founder}. 
    Focus on verifying 2025-2026 developments specifically."""

  
    print("\n📡 Phase 1: Broad Discovery & Search...")
    queries = [
        f"{founder} biography and early education",
        f"{founder} career milestones and leadership role",
        f"{founder} recent news and 2025 2026 achievements",
        f"{founder} vision and strategy for 2026"
    ]
    
    raw_findings = []
    for q in queries:
        results = web_search(q, max_results=2)
        for r in results:
            raw_findings.append(f"Source: {r['url']}\nSnippet: {r['snippet']}")

   
    print("\n🧠 Phase 2: Internal Reflection & Deep Dive...")
    remember("user", f"I have gathered initial snippets about {founder}: {raw_findings}")
    
    reflection = ask_groq(system_prompt, 
        "Based on these snippets, identify the most important URL to scrape for a deep dive into their 2025-2026 activity. Output ONLY the URL.")
    
    target_url = reflection.strip()
    if "http" in target_url:
        deep_content = scrape_page(target_url)
        remember("assistant", f"I decided to deep-dive into {target_url} for more detail.")
        remember("user", f"Here is the full text from that page:\n{deep_content}")

   
    print("\n📝 Phase 3: Finalizing Structured Report...")
    final_report = ask_groq(
        system_prompt,
        f"""Using all gathered data and your internal memory, write a comprehensive Markdown report for {founder}.
        
        Include these exact sections:
        # 1. Personal Background
        # 2. Career Journey
        # 3. Companies Founded / Led
        # 4. Key Achievements & Awards
        # 5. Leadership Style & Vision
        # 6. Recent News & Developments (Focus on 2025-2026)
        # 7. Notable Quotes
        # 8. Summary (A 3-sentence assessment)
        
        Format beautifully in Markdown. Be precise with dates."""
    )

    return final_report

def save_report(founder: str, content: str) -> str:
    os.makedirs("output", exist_ok=True)
    filename = f"{founder.lower().replace(' ', '_')}_report.md"
    path = os.path.join("output", filename)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Research Report: {founder}\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Agent Engine: {MODEL} via Groq\n\n---\n\n")
        f.write(content)
        f.write("\n\n---\n## 🛠 Agent Navigation Log\n")
        f.write(f"The agent autonomously explored {len(set(all_sources))} unique sources to verify facts.\n")
        for src in list(set(all_sources))[:10]: 
            f.write(f"* {src}\n")

    print(f"\nReport successfully saved to: {path}")
    return path

def main():
    parser = argparse.ArgumentParser(description="Autonomous Research Agent")
    parser.add_argument("--founder", required=True, help="Name of the person to research")
    args = parser.parse_args()

    print(f"\n🚀 Launching Autonomous Research for: {args.founder}")
    report_content = research_founder(args.founder)
    save_report(args.founder, report_content)

if __name__ == "__main__":
    main()