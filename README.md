# Growing Ninja – First Steps 🥷✨

Ein kinderfreundlicher Pixel-Art-Platformer in **Godot 4.3+ (GDScript)**.
Springen, Weisheits-Sterne sammeln, das leuchtende Tor erreichen – keine
Gegner, keine Gewalt, nur eine magische Sternennacht.

Gedacht als **saubere, erweiterbare Basis** für ein späteres Zelda-like
mit Achtsamkeits- und Ethik-Lerninhalten.

---

## 1. Öffnen & Spielen

1. [Godot 4.3 oder neuer](https://godotengine.org/download) installieren (Standard-Version, **nicht** .NET).
2. Godot starten → **Importieren** → diesen Ordner auswählen (`project.godot`) → **Importieren & Bearbeiten**.
3. Beim ersten Öffnen importiert Godot kurz alle Assets (wenige Sekunden).
4. **F5** drücken (oder ▶ oben rechts) → Spiel startet mit dem Titelbildschirm.

> Liegt der Ordner noch in iCloud Drive: am besten erst auf die lokale
> Platte ziehen (z. B. nach `~/Spiele/Growing-Ninja-2`), damit Godot
> nicht durch iCloud-Sync gebremst wird.

## 2. Steuerung

| Taste | Aktion |
|---|---|
| **← →** oder **A / D** | Laufen |
| **Leertaste / W / ↑** | Springen |
| **Leertaste in der Luft** | Doppelsprung („Mut-Boost") |
| **Esc** | Pause-Menü |

## 3. Spielmechanik

- **12 Weisheits-Sterne** sammeln (Score oben links, „Super!"-Pop-up + Partikel + Klang).
- **2 Checkpoint-Kristalle**: Wer in einen Abgrund fällt, erscheint sanft am letzten Checkpoint wieder – kein Game Over, keine Strafe.
- **Leuchtendes Tor** am Level-Ende → „Gut gemacht! Du hast Weisheit gesammelt!" mit Konfetti.
- Wolken- und Pilz-Plattformen sind **von unten durchspringbar**.
- Kamera folgt weich, Sternenhimmel + Mond mit Parallax, Glühwürmchen schweben durchs Level.

## 4. Projektstruktur

```
project.godot           Hauptkonfiguration (Input-Map, Pixel-Perfect 1280×720)
scenes/
  start_screen.tscn     Titelbildschirm („Drücke LEERTASTE")
  level_1.tscn          Nacht-Level (wird aus ASCII-Karte gebaut!)
  player.tscn           Ninja (CharacterBody2D + Sprite2D + AnimationPlayer)
  star.tscn             Weisheits-Stern (Area2D, pulsiert)
  portal.tscn           Leuchtendes Ziel-Tor
  checkpoint.tscn       Checkpoint-Kristall
  ui_hud.tscn           Stern-Zähler
  pause_menu.tscn       Esc-Menü
  win_screen.tscn       Sieg + Konfetti
scripts/                Ein Skript pro Szene + game_manager.gd (Autoload)
assets/
  sprites/              Platzhalter-Pixel-Art (PNG)
  audio/                Platzhalter-Sounds (WAV) → siehe audio/QUELLEN.md
  tileset.tres          TileSet (Boden, Wolke, Pilz, Kristall)
dev_tools/              Python-Generatoren für die Platzhalter (von Godot ignoriert)
```

## 5. Level bearbeiten – die ASCII-Karte ⭐

Das komplette Level steckt in **`scripts/level_1.gd`** in der Konstante
`MAP_ROWS` – eine Zeichnung aus Textzeilen. Zeichen ändern = Level ändern:

```
#  Boden          -  Wolke (durchspringbar)   m  Pilz (durchspringbar)
c  Kristallblock  *  Weisheits-Stern          C  Checkpoint
P  Spieler-Start  T  Ziel-Tor
```

Einfach Zeilen verlängern, Sterne verschieben, neue Plattformen malen –
beim nächsten Start wird alles automatisch gebaut (inkl. Stern-Gesamtzahl).

## 6. Wo später die Lerninhalte hinkommen

Im Code sind die Andockstellen mit Kommentaren markiert – einfach nach
**„Hier später"** suchen (in Godot: `Strg/Cmd+Shift+F` → „Hier später"):

| Datei | Andockstelle |
|---|---|
| `scripts/player.gd` | Achtsamkeits-Mini-Game (z. B. Atem-Taste lädt Mut-Boost auf) |
| `scripts/star.gd` | Ethik-Quest-Dialog bei besonderen Sternen |
| `scripts/checkpoint.gd` | Achtsamkeits-Moment („Atme einmal tief ein …") |
| `scripts/portal.gd` + `level_1.gd` | Übergang zur Zelda-like Overworld statt Win-Screen |
| `scripts/game_manager.gd` | Achtsamkeits-Punkte, Quest-Flags, Speichern/Laden |
| `scripts/win_screen.gd` | Reflexions-Frage nach dem Level |
| `scripts/level_1.gd` | Neues Karten-Zeichen (z. B. `A`) für Mini-Game-Zonen |

**Richtung Zelda-like:** eine neue Szene `scenes/overworld.tscn` mit
Top-Down-Player (eigene `CharacterBody2D` ohne Schwerkraft) anlegen und im
`portal.gd`-Handler dorthin wechseln. `GameManager` trägt den Spielstand
über Szenenwechsel hinweg (ist Autoload).

## 7. Bessere Grafik & Sound einsetzen

**Sprites** (alle in `assets/sprites/`, einfach gleichnamig überschreiben):

- `ninja_sheet.png` – 6×5-Raster à 32×32 px. Reihen: Idle (4), Run (6), Jump (2), Fall (2), Land (3). Gleiche Anordnung beibehalten, dann passen die Animationen sofort.
- `tiles.png` – 5 Tiles à 32×32 nebeneinander: Boden-oben, Boden-innen, Wolke, Pilz, Kristall.
- `star.png` (16×16), `portal.png` (48×64), `checkpoint.png` (32×32), `bg_far.png` (640×360), `bg_near.png` (640×480).

**Audio:** siehe [`assets/audio/QUELLEN.md`](assets/audio/QUELLEN.md) (Kenney Audio, freesound.org).

**Schrift:** Für echten Pixel-Look eine Pixel-Schrift (z. B. „Press Start 2P", OFL-Lizenz) als `.ttf` importieren und in den Labels als Theme-Override setzen.

### Kenney-Tileset importieren (empfohlener nächster Schritt)

1. [kenney.nl/assets/pixel-platformer](https://kenney.nl/assets/pixel-platformer) laden (CC0, kostenlos).
2. Das Tilesheet-PNG nach `assets/sprites/` kopieren.
3. `assets/tileset.tres` in Godot öffnen → im TileSet-Editor die neue Textur als Atlas-Quelle hinzufügen (Tile-Größe 32×32 bzw. bei 16px-Tiles auf 16 stellen und in `level_1.gd` `TILE_SIZE` anpassen).
4. Den neuen Tiles **Physik-Polygone** geben (TileSet-Editor → Physik-Layer 0) – bei Plattformen „One Way" anhaken.
5. In `level_1.gd` die Atlas-Koordinaten-Konstanten (`T_GROUND` …) auf die neuen Tiles zeigen lassen.

## 8. Technik-Notizen

- Auflösung 1280×720, Stretch-Mode `viewport` mit Integer-Scaling, Texturfilter „Nearest" → scharfe Pixel.
- Kamera: `Camera2D` im Player mit Smoothing, Zoom 2 (Welt wird in 640×360 gerendert → kräftiger Pixel-Look).
- Renderer: GL Compatibility (läuft auch auf schwächeren Geräten, später Web-Export möglich).
- `GameManager` ist als Autoload registriert (Projekt­einstellungen → Autoload).
- Die Platzhalter-Generatoren in `dev_tools/` brauchen Python 3 + Pillow (`python3 dev_tools/make_sprites.py`).

Viel Spaß beim Wachsen! 🌱
