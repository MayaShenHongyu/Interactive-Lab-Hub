# Chatterboxes
[![Watch the video](https://user-images.githubusercontent.com/1128669/135009222-111fe522-e6ba-46ad-b6dc-d1633d21129c.png)](https://www.youtube.com/embed/Q8FWzLMobx0?start=19)

In this lab, we want you to design interaction with a speech-enabled device--something that listens and talks to you. This device can do anything *but* control lights (since we already did that in Lab 1).  First, we want you first to storyboard what you imagine the conversational interaction to be like. Then, you will use wizarding techniques to elicit examples of what people might say, ask, or respond.  We then want you to use the examples collected from at least two other people to inform the redesign of the device.

We will focus on **audio** as the main modality for interaction to start; these general techniques can be extended to **video**, **haptics** or other interactive mechanisms in the second part of the Lab.

## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 

### Pick up Additional Parts

As mentioned during the class, we ordered additional mini microphone for Lab 3. Also, a new part that has finally arrived is encoder! Please remember to pick them up from the TA.

### Get the Latest Content

As always, pull updates from the class Interactive-Lab-Hub to both your Pi and your own GitHub repo. As we discussed in the class, there are 2 ways you can do so:

**\[recommended\]**Option 1: On the Pi, `cd` to your `Interactive-Lab-Hub`, pull the updates from upstream (class lab-hub) and push the updates back to your own GitHub repo. You will need the *personal access token* for this.

```
pi@ixe00:~$ cd Interactive-Lab-Hub
pi@ixe00:~/Interactive-Lab-Hub $ git pull upstream Fall2021
pi@ixe00:~/Interactive-Lab-Hub $ git add .
pi@ixe00:~/Interactive-Lab-Hub $ git commit -m "get lab3 updates"
pi@ixe00:~/Interactive-Lab-Hub $ git push
```

Option 2: On your your own GitHub repo, [create pull request](https://github.com/FAR-Lab/Developing-and-Designing-Interactive-Devices/blob/2021Fall/readings/Submitting%20Labs.md) to get updates from the class Interactive-Lab-Hub. After you have latest updates online, go on your Pi, `cd` to your `Interactive-Lab-Hub` and use `git pull` to get updates from your own GitHub repo.

## Part 1.
### Text to Speech 

In this part of lab, we are going to start peeking into the world of audio on your Pi! 

We will be using a USB microphone, and the speaker on your webcamera. (Originally we intended to use the microphone on the web camera, but it does not seem to work on Linux.) In the home directory of your Pi, there is a folder called `text2speech` containing several shell scripts. `cd` to the folder and list out all the files by `ls`:

```
pi@ixe00:~/text2speech $ ls
Download        festival_demo.sh  GoogleTTS_demo.sh  pico2text_demo.sh
espeak_demo.sh  flite_demo.sh     lookdave.wav
```

You can run these shell files by typing `./filename`, for example, typing `./espeak_demo.sh` and see what happens. Take some time to look at each script and see how it works. You can see a script by typing `cat filename`. For instance:

```
pi@ixe00:~/text2speech $ cat festival_demo.sh 
#from: https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)#Festival_Text_to_Speech

echo "Just what do you think you're doing, Dave?" | festival --tts
```

Now, you might wonder what exactly is a `.sh` file? Typically, a `.sh` file is a shell script which you can execute in a terminal. The example files we offer here are for you to figure out the ways to play with audio on your Pi!

You can also play audio files directly with `aplay filename`. Try typing `aplay lookdave.wav`.

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)
myname.sh

Bonus: If this topic is very exciting to you, you can try out this new TTS system we recently learned about: https://github.com/rhasspy/larynx

### Speech to Text

Now examine the `speech2text` folder. We are using a speech recognition engine, [Vosk](https://alphacephei.com/vosk/), which is made by researchers at Carnegie Mellon University. Vosk is amazing because it is an offline speech recognition engine; that is, all the processing for the speech recognition is happening onboard the Raspberry Pi. 

In particular, look at `test_words.py` and make sure you understand how the vocab is defined. Then try `./vosk_demo_mic.sh`

One thing you might need to pay attention to is the audio input setting of Pi. Since you are plugging the USB cable of your webcam to your Pi at the same time to act as speaker, the default input might be set to the webcam microphone, which will not be working for recording.

\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*
speech2text.sh
test_numbers.py
Recorded: recorded_answer.wav

Bonus Activity:

If you are really excited about Speech to Text, you can try out [Mozilla DeepSpeech](https://github.com/mozilla/DeepSpeech) and [voice2json](http://voice2json.org/install.html)
There is an included [dspeech](./dspeech) demo  on the Pi. If you're interested in trying it out, we suggest you create a seperarate virutal environment for it . Create a new Python virtual environment by typing the following commands.

```
pi@ixe00:~ $ virtualenv dspeechexercise
pi@ixe00:~ $ source dspeechexercise/bin/activate
(dspeechexercise) pi@ixe00:~ $ 
```

### Serving Pages

In Lab 1, we served a webpage with flask. In this lab, you may find it useful to serve a webpage for the controller on a remote device. Here is a simple example of a webserver.

```
pi@ixe00:~/Interactive-Lab-Hub/Lab 3 $ python server.py
 * Serving Flask app "server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 162-573-883
```
From a remote browser on the same network, check to make sure your webserver is working by going to `http://<YourPiIPAddress>:5000`. You should be able to see "Hello World" on the webpage.

### Contributors
Hongyu Shen (hs692)

Xuanyu Fang (xf48)

### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

Our device is a voice interaction game. The player plays the role of a 911 operator who receives an emergency call asking for help. The other end of the phone call is a man who claims that he is trapped in a locked apartment and has lost all his memories. He asks for the player’s help to escape from the apartment. The man describes what he sees and lists out possible actions; the player instructs the man to conduct these actions by speech to move forward with the game. This game is suitable to be designed as a voice interaction game because it simulates a phone call in which the player does not have vision.

Storyboard
![Storyboard](./storyboard.jpg)

Map for the game
![Map](./map.jpg)

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

### Dialogue
Narrator: *Welcome to Hotline, a voice interaction game. You are now a 9-1-1 hotline operator, you will help a person in need over the phone,  and the only way you can do so is to talk to him and tell him what to do. Here comes your call...*

*beep beep beep*

Male voice: “Is this 911, hi, I need help, please! Can you help me?”

Player response: “yes”/“Hi”/“what happened” / “where are you” / “who are you” …

If the response is not partially detected, male voice responds: What, what are you saying? I don’t understand.

Male voice: ”I lost my memory and I’m now trapped in a room! There’s no one with me, and I don’t remember anything!”

Player response: “What is the room like” / “What’s in the room” / ”What can you see” …

Male voice: “Ok, ok, I’m in a study I guess, there’s a door, let me see … it’s locked, there are many books on a bookshelf, there's a painting on the wall… and it’s just like a regular study...”

Player response:
* door - still locked
* Painting - nothing special (0) triggered (1)
* book/bookshelf - Voice: ”Ok, I’ll check the book …… oh! There’s a book that looks strange, let me check… Oh my god, the book is carved hollow inside and there’s a key in it!” ->

Player response:
* Door - “Oh it’s the key for the door, I’m out, let me see...” ->
* Others - “what do you want me to do with the key?”

Male voice: “Ok, now I’m out, I’m in a … hallway I think, quite a simple house, there’s no window though, let me see … (walking around) … are you still there? I see three rooms, other than the study, one to my left, it says, bathroom, one to my right,I think is the kitchen, and one ahead, should be the bedroom?”

Player response:
* Bathroom / left- “The door is open, god bless, it seems to be… a normal bathroom, quite small.” ->
* Kitchen / Right - “I can smell something, it smells so good in it, the door is locked, I can’t go in, my god, I’m so hungry, how long has it been! Maybe I should try somewhere else?”
* Bedroom / Ahead - “it’s weird, there’s not even a grip on the door, wait a minute, there’s something written on the door … *What's in the soup today?* what? What does that mean? Maybe I should try somewhere else?”

Male voice: “Now I’m in the bathroom, there’s the bathtub, nothing unusual, the toilet, and a mirror ...”

Player response:
* Bathtub - “It’s … just a regular bathtub I think...”
* mirror - “ok, you are right, I should probably see what I look like, maybe I could remember something? Let me see … Oh My God!! Who am I, what’s wrong with this terrible face! I’m not looking at it anymore!”
* Toilet - “Ok, It’s really dirty, but got to do whatever gets me out of this shithole .... Wait, it’s not flushing, maybe something is clogged, let me check... who would have thought that! Are you like a detective or something? It’s a key! Probably opens the door to the kitchen!” ->

Male voice: “Now that I have the key, where should I go? Bedroom, Kitchen, or study?”

Player response:
* Bedroom - “Ok, let me see, there’s no key hole on the door, really weird, just something written on the door … *What’s in the soup today?* what does that mean?”
* Study - “Just like before, I don’t see anything useful, maybe I should do something with the key?”
Kitchen - “ahh, there’s a keyhole, let me try… Ok, the door's open, let me see what’s inside, man, it smells so good!” ->

Male Voice: “So… Here's the kitchen, some bowls … some bread, the stove is still on, and something is boiling in the pot, dang, that smells so good, Wonder what’s in it… should I go check the pot?”

Player Responses: 
* Yes / pot/ check/ why not / what/ inside - “it’s soup! I need to have some…(tasting soup) Ok, it tastes like heaven, my lord, I think there’s tomatoes, chicken, onions, and chilies, I wish you could be here to taste it.” ->
* Others - “Oh I’m too hungry, I need to know what smells that good” - then go to yes

Male Voice: “Ok, enough soup, what should I do now? Should I go Bathroom, study, or bedroom?”

Player Responses: 
* Study - “still the same old study, maybe I should check out other rooms?”
* Bathroom - “eww, it’s dirty, not going back again”
* Bedroom - “Yes! The soup! Maybe that will solve the puzzle!” ->

Male Voice: “Ok, now I’m at the bedroom door, it’s hardly a door, no grip or anything, a question on it though, *What’s in the soup today?* , oh man, I shouldn’t have finished it all, do you still remember what’s in it?”

Player Responses:
* Tomato / chicken / onion / chilli / s  - “Yes, yes, I still remember that taste! You are right!” ->

Male Voice: “So… should I just say the word? *INPUT* *INPUT* holy shit, it’s opening! The door opened automatically, is someone listening to me? …. OK, this is the bedroom, still no exit in it, how can this house have no exit! Ok, there’s the bed, of course, queen size I guess, looking cozy, a computer on the desk, and a book on the nightstand… What should I do?”

Player Responses:
* Bed - “I’m not going to sleep at this time, maybe something else?”
* Desk / computer - “you are right, maybe I can connect to the internet … ok it’s totally dead, just a decoration I guess…, maybe something else?”
* Book / nightstand - “Sure, it’s never late to read, here’s a bookmarked page *reading* Painting is always a good place for many private people to hide their secrets in their home, many indoor designs leave a secret space on the wall that is covered by paintings and decorations … wait, that sounds real familiar... ”  ->

Male Voice: “I think that’s it for the bedroom, where should I go next, I don’t see another new door… should I go back to the kitchen, or bathroom, or study?”

Player Responses:
* Study - “Wait, you are right, there’s a painting there! Maybe something hidden!” ->
* Bathroom - “eww, it’s dirty, not going back again!”
* Kitchen - “No soup there anymore, maybe somewhere else?”

Male Voice: “Ok, study, the painting, let’s see what’s behind it… My god, there is actually something! Can you imagine that? There’s a half-full vile of some greenish fluid … and a note … *drink it and you will be free*, what does that mean? Should I drink it? Shoot… the phone is going to die … hey, hey can you still hear me... should I drink … ”

The connection has been lost. After an hour or so, you received another call suddenly, “Is this 911, hi, I need help, please! Can you help me?” ”I lost my memory and I’m now trapped in a room! There’s no one with me, and I don’t remember anything!”


### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*

We asked a friend to play the game while we acted as the device. The first two interactions before the actual game began (i.e. where the man was telling his problems) was a little rough because we did not stage clear options for the player to choose. So we added clear questions like "Can you help me?" and try to detect keyword "Yes".

The rest of the game went smoothly except when the player asked the device to repeat. So we decided to add these two instructions throughout the entire game:

*If no keyword is detected - "What, what are you saying? I don’t understand."*

*If detect keyword “repeat” - the guy repeats whatever he said*

### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
3. Make a new storyboard, diagram and/or script based on these reflections.

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

*Include videos or screencaptures of both the system and the controller.*

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\**your answer here*\*\*

### What worked well about the controller and what didn't?

\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

\*\**your answer here*\*\*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

\*\**your answer here*\*\*

