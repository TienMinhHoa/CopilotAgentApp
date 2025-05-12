"use client";

import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup, CopilotChat, CopilotSidebar } from "@copilotkit/react-ui"; 
import {Spreadsheet} from "../components/spreadsheet";
import "@copilotkit/react-ui/styles.css"; 

import { YourComponent } from "../components/testCopilotChat";
export default function Home() {
  
  return (
    <>
    {/* <YourComponent/> */}
      <Spreadsheet/>
      <CopilotPopup/>
    </>
  );
}