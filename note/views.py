from django.shortcuts import render, redirect, HttpResponsePermanentRedirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import NoteBook, Note
from django.shortcuts import get_object_or_404
from .forms import EditNoteForm
from django.forms.models import model_to_dict
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import NoteForm
from django.db.models import Q
from sentence_transformers import SentenceTransformer, CrossEncoder
import torch
from transformers import AutoTokenizer, BartForConditionalGeneration
from django.views.generic import TemplateView
from .services import create_recommendations
from maip_client import MaipClient
from maip_context import MaipContext

threshold = 0.5

# Create your views here.
def frontpage(request):
    return render(request, 'frontpage.html')



def signup(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
    context={'form': form}
    return render(request, 'signup.html', context)



def userlogin(request):
    if request.method == 'POST':
         username=request.POST.get('username')
         password=request.POST.get('password')
         user=authenticate(request, username=username, password=password)
         if user is not None:
             login(request, user)
             return redirect('home') # Redirect to the dashboard after successful login
         else:
            messages.info(request, 'Username OR password is incorrect.')
    
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def logoutuser(request):
    logout(request)
    return redirect('login')


@login_required
def home(request):

    # Summarization comes into play:

    # Load model for summarization
    # model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    # # Load tokenizer
    # tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
     
    notebook, isCreated = NoteBook.objects.get_or_create(user=request.user)

    print("Calling create_recommendations function...")  # Debug line
    recommendations = create_recommendations(request.user)

    # Debugging: Print the recommendations to the console
    #print(recommendations)

    context = {
        'recommendations': recommendations
    }

    if request.method == 'POST':
        category = request.POST.get('category', '')
        subject = request.POST.get('subject', '')
        title = request.POST.get('title')
        text = request.POST.get('text')




        # Add debug statement to see if the code reaches this point
        print("Before generating summaries")

        if len(text.split()) < 25:  # Skip summarization for very short notes
            summary = text
        myClient = MaipClient("192.168.68.131", 8070)
        myClient.create_client()

        hostedModel = myClient.get_program_models()[0]

        myClient.acquire_model(hostedModel)
        chatObject : MaipContext = myClient.create_context(hostedModel, 4096)
        input = text

        msgIds = []

        messageId = chatObject.set_input("System", "You are an assistant who summarizes the given text.")
        msgIds.append(messageId)
        messageId = chatObject.set_input("User", input)
        msgIds.append(messageId)

        summary = chatObject.execute_input_sync(msgIds)
        # inputs = tokenizer(text, max_length=256, return_tensors="pt")
        # summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=200)
        # summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        print(f"Generated summary for {title}: {summary}")  # Debugging print statement

        
        Note.objects.create(
                notebook=notebook,
                title=title,
                text=text,
                subject=subject,
                category=category,
                summary=summary
        )
        
        return redirect('home')

    return render(request, 'base.html', context)   


@login_required
def notes(request):

    # Summarization comes into play:

    # Load model for summarization
    # model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    # Load tokenizer
    # tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

    
    # Semantic Search comes into play:

    #Load a pre-trained SBERT model
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    # Get all notes for the logged-in user
    notes = list(Note.objects.filter(notebook__user=request.user))

    corpus = []

    for note in notes:
        str_temp = (
            f"{note.category} "
            f"{note.subject} "
            f"{note.title} "
            f"{note.text}"
        )

        corpus.append(str_temp)

    query = request.GET.get('query')
    

    if query:

        top_k = min(5, len(corpus))

        # If there's a query, perform semantic search
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)


        # Calculate similarity scores
        similarity_scores = torch.nn.functional.cosine_similarity(query_embedding, corpus_embeddings)
        scores, indices = torch.topk(similarity_scores, k=top_k)


        # Prepare the search results for rendering
        result = []
        hits = []

        for score, idx in zip(scores, indices):
            note_obj = notes[idx] # Retrieve the corresponding Note object
            result.append(
                {
                    'id': note_obj.id,
                    'title': note_obj.title,
                    'date_created': note_obj.date_created,
                    'content': corpus[idx],
                    'score': score.item(),
                }
            )

        # Re-Ranking comes into play

        if result:
            # Load cross-encoder model
            cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

            # Create pairs of the query and each candidate note
            cross_inp = [[query, note['content']] for note in result]

            # Debugging: Print the input that is being passed to the cross-encoder
            #print(f"Input to cross-encoder: {cross_inp}")

            # Get relevance scores from the cross-encoder
            cross_scores = cross_encoder.predict(cross_inp)

            # Debugging: Print the scores returned by the cross-encoder
            #print(f"Cross-encoder scores: {cross_scores}")

            for idx, note in enumerate(result):
                note['cross-score'] = cross_scores[idx]

            hits = [note for note in result if note['cross-score'] >= threshold]
            # Sort candidates by cross-score    
            hits = sorted(hits, key=lambda x: x['cross-score'], reverse=True)

            # Debugging: Check the final sorted hits
            #print(f"Final hits after re-ranking: {hits}")
            
            # Add debug statement to see if the code reaches this point
         #print("Before generating summaries")

            #for note in hits:
                #print(f"Original text for {note['title']}: {note['content']}")  # Debug original text
                #if len(note['content'].split()) < 25:  # Skip summarization for very short notes
                #    return note['content']
                #inputs = tokenizer(note['content'], max_length=256, return_tensors="pt")
                #summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=200)
                #note['summary'] = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
                #print(f"Generated summary for {note['title']}: {note['summary']}")  # Debugging print statement
            
            context = {
                 'notes': hits
            }         

    else:
        #for note in notes:
                #print(f"Original text for {note.title}: {note.title}")  # Debug original text
                #if len(note.text.split()) < 25:  # Skip summarization for very short notes
                    #return note.text
                #inputs = tokenizer(note.text, max_length=256, return_tensors="pt")
                #summary_ids = model.generate(inputs["input_ids"], num_beams=2, min_length=0, max_length=200)
                #note.summary = tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
                #print(f"Generated summary for {note.title}: {note.summary}")  # Debugging print statement

        context = {
            'notes': notes
        }      
        

    # Pass the notes to the template
    return render(request, 'notes.html', context)


@login_required
def note_detail(request, id):
    # Get specific note for the logged-in user
    note = get_object_or_404(Note, id=id, notebook__user=request.user)

    context = {
        'note':note
    }

    # Pass the note to the template
    return render(request, 'note_detail.html', context)



@login_required
def delete_note(request, id):
    note = get_object_or_404(Note, id=id)

    if request.method=='POST':
        note.delete()
        return redirect('notes')
    
    return render(request, 'notes.html', {'note':note})





@login_required
def edit_note(request, id):
    
    note = get_object_or_404(Note, id=id)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save()
            return JsonResponse({
                'success': True,
                'note': {
                    'category': note.category,
                    'subject': note.subject,
                    'title': note.title,
                    'text': note.text,
                }
            })
        else:
            return JsonResponse({'success':False, 'error': form.errors}, status=400)

    return JsonResponse({'success':False, 'error': 'Invalid request.'}, status=400)    




