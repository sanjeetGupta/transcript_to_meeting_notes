import json
from llm import generate_chat_response
from agents.agent import Agent


class Truth(Agent):
    def __init__(self):
        super().__init__('truth')
        with open('agents/prompts/feilds.json') as f:
            self.topic_descriptions = json.load(f)

    def run(self, result, transcript, mode='debug'):
        for category in result:
            for info in result[category]:

                # Build Transcript Parts Intervals
                transcript_intervals = []
                for raw_ext in info['raw']:
                    references = raw_ext['references']
                    for reference in references:
                        transcript_intervals.append(
                            {'start': max(reference - 2, 0), 'end': min(len(transcript) - 1, reference + 2)})
                transcript_intervals = merge_intervals(transcript_intervals)

                # Build Transcript Parts from the intervals
                transcript_parts = ""
                for i, interval in enumerate(transcript_intervals):
                    chunk = ''.join(transcript[interval['start']:interval['end']])
                    transcript_parts = transcript_parts + f"\nSnippet {i}:\n{chunk}\n\n"


                # Run LLM
                user_message = f"TOPIC:{category}\nTOPIC DESCRIPTION:{self.topic_descriptions[category]}\nExtracted Information: {info['sentence']} \n\n Transcript Snippets: {transcript_parts}"
                print(user_message)
                messages = [{"role": "system", "content": self.system_prompt},
                            {"role": "user", "content": user_message}]
                validation_output = generate_chat_response(messages)

                # Add validation output
                info['is_true'] = validation_output['is_true']
                info['is_relevant'] = validation_output['is_relevant']
                info['truth_updated_sentence'] = validation_output['updated']
                info['explanation'] = validation_output.get('explanation')
                info['citation_intervals'] = transcript_intervals
                info['citation'] = transcript_parts

        if mode == 'debug':
            with open('debug_output/result_validated.json', 'w') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)

        return result


def merge_intervals(intervals):
    # First, sort the intervals by their start times
    sorted_intervals = sorted(intervals, key=lambda x: x['start'])

    # Initialize the merged list with the first interval
    merged = [sorted_intervals[0]]

    for current in sorted_intervals[1:]:
        # Get the last interval in the merged list
        last_merged = merged[-1]

        # Check if there is an overlap
        if current['start'] <= last_merged['end']:
            # Merge the intervals by updating the end time
            last_merged['end'] = max(last_merged['end'], current['end'])
        else:
            # No overlap, add the current interval to merged list
            merged.append(current)
    return merged