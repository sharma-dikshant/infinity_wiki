from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import google.generativeai as genai


genai.configure(api_key=settings.GEMINI_API_KEY)

# Create your views here.

def generate_prompt(query):
    return f"""You are a Wikipedia-style assistant.  make the answer easy to understand.

        RETURN ONLY VALID HTML. Do NOT use Markdown, triple backticks, or include any non-HTML wrapper.
        Do NOT include <script>, <iframe>, or other executable tags.

        Structure the response exactly using these sections and tags:

        <h2>{query} — short one-line summary</h2>
        <p class="tldr">One-line TL;DR (short summary).</p>

        <h3>Definition</h3>
        <p>Brief, clear definition. Bold key terms with <strong>.</p>

        <h3>Context / Background</h3>
        <p>Why it matters; simple historical/contextual notes.</p>

        <h3>How it works / Key points</h3>
        <ol>
        <li>Concise step or main idea 1</li>
        <li>Concise step or main idea 2</li>
        <li>... (use short sentences)</li>
        </ol>

        <h3>Examples</h3>
        <ul>
        <li>Example 1 — short and practical (if code, use &lt;pre&gt;&lt;code&gt;...&lt;/code&gt;&lt;/pre&gt;)</li>
        <li>Example 2</li>
        </ul>

        <h3>Common pitfalls / Tips</h3>
        <ul>
        <li>Short pitfall or tip 1</li>
        <li>Tip 2</li>
        </ul>

        <h3>Related topics</h3>
        <ul>
        <li>Related topic 1</li>
        <li>Related topic 2</li>
        </ul>

        <h3>Further reading / Search queries</h3>
        <ul>
        <li>Suggested short search queries or book/article titles (do NOT invent URLs)</li>
        </ul>

        If you are uncertain about a factual detail, clearly say "I'm not certain about this detail."
        """


def home(request):
    result = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            model = genai.GenerativeModel("gemini-1.5-flash-002")
            prompt = f"""
                    You are a Wikipedia-style assistant. For the user's query below:
                    1) Give a one-line summary.
                    2) Then explain thoroughly in an easy-to-understand way (give context).
                    3) Provide examples if applicable (as bullet points).
                    4) List related topics or short pointers for further reading.

                    Return the response using tags.
                    - Do NOT include any Markdown formatting like triple backticks.
                    - Use <h2> for the summary.
                    - Use <p> for explanations.
                    - Use <ul><li> for examples and related topics.

                    User query: {query}
                    """
            response = model.generate_content(prompt)  # Pass prompt, not query
            result = response.text

    return render(request, 'wiki/home.html', {'result': result})
