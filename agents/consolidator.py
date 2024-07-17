from agents.agent import Agent
import json
from llm import generate_chat_response


class Consolidator(Agent):
    def __init__(self):
        super().__init__('consolidator')

    def run(self, extracted_result, mode='debug'):
        result_consolidated = {}
        for category in extracted_result:
            if len(extracted_result[category]) > 0:
                system_prompt = self.system_prompt.format(CATEGORY=category)

                # Create User Message
                info_points = ""
                for i, info_point in enumerate(extracted_result[category]):
                    info_points = info_points + f"{i + 1}. {info_point['sentence']}\n"

                # Call LLM
                messages = [{"role": "system", "content": system_prompt},
                            {"role": "user", "content": info_points}]
                result_consolidated_cat = generate_chat_response(messages)
                result_consolidated[category] = result_consolidated_cat['consolidated_list']

                # Accumulate results
                for sentence in result_consolidated[category]:
                    sentence['raw'] = [extracted_result[category][reference - 1] for reference in sentence['references']]
                    del sentence['references']

        if mode == 'debug':
            with open(f'debug_output/{self.name}.json', 'w') as f:
                json.dump(result_consolidated, f, indent=4, ensure_ascii=False)

        return result_consolidated

