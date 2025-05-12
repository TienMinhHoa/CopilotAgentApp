"use client";

import {
  useCoAgent,
  useCoAgentStateRender,
  useCopilotAction,
} from "@copilotkit/react-core";
import React, { useEffect, useRef, useState } from "react";
import { AgentState, Products } from "@/lib/types";


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
    renderAndWaitForResponse: ({ args, respond }) => {
      const [isLoading, setIsLoading] = React.useState(false);

      const handleResponse = async (response: string) => {
        setIsLoading(true);
        console.log('Button clicked:', response);
        console.log('Product details:', args);
        try {
          await respond?.(response);
          console.log('Response sent successfully');
        } catch (error) {
          console.error('Error sending response:', error);
        }
        setIsLoading(false);
      };

      return (
        <div className="p-4">
          <div className="font-bold text-base mb-4">
            Add this product?
          </div>
          <div className="mb-4">
            <p><strong>ID:</strong> {args.id}</p>
            <p><strong>Name:</strong> {args.name}</p>
            <p><strong>Description:</strong> {args.description}</p>
            <p><strong>Cost:</strong> {args.cost?.toLocaleString() ?? '0'}</p>
          </div>
          <div className="flex justify-start space-x-2">
            <button
              onClick={() => handleResponse("NO")}
              className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold disabled:opacity-50 min-w-[100px] hover:bg-[#6766FC] hover:text-white transition-colors duration-200"
            >
              Cancel
            </button>
            <button
              onClick={() => handleResponse("YES")}
              className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold disabled:opacity-50 min-w-[100px] hover:bg-[#5251d9] transition-colors duration-200"
            >
              Add
            </button>
          </div>
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
        const [isLoading, setIsLoading] = React.useState(false);

        const handleResponse = async (response: string) => {
          setIsLoading(true);
          console.log('Delete button clicked:', response);
          console.log('Product ID to delete:', args.id);
          try {
            await respond?.(response);
            console.log('Delete response sent successfully');
          } catch (error) {
            console.error('Error sending delete response:', error);
          }
          setIsLoading(false);
        };

        return (
          <div className="p-4">
            <div className="font-bold text-base mb-4">
              Are you sure you want to delete this product with ID: {args.id}?
            </div>
            <div className="flex justify-start space-x-2">
              <button
                onClick={() => handleResponse("NO")}
                disabled={isLoading}
                className="px-4 py-2 text-[#6766FC] border border-[#6766FC] rounded text-sm font-bold disabled:opacity-50 min-w-[100px] hover:bg-[#6766FC] hover:text-white transition-colors duration-200"
              >
                {isLoading ? 'Processing...' : 'Cancel'}
              </button>
              <button
                onClick={() => handleResponse("YES")}
                disabled={isLoading}
                className="px-4 py-2 bg-[#6766FC] text-white rounded text-sm font-bold disabled:opacity-50 min-w-[100px] hover:bg-[#5251d9] transition-colors duration-200"
              >
                {isLoading ? 'Processing...' : 'Delete'}
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
