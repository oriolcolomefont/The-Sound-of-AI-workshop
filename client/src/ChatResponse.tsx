"use client";
import { ResponseMessage } from "./app/chat-store";

export function ChatResponse({ message }: { message: ResponseMessage }) {
  return (
    <div className="flex flex-col">
      <p>Soroll:</p>
      <div className="w-5/6 bg-zinc-600 p-4 rounded-lg">
        <div>{message.text}</div>
        {message.wav ? (
          <audio controls src={message.wav} className="mt-2" />
        ) : null}
      </div>
    </div>
  );
}
