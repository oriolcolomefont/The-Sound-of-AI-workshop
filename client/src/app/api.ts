import { QueryMessage, ResponseMessage } from "./models";

export const API = {
  clean(message: QueryMessage): Promise<ResponseMessage> {
    return API.post("clean", message);
  },
  variate(message: QueryMessage): Promise<ResponseMessage> {
    return API.post("variate", message);
  },

  post(action: string, message: QueryMessage): Promise<ResponseMessage> {
    return fetch("/api/" + action, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(message),
    }).then((httpResponse) => {
      if (!httpResponse.ok) {
        throw new Error("HTTP error: " + httpResponse.status);
      }
      return httpResponse.json();
    });
  },
};
