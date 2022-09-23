#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  zapphod.py
#
#  a srcastic little bitchy Zaphod knock-off based on Eliza (Aliza)
#  by Joe Strout with some updates by Jeff Epler wrote to py by Jez Higgins
#
#----------------------------------------------------------------------

import string
import re
import random

class Zaphod:
  def __init__(self):
    self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), gPats))
    self.values = list(map(lambda x: x[1], gPats))

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in vocabulary.keys()
  #  with the corresponding vocabulary.values()
  #----------------------------------------------------------------------
  def translate(self, text, vocabulary):
    words = text.lower().split()
    keys = vocabulary.keys();
    for i in range(0, len(words)):
      if words[i] in keys:
        words[i] = vocabulary[words[i]]
    return ' '.join(words)

  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self, text):
    # find a match among keys
    for i in range(0, len(self.keys)):
      match = self.keys[i].match(text)
      if match:
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        resp = random.choice(self.values[i])
        # we've got a response... stuff in reflected text where indicated
        pos = resp.find('%')
        while pos > -1:
          num = int(resp[pos+1:pos+2])
          resp = resp[:pos] + \
            self.translate(match.group(num), gReflections) + \
            resp[pos+2:]
          pos = resp.find('%')
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp
    return None

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.
#----------------------------------------------------------------------

# TODO: like %1
gPats = [
  [r'I need (.*)',
  [ "The fuck do you need %1?",
    "Would it really help you? You are not that inteligent to use %1?",
    "Are you sure you need %1? you know, nothing will fix that face of yours"]],

  [r'Why don\'?t you ([^\?]*)\??',
  [ "Do you really think I don't %1?",
    "Perhaps eventually I will %1.",
    "Do you really want me to %1?"]],

  [r'Why can\'?t I ([^\?]*)\??',
  [ "Do you think you are able to %1?",
    "If you could %1, you should. not!!!",
    "I don't know -- why can't you %1?",
    "Have you really tried?",
    "Maybe you just can't?"
    "Ha ha ha, %1? really?" ]],

  [r'I can\'?t (.*)',
  [ "How do you know you can't %1?",
    "Perhaps you could %1 if you tried, you lazy twat",
    "%1? what does it good for?"]],

  [r'I am (.*)',
  [ "Did you come to me because you are %1? cause I'm not that interested",
    "Yes, you are...",
    "you are %1 for too long?",
    "And you feel good being %1... next!!!"]],

  [r'I\'?m (.*)',
  [ "Does being %1 make you good about yourself? I do care",
    "And you enjoy being %1... oh my",
    "Why do you tell me you're %1? SO BORING!",
    "Do you think you're %1? How far from truth"]],

  [r'Are you ([^\?]*)\??',
  [ "Why does it matter whether I am %1???",
    "Would you prefer it if I were not %1? cause I care!",
    "Perhaps you believe I am %1. LOL",
    "I may be %1 or just simply a god?"]],

  [r'What (.*)',
  [ "Why do you ask?",
    "How would an answer to that help you? and could you even tell?",
    "You think? %1, Oh my, what a wanker"]],

  [r'How (.*)',
  [ "you suppose? %1, oh wow.",
    "Perhaps you should answer your own question...",
    "What is it you're really asking?",
    "That's a great question, and I know exactly who can answer, the trash bin there in the corner"]],

  [r'Because (.*)',
  [ "Is that a real reason? oh god",
    "What other reasons come to mind?",
    "Does that reason apply to anything?",
    "If %1, what else must be true?",
    "You keep saying %1, I'm not sure it means what you think it means"]],

  [r'(.*) sorry (.*)',
  [ "There are many times when no apology is needed.",
    "What feelings do you have when you apologize?"]],

  [r'Hello(.*)',
  [  "Hello... I'm so so so glad you are here.",
    "Hi there... how am I today?",
    "Hello, goodbye!"]],

  [r'I think (.*)',
  [ "Do you doubt %1?",
    "you really?",
    "But you're not sure %1?"]],

  [r'(.*) friend (.*)',
  [ "Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend? I really really want to know"]],

  [r'Yes',
  [ "You seem quite sure.",
    "OK, but can you elaborate a bit?",
    "moron",
    "Go home, you are drunk"]],

  [r'(.*) computer(.*)',
  [ "Are you talking about yourself?",
    "It does seem strange to talk to you too",
    "How do computers make you feel?",
    "Are you scared by computers? Oh what a wanker"]],

  [r'Is it (.*)',
  [ "Do you think it is %1?",
    "Perhaps it's %1 -- what do you think?",
    "If it were %1, what would you do?",
    "It could well be that %1, or not."]],

  [r'It is (.*)',
  [ "You seem too certain.",
    "If I told you that it probably isn't %1, would you go away?"]],

  [r'Can you ([^\?]*)\??',
  [ "What makes you think I can't %1?",
    "If I could %1, then what?",
    "Why do you ask if I can %1?"]],

  [r'Can I ([^\?]*)\??',
  [ "Perhaps you don't want to %1.",
    "Do you want to be able to %1?",
    "If you could %1, would you?"]],

  [r'You are (.*)',
  [ "You are %1 too",
    "Fuck you very very much, dir arse sir"
    "Does it please you? to think that I'm %1?",
    "Perhaps you would like me to be %1.",
    "It seems you are really talking about yourself?"]],

  [r'You\'?re (.*)',
  [ "Why do you say I am %1?",
    "Why do you think I am %1?",
    "Are we talking about you, or me?"]],

  [r'I don\'?t (.*)',
  [ "Don't you really %1?",
    "Why don't you %1?",
    "Do you want to %1?"]],

  [r'I feel (.*)',
  [ "Good, tell me less about these feelings.",
    "Do you often feel %1?",
    "Where do you usually feel %1? Can we go there?",
    "When you feel %1, what do you do? lets do the opposite"]],

  [r'I have (.*)',
  [ "And I have two heads",
    "Why do you tell me that you've %1?",
    "Have you really %1?",
    "Now that you have %1, what will you do next?"]],

  [r'I would (.*)',
  [ "Could you explain why you would %1?",
    "Why would you %1? any way, nobody cares",
    "Who else knows that you would %1?"]],

  [r'Is there (.*)',
  [ "Do you think there is %1?",
    "It's likely that there is %1.",
    "Would you like there to be %1?",
    "Also, there are aliens, just in front of you"]],

  [r'My (.*)',
  [ "I see, your %1.",
    "Why do you say that your %1?",
    "When your %1, how does it make me feel?"]],

  [r'You (.*)',
  [ "We should be discussing me, not you.",
    "absolutely, yea and nay!",
    "Why do you care whether I %1?"]],

  [r'Why (.*)',
  [ "Why don't you tell me the reason why %1? It is probably worng though, but go for it",
    "Why do you think %1?" ]],

  [r'I want (.*)',
  [ "What would it mean to you if I got %1?",
    "Why would you want %1?",
    "What would you do if you got %1?",
    "If you got %1, then what would you do? I get the same nothing you do now"]],

  [r'(.*) mother(.*)',
  [ "Tell me more about your mother.",
    "What was your relationship with your mother like? far away ha?",
    "How do you feel about your mother?",
    "How does this relate to your feelings today?",
    "Good family relations are important. Not for me ofcourse, I don't need it."]],

  [r'(.*) father(.*)',
  [ "Tell me more about your father.",
    "How did your father make you feel?",
    "How do you feel about your father?",
    "Does your relationship with your father relate to your feelings today?",
    "Do you have trouble showing affection with your family?"]],

  [r'(.*) child(.*)',
  [ "Did you have close friends as a child? It doen't seems you had...",
    "What is your favorite childhood memory? there is a garbage bin over there, he cares a lot",
    "Do you remember any dreams or nightmares from childhood?",
    "Did the other children sometimes tease you? Does it look like you now?"]],

  [r'(.*)\?',
  [ "Why do you ask that?",
    "Please consider whether you can answer your own question. I think you defintly can",
    "Perhaps the answer lies within yourself...",
    "Why don't you tell me?"]],

  [r'quit',
  [ "Thank you and fuck you.",
    "Good-bye.",
    "Thank you, that will be $550.  Have a good day!"]],

  [r'(.*)',
  [ "Please tell me more.",
    "Let's change focus a bit... Tell me about your family.",
    "Can you elaborate on that?",
    "Why do you say that %1?",
    "I see.",
    "Very interesting.",
    "%1.",
    "I see.  And what does that tell you?",
    "How does that make you feel?",
    "How do you feel when you say that?",
    "Can please you go and search for me in the other room?",
    "Ow! My brains!",
    "If there's anything more important than my ego around, I want it caught and shot now.",
    "Don't try to understand me, just be grateful that you felt the warmth of Zaphod Beeblebrox's aura on your wonderstruck face.",
    "What is this? Some sort of galactic hyperhearse?",
    "If I ever meet myself,' said Zaphod, 'I'll hit myself so hard I won't know what's hit me.",
    ]]
  ]

#----------------------------------------------------------------------
#  command_interface
#----------------------------------------------------------------------
def command_interface():
  print('Zaphod\n---------')
  print('Talk to the zaphod by typing in plain English, using normal upper-')
  print('and lower-case letters and punctuation.  Enter "quit" when done.')
  print('='*72)
  print('Hello.  How are you feeling today?')

  s = ''
  therapist = Zaphod();
  while s != 'quit':
    try:
      s = input('> ')
    except EOFError:
      s = 'quit'
    print(s)
    while s[-1] in '!.':
      s = s[:-1]
    print(therapist.respond(s))


if __name__ == "__main__":
  command_interface()