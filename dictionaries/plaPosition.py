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
        'y': s.WIDTH - s.WIDTH//4 - s.WIDTH//9}

sechs = {'x': s.HEIGHT // 16,
         'y': s.WIDTH - s.WIDTH//4 - s.WIDTH//9}

size = {'height': s.WIDTH // 4,
        'width': s.HEIGHT // 4}

stapel_width = 80
stapel_height = 120
abstand = 30

gesamt_breite = stapel_width * 2 + abstand
center_x = s.HEIGHT // 2
center_y = s.WIDTH // 2

verschiebung_nach_oben = 70

carddeck = {
    'x': center_x - gesamt_breite // 2,
    'y': center_y - stapel_height // 2 - verschiebung_nach_oben,
    'width': stapel_width,
    'height': stapel_height
}

discarddeck = {
    'x': center_x - gesamt_breite // 2 + stapel_width + abstand,
    'y': center_y - stapel_height // 2 - verschiebung_nach_oben,
    'width': stapel_width,
    'height': stapel_height
}

field_pos = {'1': eins,
             '2': zwei,
             '3': drei,
             '4': vier,
             '5': funf,
             '6': sechs,
             'size': size,
             'carddeck': carddeck,
             'discarddeck': discarddeck}

player_pos = {2: [(eins['x'], eins['y'] - s.PL_NAME_POS), (drei ['x'], drei['y'] - s.PL_NAME_POS)],
              3: [(eins['x'], eins['y'] - s.PL_NAME_POS), (drei ['x'], drei['y'] - s.PL_NAME_POS), (funf ['x'], funf['y'] - s.PL_NAME_POS)],
              4: [(eins['x'], eins['y'] - s.PL_NAME_POS), (drei ['x'], drei['y'] - s.PL_NAME_POS), (vier ['x'], vier['y'] - s.PL_NAME_POS), (sechs ['x'], sechs['y'] - s.PL_NAME_POS)],
              5: [(eins['x'], eins['y'] - s.PL_NAME_POS), (drei ['x'], drei['y'] - s.PL_NAME_POS), (vier ['x'], vier['y'] - s.PL_NAME_POS), (funf ['x'], funf['y'] - s.PL_NAME_POS), (sechs ['x'], sechs['y'] - s.PL_NAME_POS)],
              6: [(eins['x'], eins['y'] - s.PL_NAME_POS), (zwei ['x'], zwei['y'] - s.PL_NAME_POS), (drei ['x'], drei['y'] - s.PL_NAME_POS), (vier ['x'], vier['y'] - s.PL_NAME_POS), (funf ['x'], funf['y'] - s.PL_NAME_POS), (sechs ['x'], sechs['y'] - s.PL_NAME_POS)]}

