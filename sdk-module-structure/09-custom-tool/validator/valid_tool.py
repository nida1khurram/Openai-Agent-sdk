from agents import RunContextWrapper



async def tool_valid(ctx:RunContextWrapper, agent):
    if ctx.context["age"] >= 18:
        print("because age > 18")
        return True
    print("Because age < 18")
    return False