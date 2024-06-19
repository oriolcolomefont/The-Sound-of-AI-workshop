"use client";

import { useState } from "react";
import { Spinner } from "./Spinner";
import { QueryMessage, ResponseMessage, useChatStore } from "./app/chat-store";

const SAMPLES = {
  tunisia: `X:1
L:1/8
Q:1/4=120
M:4/4
K:F
A, |"Eb7" (3B,_DF c4 BF |"Dm" ^G A3- A3 A, |"Eb7" (3B,_DF c4 BF |"Dm" A4 z2 z A, | 
"Eb7" (3B,_DF c4 BF |"Dm" ^G A3- A4 |"Em7b5" ABAG"A7b5" _E2 ^CD- |"Dm" D4 z2 z A, | 
"Eb7" (3B,_DF c4 BF |"Dm" ^G A3- A3 A, |"Eb7" (3B,_DF c4 BF |"Dm" A4 z2 z A, | (3B,"Eb7"_DF c4 BF | %14
"Dm" ^G A3- A3 A |"Em7b5" ABAG"A7b5" _E2 ^CD- |"Dm" D6 A2 |"Am7b5" c4 A3 G | 
 ^F2"D7b9" _ed- d2 cA |"Gm" B G2 ^F- FGAG- | G4 z4 |"Gm7b5" B4 G3 F | E2"C7b9" _dc- c2 B^G | 
"F6" A3 F G2 FE- |"Em7b5" E4"A7b9" z2 z A, |"Eb7" (3B,_DF c4 BF |"Dm" ^G A3- A3 A, | 
"Eb7" (3B,_DF c4 BF |"Dm" A4 z2 z A, | (3B,"Eb7"_DF c4 BF |"Dm" ^G A3- A4 | 
"Em7b5" ABAG"A7b5" _E2 ^CD- |"Dm" D4 z4 |
`,
};

export function Chat() {
  const chats = useChatStore();
  return (
    <div>
      {chats.messages.map((message) =>
        message.type === "query" ? (
          <ChatQuery
            key={message.id}
            message={message}
            onSend={(request) => {
              chats.sendRequest(message.id, request);
            }}
          />
        ) : message.type === "response" ? (
          <ChatResponse key={message.id} message={message} />
        ) : null
      )}
    </div>
  );
}

function ChatResponse({ message }: { message: ResponseMessage }) {
  return (
    <div className="flex flex-col gap-2">
      <p>Response:</p>
      <pre className="text-sm w-full p-2 bg-zinc-600 text-wrap">
        {message.text}
      </pre>
    </div>
  );
}

function ChatQuery({
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
      {message.request ? (
        <div className="flex flex-col gap-4">
          <pre className="text-sm w-full p-2 bg-zinc-600 text-wrap">
            {message.request}
          </pre>
          {message.working ? <Spinner /> : null}
        </div>
      ) : (
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
      )}
    </div>
  );
}
