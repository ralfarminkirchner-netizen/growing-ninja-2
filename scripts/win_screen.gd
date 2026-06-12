extends Control
## Win-Screen: "Gut gemacht! Du hast Weisheit gesammelt!" + Konfetti.
##
## Hier später: Übergang in die Overworld oder eine kleine
## Reflexions-Frage ("Was war heute dein mutigster Sprung?").

@onready var stars_label: Label = $Center/Box/StarsLabel
@onready var retry_button: Button = $Center/Box/RetryButton
@onready var title_button: Button = $Center/Box/TitleButton


func _ready() -> void:
	stars_label.text = "%d von %d Weisheits-Sternen gesammelt" % [
		GameManager.stars, GameManager.total_stars
	]
	retry_button.pressed.connect(
		func(): get_tree().change_scene_to_file("res://scenes/level_1.tscn")
	)
	title_button.pressed.connect(
		func(): get_tree().change_scene_to_file("res://scenes/start_screen.tscn")
	)
