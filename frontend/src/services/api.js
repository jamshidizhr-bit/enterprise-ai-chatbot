export async function sendMessageStream(message, onChunk) {
  const response = await fetch("http://127.0.0.1:8000/api/chat/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  let result = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    result += chunk;

    onChunk(chunk);
  }

  return result;
}