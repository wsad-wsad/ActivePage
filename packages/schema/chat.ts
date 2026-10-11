enum MessageType {
  system = "system",
  user = "user",
  assistant = "assistant",
  reasoning = "reasoning",
  tool = "tool",
  skill = "skill"
}

type BaseMessage = {
  text: string,
  type: MessageType
  id: string          // hash

  token_count: number
}

export type Message =
  | (BaseMessage & { type: MessageType.system | MessageType.user | MessageType.assistant })
  | (BaseMessage & { type: MessageType.tool; toolId: string })
  | (BaseMessage & { type: MessageType.skill; skillId: string });

export interface Conversation {
  message: [Message],

  id: string
}
