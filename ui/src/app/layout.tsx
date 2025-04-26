import "./globals.css";
 
import { ReactNode } from "react";
import { CopilotKit } from "@copilotkit/react-core"; 
 
export default function RootLayout({ children }: { children: ReactNode }) {
    return (
      <html lang="en">
        <body> 
          {/* Use the public api key you got from Copilot Cloud  */}
          <CopilotKit publicApiKey="ck_pub_333f31a711d12cb6c23c332fd24fc11e"> 
            {children}
          </CopilotKit>
        </body>
      </html>
    );
}