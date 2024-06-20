export type QueryMessage = {
  id: number;
  type: "query";
  input: "melody" | "prompt";
  prompt?: string;
  working?: boolean;
  melody?: string;
};

export type ResponseMessage = {
  id: number;
  type: "response";
  melody?: string;
  error?: string;
  text?: string;
  wav?: string;
  uuid?: string;
};

export type ChatMessage = QueryMessage | ResponseMessage;
