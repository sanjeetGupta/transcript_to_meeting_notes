import json
from agents.agent import Agent
from llm import generate_chat_response


class Extractor(Agent):
    def __init__(self):
        super().__init__('extractor')

    def run(self, transcript, transcript_chunks, mode='debug'):
        # Raw extractor
        result = {}

        for chunk_indx in transcript_chunks:

            # Transcript Chunk string
            chunk_str = ""
            for i in range(chunk_indx['start'], chunk_indx['end']):
                chunk_str = chunk_str + f"{i}. {transcript[i]}\n"

            # Run LLM
            messages = [{"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": chunk_str}]
            result_chunk = generate_chat_response(messages)

            # Accumulate results
            for category in result_chunk:
                if category not in result:
                    result[category] = []
                result[category].extend(result_chunk[category])

        if mode == 'debug':
            with open(f'debug_output/{self.name}.json', 'w') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

        return result