class ConversationState:
    def __init__(self, max_turns=8):
        # Stores conversation as a list of messages
        self.history = []
        self.max_turns = max_turns

    def add(self, role, text):
        # Add a message to history
        self.history.append({
            "role": role,
            "text": text
        })

        # Keep only the latest max_turns messages
        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def last_assistant(self):
        # Return the most recent assistant message
        for msg in reversed(self.history):
            if msg["role"] == "assistant":
                return msg["text"]
        return None

    def last_user(self):
        # Return the most recent user message
        for msg in reversed(self.history):
            if msg["role"] == "user":
                return msg["text"]
        return None

    def all_history(self):
        # Return full conversation history
        return self.history
