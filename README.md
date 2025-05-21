# News Podcast Generator

Ten projekt automatycznie zbiera wiadomości z poprzedniego dnia, tworzy ich podsumowanie, generuje podcast oraz newsletter w wersji angielskiej i polskiej.

## Wymagania

- Python 3.11
- venv (wirtualne środowisko Pythona)

## Instalacja

1. Sklonuj repozytorium
2. Utwórz i aktywuj wirtualne środowisko:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Zainstaluj zależności:
```bash
pip install -r requirements.txt
```

4. Skopiuj plik `.env.example` do `.env` i wypełnij odpowiednie klucze API:
```bash
cp .env.example .env
```

## Użycie

Uruchom główny skrypt:
```bash
python news_podcast.py
```

## Wyjście

Program generuje następujące pliki:
- `podcast.mp3` - 10-minutowy podcast w języku angielskim
- `newsletter_en.html` - newsletter w języku angielskim
- `newsletter_pl.html` - newsletter w języku polskim

## Funkcje

- Zbieranie wiadomości z poprzedniego dnia
- Kategoryzacja wiadomości według tematów
- Generowanie podsumowania w prostym języku
- Tworzenie podcastu (max 10 minut)
- Generowanie newslettera w dwóch wersjach językowych

## Tematy wiadomości

- POLITYKA
- EKONOMIA
- TECHNOLOGIA
- BIZNES
- GIEŁDA
- ŚRODOWISKO 