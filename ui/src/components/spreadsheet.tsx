"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotAction,
} from "@copilotkit/react-core";

import { AgentState, Products } from "@/lib/types";
import { div } from "framer-motion/client";
export function Spreadsheet() {

  const { state, setState } = useCoAgent<AgentState>({
    name: "manager",
  });

  useCoAgentStateRender({
    name: "manager",
    render: ({ state, nodeName, status }) => {
      if (!state.logs || state.logs.length === 0) {
        return null;
      }
    },
  });

  useCopilotAction({
    name: "add_products",
    description:
      "Prompt the user for resource add confirmation, and then perform resource adding",
    available: "remote",
    parameters: [
      {
        name: "id",
        type: "string",
      },
      {
        name: "name",
        type: "string"
      },
      {
        name: "description",
        type: "string"
      },
      {
        name:"cost",
        type: "number"
      }
    ],
    renderAndWait: ({ args, status, respond }) => {
      return (
        <div
          className=""
          data-test-id="delete-resource-generative-ui-container"
        >
          <div className="font-bold text-base mb-2">
            Add this product?
          </div>
          {status === "executing" && (
            <div className="mt-4 flex justify-start space-x-2">
              <button
                onClick={() => respond("NO")}
                className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
              >
                Cancel
              </button>
              <button
                data-test-id="button-delete"
                onClick={() => respond("YES")}
                className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
              >
                Add
              </button>
            </div>
          )}
        </div>
      );
    },
  });

  useCopilotAction(
    {
      name: "delete_products",
      description:"Prompt the user for products delete confirmation, then perform product delete",
      available: "remote",
      parameters: [
        {
          name:"id",
          type:"string",
          description: "The id of the product need to be deleted"
        }
      ],
      renderAndWaitForResponse: ({ args, respond}) => {
        return (
          <div className="font-bold text-base mb-2">
            Are you sure you want to delete this product with ID: {args.id}?
            <div className="mt-4 flex justify-start space-x-2">
              <button
                onClick={() => respond?.("NO")}
                className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold"
              >
                Cancel
              </button>
              <button
                onClick={() => respond?.("YES")}
                className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold"
              >
                Delete
              </button>
            </div>
          </div>
        );
      }
    }
  )

  const products  = state.products || []

  

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-collapse border border-gray-300">
        <thead className="bg-gray-100">
          <tr>
            <th className="border border-gray-300 px-4 py-2 text-left">ID</th>
            <th className="border border-gray-300 px-4 py-2 text-left">Name</th>
            <th className="border border-gray-300 px-4 py-2 text-left">Description</th>
            <th className="border border-gray-300 px-4 py-2 text-left">Cost</th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id} className="hover:bg-gray-50">
              <td className="border border-gray-300 px-4 py-2">{product.id}</td>
              <td className="border border-gray-300 px-4 py-2">{product.name}</td>
              <td className="border border-gray-300 px-4 py-2">{product.description}</td>
              <td className="border border-gray-300 px-4 py-2">{product.cost.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
