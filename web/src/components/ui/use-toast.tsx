"use client";

export function useToast() {
  return {
    toast: (options: { title: string; description?: string; variant?: string }) => {
      console.log('Toast:', options);
    },
  };
}