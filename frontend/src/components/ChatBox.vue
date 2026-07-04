<template>
  <div class="chat-container">

    <!-- Header -->
    <header class="header">
      <div class="title">
        <h2>🤖 Enterprise AI Assistant</h2>
        <span>Powered by FastAPI + Groq</span>
      </div>

      <div class="status">
        <span class="status-dot"></span>
        Online
      </div>
    </header>

    <!-- Messages -->
    <div class="messages" ref="chatBox">

      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-row', msg.role]"
      >

        <div class="avatar">
          {{ msg.role === "user" ? "👤" : "🤖" }}
        </div>

        <div class="bubble">

          <div class="text">
            {{ msg.text }}
          </div>

          <div v-if="msg.time" class="time">
            {{ msg.time }}
          </div>

        </div>

      </div>

      <!-- Thinking Indicator -->
      <div v-if="loading" class="message-row ai">

        <div class="avatar">🤖</div>

        <div class="bubble">
          <div class="thinking">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>

      </div>

    </div>

    <!-- Input -->
    <div class="input-box">

      <input
        v-model="input"
        @keyup.enter="sendMessage"
        :disabled="loading"
        placeholder="پیام خود را بنویس..."
      />

      <button
        @click="sendMessage"
        :disabled="loading"
      >
        ارسال
      </button>

    </div>

  </div>
</template>

<script>
import { sendMessageStream } from "../services/api";

export default {
  data() {
    return {
      input: "",
      loading: false,
      messages: []
    };
  },

  methods: {

    scrollToBottom() {
      this.$nextTick(() => {
        if (this.$refs.chatBox) {
          this.$refs.chatBox.scrollTop =
            this.$refs.chatBox.scrollHeight;
        }
      });
    },

    currentTime() {
      return new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
      });
    },

    async sendMessage() {
      if (!this.input.trim()) return;

      const message = this.input;

      // 1. user message
      this.messages.push({
        role: "user",
        text: message,
        time: new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit"
        })
      });

      this.input = "";
      this.loading = true;

      // 2. placeholder AI message (stream target)
      const aiIndex = this.messages.length;

      this.messages.push({
        role: "ai",
        text: "",
        time: ""
      });

      try {
        await sendMessageStream(message, (chunk) => {
          this.messages[aiIndex].text += chunk;

          this.$nextTick(() => {
            this.$refs.chatBox.scrollTop =
              this.$refs.chatBox.scrollHeight;
          });
        });

        // 3. time after completion
        this.messages[aiIndex].time =
          new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
          });

      } catch (e) {
        this.messages[aiIndex].text =
          "❌ خطا در دریافت پاسخ از سرور";
      } finally {
        this.loading = false;

        this.$nextTick(() => {
          this.$refs.chatBox.scrollTop =
            this.$refs.chatBox.scrollHeight;
        });
      }
    }
  

  }
};
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background: #7a97da;
  font-family: Segoe UI, Tahoma, sans-serif;
}

.chat-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #0f172a;
  color: white;
}

/* Header */
.header {
  height: 72px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 24px;
  background: #111827;
  border-bottom: 1px solid #1f2937;
}

.title h2 {
  margin: 0;
  font-size: 20px;
}

.title span {
  color: #94a3b8;
  font-size: 13px;
}

.status {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #22c55e;
  font-weight: bold;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #22c55e;
}

/* Messages */
.messages {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  padding: 24px;
  gap: 18px;
}

.message-row {
  display: flex;
  align-items: flex-end;
  gap: 12px;
}

.message-row.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #334155;
  font-size: 22px;
}

.bubble {
  max-width: 70%;
  display: flex;
  flex-direction: column;
}

.text {
  padding: 14px 18px;
  border-radius: 18px;
  line-height: 1.6;
  word-break: break-word;
}

.user .text {
  background: #2563eb;
  border-bottom-right-radius: 6px;
}

.ai .text {
  background: #1e293b;
  border-bottom-left-radius: 6px;
}

.time {
  margin-top: 6px;
  font-size: 11px;
  color: #94a3b8;
  padding: 0 8px;
}

/* Input */
.input-box {
  display: flex;
  gap: 12px;
  padding: 18px;
  background: #111827;
  border-top: 1px solid #1f2937;
}

.input-box input {
  flex: 1;
  background: #1e293b;
  color: white;
  border: none;
  outline: none;
  border-radius: 12px;
  padding: 14px 16px;
  font-size: 15px;
}

.input-box input::placeholder {
  color: #94a3b8;
}

button {
  width: 110px;
  border: none;
  border-radius: 12px;
  background: #2563eb;
  color: white;
  font-size: 15px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Thinking */
.thinking {
  width: 70px;
  height: 44px;
  background: #1e293b;
  border-radius: 18px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
}

.thinking span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: white;
  animation: bounce 1.2s infinite;
}

.thinking span:nth-child(2) {
  animation-delay: 0.2s;
}

.thinking span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0.5);
    opacity: 0.4;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>