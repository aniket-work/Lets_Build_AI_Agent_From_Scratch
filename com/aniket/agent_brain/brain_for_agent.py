import requests
import json
from com.aniket.utils.agent_util import load_config

# Load configuration
config = load_config()

class AgentBrain:
    def __init__(self):
        self.model          = config["model"]
        self.system_prompt  = config["system_prompt"]
        self.model_endpoint = config["model_endpoint"]
        self.temperature    = config["temperature"]
        self.headers        = {"Content-Type": "application/json"}

    def generate_text(self, prompt):

        try:
            request_response = requests.post(
                self.model_endpoint,
                headers=self.headers,
                data=json.dumps({
                                "model": self.model,
                                "format": "json",
                                "prompt": prompt,
                                "system": self.system_prompt,
                                "stream": False,
                                "temperature": self.temperature
                            })
            )

            print("Request : ", request_response)
            request_response_json = request_response.json()
            response = request_response_json['response']
            response_dict = json.loads(response)
            print(f"\n\nResponse : {response_dict}")
            return response_dict
        except requests.RequestException as e:
            response = {"error": f"Error in processing response from llm :  {str(e)}"}
            return response