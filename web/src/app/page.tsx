import React from 'react';
import { NoteForm } from '@/components/NoteForm';

export default function Page() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Knowledge Vault</h1>
      <NoteForm />
    </main>
  );
}
