import settings as s

# Für Spiel mit 2 Leuten: 1 & 3 (oder 2 & 5)
# Für Spiel mit 3 Leuten: 1 & 3 & 5
# Für Spiel mit 4 Leuten: 1 & 3 & 4 & 6
# Für Spiel mit 5 Leuten: 1 & 2 & 3 & 4 & 6
# Für Spiel mit 6 Leuten : 1 & 2 & 3 & 4 & 5 & 6

eins = {'x': s.HEIGHT // 16,
        "y": s.WIDTH // 16}

zwei = {'x': s.HEIGHT * 2 // 16 + s.HEIGHT // 4,
        'y': s.WIDTH // 16}

drei = {'x': s.HEIGHT * 3 // 4 - s.HEIGHT // 16,
        'y': s.WIDTH // 16}

vier = {'x': s.HEIGHT * 3 // 4 - s.HEIGHT // 16,
        'y': s.WIDTH - s.WIDTH//4 - s.WIDTH//9} 

funf = {'x': s.HEIGHT // 8 + s.HEIGHT // 4,
        'y': s.WIDTH - s.WIDTH//4 - s.WIDTH//16}

sechs = {'x': s.HEIGHT // 16,
         'y': s.WIDTH - s.WIDTH//4 - s.WIDTH//9} 

size = {'height': s.WIDTH // 4,
        'width': s.HEIGHT // 4}

carddeck = {'x': (s.HEIGHT - (2*s.HEIGHT // 16 + s.HEIGHT // 4)) // 2,
            'y': s.WIDTH // 2 - (s.WIDTH // 4) // 2,
            'width': 2 * s.HEIGHT // 16 + s.HEIGHT // 4,
            'height': s.WIDTH // 4}

field_pos = {'1': eins,
             '2': zwei,
             '3': drei,
             '4': vier,
             '5': funf,
             '6': sechs,
             'size': size,
             'carddeck': carddeck}

player_pos = {2: [(eins['x'], eins['y']), (drei ['x'], drei['y'])],
              3: [(eins['x'], eins['y']), (drei ['x'], drei['y']), (funf ['x'], funf['y'])],
              4: [(eins['x'], eins['y']), (drei ['x'], drei['y']), (vier ['x'], vier['y']), (sechs ['x'], sechs['y'])],
              5: [(eins['x'], eins['y']), (drei ['x'], drei['y']), (vier ['x'], vier['y']), (funf ['x'], funf['y']), (sechs ['x'], sechs['y'])],
              6: [(eins['x'], eins['y']), (zwei ['x'], zwei['y']), (drei ['x'], drei['y']), (vier ['x'], vier['y']), (funf ['x'], funf['y']), (sechs ['x'], sechs['y'])]}

