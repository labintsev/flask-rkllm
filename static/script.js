async function streamRKLLMChat(messages, enable_thinking = false, tools = null) {

  const url = '/v1/chat/completions'; // Update this if your endpoint is different
  const stream_llm_response = true;

const payload = {
  model: "rkllm", // any model name, board suppots only one model for now
  enable_thinking: enable_thinking,
  messages: messages,
  stream: stream_llm_response,
  // Add other OpenAI parameters if needed (e.g., temperature, max_tokens)
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
    const decoder = new TextDecoder();
    let buffer = '';

    const chatBox = document.getElementById('chat-box');
    const userMessage = messages[0].content;

    if (stream_llm_response) {
      chatBox.innerHTML += `<div class="message user"><strong>You:</strong> <pre> ${userMessage} </pre> </div>`;
      chatBox.innerHTML += `<div class="message llm"><strong>LLM:</strong><pre id="response"> </pre> </div>`
      const preResponse = document.getElementById('chat-box').lastChild.getElementsByTagName('pre')[0];
      chatBox.scrollTop = chatBox.scrollHeight;
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer = decoder.decode(value, { stream: true });
        // Replace newlines in choices delta content
        buffer = buffer.replace(/\n/g, ' ');

        try {
          buffer = JSON.parse(buffer);
        } catch (error) {
          console.error('Error parsing JSON:', error, "Buffer content:", buffer);
          continue;
        }

        if (buffer.choices && buffer.choices[0] && buffer.choices[0].delta && buffer.choices[0].delta.content) {
          const content = buffer.choices[0].delta.content;
          preResponse.textContent += content;
        };
      }

    }
    else {
      chatBox.innerHTML += `<div class="message user"><strong>You:</strong><pre> ${userMessage} </pre> </div>`;
      const { done, value } = await reader.read();
      buffer = decoder.decode(value, { stream: false });
      const data = JSON.parse(buffer);
      const content = data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content
        ? data.choices[0].message.content
        : "No response from AI.";
      console.log(content)
      chatBox.innerHTML += `<div class="message llm"><strong>LLM:</strong><pre> ${content} </pre> </div>`;
    }

  } catch (error) {
    console.error('Error streaming from RKLLM:', error);
    throw error;
  }
}

document.getElementById('chat-form').addEventListener('submit', async function (e) {
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
// document.getElementById('user-input').addEventListener('keydown', function (event) {
//   if (event.key === 'Enter' && !event.shiftKey) {
//     event.preventDefault();
//     document.getElementById('chat-form').submit;
//   }
// });


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