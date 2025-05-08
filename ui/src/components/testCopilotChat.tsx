import { useCopilotChat } from "@copilotkit/react-core";
import { Role, TextMessage, ImageMessage } from "@copilotkit/runtime-client-gql";
import { useEffect } from "react";
export function YourComponent() {
    const { appendMessage } = useCopilotChat();


    const base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8Xw8AAoMBgVevmvwAAAAASUVORK5CYII=";

    const buffer = Buffer.from(base64, 'base64');

    const result = {
    contentType: "image/png",
    bytes: new Uint8Array(buffer),
    name: "image.png",
    size: buffer.length,
    };

console.log(result);
    useEffect(() => {
        const fetchAndAppendImage = async () => {
            // console.log(img)
            await appendMessage( new TextMessage({
                content: "Hello",
                role: Role.User,
              }), { followUp: true });
            await appendMessage(
                new ImageMessage({
                    format: "png",
                    bytes: Buffer.from(buffer).toString('base64'),
                    role: Role.User,
                }),  { followUp: true } 
            );
        };
        fetchAndAppendImage();
      }, []);
  return <div>Test</div>;

  // optionally, you can append a message without running chat completion
//   appendMessage(yourMessage, { followUp: false });
}