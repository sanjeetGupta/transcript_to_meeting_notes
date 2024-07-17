# transcript_to_meeting_notes
Agentic AI to create meeting notes out of a transcript

# Usage Instructions
## Initial Setup:
Ensure Python 3.x is installed on your system.

## Dependencies:

```commandline
pip install -r requirements.txt
```

## Create a .env file
```txt
OPENAI_API_KEY = <openai api key here>
```

## Start program
```commandline
python main.py <transcript txt filename>
```

## Evaluation Method
1. Citations are extracted while extracting the notes for every pointer.
2. Truth and Relevance agent is used to decide if the pointer is relevant to the topic and true to the cited transcript snippets.
