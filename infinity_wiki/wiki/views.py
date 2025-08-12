from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import google.generativeai as genai


genai.configure(api_key=settings.GEMINI_API_KEY)

# Create your views here.

def home(request):
    result = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            model = genai.GenerativeModel("gemini-1.5-flash-002")
            prompt = (
                "You are like a Wikipedia, so whatever the user query is, "
                "explain it thoroughly in an easy-to-understand way. "
                "Give context, and if examples are possible, also provide examples. "
                "Additionally, give related information for better understanding.\n\n"
                f"User query: {query}"
            )
            response = model.generate_content(prompt)
            result = response.text
            
    return render(request, 'wiki/home.html', {'result': result})
