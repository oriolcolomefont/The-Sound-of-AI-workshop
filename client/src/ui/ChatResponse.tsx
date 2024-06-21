"use client";
import { useState } from "react";
import { ResponseMessage } from "../app/models";

export function ChatResponse({ message }: { message: ResponseMessage }) {
  const [isMelodyVisible, setMelodyVisible] = useState(false);
  return (
    <div className="flex flex-col">
      <p className="text-lg">🤖 Soroll</p>
      <div className="w-5/6 bg-zinc-600 p-4 rounded-lg">
        {message.text && <div>{message.text}</div>}
        {message.uuid && (
          <>
            <audio
              controls
              src={`/assets/${message.uuid}.wav`}
              className="mt-2"
            />
          </>
        )}
        {message.error && (
          <div className="text-orange-400">💣 💥 Hmmmm: {message.error}</div>
        )}
      </div>
      {isMelodyVisible ? (
        <pre className="">{message.melody}</pre>
      ) : (
        <button
          onClick={() => setMelodyVisible(true)}
          className="text-blue-400"
        >
          melody
        </button>
      )}
    </div>
  );
}
