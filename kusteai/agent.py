from kusteai.config import get_settings
from kusteai.llm_client import LLMClient
from kusteai.memory import MemoryStore
from kusteai.search import WebSearch, format_search_results


class KusteAIAgent:
    def __init__(self) -> None:
        self.settings = get_settings()
        self.memory = MemoryStore(self.settings.db_path)
        self.search_client = WebSearch()
        self.llm = LLMClient(
            api_key=self.settings.api_key,
            base_url=self.settings.base_url,
            model=self.settings.model,
        )

    def _build_system_prompt(self) -> str:
        memories = self.memory.get_recent_memories(limit=10)
        memories_text = "\n".join(f"- {m}" for m in memories) if memories else "(пока пусто)"

        return (
            "Ты ассистент с именем KusteAI. "
            f"Твой владелец: {self.settings.owner_name}. "
            "Всегда отвечай на русском языке. "
            "Используй память о владельце, если это уместно.\n\n"
            f"Память:\n{memories_text}"
        )

    def remember(self, text: str) -> None:
        self.memory.save_memory(text)

    def list_memories(self) -> str:
        memories = self.memory.get_recent_memories(limit=20)
        if not memories:
            return "Память пока пустая."
        return "\n".join(f"- {m}" for m in memories)

    def search_web(self, query: str) -> str:
        results = self.search_client.search(query, max_results=self.settings.max_search_results)
        return format_search_results(results)

    def chat(self, user_input: str) -> str:
        self.memory.save_message("user", user_input)
        self.memory.save_memory(f"Пользователь сказал: {user_input}")

        recent_messages = self.memory.get_recent_messages(limit=8)
        messages = [{"role": "system", "content": self._build_system_prompt()}]
        for role, content in recent_messages:
            messages.append({"role": role, "content": content})

        assistant_reply = self.llm.generate(messages)
        self.memory.save_message("assistant", assistant_reply)
        return assistant_reply
