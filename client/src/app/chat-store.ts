import { create } from "zustand";

export type QueryMessage = {
  id: number;
  type: "query";
  request?: string;
  working?: boolean;
};

export type ResponseMessage = {
  id: number;
  type: "response";
  text: string;
};

export type ChatMessage = QueryMessage | ResponseMessage;

interface ChatStore {
  nextId: number;
  messages: ChatMessage[];
  sendRequest(messageId: number, request: string): void;
}
const getQueryMessage = (id: number, messages: ChatMessage[]) => {
  return messages.find(
    (m) => m.id === id && m.type === "query"
  ) as QueryMessage;
};

export const useChatStore = create<ChatStore>((set, get) => {
  const addResponse = (initiatorId: number, response: ResponseMessage) => {
    const { messages } = get();

    const initiator = getQueryMessage(initiatorId, messages);
    if (initiator) initiator.working = false;

    const newQuery: QueryMessage = { id: response.id + 1, type: "query" };
    const newMessages = [...messages, response, newQuery];
    const nextId = response.id + 2;
    set({ nextId, messages: newMessages });
  };

  return {
    nextId: 2,
    messages: [{ id: 1, type: "query" }],

    sendRequest(messageId, request) {
      const { nextId, messages } = get();
      const message = getQueryMessage(messageId, messages);
      if (!message) return;
      message.request = request;
      message.working = true;
      set({ nextId: nextId + 1, messages });
      fetch("/api/echo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(message),
      })
        .then((response) => response.json())
        .then((data) => {
          message.working = false;
          addResponse(messageId, data);
        })
        .catch((error) => {
          console.error({ error });
        });
    },
  };
});
