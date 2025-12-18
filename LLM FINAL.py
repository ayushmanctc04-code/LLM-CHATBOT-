#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sys
import subprocess

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", package])

try:
    import requests
except:
    install_package("requests")
    import requests

import json

class LLMChatbot:
    
    def __init__(self):
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.conversation_history = []
        self.message_count = 0
    
    def chat(self, user_message):
        if not user_message.strip():
            return "Please enter a message!"
        
        print("\n" + "="*70)
        print(f"YOU: {user_message}")
        print("="*70)
        
        self.conversation_history.append(f"User: {user_message}")
        prompt = self._build_prompt(user_message)
        
        print("\nAI is thinking...\n")
        response = self._get_ai_response(prompt)
        
        print("AI ASSISTANT:")
        print("-"*70)
        print(response)
        print("-"*70)
        
        self.conversation_history.append(f"Assistant: {response}")
        self.message_count += 1
        
        return response
    
    def _build_prompt(self, user_message):
        context = "\n".join(self.conversation_history[-6:])
        
        if context:
            prompt = f"""{context}

User: {user_message}
Assistant: """
        else:
            prompt = f"User: {user_message}\nAssistant: "
        
        return prompt
    
    def _get_ai_response(self, prompt):
        try:
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 512,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True,
                    "return_full_text": False
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    text = result[0].get("generated_text", "").split("User:")[0].strip()
                    return text if text else self._get_smart_response(prompt)
                else:
                    return self._get_smart_response(prompt)
            else:
                return self._get_smart_response(prompt)
                
        except Exception as e:
            return self._get_smart_response(prompt)
    
    def _get_smart_response(self, prompt):
        user_msg = prompt.split("User:")[-1].split("Assistant:")[0].strip().lower()
        
        if any(word in user_msg for word in ["hello", "hi", "hey"]):
            return "Hello! I'm an AI assistant. I can help you with coding, explanations, problem-solving, writing, data analysis, and much more. What would you like to explore?"
        
        if "python" in user_msg or "code" in user_msg or "program" in user_msg:
            if "function" in user_msg or "write" in user_msg:
                return """I'd be happy to help with Python code! Here's an example:

def example_function(n):
    result = []
    for i in range(n):
        result.append(i * 2)
    return result

print(example_function(5))

What specific functionality would you like?"""
            else:
                return "Python is a versatile programming language used in web development, data science, machine learning, and automation. What aspect interests you?"
        
        if "machine learning" in user_msg or "ml" in user_msg or "ai" in user_msg:
            return """Machine Learning enables systems to learn from data. Key concepts:

1. Supervised Learning: Learning from labeled data
2. Unsupervised Learning: Finding patterns in unlabeled data
3. Neural Networks: Deep learning models
4. Training: Optimizing model parameters

Popular libraries: scikit-learn, TensorFlow, PyTorch. What ML topic interests you?"""
        
        if "data" in user_msg and any(w in user_msg for w in ["science", "analysis", "pandas", "numpy"]):
            return """Data Science tools:

- Pandas: Data manipulation
- NumPy: Numerical computing
- Matplotlib/Seaborn: Visualization
- Scikit-learn: Machine learning

What data science task can I help with?"""
        
        if "help" in user_msg or "can you" in user_msg or ("what" in user_msg and "do" in user_msg):
            return """I can assist with:

- Writing and debugging code
- Explaining programming concepts
- Data science and machine learning
- Problem-solving and algorithms
- Writing and editing
- Math and statistics

What would you like help with?"""
        
        if "thank" in user_msg:
            return "You're welcome! Feel free to ask anything else."
        
        return "I'm here to help with programming, data analysis, machine learning, problem-solving, and more. What would you like to work on?"
    
    def show_stats(self):
        print("\n" + "="*70)
        print("STATISTICS")
        print("="*70)
        print(f"Total messages: {self.message_count}")
        print(f"Conversation turns: {len(self.conversation_history)}")
        print("="*70 + "\n")
    
    def show_history(self):
        if not self.conversation_history:
            print("No conversation yet.")
            return
        
        print("\n" + "="*70)
        print("HISTORY")
        print("="*70 + "\n")
        
        for i, msg in enumerate(self.conversation_history, 1):
            print(f"{i}. {msg}\n")
        
        print("="*70 + "\n")

def start_chatbot():
    bot = LLMChatbot()
    print("Chatbot Ready\n")
    
    while True:
        try:
            user_input = input("YOUR QUESTION: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'stop']:
                bot.show_stats()
                print("Session ended")
                break
            
            elif user_input.lower() == 'stats':
                bot.show_stats()
                continue
            
            elif user_input.lower() == 'history':
                bot.show_history()
                continue
            
            elif not user_input:
                print("Please enter a question\n")
                continue
            
            bot.chat(user_input)
            print()
            
        except KeyboardInterrupt:
            bot.show_stats()
            break
        
        except Exception as e:
            print(f"Error: {e}\n")
    
    return bot

bot = start_chatbot()


# In[ ]:




