"use client";
import { useState } from "react";
import { QueryMessage } from "../app/models";
import { SAMPLES } from "../data";
import { Spinner } from "./Spinner";

export function ChatQuery({
  message,
  onSend,
}: {
  message: QueryMessage;
  onSend: (text: string) => void;
}) {
  return message.prompt ? (
    <ChatQuerySent message={message} />
  ) : (
    <ChatQueryOpen message={message} onSend={onSend} />
  );
}

function ChatQuerySent({ message }: { message: QueryMessage }) {
  return (
    <div className="flex flex-col items-end">
      <p className="text-xl">🫵 You</p>
      <pre className="text-sm w-5/6 p-2 bg-zinc-600 text-wrap rounded">
        {message.prompt}
      </pre>
      {message.working ? <Spinner className="mt-2" /> : null}
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
      {message.input === "melody" ? (
        <>
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
        </>
      ) : message.input === "prompt" ? (
        <p>How can I variate your melody?</p>
      ) : null}
      <div>
        <textarea
          className="text-sm h-40 w-full p-2 bg-zinc-600 focus:outline-none"
          value={text}
          onChange={(e) => setText(e.target.value)}
        ></textarea>
        <button
          className="bg-emerald-500 rounded px-4 py-2 disabled:opacity-25"
          disabled={text === ""}
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
