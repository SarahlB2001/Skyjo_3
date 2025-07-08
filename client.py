# In client.py im Handler für "punkte_aktualisiert"
elif msg.get("update") == "punkte_aktualisiert":
    s.scores = msg["scores"]
    # Speichern für lila Klammern
    s.last_round_scores = msg["scores"].copy()
    s.points_calculated_time = pygame.time.get_ticks()
    # Rest wie gehabt...