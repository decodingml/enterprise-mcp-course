import asyncio
from host.host import MCPHost

async def main():
    client = MCPHost()
    await client.connect_to_server("github")
    response = await client.process_query("Summarize this PR: https://github.com/915-Muscalagiu-AncaIoana/Mock-App/pull/1")
    print(f"\n📝 Response:\n{response}")
    await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
