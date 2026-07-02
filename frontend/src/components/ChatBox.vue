<template>
  <div class="chat-container">

    <!-- messages -->
    <div class="messages" ref="box">
      <div
        v-for="(msg, i) in messages"
        :key="i"
        :class="msg.role"
      >
        {{ msg.text }}
      </div>
    </div>

    <!-- input -->
    <div class="input-box">
      <input
        v-model="input"
        @keyup.enter="sendMessage"
        placeholder="پیام خود را بنویس..."
      />
      <button @click="sendMessage">Send</button>
    </div>

  </div>
</template>

<script setup>
import { ref, nextTick } from "vue"

const input = ref("")
const messages = ref([])
const box = ref(null)

async function scrollToBottom() {
  await nextTick()
  if (box.value) {
    box.value.scrollTop = box.value.scrollHeight
  }
}

async function sendMessage() {
  if (!input.value) return

  const text = input.value
  input.value = ""

  // user message
  messages.value.push({ role: "user", text })

  // bot placeholder (برای streaming)
  messages.value.push({ role: "bot", text: "" })

  await scrollToBottom()

  const res = await fetch("http://127.0.0.1:8000/api/chat-stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: text })
  })

  const reader = res.body.getReader()
  const decoder = new TextDecoder()

  let fullText = ""

  while (true) {
    const { value, done } = await reader.read()
    if (done) break

    fullText += decoder.decode(value)

    messages.value[messages.value.length - 1].text = fullText

    await scrollToBottom()
  }
}
</script>

<style>
.chat-container {
  width: 420px;
  margin: 40px auto;
  border: 1px solid #ddd;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  height: 500px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: #f9f9f9;
}

.user {
  text-align: right;
  background: #d1e7ff;
  padding: 8px;
  margin: 5px;
  border-radius: 8px;
}

.bot {
  text-align: left;
  background: #e8e8e8;
  padding: 8px;
  margin: 5px;
  border-radius: 8px;
}

.input-box {
  display: flex;
  border-top: 1px solid #ddd;
}

input {
  flex: 1;
  padding: 10px;
  border: none;
  outline: none;
}

button {
  padding: 10px 15px;
  border: none;
  background: #4f46e5;
  color: white;
  cursor: pointer;
}
</style>