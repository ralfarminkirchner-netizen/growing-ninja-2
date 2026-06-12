extends CanvasLayer
## Einfaches HUD: zeigt die gesammelten Weisheits-Sterne.
##
## Hier später: Anzeige für Achtsamkeits-Punkte / Quest-Hinweise ergänzen.

@onready var label: Label = $Margin/Box/ScoreLabel
@onready var icon: TextureRect = $Margin/Box/Icon


func _ready() -> void:
	GameManager.star_collected.connect(_on_star_collected)
	# Einen Frame warten, bis das Level die Karte gebaut und total_stars gesetzt hat.
	await get_tree().process_frame
	_refresh()


func _on_star_collected(_count: int) -> void:
	_refresh()
	# Kleiner Freuden-Huepfer des Stern-Icons
	icon.pivot_offset = icon.size / 2.0
	var tween := create_tween()
	tween.tween_property(icon, "scale", Vector2(1.35, 1.35), 0.08)
	tween.tween_property(icon, "scale", Vector2.ONE, 0.15)


func _refresh() -> void:
	label.text = "%d / %d" % [GameManager.stars, GameManager.total_stars]
