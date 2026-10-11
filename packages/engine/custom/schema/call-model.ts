import type { CallModel } from "../../schema/call-model"

enum ApiType {
  openai = "openai",
}

export interface CallModelCustom extends CallModel {
  apiType: ApiType,
  baseUrl: URL

  apiKey: string
}
