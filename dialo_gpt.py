from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load pre-trained DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Define a max history length to prevent repetitive responses
MAX_HISTORY_LENGTH = 100  # Adjust as needed for context depth

# Function to generate a response
def get_response(input_text, chat_history_ids=None):
    # Encode the new user input, add the eos_token, and return a tensor with attention mask
    new_user_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors='pt')

    # Concatenate new user input with previous chat history
    if chat_history_ids is not None:
        chat_history_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
        # Truncate chat history to a manageable length
        chat_history_ids = chat_history_ids[:, -MAX_HISTORY_LENGTH:]
    else:
        chat_history_ids = new_user_input_ids

    # Recompute the attention mask for the combined chat history
    attention_mask = torch.ones(chat_history_ids.shape, dtype=torch.long)

    # Generate response with limited max_length to avoid overloading
    chat_history_ids = model.generate(chat_history_ids, max_length=500, pad_token_id=tokenizer.eos_token_id, attention_mask=attention_mask)

    # Decode the generated response and return it
    bot_response = tokenizer.decode(chat_history_ids[:, new_user_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return bot_response, chat_history_ids

# Example usage
chat_history = None
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break
    bot_output, chat_history = get_response(user_input, chat_history)
    print(f"Bot: {bot_output}")
