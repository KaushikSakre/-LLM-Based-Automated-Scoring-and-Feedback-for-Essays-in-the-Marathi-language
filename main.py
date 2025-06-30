# main.py
#model_name="gemma2-9b-it",#mixtral-8x7b-32768
#prompt = '''Censorship in the Libraries
#"All of us can think of a book that we hope none of our children or any other children have taken off the shelf. But if I have the right to remove that book from the shelf -- that work I abhor -- then you also have exactly the same right and so does everyone else. And then we have no books left on the shelf for any of us." --Katherine Paterson, Author
#Write a persuasive essay to a newspaper reflecting your vies on censorship in libraries. Do you believe that certain materials, such as books, music, movies, magazines, etc., should be removed from the shelves if they are found offensive? Support your position with convincing arguments from your own experience, observations, and/or reading.

from flask import Flask, request, render_template
from dotenv import load_dotenv
from results import generate_results
from context import Rubric
from examples import (
    EXAMPLE_PROMPT_1, EXAMPLE_ESSAY_1, EXAMPLE_EVALUATION_1,
    EXAMPLE_PROMPT, EXAMPLE_ESSAY, EXAMPLE_EVALUATION
)
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Constants
TEMPERATURE = 0.4
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL_NAME = "llama3-70b-8192"

@app.route('/', methods=['GET', 'POST'])
def index():
    score = None
    #prompt = ""
    essay = ""
    
    if request.method == 'POST':
        #prompt = request.form.get('prompt')
        essay = request.form.get('essay')

        # Use the example-based system prompt
        system_prompt = (
        """
            तुम्ही परीक्षक समितीतील तज्ज्ञ आहात आणि तुमचे कार्य दिलेल्या मार्गदर्शक तत्त्वांनुसार निबंधाचे मूल्यांकन करणे व गुणांकन करणे आहे.

            **सामान्य मार्गदर्शक तत्त्वे:** \n
            **गुणांकन (Scoring)** \n
            1)निबंधातील सर्व वाक्ये परस्पर-संबंधित (co-related) आहेत का, हे तपासा.\n
            2)निबंधाची लांबी महत्त्वाची आहे.\n
            3)भाषा, व्याकरण, मांडणी, संदर्भ, वाक्यरचना आणि सुसूत्रता यांचे मूल्यांकन करा.\n
            **अभिप्राय (Feedback):** \n
            1)गुण देण्याचे कारण स्पष्ट करा.\n
            2)फक्त मराठी भाषेत अभिप्राय द्या. इंग्रजीचा वापर टाळावा. \n
            3)गुणांकन आणि अभिप्राय हे दिलेल्या मूल्यमापन निकषांनुसार (rubric){Rubric} केले जावे.\n
            4)अभिप्रायामध्ये पुढील गोष्टींचा समावेश असावा:  \n
            5)निबंधातील चांगले पैलू कोणते आहेत. \n
            6)सुधारण्याच्या संधी कुठे आहेत.\n
            7)लेखक निबंध सुधारण्यासाठी कोणते ठोस पाऊल उचलू शकतो.\n
            8)भाषिक अर्थ बदलू नये; तो समान राहिला पाहिजे.\n

            **निबंध: {essay}**

        """
        ).format(
            Rubric=Rubric,
            essay=essay
        )

        # Call the generate_results function to get the score
        score = generate_results(GROQ_API_KEY, LLM_MODEL_NAME, system_prompt, essay, TEMPERATURE)
        return render_template('index.html', score=score, essay=essay)

    return render_template('index.html', score=None)

if __name__ == "__main__":
    app.run(debug=True)



