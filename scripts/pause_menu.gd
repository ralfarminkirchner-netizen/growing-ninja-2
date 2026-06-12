extends CanvasLayer
## Pause-Menü (Esc). Läuft mit process_mode = ALWAYS,
## damit die Buttons auch bei pausiertem Spielbaum funktionieren.

@onready var continue_button: Button = $Center/Panel/Margin/Box/ContinueButton
@onready var restart_button: Button = $Center/Panel/Margin/Box/RestartButton
@onready var quit_button: Button = $Center/Panel/Margin/Box/QuitButton


func _ready() -> void:
	continue_button.pressed.connect(_close)
	restart_button.pressed.connect(_restart)
	quit_button.pressed.connect(_to_title)


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		_toggle()


func _toggle() -> void:
	visible = not visible
	get_tree().paused = visible


func _close() -> void:
	visible = false
	get_tree().paused = false


func _restart() -> void:
	_close()
	get_tree().reload_current_scene()


func _to_title() -> void:
	_close()
	get_tree().change_scene_to_file("res://scenes/start_screen.tscn")
