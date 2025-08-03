async function streamRKLLMChat(messages, enable_thinking = false, tools = null) {
  const url = '/chat'; // Update this if your endpoint is different
  const stream_llm_response = false;

  const payload = {
    messages,
    enable_thinking,
    stream: stream_llm_response, // This is crucial for streaming
  };

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
    console.log(reader);
    const decoder = new TextDecoder();
    let buffer = '';

    const chatBox = document.getElementById('chat-box');
    const userMessage = messages[0].content;

    if (stream_llm_response) {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer = decoder.decode(value, { stream: true });
        document.getElementById('chat-box').lastChild.getElementById('response').textContent += buffer || "No response from AI.";
      }

    }
    else {
      chatBox.innerHTML += `<div class="message user"><strong>You:</strong> ${userMessage}</div>`;
      const { done, value } = await reader.read();
      buffer = decoder.decode(value, { stream: false });
      const data = JSON.parse(buffer);
      const content = data.message
      console.log(content)
      document.getElementById('chat-box').lastChild.getElementById('response').textContent = content || "No response from AI.";
    }

  } catch (error) {
    console.error('Error streaming from RKLLM:', error);
    throw error;
  }
}

document.getElementById('chat-form').addEventListener('submit', async function(e) { 
  e.preventDefault();
  console.log("Form submitted, begin ...")
  const input = document.getElementById('user-input').value;

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

});

// Add Enter key support for textarea
document.getElementById('user-input').addEventListener('keydown', function (event) {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault();
    document.getElementById('chat-form').submit;
  }
});


// From the flask-llm project

// document.getElementById('chat-form').addEventListener('submit', async function(e) {
//     e.preventDefault();
//     const input = document.getElementById('user-input');
//     const chatBox = document.getElementById('chat-box');
//     const userMessage = input.value.trim();
//     if (!userMessage) return;

//     // Display user message
//     chatBox.innerHTML += `<div class="message user"><strong>You:</strong> ${userMessage}</div>`;
//     chatBox.scrollTop = chatBox.scrollHeight;
//     input.value = '';

//     // Send to backend (adjust endpoint as needed)
//     const response = await fetch('/chat', {
//         method: 'POST',
//         headers: {'Content-Type': 'application/json'},
//         body: JSON.stringify({message: userMessage})
//     });
//     const data = await response.json();

//     // Display LLM response
//     chatBox.innerHTML += `<div class="message llm"><strong>LLM:</strong> ${data.reply}</div>`;
//     chatBox.scrollTop = chatBox.scrollHeight;
// });