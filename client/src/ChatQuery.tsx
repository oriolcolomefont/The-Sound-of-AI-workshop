"use client";
import { useState } from "react";
import { Spinner } from "./Spinner";
import { QueryMessage } from "./app/chat-store";
import { SAMPLES } from "./data";

export function ChatQuery({
  message,
  onSend,
}: {
  message: QueryMessage;
  onSend: (text: string) => void;
}) {
  return message.request ? (
    <ChatQuerySent message={message} />
  ) : (
    <ChatQueryOpen message={message} onSend={onSend} />
  );
}

function ChatQuerySent({ message }: { message: QueryMessage }) {
  return (
    <div className="flex flex-col items-end">
      <p>You:</p>
      <pre className="text-sm w-5/6 p-2 bg-zinc-600 text-wrap">
        {message.request}
      </pre>
      {message.working ? <Spinner /> : null}
    </div>
  );
}

function ChatQueryOpen({
  message,
  onSend,
}: {
  message: QueryMessage;
  onSend: (text: string) => void;
}) {
  const [text, setText] = useState("");
  return (
    <div className="w-full flex flex-col gap-2">
      <p>Write an abc melody:</p>
      {text === "" ? (
        <p>
          Or choose a sample:{" "}
          <button
            className="p-1 bg-zinc-600 rounded"
            onClick={() => setText(SAMPLES.tunisia)}
          >
            A night in tunisia
          </button>
        </p>
      ) : null}
      <div>
        <textarea
          className="text-sm h-40 w-full p-2 bg-zinc-600 focus:outline-none"
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        <button
          className="bg-emerald-500 rounded px-4 py-2"
          onClick={() => {
            onSend(text);
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
