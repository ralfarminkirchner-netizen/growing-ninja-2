extends Node
## Globaler Spielstand (Autoload "GameManager").
##
## Hier später erweitern:
##  - Achtsamkeits-Punkte / "Ruhe-Energie" für Mini-Games
##  - Ethik-Quest-Flags (welche Quests erledigt sind)
##  - Spielstand speichern/laden (FileAccess + JSON)
##  - Übergang zur Zelda-like Overworld (aktuelle Karte, Spawn-Punkt)

signal star_collected(count: int)

var stars := 0
var total_stars := 0


func reset() -> void:
	stars = 0


func add_star() -> void:
	stars += 1
	star_collected.emit(stars)
