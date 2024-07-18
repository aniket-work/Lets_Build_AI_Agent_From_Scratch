from com.aniket.agent_brain.brain_for_agent import AgentBrain


agent = AgentBrain("How many words are in words under <QUERY> tag? <QUERY>This is my first query to LLM</QUERY>")

print(agent.get_response())
