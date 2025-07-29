async function streamRKLLMChat(messages, enable_thinking = false, tools = null) {
  const url = '/rkllm_chat'; // Update this if your endpoint is different
  const payload = {
    messages,
    enable_thinking,
    stream: true, // This is crucial for streaming
  };

  if (tools) {
    payload.tools = tools;
  }

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'RKLLM Server error');
    }

    if (!response.body) {
      throw new Error('ReadableStream not supported in this browser');
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      
      // Process each complete JSON object in the buffer
      let boundary;
      while ((boundary = buffer.indexOf('\n\n')) >= 0) {
        const chunk = buffer.slice(0, boundary);
        buffer = buffer.slice(boundary + 2);
        
        if (chunk) {
          try {
            const data = JSON.parse(chunk);
            console.log('data:', data);
            // Handle the streamed data here
            if (data.choices && data.choices.length > 0) {
              const content = data.choices.at(-1).delta?.content;
              if (content) {

                // Do something with the content, e.g., display it
                document.getElementById('response').textContent += content || "No response from AI.";
              }
            }
          } catch (e) {
            console.error('Error parsing JSON chunk:', e);
          }
        }
      }
    }

    // Process any remaining data in the buffer
    if (buffer.trim()) {
      try {
        const result = JSON.parse(buffer);
        // Handle the final data
        document.getElementById('response').innerText = result || "No response from AI.";
      } catch (e) {
        console.error('Error parsing final JSON chunk:', e);
      }
    }

  } catch (error) {
    console.error('Error streaming from RKLLM:', error);
    throw error;
  }
}

document.getElementById('send-btn').onclick = async function () {
  const input = document.getElementById('user-input').value;
  document.getElementById('response').innerText = "Thinking...";

  const messages = [
      // {
      //   "role": "system",
      //   "content": `Ты консультант фирмы по продаже квартир. `
      // },
      {
        "role": "user",
        "content": `${input}`
      }

    ]

  // Example rkllm chat integration 
  streamRKLLMChat(messages)
  .then(() => console.log('Stream completed'))
  .catch(error => console.error('Stream error:', error));

};

// Add Enter key support for textarea
document.getElementById('user-input').addEventListener('keydown', function(event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    document.getElementById('send-btn').click();
  }
});
