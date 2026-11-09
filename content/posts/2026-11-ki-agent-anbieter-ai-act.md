---
title: "Ich baue einen KI-Agenten mit dem SDK des Herstellers. Bin ich jetzt Anbieter nach dem AI Act?"
type: Artikel
description: "Wer mit dem Agenten-SDK eines Modellherstellers einen eigenen Agenten baut, ist nach dem EU AI Act in aller Regel Anbieter. Was das bedeutet, wann es teuer wird und warum ISO 42001 und die Plattformwahl daran hängen."
excerpt: "Wer mit dem Agenten-SDK eines Modellherstellers einen eigenen Agenten baut, ist nach dem EU AI Act in aller Regel Anbieter. Was das kostet, entscheidet der Zweck."
meta_title: "KI-Agent mit Hersteller-SDK: Anbieter oder Betreiber nach dem AI Act?"
meta_description: "Agenten mit dem Mistral Agents SDK oder ähnlichen Werkzeugen bauen: Warum man dadurch Anbieter nach Art. 3 KI-VO wird, wann Art. 25 greift und welche Plattform-Kriterien daraus folgen."
tags:
  - KI & Automation
  - KI-Governance
status: draft
featured: false
timestamp: 2026-11-09T10:00:00+01:00
---

# Ich baue einen KI-Agenten mit dem SDK des Herstellers. Bin ich jetzt Anbieter?

Ich sitze gerade in der Fortbildung zum KI-Beauftragten, und eine Frage hat mich dort länger beschäftigt als gedacht.
Ich baue Agenten mit dem Agents SDK von Mistral. Das Modell kommt von Mistral, die Laufzeit auch, auf Wunsch sogar
das Hosting. Mein Gefühl war: Ich bleibe doch im Framework des Herstellers, also bin ich Betreiber. Anbieter wird man
nach meiner Erinnerung erst, wenn man selbst etwas entwickelt oder ein fremdes System umfangreich ändert.

Das Gefühl war falsch. Hier ist die Herleitung, damit du sie für deine eigenen Agenten nachvollziehen kannst.

## Kurz: Betreiber und Anbieter

Der EU AI Act (auf Deutsch KI-Verordnung, KI-VO) verteilt Pflichten nach Rollen.

- **Betreiber** ist, wer ein KI-System in eigener Verantwortung verwendet (Art. 3 Nr. 4). Typisch: Eine Firma führt
  einen fertigen Chatassistenten ein.
- **Anbieter** ist, wer ein KI-System entwickelt oder entwickeln lässt und es unter eigenem Namen in Verkehr bringt
  oder in Betrieb nimmt (Art. 3 Nr. 3).

Der Haken steckt in „in Betrieb nimmt“. Laut Art. 3 Nr. 11 gehört dazu ausdrücklich auch der Einsatz „for own use“, also
für den Eigengebrauch. Man muss einen Agenten nicht verkaufen, um Anbieter zu sein.

## Drei Ebenen, drei Anbieter

Bei Agenten hilft es, drei Ebenen zu trennen:

| Ebene | Wer ist Anbieter? |
|---|---|
| Das Sprachmodell (z. B. Mistral Large) | der Hersteller |
| Die Agentenplattform mit SDK | der Hersteller |
| **Dein Agent**: Modell plus deine Anweisungen, deine Werkzeuge, deine Konnektoren, dein Zweck | **du** |

Durch Agentenbau wird man nie Anbieter des Modells. Anbieter des Agenten wird man dagegen fast immer. Die Verordnung
hat dafür sogar einen eigenen Begriff, den **nachgelagerten Anbieter** (Art. 3 Nr. 68): Anbieter eines KI-Systems, das
ein KI-Modell einbaut, egal ob das Modell von ihm selbst stammt oder von einem anderen.

## Und das SDK?

Ein SDK (Software Development Kit, also eine Programmierbibliothek) ist Werkzeug, genauso wie Python oder LangChain.
Die Verordnung fragt nicht, mit wessen Bibliothek du baust. Sie fragt, wer das System entwickelt hat und unter wessen
Namen es läuft.

Beim Mistral Agents SDK sieht man das gut. Laut Doku definierst du „its model and instructions, its tools, connectors
and skills, its environment“. Deine Werkzeuge schreibst du als eigene Python-Funktionen. Starten kannst du den Agenten
lokal, auf eigenen Servern oder bei Mistral. Das alles ist Entwicklung. Auch wenn Mistral ihn hostet, wird Mistral
dadurch nicht Anbieter deines Agenten.

Die Verordnung rechnet sogar fest mit diesem Fall. Art. 53 Abs. 1 Buchst. b verpflichtet Modellhersteller, „providers
of AI systems who intend to integrate the general-purpose AI model into their AI systems“ mit Informationen und
Dokumentation zu versorgen. Gemeint sind Leute wie du, die mit dem SDK bauen. Eine Einschränkung gibt es: Für Modelle
unter freier Open-Source-Lizenz entfällt diese Pflicht (Art. 53 Abs. 2), außer bei Modellen mit systemischem Risiko.
Bei offenen Modellen musst du dir die Unterlagen also eher selbst zusammensuchen.

## Woher mein falsches Gefühl kam

Mein Bild vom „umfangreich ändern“ stammt aus Art. 25. Der regelt, wann jemand ein **fremdes, fertiges** System so
verändert, dass er zum Anbieter wird, und er dreht sich um Hochrisiko-Systeme. Mit dem SDK verändere ich aber kein
fremdes System, ich baue ein eigenes. Art. 25 ist deshalb nicht der Prüfweg.

In meinem Kursmaterial hieß es zu Agenten sinngemäß, Betreiber bleibe das Unternehmen. Für eingekaufte, fertige
Agenten stimmt das. Für selbst gebaute greift er zu kurz.

## Wie teuer ist „Anbieter“?

Meistens weniger, als das Wort klingt. Die schweren Pflichten gelten für Hochrisiko-Systeme. Ein Rechercheagent, ein
Assistent für Angebotsentwürfe oder ein Wissensassistent ist das nicht. Dann bleibt vor allem:

- **Art. 50 Abs. 1:** Wer mit deinem Agenten chattet, muss erkennen können, dass es eine KI ist.
- **Art. 50 Abs. 2:** Erzeugte Inhalte maschinenlesbar kennzeichnen, soweit technisch machbar.
- **Art. 4:** KI-Kompetenz der Leute, die damit arbeiten. Das gilt für Betreiber genauso.

Teuer wird es über den Zweck. Bekommt ein allgemeiner Agent eine Aufgabe aus Anhang III, etwa Bewerbungen vorsortieren
oder Risiko und Preis in der Lebens- und Krankenversicherung bewerten, dann greift Art. 25 Abs. 1 Buchst. c: Wer den
Zweck eines Systems so ändert, dass es hochriskant wird, trägt die vollen Anbieterpflichten. Dazu gehören
Risikomanagement, technische Dokumentation, Protokollierung, menschliche Aufsicht, ein Qualitätsmanagementsystem und
die Konformitätsbewertung.

Und wenn du als Dienstleister für einen Kunden baust? Nutzt der Kunde den Agenten unter seinem Namen, ist in der Regel
er der Anbieter, weil er ihn „entwickeln lässt“. Wer welche Dokumentation liefert, gehört dann in den Vertrag.

## Was das für Firmen heißt, die Agenten selbst bauen

Wer eigene Agenten baut, ist mit jedem einzelnen Agenten Anbieter. Jede neue Aufgabe und jede Zweckänderung kann einen
Hochrisiko-Fall auslösen. Das klärt man nicht einmal mit einem Gutachten und legt es ab. Es braucht einen Ablauf, der
bei jedem Agenten wieder läuft.

**Rollenprüfung je Agent.** Vor dem ersten Einsatz und bei jeder Zweckänderung: Wofür ist der Agent da, unter wessen
Namen läuft er, welche Rolle hat die Firma, welche Risikoklasse, fällt der Zweck unter Anhang III? Das Ergebnis kommt
ins Inventar der KI-Systeme.

**ISO/IEC 42001 als Rahmen.** Die Norm für KI-Managementsysteme verlangt genau diese Bausteine: Inventar,
Risiko- und Folgenabschätzung, Zuständigkeiten, Steuerung der Lieferanten, Überwachung und Verbesserung. Eine
Konformitätsbewertung nach dem AI Act ersetzt sie nicht. Für eine Firma, die laufend Anbieter wird, ist sie aber der
naheliegende Rahmen, und falls ein Agent hochriskant wird, hat man das nötige Qualitätsmanagementsystem schon in
Grundzügen.

**Plattformen nach abgedeckten Pflichten auswählen.** Eine Agentenplattform führt Agenten aus. Bei der Auswahl lohnt
die Frage, welche Pflicht sie einem abnimmt:

| Pflicht | Worauf ich bei der Plattform achte |
|---|---|
| Protokollierung (Art. 12) | Laufprotokolle je Sitzung, exportierbar, mit Aufbewahrungsfrist |
| Menschliche Aufsicht (Art. 14) | Freigaben vor Werkzeugaufrufen, Abbruch, Rollenrechte |
| Transparenz (Art. 50) | KI-Hinweis im Dialog, Kennzeichnung erzeugter Inhalte |
| Dokumentation (Art. 11, 53) | Modelldokumentation des Herstellers, versionierte Agentendefinitionen |
| Robustheit und Sicherheit (Art. 15) | Leitplanken, Sandbox, Verwaltung von Zugangsdaten, Tests |
| Datenschutz (DSGVO) | Vertrag zur Auftragsverarbeitung, Liste der Unterauftragnehmer, Datenstandort |

Was die Plattform liefert, muss man nicht selbst bauen. Was sie nicht liefert, bleibt eine Lücke, und die sollte man
kennen, bevor der erste Agent live geht.

Wie ich das für Firmen als offene Vorlage aufbaue, steht im Repo
[kobetriebssystem](https://github.com/enving/kobetriebssystem/blob/main/docs/architektur/anbieterrolle-und-pflichtenabdeckung-2026-11-09.md).

## Mein Fazit

Wer mit einem Hersteller-SDK einen Agenten für einen festen Zweck baut und unter eigenem Namen einsetzt, ist Anbieter.
Das ist im Normalfall kein Drama, solange man den Zweck kennt und Anhang III im Blick behält. Ich prüfe deshalb vor
jedem Agenten: Zweck, Name, Risikoklasse. Und bei der Plattform frage ich nicht nur, was sie kann, sondern auch, welche
Pflichten sie mir abnimmt.

*Das ist meine Einordnung, keine Rechtsberatung. Zitierte Stellen: Art. 3 Nr. 3, 4, 11 und 68, Art. 25, Art. 50,
Art. 53 der Verordnung (EU) 2024/1689.*
