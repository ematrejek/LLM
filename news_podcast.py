import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
import httpx

# Ładowanie zmiennych środowiskowych
load_dotenv()

# Konfiguracja klienta OpenAI
http_client = httpx.Client(transport=httpx.HTTPTransport())
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    http_client=http_client
)

CATEGORIES = ["POLITICS", "TECHNOLOGY", "BUSINESS", "STOCK", "ENVIRONMENT"]

def get_yesterday_date():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def build_news_prompt(yesterday_date, categories):
    categories_str = ', '.join(categories)
    return f"""
<objective>
Jesteś profesjonalnym redaktorem newsowym. Twoim zadaniem jest wygenerowanie podsumowania najważniejszych wydarzeń, które miały miejsce DOKŁADNIE WCZORAJ ({yesterday_date}) w następujących kategoriach: {categories_str}.
</objective>

<rules>
- Uwzględnij TYLKO newsy, które wydarzyły się WCZORAJ (nie wcześniej, nie dziś).
- Dla każdej kategorii podaj 2-3 najważniejsze newsy.
- Każdy news opowiedz w kilku zdaniach (nie jednym!), tak by jego prezentacja trwała kilkanaście-kilkadziesiąt sekund.
- Używaj prostego, zrozumiałego języka angielskiego.
- Każdy news zaczynaj od NAZWY KATEGORII (wielkimi literami).
- Nie wymyślaj newsów – korzystaj z prawdziwych, istotnych wydarzeń.
- Nie powtarzaj tych samych informacji.
- Nie dodawaj newsów spoza {yesterday_date}.
</rules>

<categories>
{categories_str}
</categories>

<format>
KATEGORIA: [Tytuł newsa]
[Kilka zdań opisu newsa, prostym językiem, z najważniejszymi szczegółami]

KATEGORIA: [Tytuł newsa]
[Opis...]

...
</format>

<example>
POLITICS: Parliament Approves New Law
Yesterday, the parliament passed a new law aimed at improving public healthcare. The law introduces free annual check-ups for all citizens and increases funding for hospitals. Lawmakers hope this will reduce waiting times and improve overall health outcomes. (+ a few more sentences)

TECHNOLOGY: Major Breakthrough in AI
A leading tech company announced a breakthrough in artificial intelligence research. The new model can understand and generate human-like text with unprecedented accuracy. Experts say this could revolutionize customer service and content creation.(+ a few more sentences)

...
</example>

<instructions>
Wygeneruj podsumowanie zgodnie z powyższymi zasadami i formatem. Każdy news powinien być opowiedziany w kilku zdaniach, tak by był zrozumiały dla szerokiego grona odbiorców. Nie dodawaj żadnych informacji spoza {yesterday_date}.
</instructions>
""".strip()

def generate_news_summary():
    yesterday = get_yesterday_date()
    prompt = build_news_prompt(yesterday, CATEGORIES)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant and news editor."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1800
    )
    return response.choices[0].message.content.strip()

def generate_podcast_script(summary):
    prompt = (
        "Transform the following news summary into a natural-sounding podcast script. "
        "The script should be in English, sound like a friendly news presenter, and last no more than 10 minutes when read aloud. "
        "Use simple language and make it engaging:\n\n"
        f"{summary}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional podcast scriptwriter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1200
    )
    return response.choices[0].message.content.strip()

def split_text(text, max_length=4096):
    parts = []
    while len(text) > max_length:
        split_at = text.rfind('.', 0, max_length)
        if split_at == -1:
            split_at = max_length
        else:
            split_at += 1  # uwzględnij kropkę
        parts.append(text[:split_at].strip())
        text = text[split_at:].strip()
    if text:
        parts.append(text)
    return parts

def generate_tts_audio(text, voice="alloy"):
    try:
        parts = split_text(text)
        audio_data = b""
        for idx, part in enumerate(parts):
            speech_response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=part
            )
            audio_data += speech_response.content
        return audio_data
    except Exception as e:
        print(f"Błąd podczas generowania podcastu: {e}")
        return None

def generate_newsletter(summary, language):
    prompt = (
        f"Generate an email newsletter in {language.upper()} based on the following news summary. "
        f"The newsletter should be formatted in HTML, with clear sections for each category. "
        f"Use simple language and make it suitable for a general audience:\n\n"
        f"{summary}"
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert newsletter writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content.strip()

def main():
    print("Generowanie podsumowania wiadomości z dnia:", get_yesterday_date())
    summary = generate_news_summary()
    print("Podsumowanie wygenerowane.\n")

    print("Generowanie skryptu podcastu...")
    podcast_script = generate_podcast_script(summary)
    print("Skrypt podcastu wygenerowany.\n")

    print("Generowanie podcastu (TTS)...")
    podcast_audio = generate_tts_audio(podcast_script)
    if podcast_audio:
        with open("podcast.mp3", "wb") as f:
            f.write(podcast_audio)
        print("Zapisano podcast.mp3\n")
    else:
        print("Nie udało się wygenerować podcastu.\n")

    print("Generowanie newslettera po angielsku...")
    newsletter_en = generate_newsletter(summary, "english")
    with open("newsletter_en.html", "w", encoding="utf-8") as f:
        f.write(newsletter_en)
    print("Zapisano newsletter_en.html\n")

    print("Generowanie newslettera po polsku...")
    newsletter_pl = generate_newsletter(summary, "polish")
    with open("newsletter_pl.html", "w", encoding="utf-8") as f:
        f.write(newsletter_pl)
    print("Zapisano newsletter_pl.html\n")

    print("Zakończono generowanie wszystkich plików.")

if __name__ == "__main__":
    main() 