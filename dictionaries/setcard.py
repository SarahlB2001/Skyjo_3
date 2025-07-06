import settings as s
from dictionaries import plaPosition as pla

card_width = pla.size["width"] / 5
card_height = pla.size ["height"] / 4 

x1 = 0
x2 = s.gap_height + card_width
x3 = 2*(s.gap_height + card_width)
x4 = 3*(s.gap_height + card_width)

y1 = 0 
y2 = s.gap_width + card_height
y3 = 2*(s.gap_width + card_height)



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
