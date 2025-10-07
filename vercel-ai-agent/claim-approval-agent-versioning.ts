import * as restate from "@restatedev/restate-sdk";
import { durableCalls } from "@restatedev/vercel-ai-middleware";
import { openai } from "@ai-sdk/openai";
import { generateText, tool, wrapLanguageModel, stepCountIs } from "ai";
import { z } from "zod";

export const InsuranceClaimSchema = z.object({
  date: z.string().nullable().optional(),
  category: z.string().nullable().optional(),
  reason: z.string().nullable().optional(),
  amount: z.number().nullable().optional(),
  placeOfService: z.string().nullable().optional(),
});

export type InsuranceClaim = z.infer<typeof InsuranceClaimSchema>;

const claimApprovalAgent = restate.service({
  name: "ClaimApprovalAgent",
  handlers: {
    run: async (
      ctx: restate.Context,
      { customerId, prompt }: { customerId: string; prompt: string },
    ) => {
      // enrich with database data
      const customerPolicy = ctx.run("fetch customer policy from DB", () =>
        retrieveCustomerPolicy(customerId),
      );

      const model = wrapLanguageModel({
        model: openai("gpt-4o"),
        middleware: durableCalls(ctx),
      });

      const { text } = await generateText({
        model,
        system:
          "You are an insurance claim evaluation agent. Use these rules: " +
          "* if the amount is more than 1000, ask for human approval, " +
          "* if the amount is less than 1000, decide by yourself",
        prompt: `${prompt}\n\nCustomer Policy Info: ${JSON.stringify(customerPolicy)}`,
        tools: {
          humanApproval: tool({
            description: "Ask for human approval for high-value claims.",
            inputSchema: InsuranceClaimSchema,
            execute: async (claim: InsuranceClaim): Promise<boolean> => {
              const approval = ctx.awakeable<boolean>();
              await ctx.run("request-review", () =>
                requestHumanReview(claim, approval.id),
              );
              return approval.promise;
            },
          }),
        },
        stopWhen: [stepCountIs(5)],
      });
      return text;
    },
  },
});

restate.serve({
  services: [claimApprovalAgent],
});

// UTILS

export function requestHumanReview(
  message: InsuranceClaim,
  responseId: string = "",
) {
  console.log(`>>> ${message} \n
  Submit your claim review via: \n
    curl localhost:8080/restate/awakeables/${responseId}/resolve --json 'true'
  `);
}

export function retrieveCustomerPolicy(customerId: string) {
  console.log(`Retrieving policy info for customer ${customerId}...`);
  return {
    policyNumber: "POL123456",
    coverage: "Full",
    validTill: "2025-12-31",
  };
}
