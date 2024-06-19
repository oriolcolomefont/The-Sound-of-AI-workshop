"use client";

import { useEffect } from "react";
import { useChatStore } from "../app/chat-store";
import { ChatQuery } from "./ChatQuery";
import { ChatResponse } from "./ChatResponse";

export function Chat() {
  const chats = useChatStore();

  useEffect(() => {
    window.scrollTo({
      top: document.documentElement.scrollHeight,
      behavior: "smooth",
    });
  }, [chats.nextId]);

  return (
    <div className="flex flex-col gap-4">
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
