import re


def extract_action_items(text: str) -> list[str]:
    """
    Extracts action items from text using pattern matching.
    Supports:
    - Lines starting with TODO:, ACTION:, FIXME:, TASK: (case insensitive)
    - Markdown task list items: - [ ] 
    - Lines ending with exclamation marks (!)
    """
    patterns = [
        r"(?i)^(?:[-*]\s*)?(?:todo|action|fixme|task):\s*(.*)",
        r"^(?:[-*]\s*)?\[ \]\s*(.*)",
        r"(.*!)$"
    ]
    
    results: list[str] = []
    seen = set()
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
            
        is_match = False
        extracted_content = line
        
        for p in patterns:
            match = re.search(p, line)
            if match:
                # Use the captured group if available, else the whole line
                extracted_content = match.group(1).strip() if match.groups() else line.strip()
                # Clean up any leading bullet points if they were captured or remained
                extracted_content = extracted_content.lstrip("-* ")
                is_match = True
                break
        
        if is_match and extracted_content:
            # Simple deduplication
            if extracted_content.lower() not in seen:
                results.append(extracted_content)
                seen.add(extracted_content.lower())
                
    return results


