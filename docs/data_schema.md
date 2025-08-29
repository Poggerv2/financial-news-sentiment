# Esquema de Datos - Crypto News Collector

Este documento define el esquema base utilizado para almacenar noticias recopiladas de diferentes API y fuentes. El esquema garantiza la coherencia entre entradas heterogéneas.

---

## Campos

| Campo        | Tipo     | Descripción                                              | Ejemplo |
|--------------|----------|----------------------------------------------------------|---------|
| `id`         | string   | Identificador único (puede ser UUID o hash de URL+date)  | `"news_20250825_001"` |
| `source`     | string   | Fuente de los datos (API, sitio web, nombre del feed, etc.) | `"NewsAPI"` |
| `title`      | string   | Titular o título del artículo                            | `"Bitcoin rises above $65k"` |
| `description`| string   | Breve descripción o resumen (si está disponible)         | `"BTC reached new highs..."` |
| `content`    | string   | Texto completo del artículo si está disponible, si no, null | `"Bitcoin price surged today as..."` |
| `url`        | string   | Enlace al artículo original                              | `"https://www.coindesk.com/..."` |
| `publishedAt`| datetime | Fecha de publicación (formato ISO 8601)                  | `"2025-08-25T14:32:00Z"` |
| `collectedAt`| datetime | Fecha y hora en que se recopiló el dato                  | `"2025-08-25T18:45:00Z"` |
| `extra`      | dict     | Metadatos opcionales adicionales según la fuente         | `{"author": "John Doe", "category": "crypto"}` |

---

## Notas
- Todas las fuentes deben ser transformadas a este esquema antes de almacenarse.  
- Los campos faltantes deben guardarse como `null` (o empty string para texto).  
- El campo `extra` es flexible y permite conservar metadata que no están estandarizados entre fuentes. Cosa que a la hora de realizar el data collection se va a modificar bastante seguido.
---