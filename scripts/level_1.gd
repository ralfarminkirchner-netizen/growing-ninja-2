extends Node2D
## Level 1 – "Sternennacht".
## Die ganze Welt wird aus der ASCII-Karte unten gebaut:
## KARTE BEARBEITEN = LEVEL BEARBEITEN. Zeichen:
##
##   #  Boden (füllt automatisch nach unten auf)
##   -  Wolken-Plattform (von unten durchspringbar)
##   m  Pilz-Plattform (von unten durchspringbar)
##   c  Kristallblock (fest, als Treppenstufe)
##   *  Weisheits-Stern
##   C  Checkpoint-Kristall
##   P  Spieler-Startpunkt
##   T  Ziel-Tor
##
## Hier später: weitere Level als level_2.gd/.tscn kopieren und neue
## Karte zeichnen – oder Achtsamkeits-Mini-Game-Zonen als neues Zeichen
## (z. B. "A") einführen und unten im match-Block behandeln.

const StarScene := preload("res://scenes/star.tscn")
const PortalScene := preload("res://scenes/portal.tscn")
const CheckpointScene := preload("res://scenes/checkpoint.tscn")

const TILE_SIZE := 32
const FILL_BOTTOM_ROW := 15
const KILL_Y := 620.0  # darunter: sanfter Respawn am Checkpoint
const WIN_SCENE := "res://scenes/win_screen.tscn"

const MAP_ROWS := [
	"",
	"",
	"",
	"",
	"",
	"",
	"                 *",
	"                ---                                                       *",
	"            *              *                                              --",
	"           ---            ---                          *              *",
	"       *                                 *            ---             --",
	"      ---              c                ####",
	"  P            --   * cc      C  --  mm      *   --  m    C *    mm          *  T",
	"##############    ##############    ####    ####    ############    ################",
	"",
	"",
]

# Atlas-Koordinaten im TileSet (assets/tileset.tres)
const T_GROUND := Vector2i(0, 0)
const T_INNER := Vector2i(1, 0)
const T_CLOUD := Vector2i(2, 0)
const T_MUSHROOM := Vector2i(3, 0)
const T_CRYSTAL := Vector2i(4, 0)

var respawn_point := Vector2(80, 380)
var map_width := 0

@onready var ground: TileMapLayer = $Ground
@onready var player: CharacterBody2D = $Player
@onready var stars_node: Node2D = $Stars
@onready var checkpoints_node: Node2D = $Checkpoints
@onready var music: AudioStreamPlayer = $Music


func _ready() -> void:
	GameManager.reset()
	_build_from_map()
	_setup_camera_limits()
	music.finished.connect(music.play)  # Musik loopt endlos


func _physics_process(_delta: float) -> void:
	if player.global_position.y > KILL_Y:
		_respawn()


func _build_from_map() -> void:
	var total := 0
	for row in range(MAP_ROWS.size()):
		var line: String = MAP_ROWS[row]
		map_width = maxi(map_width, line.length())
		for col in range(line.length()):
			var ch := line[col]
			var cell := Vector2i(col, row)
			var center := Vector2(col * TILE_SIZE + 16, row * TILE_SIZE + 16)
			var foot := Vector2(col * TILE_SIZE + 16, (row + 1) * TILE_SIZE)
			match ch:
				"#":
					ground.set_cell(cell, 0, T_GROUND)
					_fill_below(col, row)
				"c":
					ground.set_cell(cell, 0, T_CRYSTAL)
				"-":
					ground.set_cell(cell, 0, T_CLOUD)
				"m":
					ground.set_cell(cell, 0, T_MUSHROOM)
				"*":
					var star := StarScene.instantiate()
					star.position = center
					stars_node.add_child(star)
					total += 1
				"C":
					var cp := CheckpointScene.instantiate()
					cp.position = foot
					cp.reached.connect(_on_checkpoint_reached)
					checkpoints_node.add_child(cp)
				"P":
					player.position = foot - Vector2(0, 16)
					respawn_point = player.position
				"T":
					var portal := PortalScene.instantiate()
					portal.position = foot
					portal.player_entered.connect(_on_portal_entered)
					add_child(portal)
	GameManager.total_stars = total


func _fill_below(col: int, row: int) -> void:
	# Unter jeder Boden-Oberkante automatisch "Erde" bis zum Kartenboden
	for r in range(row + 1, FILL_BOTTOM_ROW + 1):
		if _map_char(col, r) == " ":
			ground.set_cell(Vector2i(col, r), 0, T_INNER)


func _map_char(col: int, row: int) -> String:
	if row >= MAP_ROWS.size():
		return " "
	var line: String = MAP_ROWS[row]
	if col >= line.length():
		return " "
	return line[col]


func _setup_camera_limits() -> void:
	var cam: Camera2D = player.get_node("Camera2D")
	cam.limit_left = 0
	cam.limit_right = map_width * TILE_SIZE
	cam.limit_top = -150
	cam.limit_bottom = (FILL_BOTTOM_ROW + 1) * TILE_SIZE
	cam.reset_smoothing()


func _respawn() -> void:
	player.respawn(respawn_point)


func _on_checkpoint_reached(pos: Vector2) -> void:
	respawn_point = pos + Vector2(0, -16)


func _on_portal_entered() -> void:
	# Hier später: statt Win-Screen → Übergang in die Zelda-like Overworld
	get_tree().change_scene_to_file.call_deferred(WIN_SCENE)
