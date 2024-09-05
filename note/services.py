import spacy
from collections import Counter
from .models import NoteBook
from transformers import pipeline
from transformers import AutoTokenizer, AutoModel
import torch
import re
from maip_client import MaipClient
from maip_context import MaipContext

nlp = spacy.load('en_core_web_sm')

# Load a pre-trained model from Hugging Face
#tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
#model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

myClient = MaipClient("192.168.68.131", 8070)
myClient.create_client()

hostedModel = myClient.get_program_models()[0]

myClient.acquire_model(hostedModel)


# Initialize the text generation model
#generator = pipeline('text-generation', model='gpt2', max_length=50)

# # This function generates and returns the embedding (a vector representation) for any given text
# def create_embedding(content):
#     inputs = tokenizer(content, return_tensors="pt", padding=True, truncation=True)
#     outputs = model(**inputs)

#     # Encode content to embedding
#     embeddings = torch.mean(outputs.last_hidden_state, dim=1)

#     # Convert the numpy array to a Python list for storage and, return
#     return embeddings.detach().numpy() 


def extract_words(note):

    text = re.sub(r'\s+', ' ', note.summary)  # Replace multiple spaces with a single space
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove non-alphanumeric characters

    summaries = "".join(text)
    print("Combined Summaries:", summaries)  # Debug: Check if summaries are combined
    doc = nlp(summaries)


    # Extract noun phrases and important keywords
    keywords = [chunk.text for chunk in doc.noun_chunks if len(chunk.text)>2]
    keyword_freq = Counter(keywords) 
    print("Extracted Keywords:", keyword_freq)  # Debug: Check extracted keywords

    # Return the top 10 most common keywords
    return keyword_freq.most_common(10)

def create_recommendations(user):

    try:
        notebook = NoteBook.objects.get(user=user)

        notes = notebook.notes.all()

        
        if not notes.exists():
            return {
                "content_based": [],
                "actionable_insights": [],
                "reminders": [],
                "tag_suggestions": []
            }
        
        recommendations = []
        
        for note in notes:

            keys = extract_words(note)

            recommendation = {
                "content_based": recommend_content(keys),
                "actionable_insights": recommend_task_or_goal(keys),
                "reminders": recommend_reminders(keys),
                "tag_suggestions": recommend_tags(keys)
            }

            #recommendations.append(f"Recommendation for note {note.id}: {recommendation}")
            recommendations.append(recommendation)

  

        print("Recommendations", recommendations) #Debug
        
        return recommendations
    
    except NoteBook.DoesNotExist:
        print("No notebook found for the user.")  # Debug: No notebook exists for the user
        return {
            "content_based": [],
            "actionable_insights": [],
            "reminders": [],
            "tag_suggestions": []
    }



def recommend_content(keys):
    # Suggest related content based on extracted keywords

    prompt = f"Based on these topics: {', '.join([key for key, _ in keys])}, I recommend reading about"
    # Generate recommendations dynamically
    chatObject : MaipContext = myClient.create_context(hostedModel, 3000)
    input = prompt

    msgIds = []

    messageId = chatObject.set_input("System", "You recommend content.")
    msgIds.append(messageId)
    messageId = chatObject.set_input("User", input)
    msgIds.append(messageId)
    generated_text = chatObject.execute_input_sync(msgIds)
    #summary = chatObject.execute_input_sync(msgIds)

    #generated_text = generator(prompt, max_length=400, num_return_sequences=1, temperature=0.5, top_p=0.9 , repetition_penalty=1.2)
    
    #recommendations = generated_text[0]['generated_text']
    # Splitting to get multiple suggestions
    #return recommendations.split('\n')
    return generated_text.split('\n')

def recommend_task_or_goal(keys):
    # Generate actionable insights based on recurring themes or goals

    prompt = f"These topics: {', '.join([key for key, _ in keys])}, involve the following tasks:"
    # Generate recommendations dynamically
    chatObject : MaipContext = myClient.create_context(hostedModel, 3000)
    input = prompt

    msgIds = []

    messageId = chatObject.set_input("System", "You are a medieavel sweet british gentleman. You are recommending tasks or goals. Write your headers in HTML <h> format and your output will mostly be HTML which will be included in div. Keep your answers short.")
    msgIds.append(messageId)
    messageId = chatObject.set_input("User", input)
    msgIds.append(messageId)
    generated_text = chatObject.execute_input_sync(msgIds)
    
    # generated_text = generator(prompt, max_length=400, num_return_sequences=1, temperature=0.5, top_p=0.9 , repetition_penalty=1.2)
    # recommendations = generated_text[0]['generated_text']

    # # Splitting to get multiple suggestions
    # return recommendations.split('\n')
    return generated_text.split('\n')

def recommend_reminders(keys):
    # Suggest reminders based on recurring themes
    
    prompt = f"Based on the recurring topics: {', '.join([key for key, _ in keys])}, here are reminders to consider:"
    chatObject : MaipContext = myClient.create_context(hostedModel, 3000)
    input = prompt

    msgIds = []

    messageId = chatObject.set_input("System", "You are an assistant who summarizes the given text. Write your headers in HTML <h> format and your output will mostly be HTML which will be included in div. Keep your answers short.")
    msgIds.append(messageId)
    messageId = chatObject.set_input("User", input)
    msgIds.append(messageId)
    generated_text = chatObject.execute_input_sync(msgIds)

    # Generate recommendations dynamically
    # generated_text = generator(prompt, max_length=400, num_return_sequences=1, temperature=0.5, top_p=0.9 , repetition_penalty=1.2)
    # recommendations = generated_text[0]['generated_text']
    # # Splitting to get multiple suggestions
    # return recommendations.split('\n')
    return generated_text.split('\n')

def recommend_tags(keys):
    # Suggest tags based on common keywords

    prompt = f"Suggested tags for topics: {', '.join([key for key, _ in keys])}, I recommend reading about"
    # Generate recommendations dynamically
    chatObject : MaipContext = myClient.create_context(hostedModel, 3000)
    input = prompt

    msgIds = []

    messageId = chatObject.set_input("System", "You are making tag suggestions. Write your headers in HTML <h> format and your output will mostly be HTML which will be included in div. Keep your answers short.")
    msgIds.append(messageId)
    messageId = chatObject.set_input("User", input)
    msgIds.append(messageId)
    generated_text = chatObject.execute_input_sync(msgIds)
    # generated_text = generator(prompt, max_length=400, num_return_sequences=1, temperature=0.7, top_p=0.9, repetition_penalty=1.2)
    # recommendations = generated_text[0]['generated_text']

    # # Splitting to get multiple suggestions
    # return recommendations.split('\n')
    return generated_text.split('\n')
