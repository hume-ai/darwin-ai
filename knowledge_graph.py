# knowledge_graph.py

import os
import re
import json
import frontmatter              # pip install python-frontmatter
import openai                   # pip install openai
import pandas as pd            # pip install pandas
from dotenv import load_dotenv # pip install python-dotenv
from neo4j import GraphDatabase  # pip install neo4j-driver

# ------------------------------------------------------------------------------
# 1) Load environment
# ------------------------------------------------------------------------------
load_dotenv()
VAULT_PATH              = os.getenv("VAULT_PATH", "vault")
PROCESSED_FILES_PATH    = os.getenv("PROCESSED_FILES_PATH", "processed_files.json")
OPENAI_API_KEY          = os.getenv("OPENAI_API_KEY")
NEO4J_URI               = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER              = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD          = os.getenv("NEO4J_PASSWORD", "12345678")
NEO4J_DB                = os.getenv("NEO4J_DB", "neo4j")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment!")
openai.api_key = OPENAI_API_KEY

# ------------------------------------------------------------------------------
# 1.5) Track processed files
# ------------------------------------------------------------------------------
def load_processed_files(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return set(json.load(f))
    return set()

def save_processed_files(path, processed):
    with open(path, "w") as f:
        json.dump(list(processed), f)

# ------------------------------------------------------------------------------
# 2) Utility: Chunk text into overlapping windows
# ------------------------------------------------------------------------------
def chunk_text(text, chunk_size=150, overlap=30):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        if end == len(words):
            break
        start += chunk_size - overlap
    return chunks

# ------------------------------------------------------------------------------
# 3) Extract SPO triples via OpenAI
# ------------------------------------------------------------------------------
client = openai.OpenAI(api_key=OPENAI_API_KEY)
llm_model_name = "gpt-3.5-turbo"

def extract_triples_from_chunk(system_prompt, user_prompt, temperature=0.0, max_tokens=1024):
    resp = client.chat.completions.create(
        model=llm_model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    raw = resp.choices[0].message.content.strip()
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            for v in data.values():
                if isinstance(v, list):
                    data = v
                    break
    except Exception:
        m = re.search(r"(\[.*\])", raw, re.DOTALL)
        data = json.loads(m.group(1)) if m else []
    triples = []
    for t in data:
        if isinstance(t, dict) and all(
            k in t and isinstance(t[k], str) for k in ("subject", "predicate", "object")
        ):
            triples.append(t)
    return triples

# ------------------------------------------------------------------------------
# 4) Normalize & dedupe triples
# ------------------------------------------------------------------------------
def normalize_and_dedupe(triples):
    seen = set()
    normalized = []
    for t in triples:
        s = t["subject"].strip().lower()
        p = re.sub(r"\s+", " ", t["predicate"].strip().lower())
        o = t["object"].strip().lower()
        if not (s and p and o):
            continue
        key = (s, p, o)
        if key in seen:
            continue
        seen.add(key)
        normalized.append({"subject": s, "predicate": p, "object": o})
    return normalized

# ------------------------------------------------------------------------------
# 5) Ingest to Neo4j
# ------------------------------------------------------------------------------
def ingest_to_neo4j(notes, triples):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session(database=NEO4J_DB) as sess:
        for note in notes:
            sess.run(
                """
                MERGE (n:Note {id:$id})
                SET n.heading=$h, n.date=$d
                """,
                {"id": note["id"], "h": note["heading"], "d": note["date"]}
            )
            for tag in note.get("tags", []):
                sess.run(
                    """
                    MERGE (t:Tag {name:$tag})
                    WITH t
                    MATCH (n:Note {id:$id})
                    MERGE (n)-[:HAS_TAG]->(t)
                    """,
                    {"tag": tag, "id": note["id"]}
                )
        for t in triples:
            s, p, o = t["subject"], t["predicate"], t["object"]
            rel = p.replace(" ", "_").upper()
            sess.run("MERGE (a:Entity {name:$s})", {"s": s})
            sess.run("MERGE (b:Entity {name:$o})", {"o": o})
            sess.run(
                f"""
                MATCH (a:Entity {{name:$s}}),(b:Entity {{name:$o}})
                MERGE (a)-[:{rel}]->(b)
                """,
                {"s": s, "o": o}
            )
    driver.close()

# ------------------------------------------------------------------------------
# 6) Main entrypoint: only process new .md files
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    vault_dir = os.path.abspath(VAULT_PATH)
    print(f"→ Scanning vault at: {vault_dir}")
    if not os.path.isdir(vault_dir):
        raise RuntimeError(f"Vault directory not found: {vault_dir}")

    # A) Load already‐processed filenames
    processed = load_processed_files(PROCESSED_FILES_PATH)

    # B) Discover all .md files and compute which are new
    all_files = []
    for root, _, files in os.walk(vault_dir):
        for fname in files:
            if fname.lower().endswith(".md"):
                rel = os.path.relpath(os.path.join(root, fname), vault_dir)
                all_files.append(rel)

    new_files = [f for f in all_files if f not in processed]
    if not new_files:
        print("No new markdown files to process.")
        exit()

    print(f"  • {len(new_files)} new markdown files to process.")

    # C) Load contents + metadata for new files
    docs, notes = [], []
    for rel in new_files:
        path = os.path.join(vault_dir, rel)
        post = frontmatter.load(path)
        docs.append(post.content)
        notes.append({
            "id":      os.path.splitext(os.path.basename(rel))[0],
            "heading": post.metadata.get("notes_heading", ""),
            "date":    post.metadata.get("date", ""),
            "tags":    post.metadata.get("tags", []),
        })

    # D) Chunk & extract triples
    full_text = "\n\n".join(docs)
    print(f"Total characters to process: {len(full_text)}")
    print("Chunking text…")
    chunks = chunk_text(full_text)
    print(f"  • {len(chunks)} chunks created.")

    system_prompt = """
You are an AI expert specialized in knowledge graph extraction.
Your task is to identify and extract factual Subject-Predicate-Object (SPO) triples from the given text.
Focus on accuracy and adhere strictly to the JSON output format requested.
"""
    user_template = """Please extract Subject-Predicate-Object (S-P-O) triples from the text below.

Text:
```text
{chunk}
```"""

    all_triples = []
    for i, chunk in enumerate(chunks, start=1):
        print(f"Extracting triples from chunk {i}/{len(chunks)}…")
        prompt = user_template.format(chunk=chunk)
        all_triples.extend(extract_triples_from_chunk(system_prompt, prompt))

    normalized = normalize_and_dedupe(all_triples)
    print(f"Raw: {len(all_triples)} → Normalized & deduped: {len(normalized)}")

    # E) Ingest into Neo4j & mark files as processed
    print("Ingesting into Neo4j…")
    ingest_to_neo4j(notes, normalized)

    processed.update(new_files)
    save_processed_files(PROCESSED_FILES_PATH, processed)

    print("✅ All new data loaded into Neo4j. Done.")
