# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **[YOUR NAME]** \
SUNet ID: **[YOUR ID]** \
Citations: **None**

This assignment took me about **2** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
Implement `extract_action_items_llm` using Ollama's structured output. 
It should take a string and return a list of strings representing extracted action items. 
Use `llama3.1:8b` as the model. 
Ensure the output schema is strictly enforced using Pydantic.
``` 

Generated Code Snippets:
```
Modified: week2/app/services/extract.py
- Added ActionItemsResponse Pydantic model
- Added extract_action_items_llm function
```

### Exercise 2: Add Unit Tests
Prompt: 
```
Add comprehensive tests for `extract_action_items_llm` including:
1. Structure verification (is it a list?)
2. Keyword hitting for natural language (fuzzy matching)
3. Empty input handling (preventing hallucinations)
``` 

Generated Code Snippets:
```
Modified: week2/tests/test_extract.py
- Added test_llm_extract_explicit
- Added test_llm_extract_natural_language
- Added test_llm_extract_empty_or_none
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
Refactor the backend API to use Pydantic schemas instead of Dict[str, Any].
1. Create a schemas.py file with input/output models.
2. Update routers/notes.py and routers/action_items.py to use these schemas.
3. Improve error handling (explicit HTTP exceptions).
``` 

Generated/Modified Code Snippets:
```
Created: week2/app/schemas.py
Modified: week2/app/routers/notes.py
Modified: week2/app/routers/action_items.py
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
Integrate the new LLM features into the app:
1. Backend: Add POST /action-items/extract-llm endpoint.
2. Backend: Add GET /notes endpoint to list all notes.
3. Frontend: Add "Extract LLM" and "List Notes" buttons to index.html with corresponding JS fetch logic.
``` 

Generated Code Snippets:
```
Modified: week2/app/routers/action_items.py (added extract_llm)
Modified: week2/app/routers/notes.py (added list_notes)
Modified: week2/frontend/index.html (added buttons and JS handlers)
```


### Exercise 5: Generate a README from the Codebase
Prompt: 
```
Analyze the current codebase and generate a comprehensive README.md.
Include sections for Features, Setup, API Endpoints, and Testing.
``` 

Generated Code Snippets:
```
Created: week2/README.md
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 
 