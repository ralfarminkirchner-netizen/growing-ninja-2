extends CharacterBody2D
## Der kleine Growing Ninja: laufen, springen, Doppelsprung ("Mut-Boost").
##
## Hier später: Achtsamkeits-Mini-Game einbauen –
## z. B. eine Atem-Taste, die gedrückt gehalten den Mut-Boost wieder auflädt,
## oder ein "Ruhe-Modus", in dem die Welt langsamer und leuchtender wird.

const SPEED := 160.0
const ACCELERATION := 1400.0
const FRICTION := 1600.0
const JUMP_VELOCITY := -360.0
const DOUBLE_JUMP_VELOCITY := -320.0  # der "Mut-Boost" in der Luft
const GRAVITY := 900.0
const MAX_FALL_SPEED := 420.0
const COYOTE_TIME := 0.12  # kleine Gnadenfrist nach Plattform-Kante

var can_double_jump := true
var coyote_timer := 0.0
var control_enabled := true
var land_timer := 0.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var anim: AnimationPlayer = $AnimationPlayer
@onready var camera: Camera2D = $Camera2D
@onready var jump_particles: CPUParticles2D = $JumpParticles
@onready var land_particles: CPUParticles2D = $LandParticles
@onready var jump_sound: AudioStreamPlayer2D = $JumpSound


func _physics_process(delta: float) -> void:
	var was_on_floor := is_on_floor()

	# Schwerkraft (sanft gedeckelt, damit Fallen nie hektisch wirkt)
	if not is_on_floor():
		velocity.y = minf(velocity.y + GRAVITY * delta, MAX_FALL_SPEED)
		coyote_timer = maxf(coyote_timer - delta, 0.0)

	# Laufen
	var direction := Input.get_axis("move_left", "move_right") if control_enabled else 0.0
	if direction != 0.0:
		velocity.x = move_toward(velocity.x, direction * SPEED, ACCELERATION * delta)
		sprite.flip_h = direction < 0.0
	else:
		velocity.x = move_toward(velocity.x, 0.0, FRICTION * delta)

	# Springen + Mut-Boost (Doppelsprung)
	if control_enabled and Input.is_action_just_pressed("jump"):
		if is_on_floor() or coyote_timer > 0.0:
			_do_jump(JUMP_VELOCITY)
		elif can_double_jump:
			can_double_jump = false
			_do_jump(DOUBLE_JUMP_VELOCITY)

	move_and_slide()

	if is_on_floor():
		coyote_timer = COYOTE_TIME
		can_double_jump = true
		if not was_on_floor:
			_on_landed()

	land_timer = maxf(land_timer - delta, 0.0)
	_update_animation()


func _do_jump(strength: float) -> void:
	velocity.y = strength
	coyote_timer = 0.0
	jump_particles.restart()
	jump_sound.play()


func _on_landed() -> void:
	land_timer = 0.22
	land_particles.restart()  # kleine Staubwolke


func _update_animation() -> void:
	if not is_on_floor():
		anim.play("jump" if velocity.y < 0.0 else "fall")
	elif land_timer > 0.0 and absf(velocity.x) < 10.0:
		anim.play("land")
	elif absf(velocity.x) > 10.0:
		anim.play("run")
	else:
		anim.play("idle")


func respawn(pos: Vector2) -> void:
	## Sanfter Respawn am letzten Checkpoint – kein Game Over, keine Strafe.
	velocity = Vector2.ZERO
	global_position = pos
	can_double_jump = true
	camera.reset_smoothing()
	modulate.a = 0.0
	var tween := create_tween()
	tween.tween_property(self, "modulate:a", 1.0, 0.6)
