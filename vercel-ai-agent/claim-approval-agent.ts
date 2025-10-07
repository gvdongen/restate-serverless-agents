import * as restate from "@restatedev/restate-sdk";
import { durableCalls } from "@restatedev/vercel-ai-middleware";
import { openai } from "@ai-sdk/openai";
import { generateText, tool, wrapLanguageModel, stepCountIs } from "ai";


const claimApprovalAgent = restate.service({
  name: "ClaimApprovalAgent",
  handlers: {
    run: async (ctx: restate.Context, { prompt }: { prompt: string }) => {
      const model = wrapLanguageModel({
        model: openai("gpt-4o"),
        middleware: durableCalls(ctx),
      });

      const { text } = await generateText({
        model,
        system: "You are an insurance claim evaluation agent.",
        prompt,
        stopWhen: [stepCountIs(5)],
      });
      return text;
    },
    },
  })

restate.serve({
  services: [claimApprovalAgent],
});
