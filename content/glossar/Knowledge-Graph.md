---
title: Knowledge Graph
category: Konzepte & Technologien
difficulty: mittel
related_terms: ["Ontologie", "Datenbank", "KI", "API"]
---

# Knowledge Graph

## Was ist das?

Ein **Knowledge Graph** (Wissensgraph) ist wie ein digitales Gehirn: Er speichert nicht nur Informationen, sondern auch die **Beziehungen** zwischen diesen Informationen.

### Vereinfacht erklärt

Stell dir vor, du hast ein Notizbuch mit Fakten:

**Traditionelle Datenbank (Liste):**
- "Berlin ist die Hauptstadt"
- "Deutschland hat 83 Millionen Einwohner"
- "Angela Merkel war Bundeskanzlerin"

**Knowledge Graph (vernetzt):**
```
Berlin
├── ist Hauptstadt von → Deutschland
├── hat Einwohner → 3,7 Millionen
└── liegt in → Europa

Deutschland
├── hat Hauptstadt → Berlin
├── hat Einwohner → 83 Millionen
└── hatte Bundeskanzlerin → Angela Merkel (2005-2021)
```

Der Knowledge Graph **weiß**, wie die Informationen zusammenhängen.

## Warum ist das nützlich?

### Beispiel: Förderantrag prüfen

**Ohne Knowledge Graph:**
- Sachbearbeiter liest Antrag
- Sucht manuell in Förderrichtlinie
- Prüft Gesetzestexte
- Stellt Querverbindungen selbst her

**Mit Knowledge Graph:**
```
Antrag sagt: "Antragsteller ist gemeinnützig"
↓
Knowledge Graph weiß:
- Gemeinnützig → Gilt Vereinsrecht
- Vereinsrecht § 5 → Ausnahme bei Beihilferecht
- Beihilferecht → Gilt ab 200.000 € Förderung
↓
System schlägt vor: "Prüfe Paragraph 5 Vereinsrecht"
```

Das System macht **intelligente Vorschläge**, weil es die Zusammenhänge kennt.

## Praxis-Beispiele

### Google Suche
Wenn du "Eiffelturm Höhe" suchst, zeigt Google direkt "330 Meter" – ohne dass du eine Website öffnen musst. Das kommt aus Googles Knowledge Graph.

### Medizin
Krankenhäuser nutzen Knowledge Graphs, um Wechselwirkungen zwischen Medikamenten zu erkennen:
```
Medikament A
└── reagiert mit → Medikament B
    └── Risiko → Herzrhythmusstörungen
```

### Verwaltung (Vision)
Ein Verwaltungs-Knowledge-Graph könnte verbinden:
- Gesetze ↔ Förderrichtlinien
- Paragraphen ↔ Ausnahmen
- Antragsteller ↔ Förderprogramme

## Verwandte Begriffe

- **Ontologie**: Die Wissenschaft hinter Knowledge Graphs – wie man Wissen strukturiert
- **Semantisches Netz**: Älterer Begriff für ähnliche Konzepte
- **Graph-Datenbank**: Die technische Grundlage (z.B. Neo4j)

## Technischer Hintergrund (optional)

Knowledge Graphs basieren auf **Tripel-Strukturen**:
```
Subjekt → Prädikat → Objekt

Beispiel:
Berlin → ist_Hauptstadt_von → Deutschland
```

Daraus entsteht ein **Netzwerk von Beziehungen**, das Computer verstehen und durchsuchen können.

## Unterschied zu normalen Datenbanken

| Traditionelle Datenbank | Knowledge Graph |
|-------------------------|-----------------|
| Speichert Daten in Tabellen | Speichert Daten als Netzwerk |
| Beziehungen sind "hart codiert" | Beziehungen sind flexibel |
| Schwer erweiterbar | Einfach erweiterbar |
| Gut für strukturierte Daten | Gut für vernetzte Informationen |

## Für wen ist das relevant?

- **Verwaltung**: Komplexe Regelwerke vernetzen
- **Forschung**: Literatur und Daten verbinden
- **E-Commerce**: Produkt-Empfehlungen
- **Content-Management**: Inhalte intelligent verlinken

## Weiterführende Links

- [Wikipedia: Knowledge Graph](https://de.wikipedia.org/wiki/Knowledge_Graph)
- Neo4j Graph Database (Open Source)
- Google Knowledge Graph (Beispiel)

---

**Erstellt**: 2025-12-21
**Schwierigkeitsgrad**: Mittel
**Lesedauer**: 4 Minuten
