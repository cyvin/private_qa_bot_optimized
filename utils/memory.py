# utils/memory.py
from langchain.memory import ConversationBufferMemory

def get_memory():
    return ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="result"  # ✅ 关键修复：明确告诉 memory 要记住哪个字段
    )

