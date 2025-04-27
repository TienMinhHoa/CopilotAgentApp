"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui"; 
import "@copilotkit/react-ui/styles.css"; 
 
export default function Home() {
  return (
    <>
      <CopilotPopup />
      <h1>Hello</h1>
    </>
  );
}