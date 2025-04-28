import {
    CopilotRuntime,
    ExperimentalEmptyAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    OpenAIAdapter,
    langGraphPlatformEndpoint
  } from "@copilotkit/runtime";;
  import OpenAI from "openai";
  import { NextRequest } from "next/server";
   
  // You can use any service adapter here for multi-agent support.
  const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
  const serviceAdapter = new ExperimentalEmptyAdapter();
  const llmAdapter = new OpenAIAdapter({ openai } as any);
  const runtime = new CopilotRuntime({
    remoteEndpoints: [
        { url: "http://localhost:8000/copilotkit" },
    ],
  });
   
  export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
      runtime,
      serviceAdapter:serviceAdapter,
      endpoint: "/api/copilotkit",
    });
   
    return handleRequest(req);
  };