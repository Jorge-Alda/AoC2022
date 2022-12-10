letters = {
    """
 ## 
#  #
#  #
####
#  #
#  #
""": 'A',
    """
### 
#  #
### 
#  #
#  #
### 
""": 'B',
    """
 ## 
#  #
#   
#   
#  #
 ## 
""": 'C',
    """
####
#   
### 
#   
#   
####
""": 'E',
    """
####
#   
### 
#   
#   
#   
""": 'F',
    """
 ## 
#  #
#   
# ##
#  #
 ###
""": 'G',
    """
#  #
#  #
####
#  #
#  #
#  #
""": 'H',
    """
 ###
  # 
  # 
  # 
  # 
 ###
""": 'I',
    """
  ##
   #
   #
   #
#  #
 ## 
""": 'J',
    """
#  #
# # 
##  
# # 
# # 
#  #
""": 'K',
    """
#   
#   
#   
#   
#   
####
""": 'L',
    """
 ## 
#  #
#  #
#  #
#  #
 ## 
""": 'O',
    """
### 
#  #
#  #
### 
#   
#   
""": 'P',
    """
### 
#  #
#  #
### 
# # 
#  #
""": 'R',
    """
 ###
#   
#   
 ## 
   #
### 
""": 'S',
    """
#  #
#  #
#  #
#  #
#  #
 ## 
""": 'U',
    """
#   
#   
 # #
  #  
  # 
  # 
""": 'Y',
    """
####
   #
  # 
 #  
#   
####
""": 'Z',

}


def ocr_scan(inp: str, *, on: str = '#', off: str = ' ') -> str:
    word = ""
    inp = inp.replace(on, '#').replace(off, ' ')
    lines = inp.split('\n')
    if len(lines) != 6:
        raise ValueError("Not enough lines!")
    width = len(lines[0])
    if width % 5 != 0:
        raise ValueError("Lines have wrong width!")
    if any(len(l) != width for l in lines):
        raise ValueError("The lines have mismatched widths!")
    for i in range(width//5):
        char = '\n'
        for j in range(6):
            char += lines[j][5*i:5*i+4] + '\n'
        word += letters[char]
    return word
