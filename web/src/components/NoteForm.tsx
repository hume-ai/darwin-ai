// web/src/components/NoteForm.tsx
'use client'

import React, { useState } from 'react'
import axios from 'axios'
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'
import { useToast } from '@/components/ui/use-toast'

export const NoteForm: React.FC = () => {
  const [username, setUsername] = useState('')
  const [folder, setFolder]     = useState('')
  const [heading, setHeading]   = useState('')
  const [content, setContent]   = useState('')
  const [tags, setTags]         = useState('')
  const [date, setDate]         = useState(() => new Date().toISOString().slice(0, 10))
  const [loading, setLoading]   = useState(false)
  const [serverLogs, setServerLogs] = useState<string | null>(null)
  const { toast } = useToast()

  const handleSave = async () => {
    console.log('🔔 [UI] handleSave', { username, folder, heading })
    setLoading(true)
    setServerLogs(null)

    try {
      const res = await axios.post('/api/notes', {
        username,
        notes_folder: folder,
        notes_heading: heading,
        content,
        tags: tags.split(',').map(t => t.trim()).filter(Boolean),
        date,
      })

      // show returned logs (stdout/stderr and any error)
      setServerLogs(res.data.logs)

      toast({
        title: 'Saved!',
        description: res.data.ok
          ? 'Note + graph ingestion complete.'
          : 'Ingestion had issues—see logs below.',
      })

      if (res.data.ok) {
        setHeading('')
        setContent('')
        setTags('')
      }
    } catch (err: any) {
      // capture logs even on 500
      const logs = err.response?.data?.logs ?? 'No logs returned'
      setServerLogs(logs)

      console.error('❌ [UI] Save failed:', err)
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'See logs below.',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Card className="max-w-lg mx-auto">
        <CardHeader>
          <CardTitle>Create New Note</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Label>Username</Label>
            <Input
              value={username}
              onChange={e => setUsername(e.target.value)}
            />
          </div>
          <div>
            <Label>Folder</Label>
            <Input
              value={folder}
              onChange={e => setFolder(e.target.value)}
            />
          </div>
          <div>
            <Label>Heading</Label>
            <Input
              value={heading}
              onChange={e => setHeading(e.target.value)}
            />
          </div>
          <div>
            <Label>Date</Label>
            <Input
              type="date"
              value={date}
              onChange={e => setDate(e.target.value)}
            />
          </div>
          <div>
            <Label>Tags</Label>
            <Input
              placeholder="tag1,tag2"
              value={tags}
              onChange={e => setTags(e.target.value)}
            />
          </div>
          <div>
            <Label>Content</Label>
            <Textarea
              className="h-32"
              value={content}
              onChange={e => setContent(e.target.value)}
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button onClick={handleSave} disabled={loading}>
            {loading ? 'Saving…' : 'Save Note'}
          </Button>
        </CardFooter>
      </Card>

      {serverLogs && (
        <div className="max-w-lg mx-auto mt-4 p-4 bg-gray-100 rounded">
          <h3 className="font-semibold mb-2">Server Logs</h3>
          <pre className="whitespace-pre-wrap text-sm">{serverLogs}</pre>
        </div>
      )}
    </>
  )
}