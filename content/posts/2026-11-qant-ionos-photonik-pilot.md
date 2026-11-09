---
title: "Rechnen mit Licht im deutschen Rechenzentrum: Warum der Q.ANT-Pilot bei IONOS für Europa wichtig werden kann"
type: Artikel
description: "Q.ANT aus Stuttgart stellt seinen photonischen Prozessor als Server bei IONOS bereit, kostenlos für ausgewählte Pilotpartner. Was belegt ist, was nicht, warum das für KI-Inferenz in Europa zählt und welchen Piloten wir vorschlagen."
excerpt: "Ein Prozessor aus Stuttgart, der mit Licht rechnet, steht jetzt in einem deutschen Rechenzentrum. Für Sprachmodelle ist das noch nicht bewiesen. Genau deshalb schlagen wir einen Piloten vor."
meta_title: "Q.ANT und IONOS: Photonischer Prozessor für KI-Inferenz in Europa"
meta_description: "Photonische NPU von Q.ANT im IONOS-Rechenzentrum: was der LRZ-Test gemessen hat, was für LLM-Inferenz noch fehlt und welchen Messpiloten Digitalalchemisten vorschlägt."
tags:
  - KI & Automation
  - Digitale Souveränität
featured: false
status: published
timestamp: 2026-11-09T16:00:00+01:00
---

Wer in Europa ein Sprachmodell betreibt, rechnet fast immer auf Grafikkarten aus den USA. Das gilt auch dann, wenn
Rechenzentrum, Betreiber und Daten in Deutschland liegen. Bei der Hardware bleibt man abhängig.

Seit Kurzem gibt es dazu ein Angebot, das ich mir genauer angesehen habe: Q.ANT, ein Unternehmen aus Stuttgart, stellt
seinen photonischen Prozessor als Server im Rechenzentrum von IONOS bereit. Ausgewählte Pilotpartner bekommen
kostenlos Zugang. Ich halte das für einen möglichen Meilenstein. Für große Sprachmodelle fehlen auf der Pilotseite
jedoch konkrete Messergebnisse. Deshalb werden wir einen Piloten vorschlagen.

## Was ein photonischer Prozessor ist

Ein normaler Chip rechnet mit elektrischen Signalen. Ein photonischer Chip rechnet mit Licht. Q.ANT nennt seinen
Baustein „Native Processing Unit“ (NPU). Er steckt als Karte in einem gewöhnlichen Server und übernimmt dort
bestimmte Rechenschritte, ähnlich wie eine Grafikkarte. Laut Q.ANT berechnet er auch nichtlineare Funktionen direkt
im Licht, die in neuronalen Netzen ständig vorkommen.

Der erhoffte Vorteil ist der Stromverbrauch: Bestimmte Rechenschritte sollen mit Licht deutlich weniger Energie
brauchen. Strom und Kühlung gehören heute zu den größten Kosten im Rechenzentrum.

## Was das Pilotprogramm anbietet

Laut der [Pilotseite von Q.ANT](https://qant.com/ionos-pilot/):

- Bare-Metal-Server mit der NPU der zweiten Generation, im IONOS-Rechenzentrum in Deutschland (ISO 27001)
- Zugang per SSH mit Root-Rechten, also wie ein eigener Server
- ein SDK mit Python- und C/C++-Schnittstelle sowie PyTorch-Anbindung
- kostenlos für ausgewählte Partner, mit Bewerbung, Auswahlgespräch, Begleitung und Abschlussworkshop
- Daten und Ergebnisse bleiben laut Seite beim Teilnehmer

Dauer und Bewerbungsfrist nennt die Seite nicht. Die Plätze sind begrenzt.

## Was gemessen wurde

Die beste unabhängige Quelle, die ich gefunden habe, ist ein [Bericht des Leibniz-Rechenzentrums](https://www.lrz.de/en/news/detail/photonic-computers-in-real-world-test)
(LRZ) vom April 2026. Das LRZ hat Q.ANT-Server der ersten und zweiten Generation im Alltagsbetrieb getestet:
Rechenaufgaben aus dem Hochleistungsrechnen, Bilderkennung sowie Training und Inferenz kleiner neuronaler Netze.

Laut LRZ:

- ein Bilderkennungsnetz lief um den Faktor 25 schneller, im besten Fall waren die Chips der zweiten Generation
  50-mal schneller (die Vergleichsbasis nennt der Bericht nicht genau);
- von der ersten zur zweiten Generation sank der Energiebedarf je nach Aufgabe um etwa 50 bis 84 Prozent;
- ein Q.ANT-System aus Server und Karte braucht 350 bis 420 Watt, eine einzelne große Grafikkarte bis zu 1.000 Watt.
  Diese Werte stammen vom Hersteller.

Das LRZ nennt auch die Grenzen: Nicht jede Rechenoperation lässt sich mit Licht ausführen, die Daten wandern ständig
zwischen optischem und klassischem Teil hin und her, und die Softwarebibliothek ist noch schmal.

## Was für Sprachmodelle fehlt

Hier muss man genau lesen. Q.ANT schreibt, die NPU beschleunige die linearen und nichtlinearen Operationen großer
Sprachmodelle „in einem einzigen optischen Schritt“, und nennt die Inferenz mit Open-Source-Sprachmodellen als
Einsatzfeld. Inferenz heißt: ein fertig trainiertes Modell beantwortet Anfragen. Das ist der Teil, der im Alltag
von Unternehmen den Strom verbraucht.

Was fehlt:

- Der LRZ-Bericht beschreibt keinen Test großer Sprachmodelle.
- Q.ANT nennt kein Modell, keine Modellgröße, keinen Durchsatz und keinen Energiewert pro Antwort.
- Die Zahlen auf der Pilotseite („40 Prozent weniger Parameter“ in der Bildverarbeitung, „99,7 Prozent der
  BF16-Genauigkeit“) kommen ohne Angabe, wie sie gemessen wurden.

Für Sprachmodelle ist der Vorteil also eine Behauptung, keine Messung. Q.ANT sagt das indirekt selbst: Erst im
Abschlussworkshop des Piloten sollen Energie- und Leistungswerte ausgewertet und die Eignung für den Produktivbetrieb
beurteilt werden.

## Warum es trotzdem ein Meilenstein sein kann

Drei Gründe:

1. **Chipentwicklung und Betrieb liegen in Deutschland.** Q.ANT entwickelt und fertigt die NPU laut eigener Angabe
   in Stuttgart, IONOS betreibt den Server in Deutschland. Das schafft eine europäische Hardwareoption;
   über die Herkunft sämtlicher Serverkomponenten sagt es nichts aus.
2. **Energie begrenzt den Ausbau der Inferenz.** Wenn ein Teil der Rechenarbeit mit deutlich weniger Strom läuft, sinken
   Kosten und Abhängigkeit von knappen Grafikkarten.
3. **Der Zugang ist niedrig.** Ein Server per SSH und ein PyTorch-SDK, das ist kein Forschungslabor. Damit können
   auch kleinere Teams prüfen, ob die Technik für sie trägt.

Ob daraus mehr wird als ein gutes Labor-Ergebnis, entscheidet sich bei der Inferenz echter Sprachmodelle.

## Unser Pilotvorschlag

Wir werden uns mit einem Pilotvorschlag bewerben, der genau diese Lücke misst:

- ein offenes Sprachmodell, das wir heute schon auf herkömmlicher Hardware betreiben, als Vergleich;
- dieselben Anfragen auf beiden Systemen: Antworten pro Sekunde, Strom pro Antwort, Abweichung der Antworten;
- ein realistischer Anwendungsfall: Fragen an interne Dokumente, wie sie in Unternehmen täglich vorkommen;
- offen dokumentiert, welche Teile des Modells tatsächlich auf der NPU laufen und welche nicht.

Die Ergebnisse veröffentlichen wir hier, auch wenn sie ernüchternd ausfallen. Ob wir angenommen werden, steht noch
nicht fest.

*Offenlegung: Dieser Blog läuft auf einem Server von IONOS. Von Q.ANT oder IONOS bekommen wir für diesen Beitrag
nichts.*

## Quellen

- Q.ANT: [Pilotprogramm mit IONOS](https://qant.com/ionos-pilot/) (abgerufen am 9.11.2026)
- Leibniz-Rechenzentrum: [Photonic computers in real-world test](https://www.lrz.de/en/news/detail/photonic-computers-in-real-world-test) (21.04.2026)
- Q.ANT: [Native Computing Toolkit auf GitHub](https://github.com/Q-ANT-GmbH/qant_native_computing_toolkit) (Apache-2.0)
