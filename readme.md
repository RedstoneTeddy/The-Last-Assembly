# The Last Assembly

A **roguelite tower defense game** built in Python with Pygame. You build and upgrade towers, manage a shop economy, hire specialists, survive enemy waves, and push through increasingly difficult runs across a selection of handcrafted maps.

## Overview

The Last Assembly combines classic tower-defense play with roguelite progression. Each run begins with a map selection and difficulty choice, followed by a shop phase where you buy towers, specialists, mods, zones, and events. Once the round starts, enemies spawn along a defined path and your defenses must hold the line to protect your base.

The game loop is designed around short, replayable runs where every run can evolve differently based on map, difficulty, the random shop offers and the randomly generated waves.

## Features

### Tower defense loop

- Multiple tower types (11 towers) with different damage profiles and roles.
- Map-based placement and path management.
- Enemy waves with scaling difficulty.
- Base health and economy management.

### Roguelite progression

- Difficulty selection influences run pressure.
- Shop offers are random and and you need to adopt to them.
- Playing games unlocks new towers and specialists (see Collection-Menu for details).

### Deep build customization

- Towers can receive mods to improve stats, effects, or special behavior.
- Zones provide battlefield modifiers and strategic bonuses.
- Specialists add non-standard support layers to a run.
- Events create temporary buffs for act as an emergency mechanic to help you survive a run.

## Installation

This project uses Python and a small set of dependencies.

1. Clone the repository.
2. Open a terminal in the project root.
3. Create and activate a virtual environment if desired.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

### Requirements

The project currently depends on:

- pygame-ce
- numpy
- matplotlib (only for balance tuning scripts)

## Running the game

From the project root, start the game with:

```bash
python main.py
```

There is also a Windows packaging script in `compile.bat` for building a standalone executable with Nuitka.


## Project structure

```text
The-Last-Assembly/
├── assets/                # Art and visual assets
├── debug/                 # Debugging tools and utilities
├── enemy/                 # Enemy logic, wave generation, and groups
├── events/                # Event system data and handlers
├── map/                   # Map loading, generation, and editor helpers
├── map_data/              # Saved map data files
├── menu/                  # Main menu, settings, collection, and game menus
├── mods/                  # Mod definitions and metadata
├── renderer/              # Drawing and HUD systems
├── shop/                  # Shop flow and item generation
├── sound/                 # Audio and SFX logic
├── specialists/           # Specialist definitions and behaviors
├── statistic/             # Run stats and tracking
├── towers/                # Tower implementations and logic
├── zones/                 # Zone system and placement rules
├── balancer_*.py          # Balance and tuning utilities
├── data_class.py          # Core game data and state container
├── main.py                # Game entry point
├── map_editor.py          # Map editor tool
├── requirements.txt       # Python dependencies
├── readme.md              # Project overview
└── compile.bat            # Windows build helper
```

## Current status

This project is a playable in-development project with a rich set of systems including towers, specialists, zones, events, map selection, and a roguelite shop loop.

## Notes

- The game is still under active development.
- Balance and gameplay tuning scripts exist in the root for experimentation.
- Assets and content are organized under the `assets` directory and are used by the game renderers and shop systems.
