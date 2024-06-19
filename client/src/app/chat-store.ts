import { create } from "zustand";

export type QueryMessage = {
  id: number;
  type: "query";
  request?: string;
  working?: boolean;
};

interface ChatStore {
  nextId: number;
  messages: QueryMessage[];
  sendRequest(messageId: number, request: string): void;
}

export const useChatStore = create<ChatStore>((set, get) => ({
  nextId: 2,
  messages: [{ id: 1, type: "query" }],

  sendRequest(messageId, request) {
    const { nextId, messages } = get();
    const message = messages.find((m) => m.id === messageId);
    if (!message) return;
    message.request = request;
    message.working = true;
    set({ nextId: nextId + 1, messages });
    fetch("/api/abc", {
      method: "POST",
      body: JSON.stringify({ message }),
    }).then((response) => {
      console.log({ response });
    });
  },
}));
