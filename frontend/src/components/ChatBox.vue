

<template>
  <div class="chat-container">

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

    <div class="messages" ref="chatBox">

      <div
        v-for="(msg,index) in messages"
        :key="index"
        :class="['message-row',msg.role]"
      >

        <div class="avatar">
          {{ msg.role === "user" ? "👤" : "🤖" }}
        </div>

        <div class="bubble">

          <div class="text">
            {{ msg.text }}
          </div>

          <div class="time">
            {{ msg.time }}
          </div>

        </div>

      </div>

    </div>

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
        {{ loading ? "..." : "ارسال" }}
      </button>

    </div>

  </div>
</template>

<script>
export default {

  data() {
    return {
      input: "",
      loading: false,
      messages: []
    }
  },

  methods: {

    async sendMessage() {

      if (!this.input.trim()) return;

      const message = this.input;

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

      this.messages.push({
        role: "ai",
        text: "💭 در حال فکر کردن...",
        time: ""
      });

      this.$nextTick(() => {
        this.$refs.chatBox.scrollTop =
          this.$refs.chatBox.scrollHeight;
      });

      try {

        const res = await fetch(
          "http://127.0.0.1:8000/api/chat",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              message
            })
          }
        );

        const data = await res.json();

        this.messages[this.messages.length - 1] = {
          role: "ai",
          text: data.answer,
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
          })
        };

      } catch (e) {

        this.messages[this.messages.length - 1] = {
          role: "ai",
          text: "❌ ارتباط با سرور برقرار نشد",
          time: ""
        };

      } finally {

        this.loading = false;

        this.$nextTick(() => {
          this.$refs.chatBox.scrollTop =
            this.$refs.chatBox.scrollHeight;
        });

      }

    }

  }

}
</script>

<style>

*{
    box-sizing:border-box;
}

body{
    margin:0;
    background:#0f172a;
    font-family:Segoe UI,Tahoma,sans-serif;
}

.chat-container{

    height:100vh;
    display:flex;
    flex-direction:column;

    background:#0f172a;
    color:white;

}

.header{

    height:72px;

    display:flex;
    justify-content:space-between;
    align-items:center;

    padding:0 24px;

    background:#111827;

    border-bottom:1px solid #1f2937;

}

.title h2{

    margin:0;
    font-size:20px;

}

.title span{

    color:#94a3b8;
    font-size:13px;

}

.status{

    display:flex;
    align-items:center;
    gap:8px;

    color:#22c55e;
    font-weight:bold;

}

.status-dot{

    width:10px;
    height:10px;

    border-radius:50%;
    background:#22c55e;

}
.messages{

    flex:1;

    overflow-y:auto;

    display:flex;
    flex-direction:column;

    padding:24px;

    gap:18px;

}

.message-row{

    display:flex;
    align-items:flex-end;

    gap:12px;

    animation:fade .25s ease;

}

.message-row.user{

    flex-direction:row-reverse;

}

.avatar{

    width:42px;
    height:42px;

    border-radius:50%;

    display:flex;
    justify-content:center;
    align-items:center;

    background:#334155;

    font-size:22px;

    flex-shrink:0;

}

.bubble{

    max-width:70%;

    display:flex;
    flex-direction:column;

}

.text{

    padding:14px 18px;

    border-radius:18px;

    line-height:1.6;

    word-break:break-word;

}

.user .text{

    background:#2563eb;

    border-bottom-right-radius:6px;

}

.ai .text{

    background:#1e293b;

    border-bottom-left-radius:6px;

}

.time{

    margin-top:6px;

    font-size:11px;

    color:#94a3b8;

    padding:0 8px;

}

.input-box{

    display:flex;

    gap:12px;

    padding:18px;

    background:#111827;

    border-top:1px solid #1f2937;

}

.input-box input{

    flex:1;

    background:#1e293b;

    color:white;

    border:none;

    outline:none;

    border-radius:12px;

    padding:14px 16px;

    font-size:15px;

}

.input-box input::placeholder{

    color:#94a3b8;

}

button{

    width:110px;

    border:none;

    border-radius:12px;

    background:#2563eb;

    color:white;

    font-size:15px;

    cursor:pointer;

    transition:.25s;

}

button:hover{

    background:#1d4ed8;

}

button:disabled{

    opacity:.6;

    cursor:not-allowed;

}

@keyframes fade{

    from{

        opacity:0;

        transform:translateY(12px);

    }

    to{

        opacity:1;

        transform:translateY(0);

    }

}
</style>