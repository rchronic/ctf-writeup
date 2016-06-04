import PIL.Image
import io

dat = '''\
00000000000000000000000000000000000
01111111000100101011110100011111110
01000001010000111100011001010000010
01011101010111011011001111010111010
01011101010001101001001011010111010
01011101011110011110010111010111010
01000001010011000000111101010000010
01111111010101010101010101011111110
00000000001110000110110100000000000
00010011110001010010000011101111100
00100100011100000010111010010010010
01000001000111011111010011010100010
00000000011111000010111001001010000
00011011110001000010001000011010110
00101110000100001001001010111011100
01110101100110100000110010000110010
00010000110000101010010010010010010
01101101010001000111100111011010000
00100110110011010001001011010001000
01010011111100111001010010110001010
00101110100101001111000111011110010
00010001011101101000110111110010010
00101100000111110000010001001001010
01101111100110001010010101111111010
00000100100100101011000111001010110
01111011110100001101010001111100000
00000000011111011001000101000111010
01111111011101111101101101010100110
01000001011111010011010111000110100
01011101001110011010001111111110110
01011101001100011011100111101100100
01011101011101000110010001010101110
01000001000100110101001011001110000
01111111000011101100000001110010010
00000000000000000000000000000000000\
'''

h = 0
img = PIL.Image.new('RGB', (35, 35))

for row in dat.split():
    i = 0
    for c in row:
        if c == '0':
            img.putpixel((h, i), (255,255,255))
        i += 1
    h += 1

img.save(open('final.png', 'wb'), 'PNG')

# You Win! https://goo.gl/cvNaab