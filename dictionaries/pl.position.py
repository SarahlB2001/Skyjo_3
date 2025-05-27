import settings as s

eins = {'x': s.WIDTH // 16,
        "y": s.HEIGHT // 16,
        'width': s.WIDTH // 4,
        'height': s.HEIGHT // 4}

zwei = {'x': 2 * s.WIDTH // 16 + s.WIDTH // 4,
        'y': s.HEIGHT // 16,
        'width': s.WIDTH // 4,
        'height': s.HEIGHT // 4}

drei = {'x': s.WIDTH * 3 // 4 + 2 * s.WIDTH // 4,
        'y': s.HEIGHT // 16,
        'width': s.WIDTH // 4,
        'height': s.HEIGHT // 4}

vier = {'x': s.WIDTH * 3 // 4 + 2 * s.WIDTH // 4,
        'y': s.HEIGHT - s.HEIGHT//4 - s.HEIGHT//16,
        'width': s.WIDTH // 4,
        'height': s.HEIGHT // 4}

fünf = {'x': 2 * s.WIDTH // 16 + s.WIDTH // 4,
        'y': s.HEIGHT - s.HEIGHT//4 - s.HEIGHT//16,
        'width': s.WIDTH // 4,
        'height': s.HEIGHT // 4}

sechs = {'x': s.WIDTH // 16,
         'y': s.HEIGHT - s.HEIGHT//4 - s.HEIGHT//16,
         'width': s.WIDTH // 4,
         'height': s.HEIGHT // 4}

carddeck = {'x': (s.WIDTH - (2*s.WIDTH // 16 + s.WIDTH // 4)) // 2,
            'y': s.HEIGHT // 2 - (s.HEIGHT // 4) // 2,
            'width': 2 * s.WIDTH // 16 + s.WIDTH // 4,
            'height': s.HEIGHT // 4}

field_pos = {'1': eins,
             '2': zwei,
             '3': drei,
             '4': vier,
             '5': fünf,
             '6': sechs,
             'carddeck': carddeck}
