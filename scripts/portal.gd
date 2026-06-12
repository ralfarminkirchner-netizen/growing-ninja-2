extends Area2D
## Das leuchtende Ziel-Tor am Level-Ende.
##
## Hier später: statt zum Win-Screen direkt in die Zelda-like Overworld
## wechseln (z. B. get_tree().change_scene_to_file("res://scenes/overworld.tscn"))
## oder einen Ethik-Quest-Dialog zeigen, bevor es weitergeht.

signal player_entered

var used := false


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(_body: Node2D) -> void:
	if used:
		return
	used = true
	player_entered.emit()
