import requests
import sys

# ── Tvoj zadatak ──────────────────────────────────────────────────────────────

MENU_FILE = "data/lounge-menu.md"  # mozes promeniti na 'data/lounge-menu.txt'

LLM_MODEL = ""  # TODO: izaberi model: "pozovi 'python main.py --models' da vidis dostupne modele

SYSTEM_PROMPT = ""  # TODO: napisi system prompt za asistenta restorana


# ── Pomocne funkcije (NE MENJAJ) ─────────────────────────────────────────────

API_URL = "https://api.ukisai.academy" 

def list_models() -> list[str]:
    """Vraca listu dostupnih modela sa servera."""
    r = requests.get(f"{API_URL}/models")
    r.raise_for_status()
    return r.json()["models"]


def load_menu() -> str:
    """Ucitava meni iz fajla. NE MENJAJ."""
    with open(MENU_FILE, encoding="utf-8") as f:
        return f.read()


def ask(question: str) -> str:
    """
    Ova funkcija treba da:
      1. Ucita meni pozivom load_menu()
      2. Sastavi poruku koja sadrzi meni + pitanje korisnika
      3. Posalje poruku LLM-u preko /chat endpoint-a
      4. Vrati odgovor kao string
    """
    menu = load_menu()
    message = f"PRAVI Meni restorana:\n\n{menu}\n\nPitanje: {question}"
    r = requests.post(f"{API_URL}/chat", json={
        "model": LLM_MODEL,
        "system": SYSTEM_PROMPT,
        "message": message,
    })
    r.raise_for_status()
    return r.json()["response"]


# ── Pokreni ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--models" in sys.argv:
        print("\nDostupni modeli:")
        for m in list_models():
            print(f"  - {m}")
        print()
        sys.exit(0)

    if not LLM_MODEL or not SYSTEM_PROMPT:
        print("\n[*] Izaberi LLM_MODEL i napisi SYSTEM_PROMPT pa pokreni ponovo.")
        print("    Za listu modela: python main.py --models\n")
        sys.exit(1)

    print("\nAI Asistent za Restoran — kucaj 'izlaz' za kraj\n")
    while True:
        pitanje = input("Ti: ").strip()
        if pitanje.lower() in ("izlaz", "exit", "quit"):
            print("Dovidjenja!")
            break
        if not pitanje:
            continue
        odgovor = ask(pitanje)
        if odgovor:
            print(f"\nAsistent: {odgovor}\n")
        else:
            print("\n[!] ask() vraca None — implementiraj funkciju!\n")
