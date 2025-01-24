# request-rate-test

Dies ist mein Test Projekt für "Request Info & Rate Limit"

## Features
- webserver (nginx): Statische Inhalte + Reserver Proxy für /api/
- backend (Node.js): Empfängt Formulardaten, ruft Middleware auf, schreibt in Postgres
- middleware (Nodejs): Einfache Kategorisierung
- db (Postgres): Persistente Speicherung

## Verwendung
- installieren: docker, python(lts version), flask (pip install flask)
- starten: docker-compose up --build
- docker starten

## Beispiel
![alt text](assets/image.png)

