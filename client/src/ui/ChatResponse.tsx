"use client";
import { ResponseMessage } from "../app/models";

export function ChatResponse({ message }: { message: ResponseMessage }) {
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
          <div className="text-orange-400">
            💣 💥 We f*cked up: {message.error}
          </div>
        )}
      </div>
    </div>
  );
}
