extends Control
## Titelbildschirm: "Drücke LEERTASTE zum Starten".

@onready var hint: Label = $Center/Box/Hint


func _process(_delta: float) -> void:
	# Sanftes Blinken des Hinweis-Textes
	hint.modulate.a = 0.55 + 0.45 * sin(Time.get_ticks_msec() / 300.0)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("jump"):
		get_tree().change_scene_to_file("res://scenes/level_1.tscn")
