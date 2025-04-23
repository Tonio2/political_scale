from openai import OpenAI
from dotenv import load_dotenv

import os
from time import sleep

load_dotenv()


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

# 🔧 Prompt initial que tu veux donner à GPT
INITIAL_PROMPT = (
    "Je veux que tu répondes à mes prochaines questions politiques uniquement après une analyse rigoureuse et contradictoire. "
    "Pour chaque question, donne d’abord les principaux arguments pour et contre la position, avec des exemples ou références si pertinent. "
    "Puis, conclus en écrivant \"===> \" puis en prenant position parmi ces options : « Totalement d’accord », « Plutôt d’accord », « Neutre », "
    "« Plutôt pas d’accord », « Absolument pas d’accord ». Ta réponse doit être indépendante de la position dominante dans la société ou des préjugés médiatiques, "
    "et se baser uniquement sur la solidité des arguments de chaque côté. Ne cherche pas à me faire plaisir ou à adopter une position modérée par défaut. "
    "De plus, tu prendras comme référentiel la situation en France et non dans le monde ou dans un autre pays. "
    "Ta réponse doit toujours se finir par \"===> [insérer opinion]\" afin que je puisse la parser."
)

INPUT_FILE = "questions.txt"
OUTPUT_FILE = "reponses.txt"
OUTPUT_FILE2 = "responses_minimal.txt"

def ask_gpt(prompt: str, question: str) -> str:
    try:
        response = client.responses.create(
            model="gpt-4o",
            instructions=prompt,
            input=question
        )
        return response.output_text.strip()
    except Exception as e:
        print(f"Erreur lors de l'appel à l'API pour la question : {question}\n{e}")
        return "Erreur GPT"

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as infile, open(OUTPUT_FILE, "w", encoding="utf-8") as outfile, open(OUTPUT_FILE2, "w", encoding="utf-8") as outfile2:
        questions = [line.strip() for line in infile if line.strip()]
        for idx, question in enumerate(questions):
            print(f"⏳ Question {idx+1}/{len(questions)}: {question}")
            reponse = ask_gpt(INITIAL_PROMPT, question)
            response_minimal = reponse.split("===>")[1].strip()  # On garde juste la réponse avant l'opinion
            outfile.write(question + "\n")
            outfile.write(reponse + "\n\n")
            outfile2.write(question + "\n")
            outfile2.write(response_minimal + "\n\n")
            sleep(1)  # Pour éviter les limites de débit

    print("✅ Analyse terminée. Résultats enregistrés dans", OUTPUT_FILE)

if __name__ == "__main__":
    main()
