import json

from com.aniket.agent_brain.brain_for_agent import AgentBrain
from com.aniket.tools.character_counter import count_characters
from com.aniket.tools.longest_word_finder import find_longest_words
from com.aniket.tools.unique_word_finder import find_unique_words
from com.aniket.tools.word_counter import count_words

import streamlit as st


class AIAgent:
    def __init__(self):
        self.tools = {
            "Character Count Finder": count_characters,
            "Longest Word Finder": find_longest_words,
            "Unique Word Finder": find_unique_words,
            "Word Count Finder": count_words
        }

    def parse_llm_response(self, response):
        try:
            return response
        except json.JSONDecodeError:
            print("Error: Invalid JSON response from LLM")
            return None

    def execute_tools(self, tools, query):
        results = {}
        for tool in tools:
            if tool in self.tools:
                print("working on tool : ", tool)
                results[tool] = self.tools[tool](query)
            else:
                print(f"Warning: Tool '{tool}' not found")
        return results

    def format_response(self, results, query):
        response = f"Analysis of the query: '{query}'\n\n"

        if not results:
            return response + "No analysis tools were executed or returned results."

        counter = 1

        if "Character Count Finder" in results:
            char_count = results['Character Count Finder']
            response += f"{counter}. Character Count: {char_count} character{'s' if char_count != 1 else ''}\n"
            counter += 1

        if "Longest Word Finder" in results:
            longest_words = results['Longest Word Finder']
            response += f"{counter}. Longest Word{'s' if len(longest_words) > 1 else ''}: {', '.join(longest_words)} ({len(longest_words[0])} characters)\n"
            counter += 1

        if "Unique Word Finder" in results:
            unique_words = results['Unique Word Finder']
            word_frequency = {word.lower(): query.lower().split().count(word.lower()) for word in unique_words}
            sorted_words = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

            response += f"{counter}. Unique Words: {len(unique_words)}\n"
            counter += 1
            response += f"{counter}. Word Frequency Analysis:\n"

            # Group words by frequency
            freq_groups = {}
            for word, freq in sorted_words:
                if freq not in freq_groups:
                    freq_groups[freq] = []
                freq_groups[freq].append(word)

            # Format the output
            for freq, words in sorted(freq_groups.items(), reverse=True):
                word_list = ", ".join(sorted(words))
                response += f"   {freq} time{'s' if freq > 1 else ' '}: {word_list}\n"

            counter += 1

            if sorted_words:
                most_common_words = [word for word, freq in sorted_words if freq == sorted_words[0][1]]
                if len(most_common_words) == 1:
                    response += f"{counter}. Most Frequently Used Word: {repr(most_common_words[0])} (used {sorted_words[0][1]} time{'s' if sorted_words[0][1] > 1 else ''})\n"
                else:
                    response += f"{counter}. Most Frequently Used Words: {', '.join(repr(word) for word in most_common_words)} (each used {sorted_words[0][1]} times)\n"
                counter += 1

        return response

    def process_request(self, user_input, llm_response):
        query = user_input
        parsed_response = self.parse_llm_response(llm_response)

        if parsed_response:
            tools_to_use = parsed_response.get('tools', [])
            results = self.execute_tools(tools_to_use, query)
            return self.format_response(results, query)
        else:
            return "Sorry, I couldn't process your request due to an error in the LLM response."


def main():

    st.set_page_config(page_title="Text Analysis AI Agent", page_icon="🤖")

    st.markdown(
        """
        <style>
        .title {
            font-size: 2.4rem;  
            white-space: nowrap;  
            overflow: hidden;
            text-overflow: ellipsis;  
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<h1 class="title">🤖 Text Analysis AI Agent From Scratch</h1>', unsafe_allow_html=True)

    # User input
    user_input = st.text_area("Enter your query below:",
                              "How many words are in sentence?")

    agentBrain = AgentBrain(user_input)
    response = agentBrain.get_response()

    print(response)

    if st.button("Analyze"):
        agent = AIAgent()
        result = agent.process_request(user_input, response)

        st.write("LLM Response:")
        st.write(response)

        st.write("Analysis Result:")
        st.write(result)

if __name__ == "__main__":
    main()