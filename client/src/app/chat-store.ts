import { create } from "zustand";
import { API } from "./api";
import { ChatMessage, QueryMessage, ResponseMessage } from "./models";

interface ChatStore {
  nextId: number;
  messages: ChatMessage[];
  melody?: string;
  sendRequest(messageId: number, request: string): void;
}
const getQueryMessage = (id: number, messages: ChatMessage[]) => {
  return messages.find(
    (m) => m.id === id && m.type === "query"
  ) as QueryMessage;
};

export const useChatStore = create<ChatStore>((set, get) => {
  const addResponse = (initiatorId: number, response: ResponseMessage) => {
    const { messages, melody } = get();

    const currentMelody = response.melody || melody;

    const initiator = getQueryMessage(initiatorId, messages);
    if (initiator) initiator.working = false;

    const newQuery: QueryMessage = {
      id: response.id + 1,
      type: "query",
      input: "prompt",
    };
    const newMessages = [...messages, response, newQuery];
    const nextId = response.id + 2;
    set({ nextId, messages: newMessages, melody: currentMelody });
  };

  return {
    nextId: 2,
    messages: [{ id: 1, type: "query", input: "melody" }],

    sendRequest(messageId, prompt) {
      const { nextId, messages, melody } = get();
      const message = getQueryMessage(messageId, messages);
      if (!message) return;
      message.prompt = prompt;
      message.working = true;
      set({ nextId: nextId + 1, messages });

      const sendRequest = message.input === "melody" ? API.clean : API.variate;

      if (message.input === "melody") {
        message.melody = message.prompt;
      } else {
        message.melody = melody;
      }

      sendRequest(message)
        .then((response) => {
          console.log({ response });
          message.working = false;
          addResponse(messageId, response);
        })
        .catch((error) => {
          message.working = false;
          addResponse(messageId, {
            id: message.id + 1,
            type: "response",
            error: error.message,
          });
        });
    },
  };
});
