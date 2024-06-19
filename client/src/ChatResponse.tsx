"use client";
import { ResponseMessage } from "./app/chat-store";

export function ChatResponse({ message }: { message: ResponseMessage }) {
  return (
    <div className="flex flex-col">
      <p>Soroll:</p>
      <pre className="text-sm w-5/6 p-2 bg-zinc-600 text-wrap">
        {message.text}
      </pre>
    </div>
  );
}
