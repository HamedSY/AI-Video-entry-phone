
url = "http://192.168.53.142:8080/video"
valid_imgs = []
valid_imgs_encodings = []
mode = -1
process_this_frame = True


sender = 'hamed007.saboor@gmail.com'
receiver = 'amir.h.rnn@gmail.com'
subject = 'Knock Knock!'
password = '' #TODO hamed's application password
message = "Hello!\nA Person has just ringed your house!\nHis/Her picture is attached to the mail.\n"
imageFile = "unknown.jpg"

TONES = {
        "c6":1047,
        "b5":988,
        "a5":888,
        "g5":784,
        "f5":698,
        "e5":659,
        "eb5":622,
        "d5":587,
        "c5":523,
        "b4":494,
        "a4":440,
        "ab4":415,
        "g4":392,
        "f4":349,
        "e4":330,
        "d4":294,
        "c4":262,
        }
SONG = [
        ["e5",16],["eb5",16],
        ["e5",16],["eb5",16],["e5",16],["b4",16],["d5",16],["c5",16],
        ["a4",8],["p",16],["c4",16],["e4",16],["a4",16],
        ["b4",8],["p",16],["e4",16],["ab4",16],["b4",16],
        ["c5",8],["p",16],["e4",16],["e5",16],["eb5",16],
        ["e5",16],["eb5",16],["e5",16],["b4",16],["d5",16],["c5",16],
        ["a4",8],["p",16],["c4",16],["e4",16],["a4",16],
        ["b4",8],["p",16],["e4",16],["c5",16],["b4",16],["a4",4]
       ]