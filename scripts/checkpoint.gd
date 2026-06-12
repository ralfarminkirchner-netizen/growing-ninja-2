extends Area2D
## Checkpoint-Kristall: Wer hier vorbeikommt, startet nach einem Sturz
## sanft an dieser Stelle neu.
##
## Hier später: Achtsamkeits-Moment einbauen –
## beim Aktivieren ein kurzer Atem-Hinweis ("Atme einmal tief ein ...")
## als ruhige Texteinblendung.

signal reached(pos: Vector2)

var active := false


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(_body: Node2D) -> void:
	if active:
		return
	active = true
	reached.emit(global_position)
	modulate = Color(1.3, 1.3, 1.5)  # Kristall leuchtet auf
	$Particles.restart()
	$Sound.play()
