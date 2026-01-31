import arxiv
import os
import requests

def download_paper(search_query, filename_base):
    search = arxiv.Search(
        query=search_query,
        max_results=1,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    paper = next(search.results(), None)
    if paper:
        print(f"Found: {paper.title} ({paper.entry_id})")
        filepath = f"papers/{filename_base}.pdf"
        paper.download_pdf(filename=filepath)
        return paper
    else:
        print(f"Not found: {search_query}")
        return None

os.makedirs("papers", exist_ok=True)

papers_to_find = [
    ("Large Language Models Can be Lazy Learners", "lazy_learners"),
    ("LLM Critics Help Catch LLM Bugs", "llm_critics_bugs"),
    ("CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing", "critic_self_correct"),
    ("Token-Budget-Aware LLM Reasoning", "token_budget_reasoning"),
    ("Budget-Aware Anytime Reasoning with LLM-Synthesized Preference Data", "budget_anytime_reasoning"),
    ("Self-Critique and Adapt: Large Language Models Can Self-Correct", "self_critique_adapt")
]

readme_content = "# Downloaded Papers\n\n"

for title, filename in papers_to_find:
    paper = download_paper(title, filename)
    if paper:
        readme_content += f"## [{paper.title}](papers/{filename}.pdf)\n"
        readme_content += f"- **Authors**: {', '.join([a.name for a in paper.authors])}\n"
        readme_content += f"- **Year**: {paper.published.year}\n"
        readme_content += f"- **Abstract**: {paper.summary.replace(chr(10), ' ')}\n\n"

with open("papers/README.md", "w") as f:
    f.write(readme_content)
