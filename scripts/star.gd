extends Area2D
## Weisheits-Stern: einsammeln gibt Punkte, Funkel-Partikel,
## einen freundlichen Klang und ein "Super!"-Pop-up.
##
## Hier später: Ethik-Quest-Dialog einbauen –
## besondere Sterne könnten eine kleine Frage oder einen guten Gedanken
## zeigen (z. B. als Dialog-Box, bevor der Stern zählt).

const PRAISE := ["Super!", "Toll!", "Klasse!", "Wunderbar!", "Magisch!"]

var collected := false


func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(_body: Node2D) -> void:
	if collected:
		return
	collected = true
	GameManager.add_star()
	$Sprite2D.visible = false
	$CollisionShape2D.set_deferred("disabled", true)
	$Particles.restart()
	$Sound.play()
	_show_praise()
	await get_tree().create_timer(1.2).timeout
	queue_free()


func _show_praise() -> void:
	var label := Label.new()
	label.text = PRAISE.pick_random()
	label.add_theme_font_size_override("font_size", 14)
	label.add_theme_color_override("font_color", Color(1.0, 0.95, 0.7))
	label.add_theme_color_override("font_outline_color", Color(0.2, 0.1, 0.3))
	label.add_theme_constant_override("outline_size", 4)
	label.z_index = 50
	label.position = global_position + Vector2(-24, -34)
	get_tree().current_scene.add_child(label)
	var tween := label.create_tween()
	tween.tween_property(label, "position:y", label.position.y - 24.0, 0.8)
	tween.parallel().tween_property(label, "modulate:a", 0.0, 0.8).set_delay(0.3)
	tween.tween_callback(label.queue_free)
