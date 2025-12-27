# 🚀 Crypto Dashboard

Dashboard de criptomonedes que mostra les 10 criptomonedes que han pujat més i les 10 que han baixat més durant l'última hora.

## 🌟 Característiques

- 📈 Top 10 guanyadors de l'última hora
- 📉 Top 10 perdedors de l'última hora
- 🔄 Actualització automàtica cada hora
- 💅 Interfície elegant i responsiva
- 📊 Dades en temps real de CoinGecko API

## 🚀 Com funciona

1. **Script Python** (`fetch_crypto_data.py`): Consulta l'API de CoinGecko per obtenir dades de les principals criptomonedes i identifica els top 10 guanyadors i perdedors
2. **Fitxer JSON** (`crypto_data.json`): Emmagatzema les dades processades
3. **Pàgina HTML** (`index.html`): Mostra les dades de manera visual i atractiva
4. **GitHub Actions** (`.github/workflows/update-dashboard.yml`): Automatitza l'actualització cada hora i desplega a GitHub Pages

## 🛠️ Configuració

### Habilitar GitHub Pages

1. Ves a Settings > Pages del teu repositori
2. A "Source", selecciona "GitHub Actions"
3. El workflow desplegarà automàticament el dashboard

### Execució Manual

Per executar el script localment:

```bash
python3 fetch_crypto_data.py
```

Això generarà el fitxer `crypto_data.json` amb les últimes dades.

### Visualitzar Localment

Obre el fitxer `index.html` en un navegador web o utilitza un servidor HTTP local:

```bash
python3 -m http.server 8000
```

Després visita `http://localhost:8000`

## 📅 Actualitzacions

El dashboard s'actualitza automàticament cada hora mitjançant GitHub Actions. També pots executar l'actualització manualment des de la pestanya "Actions" del repositori.

## 🔗 API Utilitzada

Aquest projecte utilitza l'[API de CoinGecko](https://www.coingecko.com/), que proporciona dades gratuïtes de criptomonedes sense necessitat d'autenticació.

## 📝 Llicència

Aquest projecte és de codi obert i està disponible per a ús públic.