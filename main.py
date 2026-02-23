from kusteai.agent import KusteAIAgent


def main() -> None:
    agent = KusteAIAgent()
    print("KusteAI готов. Команды: /search, /remember, /memories, /adb, /approve, /exit")

    while True:
        user_input = input("Вы: ").strip()
        if not user_input:
            continue

        if user_input == "/exit":
            print("KusteAI: До встречи 👋")
            break

        if user_input.startswith("/search "):
            query = user_input.removeprefix("/search ").strip()
            print(f"KusteAI:\n{agent.search_web(query)}")
            continue

        if user_input.startswith("/remember "):
            text = user_input.removeprefix("/remember ").strip()
            agent.remember(text)
            print("KusteAI: Запомнил ✅")
            continue

        if user_input == "/memories":
            print(f"KusteAI:\n{agent.list_memories()}")
            continue

        if user_input.startswith("/approve "):
            pin = user_input.removeprefix("/approve ").strip()
            ok = agent.approve_owner(pin)
            print("KusteAI: Подтверждение принято ✅" if ok else "KusteAI: Неверный PIN ❌")
            continue

        if user_input.startswith("/adb "):
            cmd = user_input.removeprefix("/adb ").strip()
            print(f"KusteAI:\n{agent.adb_shell(cmd)}")
            continue

        response = agent.chat(user_input)
        print(f"KusteAI: {response}")


if __name__ == "__main__":
    main()
