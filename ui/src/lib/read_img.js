import fs from 'fs';
import path from 'path';

export async function getServerSideProps(context) {
  const filePath = "/home/hoatien/hoa/CopilotAgentApp/ui/src/components/Screenshot from 2025-04-29 08-44-03.png"; // Đường dẫn file ảnh của bạn
  const buffer = fs.readFileSync(filePath);
  
  const contentType = 'image/jpeg'; // Hoặc xác định contentType theo file
  const bytes = new Uint8Array(buffer);
  const name = path.basename(filePath);
  const size = buffer.length;

  return {
    props: {
      contentType,
      bytes,
      name,
      size
    }
  };
}
