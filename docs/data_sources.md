# Data Sources Documentation

Este documento describe las fuentes de datos utilizadas en el proyecto, incluyendo detalles de acceso, estructura de la respuesta y ejemplos de uso.

---

## 1. NewsAPI

**Descripción:**  
*Descripcion de la pagina*:
Provides access to current and historical news articles from a vast number of sources worldwide. They focus on delivering raw news data for developers to integrate into their applications.

**Endpoint principal:**  
https://newsapi.org/v2/everything

**Ejemplo de respuesta recortado**
{
  "status": "ok",
  "totalResults": 26166,
  "articles": [
    {
      "source": {
        "id": null,
        "name": "Gizmodo.com"
      },
      "author": "Matt Novak",
      "title": "Bitcoin Flash Crash Roils Crypto Market",
      "description": "Did a single whale disrupt the crypto ocean?",
      "url": "https://gizmodo.com/bitcoin-price-flash-crash-ether-thiel-2000647613",
      "urlToImage": "https://gizmodo.com/app/uploads/2024/08/A-bitcoin-token.jpg",
      "publishedAt": "2025-08-25T17:50:49Z",
      "content": "Crypto prices dipped Monday following a so-called flash crash of Bitcoin..."
    }
  ]
}

*Notas*: 
- El campo principal es `articles`, que devuelve la lista de noticias.
- Algunos campos como `author`, `description`, `urlToImage` pueden venir vacios.
- Preferible limitar `pageSize` y paginar si se necesita mas volumen.

## 2. CryptoCompare API

**Descripcion**
- CryptoCompare proporciona datos de mercado de criptomonedas, incluyendo precios, métricas y también un feed de noticias relacionadas al mundo cripto.

**EndPoint principal (news):**
https://min-api.cryptocompare.com/data/v2/news/?lang=EN

**Ejemplo de respuesta recortado**
{
  "Type": 100,
  "Message": "News list successfully returned",
  "Data": [
    {
      "id": "50796073",
      "published_on": 1756353310,
      "title": "Bitcoin Price Astounding Surge: BTC Rockets Above $112,000",
      "url": "https://bitcoinworld.co.in/bitcoin-price-surge-4/",
      "body": "The cryptocurrency market is buzzing with excitement as the Bitcoin price has achieved...",
      "source": "bitcoinworld",
      "categories": "CRYPTOCURRENCY|BTC|TRADING|MARKET|BUSINESS"
    }
  ]
}

*Notas*: 
- La clave principal es `Data`, que devuelve la lista de articulos.
- `published_on` viene como timestamp UNIX.
- Pasa metadatos adicionales como `categories` y `source`

## 2. Infobae (Web Scraping)

**Descripcion**
- Es un medio digital de noticias, no tiene API publica, asi que por el momento se utiliza scraping del HTML.

**Endpoint principal (seccion economia):**
https://www.infobae.com/economia/

**Ejemplo de output**
[
  "El Gobierno asegura que llegó a un acuerdo con los controladores aéreos y que se levantará la medida de fuerza",
  "El Gobierno aumentó por quinta vez en el año un recargo en las facturas de gas con el que financia el subsidio a zonas frías",
  "Ajuste monetario: con tasas altas, el Gobierno colocó bonos para absorber $700.000 millones"
]

*Notas*:
- Puede haber artículos repetidos si aparecen en más de una sección, depende del metodo de extraccion de los titulares y enlaces (ejL h2 o a con clases especificas)
- La estructura del HTML muy probablemente cambie por lo que no hay una estabilidad garantizada.
- Es recomendable loguear errores en caso de cambios en la pagina.




