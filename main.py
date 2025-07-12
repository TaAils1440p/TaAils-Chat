import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk # Import ttk for modern widgets

# Try to import Langchain components; provide a mock if not available for UI testing
try:
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate

    # Define the template for the language model
    template = """
    Answer the question below.

    Here is the conversation history: {context}

    Question: {question}

    Answer:
    """
    # Initialize the Ollama model (ensure 'llama3' is available locally)
    model = OllamaLLM(model="llama3")
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model
    LLM_AVAILABLE = True
except ImportError:
    print("Langchain or Ollama not found. Running with mock AI responses.")
    LLM_AVAILABLE = False
    class MockChain:
        def invoke(self, data):
            question = data.get("question", "")
            return f"Mock AI Response to: '{question}'"
    chain = MockChain()


def handle_conversation():
    context = "" # Conversation context for the model

    def send_message():
        nonlocal context
        user_input = user_input_area.get("1.0", tk.END).strip()

        if not user_input: # Do nothing if input is empty
            return

        if user_input.lower() == 'exit':
            root.quit()
            return

        # Display user message in chat history
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"You: {user_input}\n", "user_tag") # Use tag for styling
        chat_history.config(state=tk.DISABLED)
        user_input_area.delete("1.0", tk.END) # Clear input field

        # Simulate AI response (call to the model)
        # A loading indicator could be added here for better UX
        try:
            if LLM_AVAILABLE:
                result = chain.invoke({"context": context, "question": user_input})
            else:
                result = chain.invoke({"question": user_input}) # Use mock chain
        except Exception as e:
            result = f"Error: Could not get a response from the AI model. ({e})"
            print(f"Error calling LLM: {e}")

        # Update context with the new interaction
        context += f'\nUser: {user_input}\nAI: {result}\n'

        # Display AI response in chat history
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"AI: {result}\n\n", "ai_tag") # Use tag for styling
        chat_history.config(state=tk.DISABLED)
        chat_history.see(tk.END) # Auto-scroll to the bottom

    # Main window configuration
    root = tk.Tk()
    root.title("TaAils Chat")
    root.geometry("600x700") # Initial window size
    root.resizable(True, True) # Allow resizing

    # Configure ttk styles
    style = ttk.Style()
    style.theme_use('clam') # Use a modern theme (e.g., 'clam', 'alt', 'default', 'vista', 'xpnative')

    # Styles for widgets
    style.configure('TFrame', background='#f0f2f5') # Frame background color
    style.configure('TButton',
                    font=('Inter', 12, 'bold'), # Modern font
                    background='#4CAF50', # Button background color (green)
                    foreground='white', # Button text color
                    padding=10, # Internal padding
                    relief='flat', # Flat style
                    focusthickness=0, # Remove focus outline
                    focuscolor='none')
    style.map('TButton',
              background=[('active', '#45a049')]) # Hover color

    style.configure('TScrollbar',
                    troughcolor='#e0e0e0', # Scrollbar trough color
                    background='#a0a0a0', # Scrollbar handle color
                    gripcount=0, # Remove grip lines
                    bordercolor='#a0a0a0',
                    arrowcolor='#555555')

    # Main frame to contain all elements
    main_frame = ttk.Frame(root, padding="10 10 10 10")
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Chat history area
    chat_history = scrolledtext.ScrolledText(main_frame,
                                             state='disabled',
                                             wrap=tk.WORD, # Automatic word wrapping
                                             font=('Inter', 11),
                                             bg='#ffffff', # White background
                                             fg='#333333', # Dark gray text
                                             relief=tk.FLAT, # Flat border
                                             padx=10, pady=10,
                                             borderwidth=0)
    chat_history.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # Configure tags for message styling
    chat_history.tag_configure("user_tag", foreground="#007bff", font=('Inter', 11, 'bold')) # Blue for user
    chat_history.tag_configure("ai_tag", foreground="#28a745", font=('Inter', 11)) # Green for AI

    # User input area
    user_input_area = tk.Text(main_frame,
                              height=4,
                              font=('Inter', 11),
                              bg='#ffffff',
                              fg='#333333',
                              relief=tk.SOLID, # Solid border
                              borderwidth=1,
                              padx=10, pady=10,
                              highlightbackground="#cccccc", # Border color when not focused
                              highlightcolor="#007bff", # Border color when focused
                              highlightthickness=1)
    user_input_area.pack(padx=5, pady=5, fill=tk.X, expand=False) # Fill horizontally

    # Bind Enter key to send message
    user_input_area.bind("<Return>", lambda event: (send_message(), "break")) # "break" to prevent default newline

    # Send button
    send_button = ttk.Button(main_frame, text="Send", command=send_message, style='TButton')
    send_button.pack(pady=10) # Vertical spacing

    # Start the main GUI loop
    root.mainloop()

if __name__ == "__main__":
    handle_conversation()