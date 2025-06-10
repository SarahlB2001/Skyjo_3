import settings as s
from dictionaries import plaPosition as pla

x1 = 0
x2 = s.CARD_WIDTH + s.gap_width
x3 = 2*(s.CARD_WIDTH + s.gap_width)
x4 = 3*(s.CARD_WIDTH + s.gap_width)

y1 = 0 
y2 = s.CARD_HEIGHT + s.gap_height
y3 = 2*(s.CARD_HEIGHT + s.gap_height)

card_width = pla.size["width"] / 5
card_height = pla.size ["height"] / 4 

card1 = {"x": x1, "y": y1}
card2 = {"x": x2, "y": y1}
card3 = {"x": x3, "y": y1}
card4 = {"x": x4, "y": y1}  
card5 = {"x": x1, "y": y2}
card6 = {"x": x2, "y": y2}
card7 = {"x": x3, "y": y2}
card8 = {"x": x4, "y": y2}  
card9 = {"x": x1, "y": y3}
card10 = {"x": x2, "y": y3}
card11 = {"x": x3, "y": y3}
card12 = {"x": x4, "y": y3}  

