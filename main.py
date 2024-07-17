import pandas as pd
import json
from transcript import Transcript
from agents.extractor import Extractor
from agents.consolidator import Consolidator
from agents.truth import Truth
from dotenv import load_dotenv
load_dotenv()

MODE = 'debug'


def financial_advisor_meeting_notes(transcript_filename):

    print('Read Transcript and chunk transcript')
    transcript = Transcript(transcript_filename)

    print('Performing raw extraction with citations')
    extractor = Extractor()
    result = extractor.run(transcript.transcript, transcript.transcript_chunks, mode=MODE)

    print('Consolidating Raw Extraction while maintaining citations')
    consolidator = Consolidator()
    result = consolidator.run(result, mode=MODE)

    print('Validating Truthfulness by comparing with source')
    truth_validator = Truth()
    result = truth_validator.run(result, transcript.transcript, mode=MODE)

    # final
    notes = {}
    notes_doubtful = {}
    evals = {'Total': 0, '#False': 0, '#Irrelevant':0}
    for category in result:
        notes[category] = []
        notes_doubtful[category] = []
        for point in result[category]:
            evals['Total'] += 1
            if point['is_true'] == 1 and point['is_relevant'] == 1:
                notes[category].append(point['sentence'])
            else:
                notes_doubtful[category].append({
                                                 'generated': point['sentence'],
                                                 'updated': point['truth_updated_sentence'],
                                                 'is_true': point['is_true'],
                                                 'is_relevant': point['is_relevant'],
                                                 'explanation': point['explanation']
                                                 })
                if point['is_true'] == 0:
                    evals['#False'] += 1

                if point['is_relevant'] == 0:
                    evals['#Irrelevant'] += 1
    print("===============Evaluation Result================")
    print(json.dumps(evals, indent=4))


    if MODE == 'debug':
        # create a excel file to view citations
        df = []
        for category in result:
            for sentence in result[category]:
                sentence['category'] = category
                df.append(sentence)
        df = pd.DataFrame(df)
        df.drop(columns=['raw'], inplace=True)
        df.to_excel('debug_output/citations.xlsx', index=False)

    with open(f'{transcript_filename}_output.json', 'w') as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)

    with open(f'{transcript_filename}_doubtful.json', 'w') as f:
        json.dump(notes_doubtful, f, indent=4, ensure_ascii=False)

    return notes


if __name__ == "__main__":
    financial_advisor_meeting_notes('transcript1.txt')













