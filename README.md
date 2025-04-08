# Europäische Karten - Programmdokumentation

Diese Dokumentation beschreibt die Python-Programme in diesem Verzeichnis, die verschiedene Karten und geografische Visualisierungen erstellen.

## Programme

### SchweizMap.py
Dieses Programm erstellt eine detaillierte Karte der Schweiz mit folgenden Funktionen:
- Visualisierung der Schweizer Kantone basierend auf GeoJSON-Daten
- Farbliche Hervorhebung der verschiedenen Kantone
- Interaktive Elemente zur Anzeige von Kantonsinformationen
- Möglichkeit zum Export der Karte als Bilddatei

### EuropeanMaps.py
Ein Programm zur Erstellung verschiedener Karten von Europa:
- Grundkarte mit Ländergrenzen aller europäischen Staaten
- Optionen zur thematischen Darstellung (Bevölkerungsdichte, BIP, etc.)
- Zoom-Funktionen für verschiedene Regionen Europas
- Unterstützung für verschiedene Kartenprojektionen

### lifeypectancy.py
Dieses Programm analysiert und visualisiert die Lebenserwartung in Europa:
- Lädt und verarbeitet demografische Daten zur Lebenserwartung
- Erstellt farbcodierte Karten basierend auf Lebenserwartungsdaten
- Ermöglicht Vergleiche zwischen verschiedenen Ländern/Regionen
- Unterstützt Zeitreihenanalysen zur Entwicklung der Lebenserwartung

### USA.py
Ein separates Programm zur Erstellung von Karten der Vereinigten Staaten:
- Visualisierung der US-Bundesstaaten mit ihren Grenzen
- Möglichkeit zur Integration verschiedener demografischer Daten
- Vergleichsoptionen zwischen US-Regionen und europäischen Gebieten
- Export-Funktionen für verschiedene Formate (PNG, SVG, PDF)

## Abhängigkeiten
Alle Programme benötigen folgende Python-Bibliotheken:
- geopandas
- plotly
- pandas
- numpy
- folium (für interaktive Karten)

## Verwendung
Jedes Programm kann direkt über die Kommandozeile ausgeführt werden, z.B.:
```
python SchweizMap.py
```

Die generierten Karten werden im aktuellen Verzeichnis gespeichert.