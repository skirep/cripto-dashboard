# 🚀 Crypto Dashboard

Dashboard de criptomonedes amb seguiment històric complet que mostra les 10 criptomonedes que han pujat més i les 10 que han baixat més durant l'última hora.

## 🌟 Característiques

- 📈 Top 10 guanyadors de l'última hora
- 📉 Top 10 perdedors de l'última hora
- 🔄 Actualització automàtica cada hora
- 💅 Interfície elegant i responsiva
- 📊 Dades en temps real de CoinGecko API
- 🔍 **Seguiment històric automàtic** de totes les criptomonedes que apareixen al rànquing
- ⏰ **Gestió d'inactivitat**: Les criptos que no apareixen durant més de 2 dies es marquen com inactives
- 📅 **Mitjanes diàries**: Després de 2 dies, les dades es consoliden en mitjanes diàries
- 🗂️ **Històric de 10 dies**: Es mantenen dades dels últims 10 dies com a màxim

## 🚀 Com funciona

1. **Script Python** (`fetch_crypto_data.py`): 
   - Consulta l'API de CoinGecko per obtenir dades de les principals criptomonedes
   - Identifica els top 10 guanyadors i perdedors
   - Manté un històric de totes les criptomonedes seguides
   - Calcula mitjanes diàries per dades antigües
   - Neteja automàticament dades de més de 10 dies
2. **Fitxers JSON**:
   - `crypto_data.json`: Dades actuals per mostrar al dashboard
   - `crypto_historical.json`: Històric complet de totes les criptomonedes seguides
3. **Pàgina HTML** (`index.html`): Mostra les dades de manera visual i atractiva amb indicadors d'estat
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