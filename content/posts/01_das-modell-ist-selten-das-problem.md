---
title: "Das Modell ist selten das Problem"
tags:
  - KI & Automation
  - Für Einsteiger
excerpt: "Ein KI-Assistent wird eingeführt, der Pilot läuft gut — und ein halbes Jahr später hat sich an der täglichen Arbeit wenig geändert. Dann beginnt die Suche nach dem besseren Modell. Warum sie selten irgendwohin führt."
status: draft
featured: false
meta_title: "Warum KI-Assistenten in Organisationen enttäuschen"
meta_description: "Nicht das Modell ist das Problem, sondern die fehlende Kontextschicht. Warum KI-Piloten gut laufen und trotzdem nichts an der Arbeit ändern."
---

*Warum KI-Assistenten in Organisationen enttäuschen — und woran es tatsächlich liegt*

Der Ablauf ist in den meisten Organisationen derselbe. Ein KI-Assistent wird eingeführt, oft nach einem sorgfältigen Anbietervergleich. Ein Pilot läuft, die Rückmeldungen sind freundlich, einzelne Leute sind begeistert. Ein halbes Jahr später hat sich an der täglichen Arbeit erstaunlich wenig geändert.

Dann beginnt die Suche nach dem besseren Modell.

Das ist nachvollziehbar und führt selten irgendwohin. Die verfügbaren Assistenzsysteme unterscheiden sich funktional nur noch im Detail. Wer wechselt, bekommt dieselbe Erfahrung mit einer anderen Oberfläche — und verliert dabei die Gewöhnung, die schon aufgebaut war.

Was fehlt, liegt woanders. Das System kennt die Organisation nicht. Es hat keinen Zugriff auf die Quellen, die zählen. Und die Menschen, die es benutzen sollen, haben nie erfahren, wie man ihm beides mitgibt.

## Drei Ebenen

Ein KI-System besteht immer aus drei Ebenen. Die Unterscheidung klingt zunächst akademisch, sie ist aber der einzige Weg, die Diskussion zu sortieren — weil in einem typischen Gespräch über KI alle drei Ebenen gleichzeitig gemeint sind, ohne dass jemand sagt, welche.

Die **Anwendung** ist die Oberfläche, die bedient wird. Sie stellt Eingabe, Chatverlauf, Benutzerverwaltung, Rollen und Rechte, Konfiguration und Protokollierung bereit, integriert die Anmeldung an das vorhandene Identitätsmanagement und regelt den Zugang zu allem Weiteren.

Die **Intelligenz** ist das Modell dahinter. Sprachmodelle unterscheiden sich in Qualität, Geschwindigkeit, Kosten, Fähigkeiten, Spezialisierung, Reifegrad der Dokumentation und in ihrer Bereitstellungsform — proprietär oder offen, als Dienst bezogen oder selbst betrieben.

Die **Werkzeuge** sind das, was das Modell benutzen kann: Websuche, Wissensbestände, Vektordatenbank, Dokumentenextraktion, Konnektoren in vorhandene Systeme, Code-Ausführung, agentische Fähigkeiten.

Der Punkt, auf den es ankommt: **Jede dieser Ebenen lässt sich einkaufen oder selbst betreiben, und jede Kombination verschiebt drei Dinge gleichzeitig — das Risiko, die Verantwortung, und das, was am Ende überhaupt möglich ist.** Ohne diesen Satz ist das Modell nur eine Aufzählung.

Wer alles einkauft, bekommt schnell etwas Funktionierendes und übernimmt die Verarbeitungskette des Anbieters, einschließlich seiner Unterauftragsverarbeiter. Wer alles selbst betreibt, behält die Kontrolle und trägt den Betrieb — samt Sicherheits- und Nachweispflichten, die vorher niemand hatte. Die meisten tragfähigen Antworten liegen dazwischen und sehen je nach Anwendungsfall anders aus.

## Werkzeuge sind nicht Funktionen

Eine Abgrenzung, die sich in Diskussionen als nützlich erwiesen hat: Werkzeuge sind das, was dem Sprachmodell **zur Laufzeit** zur Verfügung steht. Funktionen sind das, was **Menschen** in der Oberfläche anklicken.

Der Unterschied ist nicht kosmetisch. Ein Exportknopf ist eine Funktion. Eine Websuche, die das Modell selbst auslöst, weil es merkt, dass ihm etwas fehlt, ist ein Werkzeug. Das eine erweitert die Bedienung, das andere erweitert, was das System selbstständig herausfinden kann.

In Funktionslisten von Anbietern stehen beide unsortiert nebeneinander. Beim Vergleich zweier Systeme lohnt es deshalb, jede Zeile einmal danach zu sortieren. Übrig bleibt eine deutlich kürzere und deutlich aussagekräftigere Liste.

Nebenbei erklärt die Unterscheidung, warum Websuche und Webabruf besondere Aufmerksamkeit verdienen: Diese Werkzeuge greifen zwangsläufig nach außen. Wird die Websuche aktiviert, sendet das System aus der Anfrage abgeleitete Suchbegriffe an einen Drittanbieter. Ab dort gelten dessen Bedingungen. Das ist beherrschbar, aber es ist eine Entscheidung — und in vielen Organisationen ist sie nie bewusst getroffen worden.

## Die Kontextschicht

Wissen und Kontext sind der zentrale Erfolgsfaktor und der am besten skalierbare Hebel für bessere Ausgaben. Das ist die eine Stelle, an der sich Aufwand am zuverlässigsten auszahlt.

Es hilft, sich klarzumachen, warum. Ein Sprachmodell, das eine mittelmäßige Antwort gibt, verhält sich meistens wie eine neue Kollegin in der zweiten Woche: fachlich nicht dumm, aber ohne Kenntnis davon, wie hier gearbeitet wird, welche Vorlagen gelten, was schon entschieden wurde und wo das relevante Material liegt. Unbekanntes oder implizit verteiltes Wissen ist bei natürlichen Intelligenzen die häufigste Ursache mangelnder Qualität. Bei künstlichen ist es nicht anders.

Daraus folgt etwas Unbequemes: Der Aufbau der Kontextschicht ist nicht in erster Linie eine technische Aufgabe, sondern eine fachlich-inhaltliche. Man kann Komponenten einkaufen — Extraktion, Embedding-Modelle, Vektordatenbanken — und nimmt sich damit Betriebsaufwand ab. Die Frage, welches Wissen überhaupt hinein gehört, in welcher Form, mit welcher Aktualität und für wen, kauft man nicht mit ein.

## Wissensordner und Wissensdienste

In der Praxis zerfällt der Wissensaufbau in zwei Teile, die man auseinanderhalten sollte, weil sie unterschiedlich verantwortet werden.

**Wissensordner** bringen die meisten Systeme mit: Ein Nutzer legt eine Sammlung an, lädt Dokumente hoch, das System durchsucht sie. Für überschaubare Bestände ist das ausreichend und der schnellste Weg zu spürbarem Nutzen. Nutzende sollten nach einer gezielten Schulung in der Lage sein, solche Ordner selbst anzulegen und zu pflegen. Gerade dort, wo kein Konnektor in das Dokumentenmanagement existiert, ist das ein tragfähiger Kompromiss.

**Wissensdienste** sind etwas anderes. Sie erfassen einen abgegrenzten Quellenbestand automatisiert, bereiten Inhalte und Metadaten auf und stellen sie durchsuchbar und bei Bedarf zitierfähig bereit. Typische Kandidaten sind Bestände, die laufend nachwachsen und für viele Rollen gleichzeitig relevant sind: Rechts- und Gesetzgebungsmonitoring, Normen- und Regelwerkssammlungen, Gremienunterlagen, fachliche Publikationsreihen.

Der entscheidende Unterschied liegt nicht in der Größe, sondern in der Zuständigkeit. Ein Wissensordner gehört den Leuten, die ihn benutzen. Ein Wissensdienst gehört der Organisation, braucht Pflege, Qualitätssicherung und eine benannte Verantwortung — und wird sinnvollerweise produktunabhängig angebunden, etwa über MCP. Dann ist er vom gewählten KI-System entkoppelt und überlebt einen Anbieterwechsel.

Diese Zweiteilung ist eine der praktischsten Festlegungen, die man früh treffen kann. Sie verhindert zwei verbreitete Fehler: dass zentrale Stellen jeden kleinen Wissensbedarf selbst bedienen sollen, und dass umfangreiche, geteilte Bestände in privaten Ordnern verstreuen.

## Warum die Nutzenden nichts falsch machen

In Pilotprojekten sieht man fast immer dasselbe Muster: Der Assistent wird überwiegend als bessere Suchmaschine verwendet. Frage rein, Antwort raus, weiter.

Das wird gern als mangelnde Kompetenz gedeutet — die Leute hätten das Potenzial nicht verstanden, es brauche mehr Schulung zu Prompt-Techniken.

Ich halte das für die falsche Diagnose. Wer ein System bekommt, das seine Organisation nicht kennt, keinen Zugriff auf die relevanten Quellen hat und keine Vorlagen kennt, benutzt es vernünftigerweise für das, was es ohne all das kann: allgemeine Fragen beantworten. Das ist keine Fehlbedienung, sondern eine zutreffende Einschätzung des Werkzeugs.

Und deshalb löst zusätzliche Schulung zu Prompt-Techniken das Problem nicht. Man kann Menschen nicht beibringen, Kontext zu nutzen, den es nicht gibt.

Die Reihenfolge ist umgekehrt: erst dem System den Kontext geben, die Werkzeuge freischalten und die Quellen anbinden — dann zeigen, was damit geht. Wer so vorgeht, braucht deutlich weniger Überzeugungsarbeit, weil der Nutzen sichtbar ist statt behauptet.

## Was das für die Reihenfolge bedeutet

Der häufigste Fehler bei der Einführung ist nicht die Produktwahl, sondern deren Zeitpunkt.

Es beginnt meist mit einem Produktvergleich. Anbieter werden eingeladen, Demos geschaut, Funktionslisten verglichen. Das fühlt sich nach Fortschritt an, weil es konkret ist und sichtbar Arbeit macht. Nur vergleicht man ohne Anforderungsprofil im Wesentlichen Funktionen, die alle Anbieter haben. Der Vergleich läuft dann über Oberfläche, Preis und Sympathie, und die entscheidenden Fragen kommen auf, wenn der Vertrag steht.

Diese Fragen sind keine Produktfragen, sondern Fragen an die eigene Organisation:

- Welche Daten dürfen das Haus in welcher Form verlassen — und wer hat das je entschieden?
- Welche Quellen müssen angebunden sein, damit das System überhaupt nützlich ist?
- Wer darf welche Funktion und welches Werkzeug nutzen, und wer gibt das frei?
- Für welche Daten verarbeitet die Organisation eigentlich im Auftrag Dritter?
- Was passiert bei einem Anbieterwechsel mit dem, was aufgebaut wurde?

Ein technisch-organisatorisches Anforderungsprofil zu erheben, ist Standardvorgehen und in wenigen Wochen machbar. Danach ist der Produktvergleich kurz und klar. Vorher ist er Beschäftigung.

Umfragen aus einem Piloten ersetzen dieses Profil übrigens nicht. Sie geben Bedarfe aus Nutzersicht wieder, und das ist wertvoll — aber sie sagen nichts darüber, welche Verarbeitung zulässig ist und welches herausgenommene Risiko welche Nutzung freigäbe.

## Zwei Korrekturen zum Schluss

**Selbsthosting ist kein Compliance-Automatismus.** Es kann Übermittlungs- und Souveränitätsrisiken senken, das ist real. Zweckbindung und Rechtsgrundlage bleiben davon unberührt. Gleichzeitig wachsen Betriebs-, Sicherheits- und Nachweispflichten, und die eigene Rolle nach der KI-Verordnung kann sich vom Nutzenden zum Bereitsteller verschieben. Der Eigenbetrieb leistungsfähiger Modelle bindet zudem GPU-Kapazitäten, die in Europa knapp und im Verhältnis zu API-Preisen teuer sind. Ein selbst betriebenes Modell ist deshalb nicht allein durch seinen Verarbeitungsort die einfachere Lösung.

**Zwei Systeme parallel zu betreiben, hat einen Preis, der selten eingerechnet wird.** Es kann sinnvoll sein — ein etabliertes System für den Alltag, ein souveräneres für die Fälle, die eine strengere Verarbeitungskette brauchen. Aber Kompetenz, Gewohnheiten und Kontextaufbau verteilen sich dann ungleich auf beide. Diese Adoptions-Drift ist schwer rückgängig zu machen. Wer parallel betreibt, braucht einfache Regeln nach Datenklasse und Anwendungsfall, und dort, wo eine manuelle Auswahl nicht trägt, ein technisch erzwungenes Routing.

## Der Kern

Der Vorteil liegt selten im Modell. Er liegt in der Kontextschicht, in den Werkzeugen, in der Frage, wie viel davon tatsächlich genutzt werden darf — und darin, ob den Menschen, die damit arbeiten sollen, für ihre eigenen Aufgaben gezeigt wurde, was damit geht.

Das ist die schlechtere Nachricht, weil es nicht durch eine Bestellung zu lösen ist. Es ist aber auch die bessere, weil es in der eigenen Hand liegt.
