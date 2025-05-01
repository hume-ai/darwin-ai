// web/src/app/api/notes/route.ts
export const runtime = 'nodejs'

import { NextResponse } from 'next/server'
import * as fs from 'fs'
import * as path from 'path'
import * as matter from 'gray-matter'
import { spawnSync } from 'child_process'
import {
  Neo4jConnector,
  NEO4J_URI,
  NEO4J_USER,
  NEO4J_PASSWORD,
} from '@/lib/neo4j'

// ─── 1) Compute absolute vault directory under darwin-ai/ ────────────────────
const projectRoot = path.resolve(process.cwd(), '..')
const vaultRaw = process.env.VAULT_PATH || '../vault'           // default to "vault"
const vaultDir = path.isAbsolute(vaultRaw)
  ? vaultRaw
  : path.resolve(projectRoot, vaultRaw)

// ─── Neo4j client ───────────────────────────────────────────────────────────
const db = new Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

export async function POST(req: Request) {
  let logs = ''

  try {
    logs += `→ [API] cwd=${process.cwd()}\n`
    logs += `→ [API] vaultDir=${vaultDir}\n`
    logs += '→ [API] Received POST /api/notes\n'

    // 1) Parse request
    const { username, notes_folder, notes_heading, content, tags, date } =
      await req.json()
    logs += `   • Payload: ${JSON.stringify({
      username,
      notes_folder,
      notes_heading,
      date,
      tags,
    })}\n`

    // 2) Write the .md file to vaultDir
    logs += `→ [API] Writing Markdown to ${vaultDir}/${notes_folder}\n`
    const folderPath = path.join(vaultDir, notes_folder)
    fs.mkdirSync(folderPath, { recursive: true })

    const slug = notes_heading.toLowerCase().replace(/\s+/g, '-')
    const filePath = path.join(folderPath, `${slug}.md`)
    const md = matter.stringify(content, {
      username,
      notes_folder,
      notes_heading,
      tags,
      date,
    })
    fs.writeFileSync(filePath, md)
    logs += `   ✅ Written file: ${filePath}\n`

    // 3) Ingest metadata into Neo4j
    logs += '→ [API] Ingesting metadata into Neo4j…\n'
    await db.run_query(
      `MERGE (n:Note {id:$id})
       SET n += { heading:$h, folder:$f, date:$d, user:$u, tags:$t }`,
      { id: slug, h: notes_heading, f: notes_folder, d: date, u: username, t: tags }
    )
    for (const tag of tags) {
      await db.run_query(
        `MERGE (t:Tag { name:$tag })
         MATCH (n:Note { id:$id })
         MERGE (n)-[:HAS_TAG]->(t)`,
        { tag, id: slug }
      )
    }
    db.close()
    logs += '   ✅ Neo4j metadata ingested\n'

    // 4) Run Python ingestion script from project root
    logs += '→ [API] Spawning Python script knowledge_graph.py…\n'
    const scriptPath = path.resolve(projectRoot, 'knowledge_graph.py')
    logs += `   • scriptPath=${scriptPath}\n`
    const result = spawnSync('python3', [scriptPath], {
      cwd: projectRoot,
      env: { ...process.env, VAULT_PATH: vaultDir },
      encoding: 'utf-8',
    })
    logs += '--- [PYTHON STDOUT] ---\n' + (result.stdout || '') + '\n'
    logs += '--- [PYTHON STDERR] ---\n' + (result.stderr || '') + '\n'
    logs += '   ✅ Python ingestion finished\n'

    return NextResponse.json({ ok: true, logs }, { status: 201 })
  } catch (err: any) {
    console.error('💥 [API] Error:', err)
    logs += '‼️ [API ERROR]\n' + (err.stack || err.message || String(err)) + '\n'
    return NextResponse.json({ ok: false, logs }, { status: 500 })
  }
}