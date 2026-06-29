"""
Keyword → icon-type → emoji mappings for the auto-icon feature.
Add new entries here; printer.py imports _ICON_KEYWORDS and _ICON_EMOJIS.

Rules:
- _ICON_KEYWORDS:  keyword (lowercase) → icon_type name
                   Entries are checked in order; first match wins.
                   Keep specific / niche keywords ABOVE generic fallbacks.
- _ICON_EMOJIS:    icon_type name → single Unicode code-point string.
                   Use plain codepoints, NO variation selectors (U+FE0F)
                   — they break Pillow's bounding-box measurement.
"""

# ── Keyword → icon type ───────────────────────────────────────────────────────

_ICON_KEYWORDS = {

    # ── Ham Radio ────────────────────────────────────────────────────────────
    # Antenna / feedline / RF hardware → 📡
    "antenna":          "antenna",
    "antennas":         "antenna",
    "yagi":             "antenna",
    "beam":             "antenna",
    "dipole":           "antenna",
    "vertical":         "antenna",
    "wire antenna":     "antenna",
    "magnetic loop":    "antenna",
    "quad":             "antenna",
    "moxon":            "antenna",
    "coax":             "antenna",
    "coaxial":          "antenna",
    "feedline":         "antenna",
    "feed line":        "antenna",
    "pl-259":           "antenna",
    "so-239":           "antenna",
    "balun":            "antenna",
    "choke":            "antenna",
    "ferrite":          "antenna",
    "counterpoise":     "antenna",
    "radials":          "antenna",
    "rotator":          "antenna",
    "rotor":            "antenna",
    "tower":            "antenna",
    "mast":             "antenna",
    "swr":              "antenna",
    "dummy load":       "antenna",
    "feedthrough":      "antenna",
    "lightning arrestor": "antenna",

    # Radio / transceiver / operating gear → 📻
    "transceiver":      "radio",
    "rig":              "radio",
    "ham":              "radio",
    "ham shack":        "radio",
    "hf":               "radio",
    "vhf":              "radio",
    "uhf":              "radio",
    "handheld":         "radio",
    "walkie talkie":    "radio",
    "receiver":         "radio",
    "transmitter":      "radio",
    "sdr":              "radio",
    "scanner":          "radio",
    "repeater":         "radio",
    "amplifier":        "radio",
    "antenna tuner":    "radio",
    "keyer":            "radio",
    "paddle":           "radio",
    "morse key":        "radio",
    "morse":            "radio",
    "logbook":          "radio",
    "log book":         "radio",
    "qsl":              "radio",
    "qso":              "radio",
    "dxing":            "radio",
    "contest":          "radio",
    "field day":        "radio",
    "emcomm":           "radio",
    "aprs":             "radio",
    "ft8":              "radio",
    "ft4":              "radio",
    "wspr":             "radio",
    "callsign":         "radio",
    "propagation":      "radio",
    "grounding":        "radio",
    # Radio brand names / models
    "quansheng":        "radio",
    "baofeng":          "radio",
    "yaesu":            "radio",
    "icom":             "radio",
    "kenwood":          "radio",
    "tidradio":         "radio",
    "vgc":              "radio",
    "tecsun":           "radio",
    "tyt":              "radio",
    "raddy":            "radio",
    "radioditty":       "radio",
    "handie talkie":    "radio",
    "uv5r":             "radio",
    "uvk5":             "radio",

    # ── Warning / Hazard ─────────────────────────────────────────────────────
    "fragile":          "warning",
    "breakable":        "warning",
    "handle with care": "warning",
    "caution":          "warning",
    "careful":          "warning",
    "danger":           "warning",
    "hazard":           "warning",
    "warning":          "warning",
    "alert":            "warning",
    "unsafe":           "warning",
    "do not drop":      "warning",
    "flammable":        "warning",

    # ── People ───────────────────────────────────────────────────────────────
    "person":           "person",
    "human":            "person",
    "individual":       "person",
    "someone":          "person",
    "man":              "man",
    "male":             "man",
    "gentleman":        "man",
    "guy":              "man",
    "sir":              "man",
    "dude":             "man",
    "bloke":            "man",
    "woman":            "woman",
    "female":           "woman",
    "lady":             "woman",
    "gal":              "woman",
    "miss":             "woman",
    "boy":              "boy",
    "lad":              "boy",
    "son":              "son",
    "nephew":           "boy",
    "brother":          "boy",
    "bro":              "boy",
    "bruv":             "boy",
    "stepbrother":      "boy",
    "girl":             "girl",
    "lass":             "girl",
    "daughter":         "girl",
    "niece":            "girl",
    "sister":           "girl",
    "sis":              "girl",
    "sissy":            "girl",
    "stepsister":       "girl",
    "mom":              "woman",
    "momma":            "woman",
    "mamma":            "woman",
    "mother":           "woman",
    "mama":             "woman",
    "mommy":            "woman",
    "mum":              "woman",
    "mummy":            "woman",
    "mumma":            "woman",
    "ma":               "woman",
    "madre":            "woman",
    "stepmom":          "woman",
    "stepmother":       "woman",
    "aunt":             "woman",
    "auntie":           "woman",
    "aunty":            "woman",
    "dad":              "man",
    "daddy":            "man",
    "dada":             "man",
    "dadda":            "man",
    "father":           "man",
    "papa":             "man",
    "padre":            "man",
    "pops":             "man",
    "stepdad":          "man",
    "stepfather":       "man",
    "uncle":            "man",
    "unc":              "man",
    "uncie":            "man",
    "elder":            "elder",
    "elderly":          "elder",
    "senior":           "elder",
    "grandpa":          "elder",
    "grandfather":      "elder",
    "gramps":           "elder",
    "grampa":           "elder",
    "grampy":           "elder",
    "opa":              "elder",
    "pop pop":          "elder",
    "old man":          "elder",
    "grandma":          "grandma",
    "grandmother":      "grandma",
    "grandmama":        "grandma",
    "nana":             "grandma",
    "nan":              "grandma",
    "nanny":            "grandma",
    "gran":             "grandma",
    "granny":           "grandma",
    "grammy":           "grandma",
    "mawmaw":           "grandma",
    "memaw":            "grandma",
    "mamaw":            "grandma",
    "oma":              "grandma",
    "nonna":            "grandma",
    "abuela":           "grandma",
    "grandparent":      "elder",
    "old woman":        "grandma",
    "granddad":         "elder",
    "grandad":          "elder",
    "grandpapa":        "elder",
    "pawpaw":           "elder",
    "papaw":            "elder",
    "peepaw":           "elder",
    "pepaw":            "elder",
    "nonno":            "elder",
    "abuelo":           "elder",
    "family":           "family",
    "household":        "family",
    "relatives":        "family",
    "parents":          "family",
    "couple":           "couple",
    "partners":         "couple",
    "husband":          "couple",
    "hubby":            "couple",
    "wife":             "couple",
    "wifey":            "couple",
    "spouse":           "couple",
    "missus":           "couple",
    "other half":       "couple",
    "people":           "people",
    "folk":             "people",
    "group":            "people",
    "team":             "people",
    "friend":           "people",
    "friends":          "people",
    "buddy":            "people",
    "pal":              "people",
    "mate":             "people",
    "crew":             "people",
    "gang":             "people",
    "police":           "police",
    "cop":              "police",
    "officer":          "police",
    "sheriff":          "police",
    "law enforcement":  "police",
    "guard":            "guard",
    "security":         "guard",
    "bouncer":          "guard",
    "detective":        "detective",
    "sleuth":           "detective",
    "investigator":     "detective",
    "spy":              "detective",
    "cowboy":           "cowboy",
    "cowgirl":          "cowboy",
    "western":          "cowboy",
    "ninja":            "ninja",
    "shinobi":          "ninja",
    "wizard":           "wizard",
    "witch":            "wizard",
    "sorcerer":         "wizard",
    "mage":             "wizard",
    "vampire":          "vampire",
    "dracula":          "vampire",
    "zombie":           "zombie",
    "undead":           "zombie",
    "santa":            "santa",
    "father christmas": "santa",
    "prince":           "prince",
    "princess":         "princess",
    "superhero":        "superhero",
    "supervillain":     "superhero",
    "hero":             "superhero",
    "tuxedo":           "tuxedo",
    "worker":           "worker",
    "construction":     "worker",
    "builder":          "worker",
    "hard hat":         "worker",
    "skull":            "skull",
    "death":            "skull",
    "dead":             "skull",
    "died":             "skull",
    "toxic":            "skull",
    "pirate skull":     "skull",
    "skull crossbones": "skull_crossbones",
    "crossbones":       "skull_crossbones",
    "poison":           "skull_crossbones",
    "alcohol":          "skull_crossbones",
    "drug":             "skull_crossbones",
    "drugs":            "skull_crossbones",
    "chemical":         "skull_crossbones",
    "chemicals":        "skull_crossbones",
    "solvent":          "skull_crossbones",
    "pesticide":        "skull_crossbones",
    "hazardous":        "skull_crossbones",
    "ghost":            "ghost",
    "haunted":          "ghost",
    "spirit":           "ghost",
    "boo":              "ghost",
    "monster":          "monster",
    "ogre":             "monster",
    "creature":         "monster",
    "beast":            "monster",
    "demon":            "monster",
    "goblin":           "monster",
    "troll":            "troll",
    "middle finger":    "middle_finger",
    "flip off":         "middle_finger",
    "flipping off":     "middle_finger",
    "flipped off":      "middle_finger",
    "giving the bird":  "middle_finger",
    "the bird":         "middle_finger",
    "f you":            "middle_finger",
    "screw you":        "middle_finger",
    "damn":             "devil",
    "dammit":           "devil",
    "damnit":           "devil",
    "hell":             "devil",
    "devil":            "devil",
    "satan":            "devil",
    "evil":             "devil",
    "wtf":              "swearing",
    "what the":         "swearing",
    "cursing":          "swearing",
    "swearing":         "swearing",
    "profanity":        "swearing",
    "expletive":        "swearing",
    "cunt":             "swearing",
    "fuck":             "middle_finger",
    "fucking":          "middle_finger",
    "fucked":           "middle_finger",
    "fucker":           "middle_finger",
    "motherfucker":     "middle_finger",
    "what the fuck":    "middle_finger",
    "pussy":            "cat",
    "poop":             "poop",
    "poo":              "poop",
    "turd":             "poop",
    "crap":             "poop",
    "doo doo":          "poop",
    "doodoo":           "poop",
    "dookie":           "poop",
    "doody":            "poop",
    "number two":       "poop",
    "number 2":         "poop",
    "stinky":           "poop",
    "potty":            "poop",
    "feces":            "poop",
    "bowel movement":   "poop",
    "bathroom break":   "poop",
    "shit":             "poop",
    "shitty":           "poop",
    "bullshit":         "poop",
    "horseshit":        "poop",
    "shitstorm":        "poop",
    "holy shit":        "poop",
    "robot":            "robot",
    "robotics":         "robot",
    "android":          "robot",
    "cyborg":           "robot",
    "automaton":        "robot",
    "bot":              "robot",
    "clown":            "clown",
    "jester":           "clown",
    "circus clown":     "clown",
    "fairy":            "fairy",
    "pixie":            "fairy",
    "sprite":           "fairy",
    "tinkerbell":       "fairy",
    "mermaid":          "mermaid",
    "merman":           "mermaid",
    "siren":            "mermaid",
    "elf":              "elf",
    "elves":            "elf",
    "genie":            "genie",
    "djinn":            "genie",
    "magic wand":       "magic_wand",
    "magician":         "magic_wand",
    "abracadabra":      "magic_wand",

    # ── Professions ──────────────────────────────────────────────────────────
    "judge":            "prof_judge",
    "justice":          "prof_judge",
    "magistrate":       "prof_judge",
    "jury":             "prof_judge",
    "courtroom":        "prof_judge",
    "chef":             "prof_chef",
    "cook":             "prof_chef",
    "baker":            "prof_chef",
    "pastry chef":      "prof_chef",
    "sous chef":        "prof_chef",
    "culinary":         "prof_chef",
    "student":          "prof_student",
    "pupil":            "prof_student",
    "learner":          "prof_student",
    "undergraduate":    "prof_student",
    "scholar":          "prof_student",
    "academic":         "prof_student",
    "professor":        "prof_teacher",
    "teacher":          "prof_teacher",
    "tutor":            "prof_teacher",
    "lecturer":         "prof_teacher",
    "educator":         "prof_teacher",
    "instructor":       "prof_teacher",
    "farmer":           "prof_farmer",
    "rancher":          "prof_farmer",
    "agriculture":      "prof_farmer",
    "farming":          "prof_farmer",
    "livestock":        "prof_farmer",
    "gardener":         "herb",
    "gardening":        "herb",
    "horticulture":     "herb",
    "botanist":         "herb",
    "nursing":          "prof_medical",
    "paramedic":        "firstaid",
    "emt":              "firstaid",
    "firefighter":      "prof_firefighter",
    "fireman":          "prof_firefighter",
    "pilot":            "prof_pilot",
    "aviator":          "prof_pilot",
    "flight crew":      "prof_pilot",
    "captain":          "prof_pilot",
    "mechanic":         "prof_mechanic",
    "plumber":          "prof_mechanic",
    "electrician":      "lightning",
    "programmer":       "prof_coder",
    "coder":            "prof_coder",
    "software engineer":"prof_coder",
    "writer":           "pencil",
    "author":           "pencil",
    "journalist":       "pencil",
    "blogger":          "pencil",
    "novelist":         "pencil",
    "scientist":        "prof_scientist",
    "researcher":       "prof_scientist",
    "biologist":        "prof_scientist",
    "chemist":          "prof_scientist",
    "physicist":        "prof_scientist",
    "photographer":     "camera",
    "videographer":     "camera",
    "artist":           "prof_artist",
    "painter":          "prof_artist",
    "illustrator":      "prof_artist",
    "singer":           "prof_singer",
    "vocalist":         "prof_singer",
    "performer":        "prof_singer",

    # ── People / Gestures ────────────────────────────────────────────────────
    "thumbs up":        "thumbsup",
    "approved":         "thumbsup",
    "good job":         "thumbsup",
    "thumbs down":      "thumbsdown",
    "rejected":         "thumbsdown",
    "clap":             "clap",
    "clapping":         "clap",
    "applause":         "clap",
    "well done":        "clap",
    "bravo":            "clap",
    "handshake":        "handshake",
    "agreement":        "handshake",
    "deal":             "handshake",
    "partnership":      "handshake",
    "prayer":           "pray",
    "wishing":          "pray",
    "please":           "pray",
    "meditation":       "pray",
    "faith":            "pray",
    "worship":          "pray",
    "spiritual":        "pray",
    "religion":         "pray",
    "religious":        "pray",
    "bible":            "pray",
    "scripture":        "pray",
    "angel":            "angel",
    "angels":           "angel",
    "cherub":           "angel",
    "cherubs":          "angel",
    "halo":             "halo_face",
    "god":              "halo_face",
    "goddess":          "halo_face",
    "deity":            "halo_face",
    "divine":           "halo_face",
    "holy":             "halo_face",
    "sacred":           "halo_face",
    "blessed":          "halo_face",
    "blessing":         "halo_face",
    "saint":            "halo_face",
    "saintly":          "halo_face",
    "heaven":           "halo_face",
    "heavenly":         "halo_face",
    "almighty":         "halo_face",
    "cross":            "cross",
    "crucifix":         "cross",
    "jesus":            "cross",
    "christ":           "cross",
    "lord":             "cross",
    "savior":           "cross",
    "messiah":          "cross",
    "christian":        "cross",
    "christianity":     "cross",
    "crescent":         "moon",
    "islam":            "moon",
    "muslim":           "moon",
    "mosque":           "church",
    "star of david":    "star_of_david",
    "jewish":           "star_of_david",
    "judaism":          "star_of_david",
    "synagogue":        "church",
    "buddha":           "pray",
    "buddhism":         "pray",
    "buddhist":         "pray",
    "strength":         "muscle",
    "flexing":          "muscle",
    "crown":            "crown",
    "royalty":          "crown",
    "king":             "crown",
    "queen":            "crown",
    "vip":              "crown",
    "heart":            "heart",
    "hearts":           "heart",
    "love":             "heart",
    "romance":          "heart",
    "affection":        "heart",
    "i love":           "heart",
    "broken heart":     "broken_heart",
    "heartbreak":       "broken_heart",
    "eyes":             "eyes",
    "looking":          "eyes",
    "watching":         "eyes",
    "footprints":       "footprints",
    "footsteps":        "footprints",
    "tracks":           "footprints",

    # ── Gestures ─────────────────────────────────────────────────────────────
    "shrug":            "shrug",
    "shrugging":        "shrug",
    "whatever":         "shrug",
    "facepalm":         "facepalm",
    "doh":              "facepalm",
    "crossed fingers":  "crossed_fingers",
    "fingers crossed":  "crossed_fingers",
    "good luck":        "crossed_fingers",
    "peace":            "peace_sign",
    "peace sign":       "peace_sign",
    "victory sign":     "peace_sign",
    "hang loose":       "hang_loose",
    "call me":          "hang_loose",
    "rock on":          "rock_on",
    "heavy metal":      "rock_on",
    "horns":            "rock_on",
    "fist bump":        "fist_bump",
    "raised fist":      "fist_bump",

    # ── Greetings ────────────────────────────────────────────────────────────
    "hello":            "wave_hand",
    "hi":               "wave_hand",
    "hey":              "wave_hand",
    "howdy":            "wave_hand",
    "welcome":          "wave_hand",
    "greet":            "wave_hand",
    "greeting":         "wave_hand",
    "greetings":        "wave_hand",
    "wave hand":        "wave_hand",
    "waving":           "wave_hand",
    "bye":              "wave_hand",
    "goodbye":          "wave_hand",
    "farewell":         "wave_hand",

    # ── Questions ────────────────────────────────────────────────────────────
    "who":              "question_mark",
    "what":             "question_mark",
    "why":              "question_mark",
    "when":             "question_mark",
    "how":              "question_mark",
    "huh":              "question_mark",

    # ── Hazard / Safety ──────────────────────────────────────────────────────
    "radioactive":      "radioactive",
    "nuclear":          "radioactive",
    "radiation":        "radioactive",
    "atomic":           "radioactive",
    "biohazard":        "biohazard",
    "biological hazard":"biohazard",
    "hazmat":           "biohazard",
    "contaminated":     "biohazard",
    "prohibited":       "prohibited",
    "forbidden":        "prohibited",
    "no entry":         "prohibited",
    "not allowed":      "prohibited",
    "banned":           "prohibited",
    "off limits":       "prohibited",

    # Specific "no" signs — each has its own dedicated Unicode emoji
    "no smoking":       "no_smoking",
    "non smoking":      "no_smoking",
    "smoke free":       "no_smoking",
    "no cigarettes":    "no_smoking",
    "no littering":     "no_littering",
    "no litter":        "no_littering",
    "no dumping":       "no_littering",
    "keep clean":       "no_littering",
    "no pedestrians":   "no_pedestrians",
    "no walking":       "no_pedestrians",
    "pedestrians prohibited": "no_pedestrians",
    "no bicycles":      "no_bicycles",
    "no bikes":         "no_bicycles",
    "no cycling":       "no_bicycles",
    "bikes prohibited": "no_bicycles",
    "non potable":      "non_potable_water",
    "non potable water":"non_potable_water",
    "not drinking water":"non_potable_water",
    "do not drink":     "non_potable_water",
    "no phones":        "no_phones",
    "no cell phones":   "no_phones",
    "no mobile phones": "no_phones",
    "no cellphones":    "no_phones",
    "phone free":       "no_phones",
    "no under 18":      "no_under_18",
    "adults only":      "no_under_18",
    "18 plus":          "no_under_18",
    "age restricted":   "no_under_18",
    "mature":           "no_under_18",
    "shield":           "shield",
    "protection":       "shield",
    "armor":            "shield",
    "sword":            "sword",
    "swords":           "sword",
    "blade":            "sword",
    "medieval":         "sword",
    "knight":           "sword",
    "dagger":           "sword",

    # ── Emotions / Faces ─────────────────────────────────────────────────────
    "cry":              "face_cry",
    "crying":           "face_cry",
    "tears":            "face_cry",
    "sob":              "face_cry",
    "weeping":          "face_cry",
    "laugh":            "face_laugh",
    "laughing":         "face_laugh",
    "lol":              "face_laugh",
    "funny":            "face_laugh",
    "hilarious":        "face_laugh",
    "smile":            "face_smile",
    "smiling":          "face_smile",
    "grin":             "face_smile",
    "grinning":         "face_smile",
    "cheerful":         "face_smile",
    "sad":              "face_sad",
    "unhappy":          "face_sad",
    "frown":            "face_sad",
    "frowning":         "face_sad",
    "depressed":        "face_sad",
    "miserable":        "face_sad",
    "happy":            "face_happy",
    "happiness":        "face_happy",
    "joy":              "face_happy",
    "joyful":           "face_happy",
    "excited":          "face_happy",
    "delighted":        "face_happy",
    "angry":            "face_angry",
    "anger":            "face_angry",
    "furious":          "face_angry",
    "rage":             "face_angry",
    "mad":              "face_angry",
    "frustrated":       "face_angry",
    "bored":            "face_bored",
    "boring":           "face_bored",
    "boredom":          "face_bored",
    "expressionless":   "face_bored",
    "shocked":          "face_shocked",
    "shock":            "face_shocked",
    "surprised":        "face_shocked",
    "surprise":         "face_shocked",
    "astonished":       "face_shocked",
    "horrified":        "face_shocked",
    "lips":             "lips",
    "mouth":            "lips",
    "kiss":             "kiss",
    "kissing":          "kiss",
    "smooch":           "kiss",
    "xoxo":             "kiss",
    "hug":              "hug",
    "hugging":          "hug",
    "embrace":          "hug",
    "cuddle":           "hug",
    "melting":          "face_melt",
    "melting face":     "face_melt",
    "salute":           "face_salute",
    "saluting":         "face_salute",
    "yes sir":          "face_salute",
    "peeking":          "face_peek",
    "peeping":          "face_peek",
    "shy":              "face_peek",
    "hiding":           "face_peek",

    # ── Animals — Pets ───────────────────────────────────────────────────────
    "dog":              "dog",
    "puppy":            "dog",
    "dogs":             "dog",
    "cat":              "cat",
    "kitten":           "cat",
    "cats":             "cat",
    "rabbit":           "rabbit",
    "bunny":            "rabbit",
    "hamster":          "hamster",
    "guinea pig":       "hamster",
    "gerbil":           "hamster",

    # ── Animals — Birds ──────────────────────────────────────────────────────
    "parrot":           "parrot",
    "cockatiel":        "parrot",
    "macaw":            "parrot",
    "bird":             "bird",
    "parakeet":         "bird",
    "canary":           "bird",
    "eagle":            "eagle",
    "hawk":             "eagle",
    "falcon":           "eagle",
    "owl":              "owl",
    "penguin":          "penguin",
    "duck":             "duck",
    "duckling":         "duck",
    "swan":             "swan",
    "flamingo":         "flamingo",
    "peacock":          "peacock",
    "rooster":          "rooster",
    "hen":              "chicken",
    "chicken":          "chicken",
    "chickens":         "chicken",
    "chooks":           "chicken",
    "poultry":          "chicken",
    "chick":            "chick",
    "baby bird":        "chick",

    # ── Animals — Sea ────────────────────────────────────────────────────────
    "fish":             "fish",
    "aquarium":         "fish",
    "goldfish":         "fish",
    "shark":            "shark",
    "dolphin":          "dolphin",
    "whale":            "whale",
    "octopus":          "octopus",
    "crab":             "crab",
    "lobster":          "lobster",
    "shrimp":           "shrimp",
    "squid":            "squid",
    "jellyfish":        "jellyfish",
    "jelly fish":       "jellyfish",
    "worm":             "worm",
    "worms":            "worm",
    "earthworm":        "worm",
    "gummy worm":       "worm",
    "cockroach":        "cockroach",
    "roach":            "cockroach",
    "pest":             "cockroach",
    "seahorse":         "seahorse",
    "blowfish":         "blowfish",

    # ── Animals — Reptiles / Amphibians ──────────────────────────────────────
    "snake":            "snake",
    "turtle":           "turtle",
    "tortoise":         "turtle",
    "lizard":           "lizard",
    "gecko":            "lizard",
    "iguana":           "lizard",
    "crocodile":        "crocodile",
    "alligator":        "crocodile",
    "frog":             "frog",
    "toad":             "frog",
    "salamander":       "frog",
    "dinosaur":         "dinosaur",
    "dino":             "dinosaur",
    "trex":             "dinosaur",
    "dragon":           "dragon",

    # ── Animals — Insects ────────────────────────────────────────────────────
    "butterfly":        "butterfly",
    "bee":              "bee",
    "honeybee":         "bee",
    "bees":             "bee",
    "insect":           "bug",
    "caterpillar":      "bug",
    "ant":              "ant",
    "ants":             "ant",
    "ladybug":          "ladybug",
    "ladybird":         "ladybug",
    "spider":           "spider",
    "cricket":          "cricket",
    "mosquito":         "mosquito",
    "snail":            "snail",
    "beetle":           "beetle",
    "scarab":           "beetle",
    "bug":              "beetle",
    "crow":             "crow",
    "raven":            "crow",
    "blackbird":        "crow",

    # ── Animals — Farm / Wild ────────────────────────────────────────────────
    "horse":            "horse",
    "pony":             "horse",
    "unicorn":          "unicorn",
    "cow":              "cow",
    "cattle":           "cow",
    "dairy":            "cow",
    "pig":              "pig",
    "hog":              "pig",
    "sheep":            "sheep",
    "lamb":             "sheep",
    "goat":             "goat",
    "lion":             "lion",
    "tiger":            "tiger",
    "bear":             "bear",
    "grizzly":          "bear",
    "panda":            "panda",
    "koala":            "koala",
    "fox":              "fox",
    "wolf":             "wolf",
    "wolves":           "wolf",
    "elephant":         "elephant",
    "giraffe":          "giraffe",
    "zebra":            "zebra",
    "rhinoceros":       "rhino",
    "rhino":            "rhino",
    "hippo":            "hippo",
    "hippopotamus":     "hippo",
    "camel":            "camel",
    "gorilla":          "gorilla",
    "monkey":           "monkey",
    "ape":              "gorilla",
    "chimp":            "monkey",
    "hedgehog":         "hedgehog",
    "kangaroo":         "kangaroo",
    "llama":            "llama",
    "alpaca":           "llama",
    "sloth":            "sloth",
    "otter":            "otter",
    "beaver":           "beaver",
    "mouse":            "mouse",
    "rat":              "mouse",
    "deer":             "deer",
    "moose":            "moose",
    "elk":              "moose",
    "caribou":          "moose",
    "reindeer":         "deer",
    "boar":             "boar",
    "wild boar":        "boar",
    "bat":              "bat",
    "raccoon":          "raccoon",
    "racoon":           "raccoon",
    "trash panda":      "raccoon",
    "skunk":            "skunk",
    "badger":           "badger",
    "weasel":           "badger",
    "mink":             "badger",
    "ferret":           "badger",
    "chipmunk":         "chipmunk",
    "squirrel":         "chipmunk",
    "bison":            "bison",
    "buffalo":          "bison",
    "yak":              "bison",
    "wildebeest":       "bison",
    "dodo":             "dodo",
    "extinct":          "dodo",

    # Irregular plurals the auto-rule won't catch
    "mice":             "mouse",
    "geese":            "goose",
    "cacti":            "cactus",
    "fungi":            "mushroom",
    "octopi":           "octopus",

    # Generic pet
    "pet":              "pet",
    "animal":           "pet",
    "pet food":         "pet",
    "pet supplies":     "pet",
    "vet":              "pet",
    "kennel":           "pet",
    "collar":           "pet",
    "leash":            "pet",
    "litter":           "pet",

    # ── Seasons / Weather ────────────────────────────────────────────────────
    "snowflake":        "snowflake",
    "cold":             "snowflake",
    "frozen":           "snowflake",
    "freeze":           "snowflake",
    "refrigerate":      "snowflake",
    "keep cold":        "snowflake",
    "keep frozen":      "snowflake",
    "freezer":          "snowflake",
    "winter":           "snowflake",
    "snow":             "snowflake",
    "frost":            "snowflake",
    "icy":              "snowflake",
    "arctic":           "snowflake",
    "glacier":          "snowflake",
    "december":         "snowflake",
    "january":          "snowflake",
    "february":         "snowflake",
    "summer":           "summer",
    "sunny":            "summer",
    "sunshine":         "summer",
    "beach":            "beach",
    "pool":             "summer",
    "june":             "summer",
    "july":             "summer",
    "august":           "summer",
    "tropical":         "summer",
    "fall":             "autumn",
    "autumn":           "autumn",
    "harvest":          "autumn",
    "october":          "autumn",
    "november":         "autumn",
    "september":        "autumn",
    "pumpkin":          "autumn",
    "maple":            "autumn",
    "spring":           "spring",
    "bloom":            "spring",
    "blossom":          "spring",
    "seeds":            "spring",
    "planting":         "spring",
    "april":            "spring",
    "march":            "spring",
    "easter":           "spring",
    "rainbow":          "rainbow",
    "tornado":          "tornado",
    "hurricane":        "tornado",
    "cyclone":          "tornado",
    "storm":            "storm",
    "thunderstorm":     "storm",
    "lightning storm":  "storm",
    "wind":             "wind",
    "windy":            "wind",
    "breeze":           "wind",
    "breezy":           "wind",
    "gust":             "wind",
    "gusty":            "wind",
    "snowman":          "snowman",
    "snowmen":          "snowman",
    "rain":             "umbrella",
    "rainy":            "umbrella",
    "raining":          "umbrella",
    "umbrella":         "umbrella",
    "drizzle":          "umbrella",

    # ── Nature / Plants ──────────────────────────────────────────────────────
    "tree":             "tree",
    "trees":            "tree",
    "forest":           "tree",
    "woods":            "tree",
    "lumber":           "wood",
    "timber":           "wood",
    "palm":             "palm",
    "palm tree":        "palm",
    "cactus":           "cactus",
    "succulent":        "cactus",
    "desert plant":     "cactus",
    "rose":             "rose",
    "roses":            "rose",
    "petal":            "rose",
    "petals":           "rose",
    "sunflower":        "sunflower",
    "sunflowers":       "sunflower",
    "leaves":           "leaf",
    "tulip":            "tulip",
    "tulips":           "tulip",
    "flower":           "tulip",
    "flowers":          "tulip",
    "bouquet":          "bouquet",
    "floral":           "bouquet",
    "herb":             "herb",
    "herbs":            "herb",
    "plant":            "herb",
    "plants":           "herb",
    "seedling":         "seedling",
    "sprout":           "seedling",
    "growing":          "seedling",
    "potted plant":     "potted_plant",
    "houseplant":       "potted_plant",
    "indoor plant":     "potted_plant",
    "plant pot":        "potted_plant",
    "hibiscus":         "hibiscus",
    "tropical flower":  "hibiscus",
    "lotus":            "lotus",
    "lotus flower":     "lotus",
    "water lily":       "lotus",
    "coral":            "coral",
    "reef":             "coral",
    "coral reef":       "coral",
    "nest":             "nest",
    "bird nest":        "nest",
    "nesting":          "nest",
    "mushroom":         "mushroom",
    "clover":           "clover",
    "lucky":            "clover",
    "shamrock":         "clover",
    "leaf":             "leaf",
    "fallen leaf":      "leaf",
    "wave":             "wave_water",
    "waves":            "wave_water",
    "ocean":            "wave_water",
    "sea":              "wave_water",
    "mountain":         "mountain",
    "mountains":        "mountain",
    "volcano":          "volcano",
    "island":           "island",
    "earth":            "earth",
    "globe":            "earth",
    "world":            "earth",
    "planet earth":     "earth",
    "global":           "globe_meridians",
    "worldwide":        "globe_meridians",
    "international":    "globe_meridians",
    "internet":         "globe_meridians",
    "web":              "globe_meridians",
    "online":           "globe_meridians",

    # ── Space ────────────────────────────────────────────────────────────────
    "rocket":           "rocket",
    "launch":           "rocket",
    "spacecraft":       "rocket",
    "nasa":             "rocket",
    "space":            "rocket",
    "spaceship":        "rocket",
    "astronaut":        "astronaut",
    "cosmonaut":        "astronaut",
    "space suit":       "astronaut",
    "spacesuit":        "astronaut",
    "spacewalk":        "astronaut",
    "ufo":              "ufo",
    "alien":            "alien_face",
    "extraterrestrial": "alien_face",
    "martian":          "alien_face",
    "flying saucer":    "ufo",
    "planet":           "saturn",
    "saturn":           "saturn",
    "solar system":     "saturn",
    "telescope":        "telescope",
    "stargazing":       "telescope",
    "observatory":      "telescope",
    "moon":             "moon",
    "lunar":            "moon",
    "comet":            "comet",
    "meteor":           "comet",
    "asteroid":         "comet",
    "galaxy":           "galaxy",
    "milky way":        "galaxy",
    "nebula":           "galaxy",
    "cosmos":           "galaxy",
    "satellite":        "satellite",
    "orbit":            "satellite",
    "iss":              "satellite",

    # ── Electric / Power ─────────────────────────────────────────────────────
    "lightning":        "lightning",
    "thunder":          "lightning",
    "thunderbolt":      "lightning",
    "electric":         "lightning",
    "electronics":      "lightning",
    "battery":          "battery",
    "batteries":        "battery",
    "rechargeable":     "battery",
    "lithium":          "battery",
    "lipo":             "battery",
    "li-ion":           "battery",
    "lifepo4":          "battery",
    "lifepo":           "battery",
    "lithium iron":     "battery",
    "lithium iron phosphate": "battery",
    "lfp":              "battery",
    "18650":            "battery",
    "21700":            "battery",
    "26650":            "battery",
    "low battery":      "battery",
    "charger":          "lightning",
    "voltage":          "lightning",
    "generator":        "lightning",
    "solar":            "lightning",
    "wires":            "lightning",
    "wire":             "lightning",
    "power supply":     "lightning",
    "outlet":           "lightning",
    "electrical":       "lightning",
    "plug":             "plug",
    "connector":        "plug",
    "connectors":       "plug",
    "jack":             "plug",
    "socket":           "plug",
    "adapter":          "plug",
    "usb cable":        "plug",
    "hdmi":             "plug",

    # ── Electronic Components ─────────────────────────────────────────────────
    # Passive components → ⚡ (circuit/electrical symbol)
    "resistor":         "lightning",
    "resistors":        "lightning",
    "capacitor":        "lightning",
    "capacitors":       "lightning",
    "diode":            "lightning",
    "diodes":           "lightning",
    "rectifier":        "lightning",
    "zener":            "lightning",
    "schottky":         "lightning",
    "varistor":         "lightning",
    "thermistor":       "lightning",
    "fuse":             "lightning",
    "fuses":            "lightning",
    "relay":            "lightning",
    "relays":           "lightning",
    "oscillator":       "lightning",
    "resonator":        "lightning",
    "voltage regulator":"lightning",
    "regulator":        "lightning",
    "op-amp":           "lightning",
    "opamp":            "lightning",
    "comparator":       "lightning",
    "component":        "lightning",
    "electronic":       "lightning",
    # Inductive/magnetic → 🧲
    "inductor":         "magnet",
    "inductors":        "magnet",
    "coil":             "magnet",
    "coils":            "magnet",
    "transformer":      "magnet",
    "transformers":     "magnet",
    "toroid":           "magnet",
    "solenoid":         "magnet",
    "electromagnet":    "magnet",
    "motor driver":     "magnet",
    "stepper":          "gear",
    "stepper motor":    "gear",
    "servo":            "gear",
    "servo motor":      "gear",
    # LED → 💡
    "led":              "lightbulb",
    "leds":             "lightbulb",
    "light emitting":   "lightbulb",
    "neopixel":         "lightbulb",
    "ws2812":           "lightbulb",
    "rgb led":          "lightbulb",
    "addressable":      "lightbulb",
    # Transistors/active → ⚡
    "transistor":       "lightning",
    "transistors":      "lightning",
    "mosfet":           "lightning",
    "bjt":              "lightning",
    "fet":              "lightning",
    "igbt":             "lightning",
    "triac":            "lightning",
    "thyristor":        "lightning",
    # Microcontrollers/chips → 💻
    "microcontroller":  "computer",
    "microcontrollers": "computer",
    "microprocessor":   "computer",
    "mcu":              "computer",
    "cpu":              "computer",
    "ic":               "computer",
    "chip":             "computer",
    "chips":            "computer",
    "integrated circuit":"computer",
    "arduino":          "computer",
    "esp32":            "computer",
    "esp8266":          "computer",
    "stm32":            "computer",
    "atmega":           "computer",
    "pic microcontroller":"computer",
    "teensy":           "computer",
    "attiny":           "computer",
    "fpga":             "computer",
    "raspberry pi":     "computer",
    "pi pico":          "computer",
    "beaglebone":       "computer",
    "jetson":           "computer",
    # PCB / breadboard → ⚡
    "pcb":              "lightning",
    "circuit board":    "lightning",
    "breadboard":       "lightning",
    "protoboard":       "lightning",
    "perfboard":        "lightning",
    "veroboard":        "lightning",
    "schematic":        "ruler_tri",
    "wiring diagram":   "ruler_tri",
    # Test equipment → 🔬
    "oscilloscope":     "microscope",
    "multimeter":       "microscope",
    "voltmeter":        "microscope",
    "ammeter":          "microscope",
    "logic analyzer":   "microscope",
    "signal generator": "microscope",
    "bench supply":     "microscope",
    # Soldering → 🔧
    "solder":           "tools",
    "soldering":        "tools",
    "soldering iron":   "tools",
    "flux":             "tools",
    "desoldering":      "tools",
    "heat shrink":      "tools",
    "heatshrink":       "tools",
    "wire stripper":    "tools",
    "crimper":          "tools",
    "lightbulb":        "lightbulb",
    "idea":             "lightbulb",
    "bright":           "lightbulb",
    "light bulb":       "lightbulb",
    "lamp":             "lightbulb",
    "flashlight":       "flashlight_torch",
    "torch":            "flashlight_torch",
    "lantern":          "lightbulb",
    "candle":           "candle",
    "candles":          "candle",
    "matches":          "candle",
    "lighter":          "candle",

    # ── Paper / Documents ────────────────────────────────────────────────────
    "paper":            "paper_doc",
    "papers":           "paper_doc",
    "sheet":            "paper_doc",
    "document":         "paper_doc",
    "printout":         "paper_doc",
    "handout":          "paper_doc",
    "flyer":            "paper_doc",

    # ── Shopping ─────────────────────────────────────────────────────────────
    "shopping":         "shopping_cart",
    "shopping cart":    "shopping_cart",
    "cart":             "shopping_cart",
    "checkout":         "shopping_cart",
    "grocery":          "shopping_cart",
    "groceries":        "shopping_cart",
    "grocery store":    "shopping_cart",
    "grocery list":     "shopping_cart",
    "supermarket":      "shopping_cart",
    "publix":           "shopping_cart",
    "safeway":          "shopping_cart",
    "albertsons":       "shopping_cart",
    "wegmans":          "shopping_cart",
    "heb":              "shopping_cart",
    "h-e-b":            "shopping_cart",
    "meijer":           "shopping_cart",
    "giant":            "shopping_cart",
    "stop and shop":    "shopping_cart",
    "food lion":        "shopping_cart",
    "harris teeter":    "shopping_cart",
    "winn dixie":       "shopping_cart",
    "winn-dixie":       "shopping_cart",
    "shoprite":         "shopping_cart",
    "hannaford":        "shopping_cart",
    "hy-vee":           "shopping_cart",
    "winco":            "shopping_cart",
    "sprouts":          "shopping_cart",
    "market basket":    "shopping_cart",
    "price chopper":    "shopping_cart",
    "piggly wiggly":    "shopping_cart",
    "fresh market":     "shopping_cart",
    "natural grocers":  "shopping_cart",
    "food city":        "shopping_cart",
    "stater bros":      "shopping_cart",
    "walmart":          "shopping_cart",
    "costco":           "shopping_cart",
    "sam's club":       "shopping_cart",
    "kroger":           "shopping_cart",
    "whole foods":      "shopping_cart",
    "trader joes":      "shopping_cart",
    "aldi":             "shopping_cart",
    "lidl":             "shopping_cart",

    # ── Brand names ──────────────────────────────────────────────────────────
    # Specific menu items
    "whopper":          "burger",
    "big mac":          "burger",
    "quarter pounder":  "burger",
    "baconator":        "burger",
    "double double":    "burger",
    "mcnuggets":        "chicken",
    "nuggets":          "chicken",
    "chicken nuggets":  "chicken",
    "mcflurry":         "ice_cream",
    "blizzard storm":   "snowflake",
    "blizzard":         "ice_cream",
    "frosty":           "ice_cream",
    "dilly bar":        "ice_cream",
    "mcrib":            "food",
    "footlong":         "sandwich",
    "frappuccino":      "coffee",
    "pumpkin spice":    "coffee",
    "red bull":         "canned_food",
    "monster energy":   "canned_food",
    "gatorade":         "coffee",
    "powerade":         "coffee",
    # Snack brands
    "oreo":             "cookies",
    "chips ahoy":       "cookies",
    "nutter butter":    "cookies",
    "doritos":          "food",
    "cheetos":          "food",
    "pringles":         "canned_food",
    "lays":             "food",
    "lay's":            "food",
    "fritos":           "food",
    "ruffles":          "food",
    "m&ms":             "candy",
    "skittles":         "candy",
    "jolly rancher":    "candy",
    "reeses":           "chocolate",
    "reese's":          "chocolate",
    "kit kat":          "chocolate",
    "snickers":         "chocolate",
    "twix":             "chocolate",
    "hersheys":         "chocolate",
    "hershey's":        "chocolate",
    "nutella":          "chocolate",
    "twinkies":         "cupcake",
    "ho hos":           "cupcake",
    "little debbie":    "cupcake",
    "pop tarts":        "food",
    "lucky charms":     "food",
    "cheerios":         "food",
    "frosted flakes":   "food",
    "fruit loops":      "food",
    # Electronics / headphones
    "airpods":          "headphones_icon",
    "beats":            "headphones_icon",
    "bose":             "headphones_icon",
    "sony headphones":  "headphones_icon",
    "jabra":            "headphones_icon",
    "sennheiser":       "headphones_icon",
    # Speakers
    "jbl":              "music",
    "sonos":            "music",
    "harman":           "music",
    # Phones / tablets
    "iphone":           "phone",
    "samsung":          "phone",
    "pixel phone":      "phone",
    "oneplus":          "phone",
    "ipad":             "computer",
    "macbook":          "computer",
    "imac":             "computer",
    "surface":          "computer",
    "chromebook":       "computer",
    "kindle":           "books",
    "apple watch":      "time",
    "fitbit":           "time",
    "garmin":           "time",
    # Streaming
    "netflix":          "tv",
    "hulu":             "tv",
    "disney plus":      "tv",
    "hbo":              "tv",
    "youtube":          "tv",
    "twitch":           "tv",
    "tiktok":           "camera",
    # Music
    "spotify":          "music",
    "apple music":      "music",
    "pandora":          "music",
    "soundcloud":       "music",
    # Food brands
    "mcdonalds":        "burger",
    "mcdonald's":       "burger",
    "burger king":      "burger",
    "wendy's":          "burger",
    "wendys":           "burger",
    "five guys":        "burger",
    "in n out":         "burger",
    "kfc":              "chicken",
    "popeyes":          "chicken",
    "chick-fil-a":      "chicken",
    "chick fil a":      "chicken",
    "raising canes":    "chicken",
    "pizza hut":        "pizza",
    "dominos":          "pizza",
    "domino's":         "pizza",
    "papa johns":       "pizza",
    "little caesars":   "pizza",
    "subway":           "sandwich",
    "jimmy johns":      "sandwich",
    "jersey mikes":     "sandwich",
    "starbucks":        "coffee",
    "dunkin":           "coffee",
    "tim hortons":      "coffee",
    "peet's":           "coffee",
    "chipotle":         "food",
    "taco bell":        "food",
    "olive garden":     "food",
    "applebees":        "food",
    "panera":           "food",
    # Home improvement
    "home depot":       "tools",
    "lowes":            "tools",
    "lowe's":           "tools",
    "menards":          "tools",
    # Furniture
    "ikea":             "couch",
    "wayfair":          "couch",
    # Gaming
    "nintendo":         "gaming",
    "playstation":      "gaming",
    "xbox":             "gaming",
    "steam":            "gaming",
    "gamestop":         "gaming",
    "ps5":              "gaming",
    "ps4":              "gaming",
    "switch":           "gaming",
    # Auto brands
    "tesla":            "car",
    "ford":             "car",
    "chevy":            "car",
    "chevrolet":        "car",
    "toyota":           "car",
    "honda":            "car",
    "bmw":              "car",
    "mercedes":         "car",
    "audi":             "car",
    "dodge":            "car",
    "ram truck":        "car",
    "jeep":             "car",
    "subaru":           "car",
    "hyundai":          "car",
    "kia":              "car",
    "volkswagen":       "car",
    "vw":               "car",
    # Shipping
    "ups":              "mail",
    "fedex":            "mail",
    "dhl":              "mail",
    "usps":             "mail",
    "post office":      "mail",
    # Online services
    "amazon":           "package_box",
    "ebay":             "package_box",
    "etsy":             "package_box",
    "shopify":          "package_box",
    # Social media
    "instagram":        "camera",
    "snapchat":         "camera",
    "facebook":         "computer",
    "twitter":          "computer",
    "linkedin":         "computer",
    "pinterest":        "art",
    "reddit":           "computer",
    "discord":          "computer",
    "slack":            "computer",
    "whatsapp":         "phone",
    "imessage":         "phone",
    "signal app":       "phone",
    "zoom":             "computer",
    "teams":            "computer",
    # Smart home
    "roomba":           "cleaning",
    "alexa device":     "computer",
    "google home":      "computer",
    "amazon echo":      "computer",
    "ring doorbell":    "bell",
    "nest thermostat":  "thermometer",
    "gopro":            "camera",
    "ring camera":      "camera",
    # Streaming hardware
    "apple tv":         "tv",
    "chromecast":       "tv",
    "fire tv":          "tv",
    "roku":             "tv",
    "oculus":           "gaming",
    "quest":            "gaming",
    # Clothing / shoes
    "nike":             "shoe",
    "adidas":           "shoe",
    "new balance":      "shoe",
    "converse":         "shoe",
    "vans shoes":       "shoe",
    "jordan":           "shoe",
    "yeezy":            "shoe",
    "timberland":       "shoe",
    "uggs":             "shoe",
    "crocs":            "shoe",
    "levis":            "jeans",
    "levi's":           "jeans",
    "wranglers":        "jeans",
    # Tools brands
    "dewalt":           "tools",
    "milwaukee":        "tools",
    "makita":           "tools",
    "snap-on":          "tools",
    "craftsman":        "tools",
    "ryobi":            "tools",
    "bosch":            "tools",
    "black and decker": "tools",
    "black & decker":   "tools",
    "stanley tools":    "tools",
    # Outdoors / camping
    "yeti cooler":      "coffee",
    "yeti cup":         "coffee",
    "stanley cup":      "coffee",
    "hydroflask":       "coffee",
    "nalgene":          "coffee",
    "coleman":          "camping",
    "rei":              "camping",
    "north face":       "clothes",
    "patagonia":        "clothes",
    "carhartt":         "clothes",
    # Health / medicine brands
    "tylenol":          "medicine",
    "advil":            "medicine",
    "ibuprofen":        "medicine",
    "nyquil":           "medicine",
    "dayquil":          "medicine",
    "benadryl":         "medicine",
    "band-aid":         "firstaid",
    "bandaid":          "firstaid",
    "neosporin":        "firstaid",
    "chapstick":        "lips",
    "colgate":          "toothbrush",
    "crest":            "toothbrush",
    "listerine":        "toothbrush",
    # Toys / games
    "lego":             "gaming",
    "barbie":           "girl",
    "hot wheels":       "car",
    "nerf":             "sports",
    "monopoly":         "gaming",
    "scrabble":         "gaming",
    # Travel / transport
    "lyft":             "taxi",
    "airbnb":           "home",
    "delta airlines":   "travel",
    "united airlines":  "travel",
    "southwest":        "travel",
    "american airlines":"travel",

    # ── Computer / Tech ──────────────────────────────────────────────────────
    "floppy":           "floppy_disk",
    "floppy disk":      "floppy_disk",
    "diskette":         "floppy_disk",
    "save":             "floppy_disk",
    "saved":            "floppy_disk",
    "saving":           "floppy_disk",
    "unsaved":          "floppy_disk",
    "cd":               "cd",
    "disc":             "cd",
    "optical disc":     "cd",
    "cd-rom":           "cd",
    "cdrom":            "cd",
    "cd rom":           "cd",
    "audio cd":         "cd",
    "music cd":         "cd",
    "dvd":              "dvd",
    "blu-ray":          "dvd",
    "bluray":           "dvd",
    "blu ray":          "dvd",
    "movie disc":       "dvd",
    "developer":        "computer",
    "computer":         "computer",
    "laptop":           "computer",
    "tech":             "computer",
    "software":         "computer",
    "server":           "computer",
    "backup":           "computer",
    "hard drive":       "computer",
    "usb":              "computer",
    "monitor":          "computer",
    "desktop":          "computer",
    "tablet":           "computer",
    "programming":      "computer",
    "coding":           "computer",
    "wifi":             "wireless",
    "wi-fi":            "wireless",
    "wlan":             "wireless",
    "wireless":         "wireless",
    "hotspot":          "wireless",
    "access point":     "wireless",
    "rfid":             "wireless",
    "nfc":              "wireless",
    "near field":       "wireless",
    "bluetooth":        "wireless",
    "zigbee":           "wireless",
    "z-wave":           "wireless",
    "network":          "computer",
    "router":           "computer",
    "signal":           "signal_bars",
    "reception":        "signal_bars",
    "cell signal":      "signal_bars",
    "cellular":         "signal_bars",
    "4g":               "signal_bars",
    "5g":               "signal_bars",
    "lte":              "signal_bars",
    "no signal":        "signal_bars",
    "dead zone":        "signal_bars",
    "phone":            "phone",
    "contact":          "phone",
    "call":             "phone",
    "mobile":           "phone",
    "smartphone":       "phone",
    "voicemail":        "phone",
    "television":       "tv",
    "tv":               "tv",
    "streaming":        "tv",
    "watch tv":         "tv",

    # ── Kitchen / Cooking ────────────────────────────────────────────────────
    "kitchen":          "kitchen",
    "cooking":          "kitchen",
    "utensils":         "kitchen",
    "cookware":         "kitchen",
    "pots":             "kitchen",
    "pans":             "kitchen",
    "bakeware":         "kitchen",
    "cutlery":          "kitchen",
    "fork":             "kitchen",
    "knife":            "kitchen",
    "spoon":            "kitchen",
    "utensil":          "kitchen",
    "silverware":       "kitchen",
    "spices":           "kitchen",
    "barbecue":         "bbq",
    "grill":            "bbq",
    "bbq":              "bbq",
    "grilling":         "bbq",

    # ── Food — Fruit ─────────────────────────────────────────────────────────
    "apple":            "apple",
    "apples":           "apple",
    "banana":           "banana",
    "bananas":          "banana",
    "grape":            "grapes",
    "grapes":           "grapes",
    "strawberry":       "strawberry",
    "strawberries":     "strawberry",
    "berry":            "strawberry",
    "berries":          "strawberry",
    "blueberry":        "blueberry",
    "blueberries":      "blueberry",
    "watermelon":       "watermelon",
    "melon":            "watermelon",
    "lemon":            "lemon",
    "lemons":           "lemon",
    "citrus":           "lemon",
    "lime":             "lemon",
    "orange":           "orange_fruit",
    "oranges":          "orange_fruit",
    "tangerine":        "orange_fruit",
    "pineapple":        "pineapple",
    "mango":            "mango",
    "cherry":           "cherry",
    "cherries":         "cherry",
    "peach":            "peach",
    "butt":             "peach",
    "ass":              "peach",
    "booty":            "peach",
    "bum":              "peach",
    "tush":             "peach",
    "tushy":            "peach",
    "rear end":         "peach",
    "backside":         "peach",
    "buttocks":         "peach",
    "badonk":           "peach",
    "rump":             "peach",
    "buns":             "peach",
    "pear":             "pear",
    "kiwi":             "kiwi",
    "coconut":          "coconut",

    # ── Food — Vegetables ────────────────────────────────────────────────────
    "avocado":          "avocado",
    "guacamole":        "avocado",
    "carrot":           "carrot",
    "carrots":          "carrot",
    "corn":             "corn",
    "broccoli":         "broccoli",
    "vegetables":       "broccoli",
    "veggie":           "broccoli",
    "tomato":           "tomato",
    "tomatoes":         "tomato",
    "potato":           "potato",
    "potatoes":         "potato",
    "onion":            "onion",
    "garlic":           "garlic",
    "pepper":           "pepper",
    "chili":            "pepper",
    "hot pepper":       "pepper",
    "eggplant":         "eggplant",
    "aubergine":        "eggplant",
    "dick":             "eggplant",
    "penis":            "eggplant",
    "wiener":           "eggplant",
    "willy":            "eggplant",
    "cucumber":         "cucumber",
    "gherkin":          "cucumber",
    "pickle":           "cucumber",
    "bell pepper":      "bell_pepper",
    "capsicum":         "bell_pepper",
    "green pepper":     "bell_pepper",
    "sweet potato":     "sweet_potato",
    "yam":              "sweet_potato",
    "chestnut":         "chestnut",
    "acorn":            "chestnut",
    "leafy greens":     "salad",
    "lettuce":          "leafy_greens",
    "spinach":          "leafy_greens",
    "bok choy":         "leafy_greens",
    "kale":             "leafy_greens",
    "cabbage":          "leafy_greens",
    "salad":            "salad",

    # ── Food — Meals / Savoury ───────────────────────────────────────────────
    "pizza":            "pizza",
    "burger":           "burger",
    "hamburger":        "burger",
    "cheeseburger":     "burger",
    "fries":            "fries",
    "hot dog":          "hotdog",
    "hotdog":           "hotdog",
    "sausage":          "hotdog",
    "taco":             "taco",
    "tacos":            "taco",
    "mexican":          "taco",
    "burrito":          "burrito",
    "sandwich":         "sandwich",
    "sub":              "sandwich",
    "food wrap":        "burrito",
    "wrap sandwich":    "burrito",
    "noodles":          "noodles",
    "ramen":            "noodles",
    "pasta":            "noodles",
    "spaghetti":        "noodles",
    "sushi":            "sushi",
    "japanese food":    "sushi",
    "chopsticks":       "chopsticks",
    "chopstick":        "chopsticks",
    "rice":             "rice",
    "fried rice":       "rice",
    "curry":            "curry",
    "stew":             "stew",
    "soup":             "stew",
    "bread":            "bread",
    "sourdough":        "bread",
    "rolls":            "bread",
    "baguette":         "bread",
    "toast":            "bread",
    "cheese":           "cheese",
    "meat":             "meat",
    "steak":            "meat",
    "beef":             "meat",
    "pork":             "meat",
    "bacon":            "bacon",
    "egg":              "egg",
    "eggs":             "egg",
    "omelette":         "egg",
    "fried egg":        "egg",
    "scrambled":        "egg",
    "pancake":          "pancake",
    "pancakes":         "pancake",
    "crepe":            "pancake",
    "waffle":           "waffle",
    "waffles":          "waffle",
    "breakfast":        "breakfast",
    "brunch":           "breakfast",
    "salt":             "salt",
    "salty":            "salt",
    "seasoning":        "salt",
    "spice":            "salt",
    "butter":           "butter",
    "margarine":        "butter",
    "cookies":          "cookies",
    "cookie":           "cookies",

    # ── Food — Sweet ─────────────────────────────────────────────────────────
    "cake":             "birthday",
    "birthday cake":    "birthday",
    "ice cream":        "ice_cream",
    "gelato":           "ice_cream",
    "sorbet":           "ice_cream",
    "popsicle":         "ice_cream",
    "donut":            "donut",
    "doughnut":         "donut",
    "cupcake":          "cupcake",
    "muffin":           "cupcake",
    "fudge":            "chocolate",
    "chocolate":        "chocolate",
    "candy":            "candy",
    "sweets":           "candy",
    "lollipop":         "lollipop",
    "honey":            "honey",
    "syrup":            "honey",
    "croissant":        "croissant",
    "pretzel":          "pretzel",
    "bagel":            "bagel",
    "hotpot":           "hotpot",
    "hot pot":          "hotpot",
    "fondue":           "hotpot",
    "stew pot":         "hotpot",
    "pie":              "pie",
    "custard":          "pie",
    "pudding":          "pie",
    "cheesecake":       "pie",

    # ── Food — Generic ───────────────────────────────────────────────────────
    "food":             "food",
    "lunch":            "food",
    "dinner":           "food",
    "snacks":           "food",
    "meal prep":        "food",
    "leftovers":        "food",
    "recipe":           "food",
    "baking":           "food",
    "pantry":           "food",
    "dessert":          "food",
    "meal":             "food",
    "snack":            "food",
    "treat":            "food",
    "plate":            "food",
    "bowl":             "food",
    "dish":             "food",
    "dishes":           "food",
    "tableware":        "food",
    "dinnerware":       "food",

    # ── Drinks ───────────────────────────────────────────────────────────────
    "coffee":           "coffee",
    "espresso":         "coffee",
    "latte":            "coffee",
    "cappuccino":       "coffee",
    "cafe":             "coffee",
    "tea":              "tea",
    "chai":             "tea",
    "green tea":        "tea",
    "herbal tea":       "tea",
    "hot chocolate":    "hot_choc",
    "cocoa":            "hot_choc",
    "beer":             "beer",
    "brewing":          "beer",
    "brewery":          "beer",
    "ale":              "beer",
    "lager":            "beer",
    "wine":             "wine",
    "winery":           "wine",
    "vineyard":         "wine",
    "champagne":        "champagne",
    "sparkling wine":   "champagne",
    "cocktail":         "cocktail",
    "bartending":       "cocktail",
    "mixology":         "cocktail",
    "tropical drink":   "tropical_drink",
    "smoothie":         "tropical_drink",
    "juice":            "juice",
    "orange juice":     "juice",
    "lemonade":         "juice",
    "milk":             "milk",
    "dairy milk":       "milk",
    "milkshake":        "milk",
    "water":            "water",
    "hydration":        "water",
    "beverages":        "coffee",
    "drinks":           "coffee",
    "mugs":             "coffee",
    "thermos":          "coffee",
    "whiskey":          "spirits",
    "whisky":           "spirits",
    "bourbon":          "spirits",
    "scotch":           "spirits",
    "rum":              "spirits",
    "vodka":            "spirits",
    "gin":              "spirits",
    "tequila":          "spirits",
    "spirits":          "spirits",
    "liquor":           "spirits",
    "bubble tea":       "bubble_tea",
    "boba":             "bubble_tea",
    "boba tea":         "bubble_tea",
    "milk tea":         "bubble_tea",
    "teapot":           "teapot",
    "kettle":           "teapot",
    "soda":             "straw_drink",
    "pop":              "straw_drink",
    "soft drink":       "straw_drink",
    "lemonade cup":     "straw_drink",
    "peanut":           "peanut",
    "peanuts":          "peanut",
    "groundnut":        "peanut",
    "peanut butter":    "peanut",
    "nuts":             "peanut",
    "almond":           "peanut",
    "cashew":           "peanut",
    "walnut snack":     "peanut",
    "pecan":            "peanut",
    "pistachio":        "peanut",
    "hazelnut":         "peanut",
    "beans":            "beans",
    "lentils":          "beans",
    "chickpeas":        "beans",
    "legumes":          "beans",
    "edamame":          "beans",
    "soybeans":         "beans",
    "coffee beans":     "beans",
    "jar":              "jar",
    "mason jar":        "jar",
    "jam jar":          "jar",
    "preserves":        "jar",
    "pickles":          "jar",
    "bubbles":          "bubbles",
    "fizzy":            "bubbles",
    "carbonated":       "bubbles",
    "sparkling":        "bubbles",
    "foam":             "bubbles",
    "soap bubbles":     "bubbles",
    "falafel":          "falafel",
    "hummus":           "falafel",
    "pita":             "falafel",
    "gyro":             "falafel",
    "shawarma":         "falafel",
    "kebab":            "falafel",
    "dumpling":         "dumpling",
    "dumplings":        "dumpling",
    "gyoza":            "dumpling",
    "potsticker":       "dumpling",
    "ravioli":          "dumpling",
    "wonton":           "dumpling",

    # ── Music ────────────────────────────────────────────────────────────────
    "guitar":           "guitar",
    "acoustic":         "guitar",
    "bass guitar":      "guitar",
    "ukulele":          "guitar",
    "banjo":            "banjo_icon",
    "piano":            "piano",
    "keyboard":         "computer_keyboard",
    "piano keyboard":   "piano",
    "music keyboard":   "piano",
    "electronic keyboard": "piano",
    "organ":            "piano",
    "synthesizer":      "piano",
    "drums":            "drums",
    "drumkit":          "drums",
    "percussion":       "drums",
    "trumpet":          "trumpet",
    "trombone":         "trumpet",
    "horn":             "trumpet",
    "bugle":            "trumpet",
    "violin":           "violin",
    "cello":            "violin",
    "viola":            "violin",
    "fiddle":           "violin",
    "saxophone":        "saxophone",
    "sax":              "saxophone",
    "clarinet":         "saxophone",
    "flute":            "flute",
    "microphone":       "microphone",
    "singing":          "microphone",
    "vocals":           "microphone",
    "mic":              "microphone",
    "karaoke":          "microphone",
    "music":            "music",
    "records":          "music",
    "vinyl":            "music",
    "headphones":       "headphones_icon",
    "earphones":        "headphones_icon",
    "earbuds":          "headphones_icon",
    "speakers":         "music",
    "studio":           "music",
    "album":            "music",
    "band":             "music",
    "concert":          "music",
    "choir":            "music",
    "playlist":         "music",
    "podcast":          "music",
    "radio":            "radio",

    # ── Sports ───────────────────────────────────────────────────────────────
    "baseball":         "baseball",
    "softball":         "baseball",
    "basketball":       "basketball",
    "football":         "football",
    "nfl":              "football",
    "soccer":           "soccer",
    "futbol":           "soccer",
    "tennis":           "tennis",
    "pickleball":       "tennis",
    "golf":             "golf",
    "bowling":          "bowling",
    "volleyball":       "volleyball",
    "skiing":           "skiing",
    "snowboarding":     "skiing",
    "swimming":         "swimming",
    "swimmer":          "swimming",
    "swim":             "swimming",
    "lifeguard":        "swimming",
    "surfer":           "surfer",
    "surf":             "surfer",
    "surfing":          "surfer",
    "cycling":          "cycling",
    "biking":           "cycling",
    "boxing":           "boxing",
    "mma":              "boxing",
    "wrestling":        "wrestling",
    "sumo":             "wrestling",
    "grappling":        "wrestling",
    "gymnastics":       "gymnastics",
    "gymnast":          "gymnastics",
    "tumbling":         "gymnastics",
    "acrobatics":       "gymnastics",
    "fencing":          "fencing",
    "swordfighting":    "fencing",
    "table tennis":     "tabletennis",
    "ping pong":        "tabletennis",
    "curling":          "curling",
    "badminton":        "badminton",
    "shuttlecock":      "badminton",
    "running":          "running",
    "runner":           "running",
    "jogging":          "running",
    "jogger":           "running",
    "marathon":         "running",
    "athlete":          "running",
    "athletics":        "running",
    "hiker":            "hiking_boot",
    "hiking":           "hiking_boot",
    "trekking":         "hiking_boot",
    "trekker":          "hiking_boot",
    "mountaineer":      "climbing",
    "dance":            "dancer",
    "dancer":           "dancer",
    "dancing":          "dancer",
    "ballet":           "dancer",
    "ballroom":         "dancer",
    "salsa":            "dancer",
    "yoga":             "yoga",
    "pilates":          "yoga",
    "camping":          "camping",
    "backpacking":      "camping",
    "fishing":          "fishing",
    "angling":          "fishing",
    "kayaking":         "kayaking",
    "rowing":           "kayaking",
    "rock climbing":    "climbing",
    "climbing":         "climbing",
    "skateboarding":    "skateboard",
    "skating":          "skateboard",
    "rollerskating":    "roller_skate",
    "roller skate":     "roller_skate",
    "roller skating":   "roller_skate",
    "rollerblade":      "roller_skate",
    "rollerblading":    "roller_skate",
    "inline skate":     "roller_skate",
    "karate":           "martial_arts",
    "martial arts":     "martial_arts",
    "judo":             "martial_arts",
    "taekwondo":        "martial_arts",
    "hockey":           "hockey",
    "ice hockey":       "hockey",
    "ice":              "ice",       # after "ice cream", "ice hockey" so compounds match first
    "archery":          "archery",
    "bow and arrow":    "archery",
    "sports":           "sports",
    "diving":           "diving",
    "scuba":            "diving",
    "snorkeling":       "diving",
    "underwater":       "diving",
    "scuba diving":     "diving",
    "target store":     "shopping_cart",
    "target":           "dart",
    "bullseye":         "dart",
    "darts":            "dart",
    "dart":             "dart",
    "boomerang":        "boomerang",
    "circus":           "circus",
    "big top":          "circus",
    "carnival":         "circus",
    "fairground":       "circus",
    "yoyo":             "yoyo",
    "yo-yo":            "yoyo",
    "spinning top":     "yoyo",

    # ── Gaming ───────────────────────────────────────────────────────────────
    "chess":            "chess",
    "checkers":         "chess",
    "games":            "gaming",
    "gaming":           "gaming",
    "console":          "gaming",
    "controller":       "gaming",
    "arcade":           "gaming",
    "boardgames":       "gaming",
    "cards":            "gaming",
    "dice":             "dice_icon",
    "die":              "dice_icon",
    "d6":               "dice_icon",
    "d20":              "dice_icon",
    "tabletop":         "dice_icon",
    "poker":            "gaming",
    "playing cards":    "card_spade",
    "card deck":        "card_spade",
    "card game":        "card_spade",
    "spades":           "card_spade",
    "clubs":            "card_club",
    "diamonds":         "card_diamond",
    "hearts card":      "card_heart",
    "puzzle":           "puzzle_icon",
    "jigsaw":           "puzzle_icon",
    "jigsaw puzzle":    "puzzle_icon",
    "brainteaser":      "puzzle_icon",

    # ── Art / Craft ──────────────────────────────────────────────────────────
    "art":              "art",
    "craft":            "art",
    "paint":            "art",
    "drawing":          "art",
    "brushes":          "art",
    "canvas":           "art",
    "markers":          "art",
    "knitting":         "yarn",
    "crochet":          "thread",
    "embroidery":       "thread",
    "fabric":           "thread",
    "scrapbook":        "art",
    "watercolor":       "art",
    "sculpture":        "art",
    "origami":          "art",
    "jewelry":          "art",
    "woodworking":      "art",
    "photography":      "camera",

    # ── Home / Rooms ─────────────────────────────────────────────────────────
    "bedroom":          "bedroom",
    "bed":              "bedroom",
    "sleep":            "bedroom",
    "pillow":           "bedroom",
    "blanket":          "bedroom",
    "linens":           "bedroom",
    "mattress":         "bedroom",
    "sheets":           "bedroom",
    "duvet":            "bedroom",
    "bathroom":         "bathroom",
    "bath":             "bathroom",
    "shower":           "bathroom",
    "toilet":           "toilet",
    "loo":              "toilet",
    "restroom":         "restroom_sign",
    "restrooms":        "restroom_sign",
    "washroom":         "restroom_sign",
    "lavatory":         "restroom_sign",
    "wc":               "restroom_sign",
    "comfort room":     "restroom_sign",
    "facilities":       "restroom_sign",
    "bathtub":          "bathtub",
    "tub":              "bathtub",
    "towel":            "bathroom",
    "sink":             "bathroom",
    "soap":             "soap",
    "shampoo":          "soap",
    "conditioner":      "soap",
    "body wash":        "soap",
    "toothbrush":       "toothbrush",
    "toothpaste":       "toothbrush",
    "razor":            "razor",
    "shaving":          "razor",
    "mirror":           "mirror",
    "sponge":           "sponge",
    "loofah":           "sponge",
    "plunger":          "plunger",
    "bucket":           "bucket",
    "pail":             "bucket",
    "home":             "home",
    "house":            "home",
    "living room":      "home",
    "dining room":      "home",
    "basement":         "home",
    "attic":            "home",
    "closet":           "home",
    "moving":           "home",
    "furniture":        "home",
    "decor":            "home",
    "guest room":       "home",
    "patio":            "home",
    "couch":            "couch",
    "sofa":             "couch",
    "loveseat":         "couch",
    "chair":            "chair",
    "stool":            "chair",
    "recliner":         "chair",
    "armchair":         "chair",
    "seat":             "chair",
    "teddy bear":       "teddy_bear",
    "teddy":            "teddy_bear",
    "stuffed animal":   "teddy_bear",
    "plush":            "teddy_bear",
    "nesting doll":     "nesting_dolls",
    "nesting dolls":    "nesting_dolls",
    "matryoshka":       "nesting_dolls",
    "russian doll":     "nesting_dolls",
    "mousetrap":        "mousetrap",
    "mouse trap":       "mousetrap",
    "trap":             "mousetrap",
    "hut":              "hut",
    "cabin":            "hut",
    "shack":            "hut",
    "shed":             "hut",
    "bungalow":         "hut",
    "headstone":        "headstone",
    "gravestone":       "headstone",
    "tombstone":        "headstone",
    "grave":            "headstone",
    "cemetery":         "headstone",
    "graveyard":        "headstone",
    "rip":              "headstone",
    "door":             "door",
    "entrance":         "door",
    "exit":             "door",
    "window":           "window",

    # ── Books / Office ───────────────────────────────────────────────────────
    "book":             "books",
    "books":            "books",
    "library":          "books",
    "reading":          "books",
    "documents":        "books",
    "paperwork":        "books",
    "office":           "books",
    "school":           "books",
    "notebook":         "books",
    "journal":          "books",
    "notes":            "books",
    "study":            "books",
    "homework":         "books",
    "textbook":         "books",
    "manual":           "books",
    "magazine":         "books",
    "binder":           "books",
    "folder":           "folder_icon",
    "directory":        "folder_icon",
    "pencil":           "pencil",
    "pen":              "pencil",
    "stationery":       "pencil",
    "writing":          "pencil",
    "sketch":           "pencil",
    "crayon":           "crayon",
    "crayons":          "crayon",
    "wax crayon":       "crayon",
    "paperclip":        "paperclip",
    "paper clip":       "paperclip",
    "binder clip":      "paperclip",
    "clip":             "paperclip",
    "needle":           "needle",
    "needles":          "needle",
    "sewing needle":    "needle",
    "string":           "thread",
    "twine":            "thread",
    "knot":             "knot",
    "knots":            "knot",
    "rope":             "knot",
    "lasso":            "knot",
    "tied":             "knot",
    "chart":            "chart",
    "graph":            "chart",
    "data":             "chart",
    "spreadsheet":      "chart",
    "report":           "chart",
    "clipboard":        "clipboard",
    "checklist":        "clipboard",
    "newspaper":        "newspaper",
    "news":             "newspaper",
    "article":          "newspaper",
    "magnify":          "magnify",
    "search":           "magnify",
    "investigate":      "magnify",

    # ── Tools / Garage ───────────────────────────────────────────────────────
    "tools":            "tools",
    "garage":           "tools",
    "hardware":         "tools",
    "workshop":         "tools",
    "repair":           "tools",
    "wrench":           "tools",
    "spanner":          "tools",
    "pliers":           "tools",
    "drill":            "tools",
    "drill bit":        "tools",
    "drill bits":       "tools",
    "nail":             "tools",
    "nails":            "tools",
    "screw":            "tools",
    "screws":           "tools",
    "plumbing":         "tools",
    "hammer":           "hammer",
    "mallet":           "hammer",
    "sledgehammer":     "hammer",
    "screwdriver":      "screwdriver",
    "flathead":         "screwdriver",
    "phillips":         "screwdriver",
    "torx":             "screwdriver",
    "allen":            "screwdriver",
    "hex key":          "screwdriver",
    "saw":              "saw_tool",
    "handsaw":          "saw_tool",
    "hacksaw":          "saw_tool",
    "jigsaw saw":       "saw_tool",
    "circular saw":     "saw_tool",
    "miter saw":        "saw_tool",
    "table saw":        "saw_tool",
    "axe":              "axe",
    "hatchet":          "axe",
    "chisel":           "axe",
    "clamp":            "clamp",
    "c-clamp":          "clamp",
    "vise":             "clamp",
    "vice":             "clamp",
    "vice grip":        "clamp",
    "vise grip":        "clamp",
    "workbench clamp":  "clamp",
    "brick":            "bricks",
    "bricks":           "bricks",
    "masonry":          "bricks",
    "concrete":         "bricks",
    "tile":             "bricks",
    "gear":             "gear",
    "mechanism":        "gear",
    "engineering":      "gear",
    "assembly":         "gear",
    "magnet":           "magnet",
    "magnetic":         "magnet",
    "key":              "key",
    "keys":             "key",
    "locksmith":        "key",
    "lock":             "lock",
    "locked":           "lock",
    "secure":           "lock",
    "do not open":      "lock",
    "private":          "lock",
    "confidential":     "lock",
    "password":         "lock",
    "secret":           "lock",
    "personal":         "lock",
    "sensitive":        "lock",
    "classified":       "lock",
    "restricted":       "lock",
    "protected":        "lock",
    "vault":            "lock",
    "do not touch":     "lock",
    "toolbox":          "toolbox",
    "tool kit":         "toolbox",
    "first aid kit":    "toolbox",
    "ladder":           "ladder",
    "hook":             "hook",
    "wall hook":        "hook",
    "coat hook":        "hook",
    "safety pin":       "safety_pin",
    "pin":              "safety_pin",
    "compass":          "compass",
    "navigation":       "compass",
    "directions":       "compass",
    "basket":           "basket",
    "laundry basket":   "basket",
    "wicker":           "basket",
    "accordion":        "accordion",
    "concertina":       "accordion",
    "package box":      "package_box",
    "folder label":     "folder_icon",

    # ── 3D Printing ──────────────────────────────────────────────────────────
    "printer":          "printer_3d",
    "label printer":    "printer_3d",
    "print":            "printer_3d",
    "printing":         "printer_3d",
    "3d print":         "printer_3d",
    "3d printing":      "printer_3d",
    "3d printed":       "printer_3d",
    "fdm":              "printer_3d",
    "sla":              "printer_3d",
    "msla":             "printer_3d",
    "resin":            "printer_3d",
    "filament":         "printer_3d",
    "pla":              "printer_3d",
    "petg":             "printer_3d",
    "tpu":              "printer_3d",
    "abs filament":     "printer_3d",
    "asa":              "printer_3d",
    "nozzle":           "printer_3d",
    "extruder":         "printer_3d",
    "print bed":        "printer_3d",
    "heated bed":       "printer_3d",
    "build plate":      "printer_3d",
    "infill":           "printer_3d",
    "spool":            "printer_3d",
    "filament spool":   "printer_3d",
    "layer":            "printer_3d",
    "supports":         "printer_3d",
    "slicer":           "printer_3d",
    "sliced":           "printer_3d",
    "gcode":            "printer_3d",
    "g-code":           "printer_3d",
    "stl":              "printer_3d",
    "prototype":        "ruler_tri",
    "cad":              "ruler_tri",
    "cad design":       "ruler_tri",
    "3d model":         "ruler_tri",
    "design file":      "ruler_tri",
    "blueprint":        "ruler_tri",
    "draft":            "ruler_tri",

    # ── Laser / CNC / Engraving ──────────────────────────────────────────────
    "laser":            "laser_beam",
    "laser cut":        "laser_beam",
    "laser cutting":    "laser_beam",
    "laser cutter":     "laser_beam",
    "laser cutout":     "laser_beam",
    "cnc":              "scissors",
    "cnc router":       "scissors",
    "cnc cut":          "scissors",
    "vinyl cut":        "scissors",
    "vinyl cutter":     "scissors",
    "die cut":          "scissors",
    "engrave":          "diamond",
    "engraving":        "diamond",
    "engraved":         "diamond",
    "laser engrave":    "diamond",
    "laser engraving":  "diamond",
    "rotary engrave":   "diamond",
    "etching":          "diamond",
    "etched":           "diamond",
    "etch":             "diamond",
    "pyrography":       "wood",
    "wood burn":        "wood",
    "woodburning":      "wood",
    "wood burning":     "wood",
    "plywood":          "wood",
    "mdf":              "wood",
    "balsa":            "wood",
    "hardwood":         "wood",
    "basswood":         "wood",
    "wood":             "wood",
    "wooden":           "wood",
    "woodwork":         "wood",
    "softwood":         "wood",
    "oak":              "wood",
    "pine":             "wood",
    "walnut":           "wood",
    "mahogany":         "wood",
    "teak":             "wood",
    "cedar":            "wood",
    "spruce":           "wood",
    "cherry wood":      "wood",
    "ash wood":         "wood",
    "bamboo":           "wood",
    "chipboard":        "wood",
    "particleboard":    "wood",
    "veneer":           "wood",
    "dowel":            "wood",
    "wood log":         "wood",
    "firewood":         "wood",

    # ── Raw Materials ────────────────────────────────────────────────────────
    "rock":             "rock",
    "stone":            "rock",
    "stones":           "rock",
    "pebble":           "rock",
    "pebbles":          "rock",
    "gravel":           "rock",
    "boulder":          "rock",
    "cobblestone":      "rock",
    "granite":          "rock",
    "marble":           "rock",
    "slate":            "rock",
    "limestone":        "rock",
    "sandstone":        "rock",
    "quartz":           "rock",
    "flint":            "rock",
    "obsidian":         "rock",
    "flagstone":        "rock",
    "travertine":       "rock",
    "mineral":          "rock",
    "minerals":         "rock",
    "geode":            "rock",
    "aggregate":        "rock",

    "glass":            "crystal_glass",
    "stained glass":    "crystal_glass",
    "crystal":          "crystal_glass",
    "acrylic":          "crystal_glass",
    "perspex":          "crystal_glass",
    "plexiglass":       "crystal_glass",
    "tempered glass":   "crystal_glass",
    "frosted glass":    "crystal_glass",
    "borosilicate":     "crystal_glass",

    "metal":            "metal",
    "metals":           "metal",
    "steel":            "metal",
    "iron":             "metal",
    "aluminum":         "metal",
    "aluminium":        "metal",
    "copper":           "metal",
    "brass":            "metal",
    "titanium":         "metal",
    "stainless steel":  "metal",
    "stainless":        "metal",
    "zinc":             "metal",
    "pewter":           "metal",
    "cast iron":        "metal",
    "alloy":            "metal",
    "galvanized":       "metal",
    "sheet metal":      "metal",
    "mild steel":       "metal",

    "clay":             "clay",
    "ceramic":          "clay",
    "earthenware":      "clay",
    "terracotta":       "clay",
    "terra cotta":      "clay",
    "stoneware":        "clay",
    "porcelain":        "clay",
    "bisque":           "clay",

    # ── Parts / Fasteners ────────────────────────────────────────────────────
    "nut":              "nut_bolt",
    "hex nut":          "nut_bolt",
    "lock nut":         "nut_bolt",
    "bolt":             "nut_bolt",
    "fastener":         "nut_bolt",
    "fasteners":        "nut_bolt",
    "m3":               "nut_bolt",
    "m4":               "nut_bolt",
    "m5":               "nut_bolt",
    "m6":               "nut_bolt",
    "m8":               "nut_bolt",
    "m10":              "nut_bolt",
    "hardware bin":     "nut_bolt",
    "spare parts":      "nut_bolt",
    "components":       "nut_bolt",
    "bearings":         "nut_bolt",
    "inserts":          "nut_bolt",

    # ── Car / Automotive ─────────────────────────────────────────────────────
    "car":              "car",
    "auto":             "car",
    "automotive":       "car",
    "vehicle":          "car",
    "truck":            "car",
    "van":              "car",
    "suv":              "car",
    "oil":              "car",
    "tire":             "car",
    "tires":            "car",
    "motor":            "car",
    "engine":           "car",
    "fuel":             "fuel_pump",
    "brakes":           "car",
    "windshield":       "car",
    "maintenance":      "car",
    "detailing":        "car",
    "racing":           "racing",
    "bicycle":          "bicycle",
    "bike":             "bicycle",
    "cycling gear":     "bicycle",
    "motorcycle":       "motorcycle",
    "scooter":          "motorcycle",
    "tractor":          "tractor",
    "farm equipment":   "tractor",
    "delivery truck":   "delivery_truck",
    "shipping truck":   "delivery_truck",
    "ambulance":        "ambulance",
    "fire truck":       "fire_truck",
    "fire engine":      "fire_truck",
    "pickup truck":     "pickup_truck",
    "pickup":           "pickup_truck",
    "flatbed":          "pickup_truck",
    "truck bed":        "pickup_truck",
    "ute":              "pickup_truck",
    "minivan":          "minivan",
    "people carrier":   "minivan",

    # ── Travel / Transport ───────────────────────────────────────────────────
    "travel":           "travel",
    "vacation":         "travel",
    "trip":             "travel",
    "flight":           "airplane",
    "passport":         "travel",
    "hotel":            "travel",
    "abroad":           "travel",
    "road trip":        "travel",
    "tourism":          "travel",
    "cruise":           "ship",
    "cruise ship":      "ship",
    "anchor":           "anchor",
    "nautical":         "anchor",
    "marina":           "anchor",
    "harbor":           "anchor",
    "dock":             "anchor",
    "taxi":             "taxi",
    "cab":              "taxi",
    "rideshare":        "taxi",
    "uber":             "taxi",
    "airplane":         "airplane",
    "plane":            "airplane",
    "aircraft":         "airplane",
    "jet":              "airplane",
    "airliner":         "airplane",
    "flying":           "airplane",
    "airport":          "airplane",
    "boarding":         "airplane",
    "takeoff":          "airplane",
    "landing":          "airplane",
    "bus":              "bus",
    "transit":          "bus",
    "commute":          "bus",
    "train":            "train",
    "railway":          "train",
    "rail":             "train",
    "metro":            "train",
    "helicopter":       "helicopter",
    "boat":             "boat",
    "sailing":          "boat",
    "sailboat":         "boat",
    "speedboat":        "speedboat",
    "ferry":            "speedboat",
    "parachute":        "parachute",
    "skydiving":        "parachute",

    # ── Health / Medical ─────────────────────────────────────────────────────
    "bandages":         "firstaid",
    "first aid":        "firstaid",
    "wound":            "firstaid",
    "injury":           "firstaid",
    "medicine":         "medicine",
    "medication":       "medicine",
    "pharmacy":         "medicine",
    "vitamins":         "medicine",
    "pills":            "medicine",
    "supplements":      "medicine",
    "prescription":     "medicine",
    "medical":          "medicine",
    "health":           "medicine",
    "doctor":           "prof_medical",
    "physician":        "prof_medical",
    "surgeon":          "prof_medical",
    "nurse":            "prof_medical",
    "stethoscope":      "stethoscope",
    "clinic":           "stethoscope",
    "checkup":          "stethoscope",
    "hospital":         "stethoscope",
    "surgery":          "stethoscope",
    "x-ray":            "xray",
    "xray":             "xray",
    "x ray":            "xray",
    "scan":             "xray",
    "mri":              "xray",
    "ct scan":          "xray",
    "cardiac":          "anatomical_heart",
    "heart health":     "anatomical_heart",
    "cardiology":       "anatomical_heart",
    "syringe":          "syringe",
    "injection":        "syringe",
    "vaccine":          "syringe",
    "shot":             "syringe",
    "thermometer":      "thermometer",
    "temperature":      "thermometer",
    "fever":            "thermometer",
    "bone":             "bone",
    "bones":            "bone",
    "skeleton":         "bone",
    "fracture":         "bone",
    "ortho":            "bone",
    "tooth":            "tooth",
    "teeth":            "tooth",
    "dental":           "tooth",
    "dentist":          "tooth",
    "brain":            "brain",
    "neurology":        "brain",
    "mental":           "brain",
    "cognitive":        "brain",
    "memory":           "brain",
    "ear":              "ear",
    "hearing":          "ear",
    "nose":             "nose",
    "sinuses":          "nose",
    "eye":              "eye_body",
    "vision":           "eye_body",
    "optics":           "eye_body",
    "lungs":            "lungs",
    "lung":             "lungs",
    "respiratory":      "lungs",
    "breathing":        "lungs",
    "arm":              "muscle",
    "arms":             "muscle",
    "bicep":            "muscle",
    "biceps":           "muscle",
    "forearm":          "muscle",
    "tricep":           "muscle",
    "triceps":          "muscle",
    "leg":              "leg",
    "legs":             "leg",
    "thigh":            "leg",
    "shin":             "leg",
    "calf":             "leg",
    "knee":             "leg",
    "blood":            "blood",
    "bleeding":         "blood",
    "bloody":           "blood",
    "hemorrhage":       "blood",
    "plasma":           "blood",
    "transfusion":      "blood",
    "microscope":       "microscope",
    "lab":              "microscope",
    "laboratory":       "microscope",
    "specimens":        "microscope",
    "samples":          "microscope",
    "dna":              "dna",
    "genetics":         "dna",
    "biology":          "dna",

    # ── Barber / Hair ────────────────────────────────────────────────────────
    "barber":           "barber_pole",
    "barbershop":       "barber_pole",
    "barber shop":      "barber_pole",
    "barber pole":      "barber_pole",
    "haircut":          "barber_pole",
    "hair salon":       "barber_pole",
    "salon":            "barber_pole",
    "hairdresser":      "barber_pole",
    "stylist":          "barber_pole",
    "trim":             "barber_pole",
    "shave":            "barber_pole",

    # ── Voting / Politics ────────────────────────────────────────────────────
    "vote":             "ballot_box",
    "voting":           "ballot_box",
    "voter":            "ballot_box",
    "poll":             "ballot_box",
    "polls":            "ballot_box",
    "ballot":           "ballot_box",
    "ballots":          "ballot_box",
    "election":         "ballot_box",
    "elections":        "ballot_box",
    "referendum":       "ballot_box",
    "democracy":        "ballot_box",
    "candidate":        "ballot_box",
    "campaign":         "ballot_box",

    # ── Poles ────────────────────────────────────────────────────────────────
    "flagpole":         "flag",
    "flag pole":        "flag",
    "fishing pole":     "fishing",
    "fishing rod":      "fishing",
    "north pole":       "snowflake",
    "south pole":       "penguin",
    "telephone pole":   "antenna",
    "power pole":       "lightning",
    "totem pole":       "art",

    # ── Science ──────────────────────────────────────────────────────────────
    "science":          "science",
    "chemistry":        "science",
    "research":         "science",
    "experiment":       "science",
    "physics":          "science",
    "geology":          "science",
    "astronomy":        "telescope",

    # ── Mail / Shipping ──────────────────────────────────────────────────────
    "mail":             "mail",
    "letter":           "envelope",
    "envelope":         "envelope",
    "postcard":         "envelope",
    "mailbox":          "mailbox",
    "letterbox":        "mailbox",
    "post box":         "mailbox",
    "return":           "mail",
    "send":             "mail",
    "package":          "package_box",
    "parcel":           "package_box",
    "box":              "package_box",
    "crate":            "package_box",
    "shipping":         "package_box",
    "delivery":         "mail",
    "courier":          "mail",
    "outgoing":         "mail",
    "incoming":         "mail",
    "postage":          "mail",

    # ── Money / Finance ──────────────────────────────────────────────────────
    "money":            "money",
    "cash":             "money",
    "bills":            "money",
    "finance":          "money",
    "receipt":          "money",
    "invoice":          "money",
    "taxes":            "money",
    "budget":           "money",
    "savings":          "money",
    "coin":             "coin",
    "coins":            "coin",
    "penny":            "coin",
    "quarter":          "coin",
    "dime":             "coin",
    "nickel":           "coin",
    "token":            "coin",
    "bank":             "money",
    "payment":          "money",
    "paycheck":         "money",
    "expense":          "money",
    "checkbook":        "money",
    "credit":           "money",
    "debit":            "money",

    # ── Celebrations / Holidays ──────────────────────────────────────────────
    "christmas":        "christmas",
    "xmas":             "christmas",
    "ornaments":        "christmas",
    "halloween":        "halloween",
    "trick or treat":   "halloween",
    "costumes":         "halloween",
    "spooky":           "halloween",
    "birthday":         "birthday",
    "graduation":       "graduation",
    "graduate":         "graduation",
    "diploma":          "graduation",
    "wedding":          "wedding",
    "bride":            "wedding",
    "groom":            "wedding",
    "anniversary":      "wedding",
    "thanksgiving":     "thanksgiving",
    "turkey":           "thanksgiving",
    "turkiye":          "flag_tr",
    "türkiye":          "flag_tr",
    "valentine":        "heart",
    "valentines":       "heart",
    "party":            "party",
    "celebration":      "party",
    "confetti":         "party",
    "pinata":           "pinata",
    "piñata":           "pinata",
    "disco":            "disco_ball",
    "disco ball":       "disco_ball",
    "dance floor":      "disco_ball",
    "nightclub":        "disco_ball",
    "kite":             "kite",
    "kites":            "kite",
    "kite flying":      "kite",
    "magic 8":          "8ball",
    "magic 8 ball":     "8ball",
    "8 ball":           "8ball",
    "eight ball":       "8ball",
    "billiards":        "8ball",
    "pool ball":        "8ball",
    "new year":         "fireworks",
    "fourth of july":   "fireworks",
    "fireworks":        "fireworks",
    "balloon":          "balloon",
    "balloons":         "balloon",
    "gift":             "gift",
    "gifts":            "gift",
    "presents":         "gift",
    "wrapping":         "gift",
    "holiday":          "gift",
    "decorations":      "gift",
    "hanukkah":         "gift",
    "festive":          "gift",
    "sparkle":          "sparkles",
    "glitter":          "sparkles",
    "sparkles":         "sparkles",
    "ribbon":           "ribbon",
    "bow":              "ribbon",

    # ── Baby / Kids ──────────────────────────────────────────────────────────
    "baby":             "baby",
    "infant":           "baby",
    "toddler":          "baby",
    "nursery":          "baby",
    "diapers":          "baby",
    "stroller":         "baby",
    "formula":          "baby",
    "crib":             "baby",
    "kids":             "baby",
    "children":         "baby",
    "toys":             "baby",
    "playroom":         "baby",

    # ── Fire / Heat ──────────────────────────────────────────────────────────
    "hot":              "fire",
    "fire":             "fire",
    "heat":             "fire",
    "warm":             "fire",
    "spicy":            "fire",
    "campfire":         "fire",
    "fireplace":        "fire",

    # ── Photos / Camera ──────────────────────────────────────────────────────
    "photos":           "camera",
    "pictures":         "camera",
    "camera":           "camera",
    "video":            "camera",
    "recording":        "camera",
    "footage":          "camera",
    "memories":         "camera",
    "portraits":        "camera",

    # ── Clothes / Fashion ────────────────────────────────────────────────────
    "clothes":          "clothes",
    "clothing":         "clothes",
    "wardrobe":         "clothes",
    "laundry":          "cleaning",
    "shirt":            "clothes",
    "shirts":           "clothes",
    "tshirt":           "clothes",
    "tops":             "clothes",
    "blouse":           "clothes",
    "dress":            "dress",
    "gown":             "dress",
    "skirt":            "dress",
    "pants":            "jeans",
    "trousers":         "jeans",
    "jeans":            "jeans",
    "shorts":           "jeans",
    "leggings":         "jeans",
    "shoe":             "shoe",
    "shoes":            "shoe",
    "boots":            "shoe",
    "sneakers":         "shoe",
    "heels":            "shoe",
    "footwear":         "shoe",
    "socks":            "sock",
    "stockings":        "sock",
    "tights":           "sock",
    "jacket":           "coat",
    "jackets":          "coat",
    "coat":             "coat",
    "hoodie":           "coat",
    "sweater":          "coat",
    "sweaters":         "coat",
    "cardigan":         "coat",
    "blazer":           "coat",
    "scarf":            "scarf",
    "scarves":          "scarf",
    "wrap":             "scarf",
    "gloves":           "glove",
    "mittens":          "glove",
    "tie":              "tie",
    "necktie":          "tie",
    "bowtie":           "tie",
    "bow tie":          "tie",
    "suit":             "tie",
    "suits":            "tie",
    "swimwear":         "bikini",
    "swimsuit":         "bikini",
    "bikini":           "bikini",
    "trunks":           "bikini",
    "purse":            "purse",
    "handbag":          "purse",
    "clutch":           "purse",
    "wallet":           "purse",
    "accessories":      "clothes",
    "uniforms":         "clothes",
    "hat":              "hat",
    "hats":             "hat",
    "cap":              "hat",
    "beanie":           "hat",
    "helmet":           "hat",
    "glasses":          "glasses",
    "sunglasses":       "glasses",
    "eyewear":          "glasses",
    "goggles":          "glasses",
    "ring":             "ring",
    "engagement":       "ring",
    "wedding ring":     "ring",
    "luggage":          "luggage",
    "suitcase":         "luggage",
    "baggage":          "luggage",
    "backpack":         "backpack",
    "rucksack":         "backpack",
    "school bag":       "backpack",

    # ── Cleaning ─────────────────────────────────────────────────────────────
    "cleaning":         "cleaning",
    "clean":            "cleaning",
    "cleaned":          "cleaning",
    "chores":           "cleaning",
    "vacuum":           "cleaning",
    "vacuuming":        "cleaning",
    "mop":              "cleaning",
    "mopping":          "cleaning",
    "broom":            "cleaning",
    "sweeping":         "cleaning",
    "detergent":        "cleaning",
    "bleach":           "cleaning",
    "disinfect":        "cleaning",
    "disinfecting":     "cleaning",
    "sanitize":         "cleaning",
    "sanitizing":       "cleaning",
    "organize":         "cleaning",
    "organizing":       "cleaning",
    "tidying":          "cleaning",
    "scrubbing":        "cleaning",

    # ── Trash / Recycle ──────────────────────────────────────────────────────
    "trash":            "trash",
    "garbage":          "trash",
    "junk":             "trash",
    "dispose":          "trash",
    "donate":           "trash",
    "waste":            "trash",
    "discard":          "trash",
    "recycle":          "recycle",
    "recyclable":       "recycle",
    "eco":              "recycle",
    "green":            "recycle",
    "compost":          "recycle",
    "sustainable":      "recycle",
    "environment":      "recycle",

    # ── Time / Schedule ──────────────────────────────────────────────────────
    "time":             "time",
    "clock":            "time",
    "timer":            "stopwatch",
    "alarm":            "time",
    "schedule":         "calendar",
    "deadline":         "time",
    "appointment":      "calendar",
    "reminder":         "time",
    "weekly":           "calendar",
    "daily":            "time",
    "monthly":          "calendar",
    "calendar":         "calendar",
    "countdown":        "time",
    "annual":           "calendar",
    "hourglass":        "hourglass",
    "watch":            "time",

    # ── Star / Important ─────────────────────────────────────────────────────
    "star":             "glowing_star",
    "stars":            "glowing_star",
    "starry":           "glowing_star",
    "starlight":        "glowing_star",
    "starburst":        "glowing_star",
    "shooting star":    "shooting_star",
    "falling star":     "shooting_star",
    "wishing star":     "shooting_star",
    "important":        "star",
    "priority":         "star",
    "favorite":         "star",
    "urgent":           "star",
    "featured":         "star",
    "top":              "star",
    "best":             "star",
    "highlighted":      "star",
    "special":          "star",
    "premium":          "star",
    "number one":       "star",
    "winner":           "star",
    "award":            "star",
    "trophy":           "trophy",
    "medal":            "medal",
    "gold":             "medal",
    "gold medal":       "medal",
    "1st":              "medal",
    "1st place":        "medal",
    "first place":      "medal",
    "silver":           "medal_silver",
    "silver medal":     "medal_silver",
    "2nd":              "medal_silver",
    "2nd place":        "medal_silver",
    "second place":     "medal_silver",
    "bronze":           "medal_bronze",
    "bronze medal":     "medal_bronze",
    "3rd":              "medal_bronze",
    "3rd place":        "medal_bronze",
    "third place":      "medal_bronze",

    # ── Country flags ────────────────────────────────────────────────────────
    "united states":        "flag_us",
    "usa":                  "flag_us",
    "american":             "flag_us",
    "america":              "flag_us",
    "united kingdom":       "flag_gb",
    "uk":                   "flag_gb",
    "england":              "flag_gb",
    "britain":              "flag_gb",
    "british":              "flag_gb",
    "canada":               "flag_ca",
    "canadian":             "flag_ca",
    "australia":            "flag_au",
    "australian":           "flag_au",
    "germany":              "flag_de",
    "german":               "flag_de",
    "france":               "flag_fr",
    "french":               "flag_fr",
    "italy":                "flag_it",
    "italian":              "flag_it",
    "spain":                "flag_es",
    "spanish":              "flag_es",
    "japan":                "flag_jp",
    "japanese":             "flag_jp",
    "china":                "flag_cn",
    "chinese":              "flag_cn",
    "brazil":               "flag_br",
    "brazilian":            "flag_br",
    "mexico":               "flag_mx",
    "india":                "flag_in",
    "indian":               "flag_in",
    "russia":               "flag_ru",
    "russian":              "flag_ru",
    "south korea":          "flag_kr",
    "korean":               "flag_kr",
    "netherlands":          "flag_nl",
    "dutch":                "flag_nl",
    "sweden":               "flag_se",
    "swedish":              "flag_se",
    "norway":               "flag_no",
    "norwegian":            "flag_no",
    "denmark":              "flag_dk",
    "danish":               "flag_dk",
    "finland":              "flag_fi",
    "finnish":              "flag_fi",
    "switzerland":          "flag_ch",
    "swiss":                "flag_ch",
    "austria":              "flag_at",
    "austrian":             "flag_at",
    "belgium":              "flag_be",
    "belgian":              "flag_be",
    "portugal":             "flag_pt",
    "portuguese":           "flag_pt",
    "greece":               "flag_gr",
    "greek":                "flag_gr",
    "poland":               "flag_pl",
    "polish":               "flag_pl",
    "ukraine":              "flag_ua",
    "ukrainian":            "flag_ua",
    "turkish":              "flag_tr",
    "israel":               "flag_il",
    "israeli":              "flag_il",
    "saudi arabia":         "flag_sa",
    "saudi":                "flag_sa",
    "uae":                  "flag_ae",
    "emirates":             "flag_ae",
    "south africa":         "flag_za",
    "nigeria":              "flag_ng",
    "nigerian":             "flag_ng",
    "egypt":                "flag_eg",
    "egyptian":             "flag_eg",
    "argentina":            "flag_ar",
    "argentinian":          "flag_ar",
    "colombia":             "flag_co",
    "colombian":            "flag_co",
    "chile":                "flag_cl",
    "chilean":              "flag_cl",
    "peru":                 "flag_pe",
    "peruvian":             "flag_pe",
    "venezuela":            "flag_ve",
    "venezuelan":           "flag_ve",
    "new zealand":          "flag_nz",
    "ireland":              "flag_ie",
    "irish":                "flag_ie",
    "scotland":             "flag_gb",
    "wales":                "flag_gb",
    "singapore":            "flag_sg",
    "malaysia":             "flag_my",
    "thailand":             "flag_th",
    "thai":                 "flag_th",
    "vietnam":              "flag_vn",
    "vietnamese":           "flag_vn",
    "indonesia":            "flag_id",
    "indonesian":           "flag_id",
    "philippines":          "flag_ph",
    "filipino":             "flag_ph",
    "pakistan":             "flag_pk",
    "bangladesh":           "flag_bd",
    "iran":                 "flag_ir",
    "iranian":              "flag_ir",
    "iraq":                 "flag_iq",
    "iraqi":                "flag_iq",
    "morocco":              "flag_ma",
    "moroccan":             "flag_ma",
    "kenya":                "flag_ke",
    "kenyan":               "flag_ke",
    "ghana":                "flag_gh",
    "ethiopia":             "flag_et",
    "ethiopian":            "flag_et",
    "cuba":                 "flag_cu",
    "cuban":                "flag_cu",
    "czech republic":       "flag_cz",
    "czechia":              "flag_cz",
    "czech":                "flag_cz",
    "hungary":              "flag_hu",
    "hungarian":            "flag_hu",
    "romania":              "flag_ro",
    "romanian":             "flag_ro",
    "croatia":              "flag_hr",
    "croatian":             "flag_hr",
    "slovakia":             "flag_sk",
    "slovak":               "flag_sk",
    "slovenia":             "flag_si",
    "slovenian":            "flag_si",
    "serbia":               "flag_rs",
    "serbian":              "flag_rs",
    "bulgaria":             "flag_bg",
    "bulgarian":            "flag_bg",
    "iceland":              "flag_is",
    "icelandic":            "flag_is",
    "luxembourg":           "flag_lu",
    "estonia":              "flag_ee",
    "estonian":             "flag_ee",
    "latvia":               "flag_lv",
    "latvian":              "flag_lv",
    "lithuania":            "flag_lt",
    "lithuanian":           "flag_lt",
    "taiwan":               "flag_tw",
    "taiwanese":            "flag_tw",
    "hong kong":            "flag_hk",
    "puerto rico":          "flag_pr",
    "puerto rican":         "flag_pr",
    "european union":       "flag_eu",
    "europe":               "flag_eu",
    "united nations":       "flag_un",

    # ── Buildings / Places ───────────────────────────────────────────────────
    "building":         "office_building",
    "office building":  "office_building",
    "apartment":        "cityscape",
    "apartments":       "cityscape",
    "flat":             "cityscape",
    "condo":            "cityscape",
    "condominium":      "cityscape",
    "complex":          "cityscape",
    "downtown":         "cityscape",
    "city":             "cityscape",
    "urban":            "cityscape",
    "street":           "road",
    "road":             "road",
    "avenue":           "road",
    "boulevard":        "road",
    "highway":          "road",
    "lane":             "road",
    "drive":            "road",
    "headquarters":     "office_building",
    "workplace":        "office_building",
    "university":       "school_building",
    "college":          "school_building",
    "campus":           "school_building",
    "castle":           "castle",
    "palace":           "castle",
    "church":           "church",
    "chapel":           "church",
    "temple":           "church",
    "stadium":          "stadium",
    "arena":            "stadium",
    "theater":          "theater",
    "theatre":          "theater",
    "cinema":           "theater",
    "movies":           "theater",
    "broadway":         "theater",
    "opera":            "theater",
    "performance":      "theater",
    "film":             "clapperboard",
    "movie set":        "clapperboard",
    "clapperboard":     "clapperboard",
    "movie clapper":    "clapperboard",
    "megaphone":        "megaphone",
    "loudspeaker":      "megaphone",
    "announcement":     "megaphone",
    "cheer":            "megaphone",
    "bell":             "bell",
    "doorbell":         "bell",
    "notification bell":"bell",
    "alarm bell":       "bell",
    "can":              "canned_food",
    "canned":           "canned_food",
    "tin can":          "canned_food",
    "tin":              "canned_food",
    "canned food":      "canned_food",
    "bar":              "bar",
    "pub":              "bar",
    "tavern":           "bar",
    "saloon":           "bar",
    "badge":            "badge",
    "name badge":       "badge",
    "name tag":         "badge",
    "id badge":         "badge",
    "lanyard":          "badge",
    "bulb":             "bulb",
    "bright idea":      "bulb",
    "brush":            "paintbrush",
    "paintbrush":       "paintbrush",
    "paint brush":      "paintbrush",
    "button":           "button",
    "buttons":          "button",
    "sewing button":    "button",
    "flag":             "flag",
    "flags":            "flag",
    "flagged":          "flag",
    "checkered flag":   "checkered_flag",
    "finish line":      "checkered_flag",
    "race":             "checkered_flag",
    "polar bear":       "polar_bear",
    "arctic bear":      "polar_bear",
    "heart on fire":    "heart_fire",
    "burning heart":    "heart_fire",
    "passionate":       "heart_fire",
    "mending heart":    "heart_mend",
    "healing heart":    "heart_mend",
    "museum":           "museum",
    "gallery":          "museum",
    "bank building":    "bank",
    "atm":              "bank",
    "hospital building": "hospital_building",

    # ── Drama / theater ──────────────────────────────────────────────────────
    "drama":            "theater",
    "dramatic":         "theater",
    "acting":           "theater",
    "theatrics":        "theater",

    # ── Rock & roll (sign of the horns) ──────────────────────────────────────
    "rock and roll":    "rock_on",
    "rock n roll":      "rock_on",
    "rock 'n' roll":    "rock_on",
    "rocknroll":        "rock_on",
    "headbanger":       "rock_on",
    "metalhead":        "rock_on",
    "mosh":             "rock_on",
    "mosh pit":         "rock_on",

    # ── Blog / notes ─────────────────────────────────────────────────────────
    "blog":             "memo",
    "vlog":             "memo",
    "blogging":         "memo",
    "memo":             "memo",
    "note":             "memo",
    "notepad":          "memo",
    "sticky note":      "memo",
    "to do list":       "memo",

    # ── Burp / exhale ────────────────────────────────────────────────────────
    "burp":             "face_exhale",
    "burping":          "face_exhale",
    "belch":            "face_exhale",
    "belching":         "face_exhale",
    "sigh":             "face_exhale",
    "sighing":          "face_exhale",
    "exhale":           "face_exhale",
    "whew":             "face_exhale",
    "phew":             "face_exhale",
    "relieved":         "face_exhale",
    "breath":           "face_exhale",
    "breathe":          "face_exhale",

    # ── Fart / gas (the smelly kind) → wind ──────────────────────────────────
    "fart":             "wind",
    "farts":            "wind",
    "farting":          "wind",
    "toot":             "wind",
    "flatulence":       "wind",
    "gassy":            "wind",
    "passing gas":      "wind",
    "fluff":            "wind",

    # ── Fudgy / chocolate ────────────────────────────────────────────────────
    "fudgy":            "chocolate",
    "brownie":          "chocolate",
    "brownies":         "chocolate",
    "ganache":          "chocolate",

    # ── Fail / wrong → ❌ ─────────────────────────────────────────────────────
    "fail":             "cross_mark",
    "failed":           "cross_mark",
    "failing":          "cross_mark",
    "failure":          "cross_mark",
    "wrong":            "cross_mark",
    "wrong answer":     "cross_mark",
    "incorrect":        "cross_mark",
    "error":            "cross_mark",
    "invalid":          "cross_mark",
    "nope":             "cross_mark",
    "mistake":          "cross_mark",
    "false":            "cross_mark",
    "x mark":           "cross_mark",
    "cross mark":       "cross_mark",

    # ── Pass / correct → ✅ ───────────────────────────────────────────────────
    "pass":             "check_mark",
    "passed":           "check_mark",
    "passing":          "check_mark",
    "correct":          "check_mark",
    "complete":         "check_mark",
    "completed":        "check_mark",
    "done":             "check_mark",
    "finished":         "check_mark",
    "verified":         "check_mark",
    "success":          "check_mark",
    "successful":       "check_mark",
    "checkmark":        "check_mark",
    "valid":            "check_mark",
    "right answer":     "check_mark",

    # ── Grass / weed / marijuana → 🌿 ─────────────────────────────────────────
    "grass":            "herb",
    "lawn":             "herb",
    "yard":             "herb",
    "turf":             "herb",
    "sod":              "herb",
    "weed":             "herb",
    "weeds":            "herb",
    "marijuana":        "herb",
    "cannabis":         "herb",
    "hemp":             "herb",
    "ganja":            "herb",
    "cbd":              "herb",
    "pot leaf":         "herb",

    # ── Geometric shapes ─────────────────────────────────────────────────────
    "cube":             "ice",
    "cubes":            "ice",
    "sphere":           "crystal_glass",
    "orb":              "crystal_glass",
    "circle":           "circle",
    "circles":          "circle",
    "circular":         "circle",
    "square":           "square",
    "squares":          "square",
    "triangle":         "triangle",
    "triangles":        "triangle",
    "triangular":       "triangle",
    "pyramid":          "triangle",
    "pyramids":         "triangle",

    # ── Machine → ⚙ ──────────────────────────────────────────────────────────
    "machine":          "gear",
    "machines":         "gear",
    "machinery":        "gear",
    "machining":        "gear",
    "mechanical":       "gear",

    # ── Gun / firearms → 🔫 ───────────────────────────────────────────────────
    "gun":              "gun",
    "guns":             "gun",
    "pistol":           "gun",
    "pistols":          "gun",
    "revolver":         "gun",
    "firearm":          "gun",
    "firearms":         "gun",
    "rifle":            "gun",
    "rifles":           "gun",
    "handgun":          "gun",
    "shotgun":          "gun",
    "machine gun":      "gun",
    "ammo":             "gun",
    "ammunition":       "gun",
    "bullet":           "gun",
    "bullets":          "gun",

    # ── Factory / industrial → 🏭 ─────────────────────────────────────────────
    "factory":          "factory",
    "factories":        "factory",
    "manufacturing":    "factory",
    "industrial":       "factory",
    "mill":             "factory",
    "smokestack":       "factory",
    "assembly line":    "factory",

    # ── Label / sticker / tag → 🏷 ────────────────────────────────────────────
    "label":            "label",
    "labels":           "label",
    "sticker":          "label",
    "stickers":         "label",
    "tag":              "label",
    "tags":             "label",
    "hang tag":         "label",
    "price label":      "label",

    # ── Calendar extras → 📅 ──────────────────────────────────────────────────
    "agenda":           "calendar",
    "meeting":          "calendar",
    "meetings":         "calendar",
    "planner":          "calendar",
    "day planner":      "calendar",

    # ── Stopwatch / timing → ⏱ ────────────────────────────────────────────────
    "stopwatch":        "stopwatch",
    "lap time":         "stopwatch",
    "time trial":       "stopwatch",

    # ── Hourglass / sand timer → ⌛ ────────────────────────────────────────────
    "sand timer":       "hourglass",
    "sandglass":        "hourglass",
    "egg timer":        "hourglass",

    # ── Map / geography → 🗺 ──────────────────────────────────────────────────
    "map":              "world_map",
    "maps":             "world_map",
    "atlas":            "world_map",
    "geography":        "world_map",
    "world map":        "world_map",
    "road map":         "world_map",
    "treasure map":     "world_map",

    # ── Gas / fuel → ⛽ ───────────────────────────────────────────────────────
    "gas":              "fuel_pump",
    "gasoline":         "fuel_pump",
    "petrol":           "fuel_pump",
    "diesel":           "fuel_pump",
    "gas station":      "fuel_pump",
    "gas pump":         "fuel_pump",
    "fuel pump":        "fuel_pump",
    "filling station":  "fuel_pump",
    "unleaded":         "fuel_pump",

    # ── English / alphabet → 🔤 ───────────────────────────────────────────────
    "english":          "abc",
    "alphabet":         "abc",
    "spelling":         "abc",
    "spell":            "abc",
    "vocabulary":       "abc",
    "abc":              "abc",
    "abcs":             "abc",
    "language":         "abc",
    "grammar":          "abc",

    # ── Math / arithmetic → 🧮 ────────────────────────────────────────────────
    "math":             "abacus",
    "maths":            "abacus",
    "mathematics":      "abacus",
    "arithmetic":       "abacus",
    "algebra":          "abacus",
    "calculus":         "abacus",
    "geometry":         "abacus",
    "counting":         "abacus",
    "addition":         "abacus",
    "subtraction":      "abacus",
    "multiplication":   "abacus",
    "division":         "abacus",
    "equation":         "abacus",

    # ── Numbers → 🔢 ──────────────────────────────────────────────────────────
    "numbers":          "numbers",
    "digits":           "numbers",
    "numeric":          "numbers",

    # ── Deck of cards → 🃏 ────────────────────────────────────────────────────
    "deck":             "card_joker",
    "deck of cards":    "card_joker",

    # ── Dungeon → 🏰 ─────────────────────────────────────────────────────────
    "dungeon":          "castle",
    "dungeons":         "castle",
    "dungeon master":   "castle",

    # ── Rubbish / trash → 🗑 ──────────────────────────────────────────────────
    "rubbish":          "trash",

    # ── See / look → 👀 ───────────────────────────────────────────────────────
    "see":              "eyes",
    "seen":             "eyes",
    "look":             "eyes",
    "observe":          "eyes",
    "surveillance":     "eyes",
    "spying":           "eyes",

    # ── Hike / trail → 🥾 ────────────────────────────────────────────────────
    "hike":             "hiking_boot",
    "trek":             "hiking_boot",
    "trail":            "hiking_boot",
    "trails":           "hiking_boot",
    "trailhead":        "hiking_boot",
    "nature walk":      "hiking_boot",
    "day hike":         "hiking_boot",

    # ── Outdoor / outside → ⛺ ────────────────────────────────────────────────
    "outdoor":          "camping",
    "outdoors":         "camping",
    "outside":          "camping",
    "exterior":         "camping",
    "open air":         "camping",

    # ── Inside / indoor → 🏠 ─────────────────────────────────────────────────
    "inside":           "home",
    "indoor":           "home",
    "indoors":          "home",
    "interior":         "home",

    # ── Soldier / military → 🪖 ───────────────────────────────────────────────
    "soldier":          "military_helmet",
    "soldiers":         "military_helmet",
    "military":         "military_helmet",
    "army":             "military_helmet",
    "troops":           "military_helmet",
    "infantry":         "military_helmet",
    "marines":          "military_helmet",
    "veteran":          "military_helmet",

    # ── Underwear → 🩲 ───────────────────────────────────────────────────────
    "underwear":        "underwear",
    "undies":           "underwear",
    "briefs":           "underwear",
    "boxers":           "underwear",
    "boxer briefs":     "underwear",
    "panties":          "underwear",
    "lingerie":         "underwear",
    "thong":            "underwear",
    "g-string":         "underwear",
    "bra":              "underwear",

    # ── Cigarette / smoking → 🚬 ─────────────────────────────────────────────
    "cigarette":        "cigarette",
    "cigarettes":       "cigarette",
    "cigar":            "cigarette",
    "cigars":           "cigarette",
    "smoke":            "cigarette",
    "smoking":          "cigarette",
    "smoker":           "cigarette",
    "tobacco":          "cigarette",
    "vape":             "cigarette",
    "vaping":           "cigarette",
    "e-cigarette":      "cigarette",

    # ── Ski / skiing → 🎿 ────────────────────────────────────────────────────
    "ski":              "skiing",
    "skis":             "skiing",
    "ski gear":         "skiing",
    "ski equipment":    "skiing",

    # ── Skier → ⛷ ───────────────────────────────────────────────────────────
    "skier":            "skier",
    "skiers":           "skier",

    # ── Yarn → 🧶 ────────────────────────────────────────────────────────────
    "yarn":             "yarn",
    "yarn ball":        "yarn",
    "crochet yarn":     "yarn",
    "wool yarn":        "yarn",

    # ── OK / okay → 👌 ───────────────────────────────────────────────────────
    "ok":               "ok_hand",
    "okay":             "ok_hand",
    "okey dokey":       "ok_hand",
    "a-okay":           "ok_hand",
    "all good":         "ok_hand",

    # ── Computer mouse → 🖱 ───────────────────────────────────────────────────
    "computer mouse":   "computer_mouse",
    "pc mouse":         "computer_mouse",
    "mouse pad":        "computer_mouse",
    "mousepad":         "computer_mouse",
    "trackball":        "computer_mouse",
    "trackpad":         "computer_mouse",
    "touchpad":         "computer_mouse",

    # ── Computer keyboard → ⌨ ────────────────────────────────────────────────
    "computer keyboard": "computer_keyboard",
    "pc keyboard":      "computer_keyboard",
    "mechanical keyboard": "computer_keyboard",
    "wireless keyboard": "computer_keyboard",
    "numpad":           "computer_keyboard",
    "number pad":       "computer_keyboard",
    "keypad":           "computer_keyboard",

    # ── Animal keyword expansion ──────────────────────────────────────────────

    # seal (had zero keywords!)
    "seal":             "seal",
    "seals":            "seal",
    "sea lion":         "seal",
    "sea lions":        "seal",
    "harbor seal":      "seal",
    "leopard seal":     "seal",

    # fly / housefly
    "fly":              "fly",
    "flies":            "fly",
    "housefly":         "fly",
    "house fly":        "fly",
    "horsefly":         "fly",
    "fruit fly":        "fly",
    "bluebottle":       "fly",
    "blowfly":          "fly",

    # mosquito (had only 1 keyword)
    "mosquitos":        "mosquito",
    "mosquitoes":       "mosquito",
    "gnat":             "mosquito",
    "gnats":            "mosquito",
    "midge":            "mosquito",
    "midges":           "mosquito",

    # scorpion
    "scorpion":         "scorpion",
    "scorpions":        "scorpion",

    # microbe / germ
    "microbe":          "microbe",
    "microbes":         "microbe",
    "bacteria":         "microbe",
    "bacterium":        "microbe",
    "virus":            "microbe",
    "viruses":          "microbe",
    "germ":             "microbe",
    "germs":            "microbe",
    "pathogen":         "microbe",

    # mammoth
    "mammoth":          "mammoth",
    "mammoths":         "mammoth",
    "woolly mammoth":   "mammoth",
    "mastodon":         "mammoth",

    # donkey
    "donkey":           "donkey",
    "donkeys":          "donkey",
    "mule":             "donkey",
    "burro":            "donkey",

    # t-rex
    "t rex":            "trex",
    "t-rex":            "trex",
    "tyrannosaurus":    "trex",
    "raptor":           "trex",
    "velociraptor":     "trex",

    # feather
    "feather":          "feather",
    "feathers":         "feather",
    "plume":            "feather",
    "quill":            "feather",

    # thin animals — synonyms + common variants
    "bats":             "bat",
    "vampire bat":      "bat",
    "fruit bat":        "bat",
    "beavers":          "beaver",
    "butterflies":      "butterfly",
    "moths":            "butterfly",
    "moth":             "butterfly",
    "camels":           "camel",
    "dromedary":        "camel",
    "crabs":            "crab",
    "hermit crab":      "crab",
    "horseshoe crab":   "crab",
    "crickets":         "cricket",
    "dolphins":         "dolphin",
    "porpoise":         "dolphin",
    "bottlenose":       "dolphin",
    "flamingos":        "flamingo",
    "foxes":            "fox",
    "vixen":            "fox",
    "red fox":          "fox",
    "arctic fox":       "fox",
    "goose":            "goose",
    "gosling":          "goose",
    "gander":           "goose",
    "porcupine":        "hedgehog",
    "kangaroos":        "kangaroo",
    "wallaby":          "kangaroo",
    "joey":             "kangaroo",
    "marsupial":        "kangaroo",
    "koalas":           "koala",
    "koala bear":       "koala",
    "lobsters":         "lobster",
    "crawfish":         "lobster",
    "crayfish":         "lobster",
    "crawdad":          "lobster",
    "otters":           "otter",
    "sea otter":        "otter",
    "river otter":      "otter",
    "giant panda":      "panda",
    "peacocks":         "peacock",
    "peahen":           "peacock",
    "roosters":         "rooster",
    "cock":             "rooster",
    "seahorses":        "seahorse",
    "sharks":           "shark",
    "great white":      "shark",
    "hammerhead":       "shark",
    "bull shark":       "shark",
    "shrimps":          "shrimp",
    "prawn":            "shrimp",
    "prawns":           "shrimp",
    "skunks":           "skunk",
    "polecat":          "skunk",
    "sloths":           "sloth",
    "snails":           "snail",
    "slug":             "snail",
    "slugs":            "snail",
    "spiders":          "spider",
    "tarantula":        "spider",
    "arachnid":         "spider",
    "squids":           "squid",
    "calamari":         "squid",
    "swans":            "swan",
    "cygnet":           "swan",
    "whales":           "whale",
    "humpback":         "whale",
    "blue whale":       "whale",
    "sperm whale":      "whale",
    "orca":             "whale",
    "killer whale":     "whale",
    "beluga":           "whale",
    "zebras":           "zebra",

    # ── Generic / catch-all labels ────────────────────────────────────────────

    # "parts / spares" — mechanical context → 🔩
    "parts":            "nut_bolt",
    "spares":           "nut_bolt",
    "spare":            "nut_bolt",
    "leftover parts":   "nut_bolt",
    "extra parts":      "nut_bolt",

    # "supplies / goods / items" — box/inventory context → 📦
    "supplies":         "package_box",
    "supply":           "package_box",
    "items":            "package_box",
    "goods":            "package_box",
    "contents":         "package_box",
    "inventory":        "package_box",
    "stock":            "package_box",
    "materials":        "package_box",
    "material":         "package_box",
    "kit":              "package_box",
    "collection":       "package_box",

    # "bits and bobs / misc / stuff" — truly generic → 🗃
    "stuff":            "misc_box",
    "things":           "misc_box",
    "bits":             "misc_box",
    "bobs":             "misc_box",
    "bits and bobs":    "misc_box",
    "odds and ends":    "misc_box",
    "misc":             "misc_box",
    "miscellaneous":    "misc_box",
    "assorted":         "misc_box",
    "various":          "misc_box",
    "random":           "misc_box",
    "junk drawer":      "misc_box",
    "knick knacks":     "misc_box",
    "knick-knacks":     "misc_box",
    "trinkets":         "misc_box",
    "whatnot":          "misc_box",
    "this and that":    "misc_box",
    "everything":       "misc_box",
    "catchall":         "misc_box",
    "catch all":        "misc_box",
    "general":          "misc_box",
    "other":            "misc_box",
    "extras":           "misc_box",
    "overflow":         "misc_box",
    "spare bits":       "misc_box",
    "loose parts":      "misc_box",
    "random stuff":     "misc_box",
    "mixed":            "misc_box",

    # ── Fire extinguisher → 🧯 ───────────────────────────────────────────────
    "fire extinguisher": "fire_extinguisher",
    "extinguisher":     "fire_extinguisher",
    "fire suppression": "fire_extinguisher",
    "fire safety":      "fire_extinguisher",
    "dry chemical":     "fire_extinguisher",
    "co2 extinguisher": "fire_extinguisher",
    "halon":            "fire_extinguisher",

    # ── Sign / placard → 🪧 ──────────────────────────────────────────────────
    "sign":             "sign",
    "signs":            "sign",
    "placard":          "sign",
    "signage":          "sign",
    "notice":           "sign",
    "notice board":     "sign",
    "billboard":        "sign",
    "poster":           "sign",
    "board":            "sign",

    # ── Coffin → ⚰ ───────────────────────────────────────────────────────────
    "coffin":           "coffin",
    "casket":           "coffin",
    "burial":           "coffin",
    "funeral":          "coffin",
    "hearse":           "coffin",
    "rest in peace":    "coffin",
    "deceased":         "coffin",

    # ── Funeral urn → ⚱ ──────────────────────────────────────────────────────
    "urn":              "funeral_urn",
    "funeral urn":      "funeral_urn",
    "ashes":            "funeral_urn",
    "cremation":        "funeral_urn",
    "memorial urn":     "funeral_urn",

    # ── Moon phases ───────────────────────────────────────────────────────────
    "new moon":             "moon_new",
    "dark moon":            "moon_new",
    "no moon":              "moon_new",
    "waxing crescent":      "moon_waxing_crescent",
    "waxing crescent moon": "moon_waxing_crescent",
    "first quarter moon":   "moon_first_quarter",
    "half moon":            "moon_first_quarter",
    "waxing gibbous":       "moon_waxing_gibbous",
    "waxing gibbous moon":  "moon_waxing_gibbous",
    "waxing moon":          "moon_waxing_gibbous",
    "full moon":            "moon_full",
    "moon phase":           "moon_full",
    "lunar phase":          "moon_full",
    "waning gibbous":       "moon_waning_gibbous",
    "waning gibbous moon":  "moon_waning_gibbous",
    "waning moon":          "moon_waning_crescent",
    "last quarter moon":    "moon_last_quarter",
    "third quarter moon":   "moon_last_quarter",
    "waning crescent":      "moon_waning_crescent",
    "waning crescent moon": "moon_waning_crescent",

    # ── Zodiac signs ──────────────────────────────────────────────────────────
    "aries":            "ram",
    "aries sign":       "ram",
    "taurus":           "ox",
    "taurus sign":      "ox",
    "gemini":           "people",
    "gemini sign":      "people",
    "cancer":           "crab",
    "cancer sign":      "crab",
    "cancer zodiac":    "crab",
    "leo":              "lion",
    "leo sign":         "lion",
    "leo zodiac":       "lion",
    "virgo":            "wheat",
    "virgo sign":       "wheat",
    "libra":            "scales",
    "libra sign":       "scales",
    "scorpio":          "scorpion",
    "scorpio sign":     "scorpion",
    "sagittarius":      "archery",
    "sagittarius sign": "archery",
    "capricorn":        "goat",
    "capricorn sign":   "goat",
    "aquarius":         "wave_water",
    "aquarius sign":    "wave_water",
    "pisces":           "fish",
    "pisces sign":      "fish",
    "ophiuchus":        "snake",
    "horoscope":        "glowing_star",
    "star sign":        "glowing_star",
    "astrology":        "glowing_star",

    # ── Colored hearts ────────────────────────────────────────────────────────
    "orange heart":     "heart_orange",
    "yellow heart":     "heart_yellow",
    "gold heart":       "heart_yellow",
    "green heart":      "heart_green",
    "teal heart":       "heart_green",
    "blue heart":       "heart_blue",
    "navy heart":       "heart_blue",
    "purple heart":     "heart_purple",
    "violet heart":     "heart_purple",
    "lavender heart":   "heart_purple",
    "brown heart":      "heart_brown",
    "black heart":      "heart_black",
    "dark heart":       "heart_black",
    "white heart":      "heart_white",
    "pink heart":       "heart_pink",

    # ── Colored circles ───────────────────────────────────────────────────────
    "red circle":       "circle_red",
    "red dot":          "circle_red",
    "orange circle":    "circle_orange",
    "orange dot":       "circle_orange",
    "yellow circle":    "circle_yellow",
    "yellow dot":       "circle_yellow",
    "green circle":     "circle_green",
    "green dot":        "circle_green",
    "blue circle":      "circle",
    "blue dot":         "circle",
    "purple circle":    "circle_purple",
    "purple dot":       "circle_purple",
    "brown circle":     "circle_brown",
    "black circle":     "circle_black",
    "black dot":        "circle_black",
    "white circle":     "circle_white",
    "white dot":        "circle_white",
    "dot":              "circle",
    "color code":       "circle_red",
    "colour code":      "circle_red",

    # ── Colored squares ───────────────────────────────────────────────────────
    "red square":       "square_red",
    "orange square":    "square_orange",
    "yellow square":    "square_yellow",
    "green square":     "square_green",
    "blue square":      "square",
    "purple square":    "square_purple",
    "brown square":     "square_brown",

    # ── Weather extras ────────────────────────────────────────────────────────
    "cloudy":           "cloudy",
    "overcast":         "cloudy",
    "partly cloudy":    "cloudy",
    "partly sunny":     "cloudy",
    "clouds":           "cloudy",
    "rain cloud":       "rainy",
    "showers":          "rainy",
    "foggy":            "foggy",
    "fog":              "foggy",
    "mist":             "foggy",
    "misty":            "foggy",
    "hazy":             "foggy",
    "haze":             "foggy",
    "snowy":            "snowy_cloud",
    "snow cloud":       "snowy_cloud",
    "light snow":       "snowy_cloud",
    "flurries":         "snowy_cloud",

    # ── Hole ─────────────────────────────────────────────────────────────────
    "hole":             "hole",
    "holes":            "hole",
    "pit":              "hole",
    "void":             "hole",
    "opening":          "hole",
    "cable hole":       "hole",
    "drill hole":       "hole",
    "access hole":      "hole",

    # ── Splat / splatter / blob ───────────────────────────────────────────────
    "splat":            "splat",
    "splatter":         "splat",
    "splattered":       "splat",
    "blob":             "splat",
    "blobs":            "splat",
    "gooey":            "splat",
    "impact":           "splat",
    "collision":        "splat",
    "boom":             "splat",
    "explosion":        "splat",
    "explode":          "splat",
    "burst":            "splat",
    "bang":             "splat",

    # ── Media controls ────────────────────────────────────────────────────────
    "play":             "play_button",
    "playing":          "play_button",
    "start":            "play_button",
    "pause":            "pause_button",
    "paused":           "pause_button",
    "hold":             "pause_button",
    "stop":             "stop_button",
    "stopped":          "stop_button",
    "halt":             "stop_button",
    "end":              "stop_button",
    "record":           "record_button",
    "rec":              "record_button",
    "fast forward":     "fast_forward",
    "skip forward":     "fast_forward",
    "skip ahead":       "fast_forward",
    "ff":               "fast_forward",
    "rewind":           "rewind_button",
    "skip back":        "rewind_button",
    "skip backward":    "rewind_button",
    "rw":               "rewind_button",
    "next track":       "next_track",
    "next song":        "next_track",
    "skip next":        "next_track",
    "previous track":   "prev_track",
    "previous song":    "prev_track",
    "last track":       "prev_track",
    "shuffle":          "shuffle",
    "random play":      "shuffle",
    "repeat":           "repeat_button",
    "loop":             "repeat_button",
    "repeat all":       "repeat_button",

    # ── Directional arrows ────────────────────────────────────────────────────
    "up":               "arrow_up",
    "upward":           "arrow_up",
    "upwards":          "arrow_up",
    "above":            "arrow_up",
    "north":            "arrow_up",
    "up arrow":         "arrow_up",
    "this way up":      "arrow_up",
    "this side up":     "arrow_up",
    "down":             "arrow_down",
    "downward":         "arrow_down",
    "downwards":        "arrow_down",
    "below":            "arrow_down",
    "south":            "arrow_down",
    "down arrow":       "arrow_down",
    "left":             "arrow_left",
    "leftward":         "arrow_left",
    "west":             "arrow_left",
    "left arrow":       "arrow_left",
    "right":            "arrow_right",
    "rightward":        "arrow_right",
    "east":             "arrow_right",
    "right arrow":      "arrow_right",
    "forward":          "arrow_right",
    "up right":         "arrow_up_right",
    "upper right":      "arrow_up_right",
    "northeast":        "arrow_up_right",
    "down right":       "arrow_down_right",
    "lower right":      "arrow_down_right",
    "southeast":        "arrow_down_right",
    "down left":        "arrow_down_left",
    "lower left":       "arrow_down_left",
    "up left":          "arrow_up_left",
    "upper left":       "arrow_up_left",
    "northwest":        "arrow_up_left",
    "back":             "arrow_back",
    "go back":          "arrow_back",
    "backward":         "arrow_back",
    "clockwise":        "rotate_cw",
    "rotate right":     "rotate_cw",
    "counterclockwise": "rotate_ccw",
    "counter clockwise":"rotate_ccw",
    "anticlockwise":    "rotate_ccw",
    "rotate left":      "rotate_ccw",
    "arrow":            "arrow_right",
    "arrows":           "rotate_cw",

    # ── Pointing fingers ──────────────────────────────────────────────────────
    "point up":         "pointing_up",
    "pointing up":      "pointing_up",
    "finger up":        "pointing_up",
    "press up":         "pointing_up",
    "swipe up":         "pointing_up",
    "point down":       "pointing_down",
    "pointing down":    "pointing_down",
    "finger down":      "pointing_down",
    "swipe down":       "pointing_down",
    "point left":       "pointing_left",
    "pointing left":    "pointing_left",
    "finger left":      "pointing_left",
    "swipe left":       "pointing_left",
    "point right":      "pointing_right",
    "pointing right":   "pointing_right",
    "finger right":     "pointing_right",
    "swipe right":      "pointing_right",
    "tap":              "pointing_right",
    "press here":       "pointing_right",
    "click here":       "pointing_right",
    "one":              "pointing_index",
    "attention":        "pointing_index",
    "pointer":          "pointing_index",

    # ── Info / question / exclamation ─────────────────────────────────────────
    "information":      "info_symbol",
    "info":             "info_symbol",
    "help":             "info_symbol",
    "details":          "info_symbol",
    "more info":        "info_symbol",
    "see inside":       "info_symbol",
    "question":         "question_mark",
    "questions":        "question_mark",
    "faq":              "question_mark",
    "unknown":          "question_mark",
    "query":            "question_mark",
    "unsure":           "question_mark",
    "exclamation":      "exclamation_mark",
    "important notice": "exclamation_mark",
    "attention required":"exclamation_mark",
    "heads up":         "exclamation_mark",

    # ── Clock faces ───────────────────────────────────────────────────────────
    # On the hour
    "1 o'clock":        "clock_1",   "one o'clock":      "clock_1",
    "1am":              "clock_1",   "1pm":              "clock_1",
    "2 o'clock":        "clock_2",   "two o'clock":      "clock_2",
    "2am":              "clock_2",   "2pm":              "clock_2",
    "3 o'clock":        "clock_3",   "three o'clock":    "clock_3",
    "3am":              "clock_3",   "3pm":              "clock_3",
    "4 o'clock":        "clock_4",   "four o'clock":     "clock_4",
    "4am":              "clock_4",   "4pm":              "clock_4",
    "5 o'clock":        "clock_5",   "five o'clock":     "clock_5",
    "5am":              "clock_5",   "5pm":              "clock_5",
    "6 o'clock":        "clock_6",   "six o'clock":      "clock_6",
    "6am":              "clock_6",   "6pm":              "clock_6",
    "7 o'clock":        "clock_7",   "seven o'clock":    "clock_7",
    "7am":              "clock_7",   "7pm":              "clock_7",
    "8 o'clock":        "clock_8",   "eight o'clock":    "clock_8",
    "8am":              "clock_8",   "8pm":              "clock_8",
    "9 o'clock":        "clock_9",   "nine o'clock":     "clock_9",
    "9am":              "clock_9",   "9pm":              "clock_9",
    "10 o'clock":       "clock_10",  "ten o'clock":      "clock_10",
    "10am":             "clock_10",  "10pm":             "clock_10",
    "11 o'clock":       "clock_11",  "eleven o'clock":   "clock_11",
    "11am":             "clock_11",  "11pm":             "clock_11",
    "12 o'clock":       "clock_12",  "twelve o'clock":   "clock_12",
    "noon":             "clock_12",  "midday":           "clock_12",
    "12pm":             "clock_12",  "midnight":         "clock_12",
    "12am":             "clock_12",
    # Half past
    "1:30":             "clock_1_30",  "one thirty":     "clock_1_30",  "half one":    "clock_1_30",
    "2:30":             "clock_2_30",  "two thirty":     "clock_2_30",  "half two":    "clock_2_30",
    "3:30":             "clock_3_30",  "three thirty":   "clock_3_30",  "half three":  "clock_3_30",
    "4:30":             "clock_4_30",  "four thirty":    "clock_4_30",  "half four":   "clock_4_30",
    "5:30":             "clock_5_30",  "five thirty":    "clock_5_30",  "half five":   "clock_5_30",
    "6:30":             "clock_6_30",  "six thirty":     "clock_6_30",  "half six":    "clock_6_30",
    "7:30":             "clock_7_30",  "seven thirty":   "clock_7_30",  "half seven":  "clock_7_30",
    "8:30":             "clock_8_30",  "eight thirty":   "clock_8_30",  "half eight":  "clock_8_30",
    "9:30":             "clock_9_30",  "nine thirty":    "clock_9_30",  "half nine":   "clock_9_30",
    "10:30":            "clock_10_30", "ten thirty":     "clock_10_30", "half ten":    "clock_10_30",
    "11:30":            "clock_11_30", "eleven thirty":  "clock_11_30", "half eleven": "clock_11_30",
    "12:30":            "clock_12_30", "twelve thirty":  "clock_12_30", "half twelve": "clock_12_30",
}


# ── Emoji lookup ──────────────────────────────────────────────────────────────
# Use plain Unicode codepoints — no variation selectors (U+FE0F).

_ICON_EMOJIS = {
    # Warning / safety
    "warning":          "⚠",           # ⚠
    "snowflake":        "❄",           # ❄
    "lightning":        "⚡",           # ⚡
    "skull_crossbones": "\U00002620",       # ☠

    # Seasons / weather
    "summer":           "\U00002600",       # ☀
    "beach":            "\U0001F3D6",       # 🏖
    "autumn":           "\U0001F342",       # 🍂
    "spring":           "\U0001F338",       # 🌸
    "rainbow":          "\U0001F308",       # 🌈
    "tornado":          "\U0001F32A",       # 🌪
    "storm":            "⛈",           # ⛈
    "umbrella":         "☔",           # ☔
    "wind":             "\U0001F4A8",       # 💨
    "snowman":          "\U000026C4",       # ⛄

    # People
    "person":           "\U0001F9D1",       # 🧑
    "man":              "\U0001F468",       # 👨
    "woman":            "\U0001F469",       # 👩
    "boy":              "\U0001F466",       # 👦
    "son":              "\U0001F466",       # 👦
    "girl":             "\U0001F467",       # 👧
    "elder":            "\U0001F474",       # 👴
    "grandma":          "\U0001F475",       # 👵
    "family":           "\U0001F46A",       # 👪
    "couple":           "\U0001F491",       # 💑
    "people":           "\U0001F465",       # 👥
    "police":           "\U0001F46E",       # 👮
    "guard":            "\U0001F482",       # 💂
    "detective":        "\U0001F575",       # 🕵
    "cowboy":           "\U0001F920",       # 🤠
    "ninja":            "\U0001F977",       # 🥷
    "wizard":           "\U0001F9D9",       # 🧙
    "vampire":          "\U0001F9DB",       # 🧛
    "zombie":           "\U0001F9DF",       # 🧟
    "santa":            "\U0001F385",       # 🎅
    "prince":           "\U0001F934",       # 🤴
    "princess":         "\U0001F478",       # 👸
    "superhero":        "\U0001F9B8",       # 🦸
    "tuxedo":           "\U0001F935",       # 🤵
    "worker":           "\U0001F477",       # 👷
    # Profession person emojis (ZWJ sequences — render on Win10/11 with updated Segoe UI Emoji)
    # Profession person emojis — ZWJ sequences, shaped correctly by HarfBuzz
    "prof_judge":       "\U0001F9D1‍\U00002696",  # 🧑‍⚖️
    "prof_chef":        "\U0001F9D1‍\U0001F373",  # 🧑‍🍳
    "prof_student":     "\U0001F9D1‍\U0001F393",  # 🧑‍🎓
    "prof_teacher":     "\U0001F9D1‍\U0001F3EB",  # 🧑‍🏫
    "prof_farmer":      "\U0001F9D1‍\U0001F33E",  # 🧑‍🌾
    "prof_medical":     "\U0001F9D1‍\U00002695",  # 🧑‍⚕️
    "prof_firefighter": "\U0001F9D1‍\U0001F692",  # 🧑‍🚒
    "prof_pilot":       "\U0001F9D1‍\U00002708",  # 🧑‍✈️
    "prof_mechanic":    "\U0001F9D1‍\U0001F527",  # 🧑‍🔧
    "prof_coder":       "\U0001F9D1‍\U0001F4BB",  # 🧑‍💻
    "prof_scientist":   "\U0001F9D1‍\U0001F52C",  # 🧑‍🔬
    "prof_artist":      "\U0001F9D1‍\U0001F3A8",  # 🧑‍🎨
    "prof_singer":      "\U0001F9D1‍\U0001F3A4",  # 🧑‍🎤
    "skull":            "\U0001F480",       # 💀
    "coin":             "\U0001FA99",       # 🪙
    "paper_doc":        "\U0001F4C4",       # 📄
    "shopping_cart":    "\U0001F6D2",       # 🛒
    "ghost":            "\U0001F47B",       # 👻
    "monster":          "\U0001F479",       # 👹
    "troll":            "\U0001F9CC",       # 🧌
    "poop":             "\U0001F4A9",       # 💩
    "middle_finger":    "\U0001F595",       # 🖕
    "devil":            "\U0001F608",       # 😈
    "swearing":         "\U0001F92C",       # 🤬
    "robot":            "\U0001F916",       # 🤖
    "clown":            "\U0001F921",       # 🤡
    "fairy":            "\U0001F9DA",       # 🧚
    "mermaid":          "\U0001F9DC",       # 🧜
    "elf":              "\U0001F9DD",       # 🧝
    "genie":            "\U0001F9DE",       # 🧞
    "alien_face":       "\U0001F47D",       # 👽
    "magic_wand":       "\U0001FA84",       # 🪄

    # People / gestures
    "wave_hand":        "\U0001F44B",       # 👋
    "thumbsup":         "\U0001F44D",       # 👍
    "thumbsdown":       "\U0001F44E",       # 👎
    "clap":             "\U0001F44F",       # 👏
    "handshake":        "\U0001F91D",       # 🤝
    "pray":             "\U0001F64F",       # 🙏
    "muscle":           "\U0001F4AA",       # 💪
    "crown":            "\U0001F451",       # 👑
    "heart":            "\U00002764",       # ❤
    "broken_heart":     "\U0001F494",       # 💔
    "heart_fire":       "\U00002764‍\U0001F525",  # ❤️‍🔥 (ZWJ)
    "heart_mend":       "\U00002764‍\U0001FA79",  # ❤️‍🩹 (ZWJ)
    "face_cry":         "\U0001F62D",       # 😭
    "face_laugh":       "\U0001F602",       # 😂
    "face_smile":       "\U0001F60A",       # 😊
    "face_sad":         "\U0001F614",       # 😔
    "face_happy":       "\U0001F604",       # 😄
    "face_angry":       "\U0001F621",       # 😡
    "face_bored":       "\U0001F611",       # 😑
    "face_shocked":     "\U0001F631",       # 😱
    "lips":             "\U0001F444",       # 👄
    "kiss":             "\U0001F48B",       # 💋
    "hug":              "\U0001F917",       # 🤗
    "eyes":             "\U0001F440",       # 👀
    "footprints":       "\U0001F463",       # 👣
    # Gestures
    "shrug":            "\U0001F937",       # 🤷
    "facepalm":         "\U0001F926",       # 🤦
    "crossed_fingers":  "\U0001F91E",       # 🤞
    "peace_sign":       "\U0000270C",       # ✌
    "hang_loose":       "\U0001F919",       # 🤙
    "rock_on":          "\U0001F918",       # 🤘
    "fist_bump":        "\U0001F91B",       # 🤛

    # Animals — pets
    "pet":              "\U0001F43E",       # 🐾
    "dog":              "\U0001F415",       # 🐕
    "cat":              "\U0001F408",       # 🐈
    "rabbit":           "\U0001F430",       # 🐰
    "hamster":          "\U0001F439",       # 🐹

    # Animals — birds
    "bird":             "\U0001F426",       # 🐦
    "parrot":           "\U0001F99C",       # 🦜
    "eagle":            "\U0001F985",       # 🦅
    "owl":              "\U0001F989",       # 🦉
    "penguin":          "\U0001F427",       # 🐧
    "duck":             "\U0001F986",       # 🦆
    "swan":             "\U0001F9A2",       # 🦢
    "flamingo":         "\U0001F9A9",       # 🦩
    "peacock":          "\U0001F99A",       # 🦚
    "rooster":          "\U0001F413",       # 🐓
    "chicken":          "\U0001F414",       # 🐔
    "chick":            "\U0001F425",       # 🐥

    # Animals — sea
    "fish":             "\U0001F420",       # 🐠
    "shark":            "\U0001F988",       # 🦈
    "dolphin":          "\U0001F42C",       # 🐬
    "whale":            "\U0001F433",       # 🐳
    "octopus":          "\U0001F419",       # 🐙
    "crab":             "\U0001F980",       # 🦀
    "lobster":          "\U0001F99E",       # 🦞
    "shrimp":           "\U0001F990",       # 🦐
    "squid":            "\U0001F991",       # 🦑
    "jellyfish":        "\U0001FABC",       # 🪼  (Unicode 15 — Noto supported)
    "worm":             "\U0001FAB1",       # 🪱
    "cockroach":        "\U0001FAB3",       # 🪳
    "seahorse":         "\U0001F420",       # 🐠  (no seahorse emoji; map to fish)
    "blowfish":         "\U0001F421",       # 🐡
    "seal":             "\U0001F9AD",       # 🦭

    # Animals — reptiles / amphibians
    "snake":            "\U0001F40D",       # 🐍
    "turtle":           "\U0001F422",       # 🐢
    "lizard":           "\U0001F98E",       # 🦎
    "crocodile":        "\U0001F40A",       # 🐊
    "frog":             "\U0001F438",       # 🐸
    "dinosaur":         "\U0001F995",       # 🦕
    "trex":             "\U0001F996",       # 🦖
    "dragon":           "\U0001F409",       # 🐉

    # Animals — insects
    "butterfly":        "\U0001F98B",       # 🦋
    "bee":              "\U0001F41D",       # 🐝
    "bug":              "\U0001F41B",       # 🐛
    "ant":              "\U0001F41C",       # 🐜
    "ladybug":          "\U0001F41E",       # 🐞
    "spider":           "\U0001F577",       # 🕷
    "cricket":          "\U0001F997",       # 🦗
    "mosquito":         "\U0001F99F",       # 🦟
    "fly":              "\U0001FAB0",       # 🪰
    "scorpion":         "\U0001F982",       # 🦂
    "microbe":          "\U0001F9A0",       # 🦠
    "snail":            "\U0001F40C",       # 🐌

    # Animals — farm / wild
    "horse":            "\U0001F434",       # 🐴
    "unicorn":          "\U0001F984",       # 🦄
    "cow":              "\U0001F42E",       # 🐮
    "pig":              "\U0001F437",       # 🐷
    "sheep":            "\U0001F411",       # 🐑
    "goat":             "\U0001F410",       # 🐐
    "lion":             "\U0001F981",       # 🦁
    "tiger":            "\U0001F42F",       # 🐯
    "bear":             "\U0001F43B",       # 🐻
    "panda":            "\U0001F43C",       # 🐼
    "koala":            "\U0001F428",       # 🐨
    "fox":              "\U0001F98A",       # 🦊
    "wolf":             "\U0001F43A",       # 🐺
    "elephant":         "\U0001F418",       # 🐘
    "giraffe":          "\U0001F992",       # 🦒
    "zebra":            "\U0001F993",       # 🦓
    "rhino":            "\U0001F98F",       # 🦏
    "hippo":            "\U0001F99B",       # 🦛
    "camel":            "\U0001F42A",       # 🐪
    "gorilla":          "\U0001F98D",       # 🦍
    "monkey":           "\U0001F412",       # 🐒
    "hedgehog":         "\U0001F994",       # 🦔
    "kangaroo":         "\U0001F998",       # 🦘
    "llama":            "\U0001F999",       # 🦙
    "sloth":            "\U0001F9A5",       # 🦥
    "otter":            "\U0001F9A6",       # 🦦
    "beaver":           "\U0001F9AB",       # 🦫
    "mouse":            "\U0001F42D",       # 🐭
    "deer":             "\U0001F98C",       # 🦌
    "boar":             "\U0001F417",       # 🐗
    "bat":              "\U0001F987",       # 🦇
    "raccoon":          "\U0001F99D",       # 🦝
    "skunk":            "\U0001F9A8",       # 🦨
    "badger":           "\U0001F9A1",       # 🦡
    "chipmunk":         "\U0001F43F",       # 🐿
    "bison":            "\U0001F9AC",       # 🦬
    "mammoth":          "\U0001F9A3",       # 🦣
    "donkey":           "\U0001FACF",       # 🫏
    "feather":          "\U0001FAB6",       # 🪶
    "dodo":             "\U0001F9A4",       # 🦤

    # Nature / plants
    "tree":             "\U0001F332",       # 🌲
    "palm":             "\U0001F334",       # 🌴
    "cactus":           "\U0001F335",       # 🌵
    "rose":             "\U0001F339",       # 🌹
    "sunflower":        "\U0001F33B",       # 🌻
    "tulip":            "\U0001F337",       # 🌷
    "bouquet":          "\U0001F490",       # 💐
    "herb":             "\U0001F33F",       # 🌿
    "seedling":         "\U0001F331",       # 🌱
    "clover":           "\U0001F340",       # 🍀
    "mushroom":         "\U0001F344",       # 🍄
    "leaf":             "\U0001F342",       # 🍂
    "wave_water":       "\U0001F30A",       # 🌊
    "mountain":         "\U000026F0",       # ⛰
    "volcano":          "\U0001F30B",       # 🌋
    "island":           "\U0001F3DD",       # 🏝
    "earth":            "\U0001F30D",       # 🌍

    # Space
    "rocket":           "\U0001F680",       # 🚀
    "astronaut":        "\U0001F9D1‍\U0001F680",  # 🧑‍🚀 (ZWJ — needs Segoe UI Emoji)
    "ufo":              "\U0001F6F8",       # 🛸
    "saturn":           "\U0001FA90",       # 🪐
    "moon":             "\U0001F319",       # 🌙
    "comet":            "\U00002604",       # ☄
    "galaxy":           "\U0001F30C",       # 🌌
    "telescope":        "\U0001F52D",       # 🔭
    "satellite":        "\U0001F6F0",       # 🛰
    "shooting_star":    "\U0001F320",       # 🌠
    "glowing_star":     "\U0001F31F",       # 🌟

    # Food — fruit
    "apple":            "\U0001F34E",       # 🍎
    "banana":           "\U0001F34C",       # 🍌
    "grapes":           "\U0001F347",       # 🍇
    "strawberry":       "\U0001F353",       # 🍓
    "blueberry":        "\U0001FAD0",       # 🫐
    "lemon":            "\U0001F34B",       # 🍋
    "orange_fruit":     "\U0001F34A",       # 🍊
    "watermelon":       "\U0001F349",       # 🍉
    "pineapple":        "\U0001F34D",       # 🍍
    "mango":            "\U0001F96D",       # 🥭
    "cherry":           "\U0001F352",       # 🍒
    "peach":            "\U0001F351",       # 🍑
    "pear":             "\U0001F350",       # 🍐
    "kiwi":             "\U0001F95D",       # 🥝
    "coconut":          "\U0001F965",       # 🥥

    # Food — vegetables
    "avocado":          "\U0001F951",       # 🥑
    "carrot":           "\U0001F955",       # 🥕
    "corn":             "\U0001F33D",       # 🌽
    "broccoli":         "\U0001F966",       # 🥦
    "tomato":           "\U0001F345",       # 🍅
    "potato":           "\U0001F954",       # 🥔
    "onion":            "\U0001F9C5",       # 🧅
    "garlic":           "\U0001F9C4",       # 🧄
    "pepper":           "\U0001F336",       # 🌶
    "salad":            "\U0001F957",       # 🥗

    # Food — meals
    "food":             "\U0001F37D",       # 🍽
    "pizza":            "\U0001F355",       # 🍕
    "burger":           "\U0001F354",       # 🍔
    "fries":            "\U0001F35F",       # 🍟
    "hotdog":           "\U0001F32D",       # 🌭
    "taco":             "\U0001F32E",       # 🌮
    "burrito":          "\U0001F32F",       # 🌯
    "sandwich":         "\U0001F96A",       # 🥪
    "noodles":          "\U0001F35C",       # 🍜
    "sushi":            "\U0001F363",       # 🍣
    "rice":             "\U0001F371",       # 🍱
    "curry":            "\U0001F35B",       # 🍛
    "stew":             "\U0001F372",       # 🍲
    "bread":            "\U0001F35E",       # 🍞
    "cheese":           "\U0001F9C0",       # 🧀
    "meat":             "\U0001F969",       # 🥩
    "bacon":            "\U0001F953",       # 🥓
    "breakfast":        "\U0001F373",       # 🍳
    "egg":              "\U0001F95A",       # 🥚
    "waffle":           "\U0001F9C7",       # 🧇
    "pancake":          "\U0001F95E",       # 🥞
    "cookies":          "\U0001F36A",       # 🍪
    "bbq":              "\U0001F356",       # 🍖
    "salt":             "\U0001F9C2",       # 🧂
    "butter":           "\U0001F9C8",       # 🧈

    # Food — sweet / dessert
    "birthday":         "\U0001F382",       # 🎂
    "ice_cream":        "\U0001F366",       # 🍦
    "donut":            "\U0001F369",       # 🍩
    "cupcake":          "\U0001F9C1",       # 🧁
    "chocolate":        "\U0001F36B",       # 🍫
    "candy":            "\U0001F36C",       # 🍬
    "lollipop":         "\U0001F36D",       # 🍭
    "honey":            "\U0001F36F",       # 🍯
    "croissant":        "\U0001F950",       # 🥐
    "pretzel":          "\U0001F968",       # 🥨
    "pie":              "\U0001F967",       # 🥧

    # Drinks
    "coffee":           "\U00002615",       # ☕
    "tea":              "\U0001F375",       # 🍵
    "teapot":           "\U0001FAD6",       # 🫖
    "hot_choc":         "\U00002615",       # ☕ (fallback)
    "beer":             "\U0001F37A",       # 🍺
    "wine":             "\U0001F377",       # 🍷
    "champagne":        "\U0001F942",       # 🥂
    "cocktail":         "\U0001F378",       # 🍸
    "tropical_drink":   "\U0001F379",       # 🍹
    "spirits":          "\U0001F943",       # 🥃
    "bubble_tea":       "\U0001F9CB",       # 🧋
    "straw_drink":      "\U0001F964",       # 🥤
    "juice":            "\U0001F9C3",       # 🧃
    "milk":             "\U0001F95B",       # 🥛
    "water":            "\U0001F4A7",       # 💧
    "peanut":           "\U0001F95C",       # 🥜
    "beans":            "\U0001FAD8",       # 🫘
    "jar":              "\U0001FAD9",       # 🫙
    "bubbles":          "\U0001FAB7",       # 🫧
    "falafel":          "\U0001F9C6",       # 🧆
    "dumpling":         "\U0001F95F",       # 🥟
    "chopsticks":       "\U0001F962",       # 🥢

    # Music
    "music":            "\U0001F3B5",       # 🎵
    "guitar":           "\U0001F3B8",       # 🎸
    "piano":            "\U0001F3B9",       # 🎹
    "drums":            "\U0001F941",       # 🥁
    "trumpet":          "\U0001F3BA",       # 🎺
    "violin":           "\U0001F3BB",       # 🎻
    "microphone":       "\U0001F3A4",       # 🎤
    "saxophone":        "\U0001F3B7",       # 🎷
    "flute":            "\U0001FA88",       # 🪈
    "radio":            "\U0001F4FB",       # 📻

    # Sports
    "sports":           "\U000026BD",       # ⚽
    "soccer":           "\U000026BD",       # ⚽
    "baseball":         "\U000026BE",       # ⚾
    "basketball":       "\U0001F3C0",       # 🏀
    "football":         "\U0001F3C8",       # 🏈
    "tennis":           "\U0001F3BE",       # 🎾
    "golf":             "\U000026F3",       # ⛳
    "bowling":          "\U0001F3B3",       # 🎳
    "volleyball":       "\U0001F3D0",       # 🏐
    "skiing":           "\U0001F3BF",       # 🎿
    "swimming":         "\U0001F3CA",       # 🏊
    "surfer":           "\U0001F3C4",       # 🏄
    "dancer":           "\U0001F483",       # 💃
    "cycling":          "\U0001F6B4",       # 🚴
    "boxing":           "\U0001F94A",       # 🥊
    "wrestling":        "\U0001F93C",       # 🤼
    "fencing":          "\U0001F93A",       # 🤺
    "gymnastics":       "\U0001F938",       # 🤸
    "running":          "\U0001F3C3",       # 🏃
    "yoga":             "\U0001F9D8",       # 🧘
    "camping":          "\U000026FA",       # ⛺
    "martial_arts":     "\U0001F94B",       # 🥋
    "fishing":          "\U0001F3A3",       # 🎣
    "kayaking":         "\U0001F6F6",       # 🛶
    "climbing":         "\U0001F9D7",       # 🧗
    "skateboard":       "\U0001F6F9",       # 🛹
    "hockey":           "\U0001F3D2",       # 🏒
    "archery":          "\U0001F3F9",       # 🏹
    "curling":          "\U0001F94C",       # 🥌
    "tabletennis":      "\U0001F3D3",       # 🏓
    "badminton":        "\U0001F3F8",       # 🏸

    # Home / rooms
    "home":             "\U0001F3E0",       # 🏠
    "kitchen":          "\U0001F374",       # 🍴
    "bedroom":          "\U0001F6CF",       # 🛏
    "bathroom":         "\U0001F6BF",       # 🚿
    "toilet":           "\U0001F6BD",       # 🚽
    "bathtub":          "\U0001F6C1",       # 🛁
    "soap":             "\U0001F9FC",       # 🧼
    "toothbrush":       "\U0001FAA5",       # 🪥
    "razor":            "\U0001FA92",       # 🪒
    "mirror":           "\U0001FA9E",       # 🪞
    "couch":            "\U0001F6CB",       # 🛋
    "chair":            "\U0001FA91",       # 🪑
    "door":             "\U0001F6AA",       # 🚪
    "window":           "\U0001FA9F",       # 🪟
    "bucket":           "\U0001FAA3",       # 🪣
    "plunger":          "\U0001FAA0",       # 🪠
    "sponge":           "\U0001F9FD",       # 🧽

    # Work / study
    "books":            "\U0001F4DA",       # 📚
    "tools":            "\U0001F527",       # 🔧
    "computer":         "\U0001F4BB",       # 💻
    "wireless":         "\U0001F6DC",       # 🛜
    "signal_bars":      "\U0001F4F6",       # 📶
    "floppy_disk":      "\U0001F4BE",       # 💾
    "cd":               "\U0001F4BF",       # 💿
    "dvd":              "\U0001F4C0",       # 📀
    "phone":            "\U0001F4F1",       # 📱
    "tv":               "\U0001F4FA",       # 📺
    "science":          "\U0001F9EA",       # 🧪
    "microscope":       "\U0001F52C",       # 🔬
    "dna":              "\U0001F9EC",       # 🧬
    "stethoscope":      "\U0001FA7A",       # 🩺
    "syringe":          "\U0001F489",       # 💉

    # Office objects
    "pencil":           "\U0000270F",       # ✏
    "chart":            "\U0001F4C8",       # 📈
    "clipboard":        "\U0001F4CB",       # 📋
    "newspaper":        "\U0001F4F0",       # 📰
    "magnify":          "\U0001F50D",       # 🔍

    # Tools / objects
    "gear":             "\U00002699",       # ⚙
    "magnet":           "\U0001F9F2",       # 🧲
    "key":              "\U0001F511",       # 🔑
    "lock":             "\U0001F512",       # 🔒
    "lightbulb":        "\U0001F4A1",       # 💡
    "flashlight_torch": "\U0001F526",       # 🔦
    "candle":           "\U0001F56F",       # 🕯
    "toolbox":          "\U0001F9F0",       # 🧰
    "ladder":           "\U0001FA9C",       # 🪜
    "hook":             "\U0001FA9D",       # 🪝
    "nut_bolt":         "\U0001F529",       # 🔩
    "safety_pin":       "\U0001F9F7",       # 🧷
    "basket":           "\U0001F9FA",       # 🧺
    "compass":          "\U0001F9ED",       # 🧭
    "package_box":      "\U0001F4E6",       # 📦
    "folder_icon":      "\U0001F4C1",       # 📁
    "ruler_tri":        "\U0001F4D0",       # 📐
    "scissors":         "\U00002702",       # ✂
    "laser_beam":       "\U0001F506",       # 🔆
    "hammer":           "\U0001F528",       # 🔨
    "screwdriver":      "\U0001FA9B",       # 🪛
    "saw_tool":         "\U0001FA9A",       # 🪚
    "axe":              "\U0001FA93",       # 🪓
    "clamp":            "\U0001F5DC",       # 🗜
    "bricks":           "\U0001F9F1",       # 🧱
    "thread":           "\U0001F9F5",       # 🧵
    "knot":             "\U0001FA62",       # 🪢

    # Maker / fabrication
    "printer_3d":       "\U0001F5A8",       # 🖨
    "diamond":          "\U0001F48E",       # 💎
    "wood":             "\U0001FAB5",       # 🪵
    "rock":             "\U0001FAA8",       # 🪨  (U+1FAA8 — U+1FAB8 is coral)
    "crystal_glass":    "\U0001F52E",       # 🔮
    "metal":            "\U00002699",       # ⚙  (gear = best available for raw metal)
    "clay":             "\U0001F3FA",       # 🏺

    # Transport
    "travel":           "\U00002708",       # ✈
    "airplane":         "\U00002708",       # ✈
    "car":              "\U0001F697",       # 🚗
    "taxi":             "\U0001F695",       # 🚕
    "racing":           "\U0001F3CE",       # 🏎
    "bus":              "\U0001F68C",       # 🚌
    "train":            "\U0001F682",       # 🚂
    "bicycle":          "\U0001F6B2",       # 🚲
    "motorcycle":       "\U0001F3CD",       # 🏍
    "tractor":          "\U0001F69C",       # 🚜
    "delivery_truck":   "\U0001F69A",       # 🚚
    "ambulance":        "\U0001F691",       # 🚑
    "fire_truck":       "\U0001F692",       # 🚒
    "helicopter":       "\U0001F681",       # 🚁
    "boat":             "\U000026F5",       # ⛵
    "ship":             "\U0001F6A2",       # 🚢
    "speedboat":        "\U0001F6A4",       # 🚤
    "parachute":        "\U0001FA82",       # 🪂
    "anchor":           "\U00002693",       # ⚓
    "luggage":          "\U0001F9F3",       # 🧳
    "backpack":         "\U0001F392",       # 🎒

    # Health / body
    "medicine":         "\U0001F48A",       # 💊
    "firstaid":         "\U0001FA79",       # 🩹
    "thermometer":      "\U0001F321",       # 🌡
    "bone":             "\U0001F9B4",       # 🦴
    "tooth":            "\U0001F9B7",       # 🦷
    "brain":            "\U0001F9E0",       # 🧠
    "ear":              "\U0001F442",       # 👂
    "nose":             "\U0001F443",       # 👃
    "eye_body":         "\U0001F441",       # 👁
    "lungs":            "\U0001FAC1",       # 🫁
    "anatomical_heart": "\U0001FAC0",       # 🫀
    "leg":              "\U0001F9B5",       # 🦵
    "blood":            "\U0001FA78",       # 🩸
    "ice":              "\U0001F9CA",       # 🧊

    # Finance
    "money":            "\U0001F4B0",       # 💰
    "mail":             "\U0001F4E7",       # 📧

    # Celebrations
    "christmas":        "\U0001F384",       # 🎄
    "halloween":        "\U0001F383",       # 🎃
    "graduation":       "\U0001F393",       # 🎓
    "wedding":          "\U0001F492",       # 💒
    "thanksgiving":     "\U0001F983",       # 🦃
    "gift":             "\U0001F381",       # 🎁
    "party":            "\U0001F389",       # 🎉
    "balloon":          "\U0001F388",       # 🎈
    "fireworks":        "\U0001F386",       # 🎆
    "sparkles":         "\U00002728",       # ✨
    "ribbon":           "\U0001F38A",       # 🎊
    "trophy":           "\U0001F3C6",       # 🏆
    "medal":            "\U0001F947",       # 🥇
    "medal_silver":     "\U0001F948",       # 🥈
    "medal_bronze":     "\U0001F949",       # 🥉
    "pinata":           "\U0001FA85",       # 🪅
    "disco_ball":       "\U0001FA69",       # 🪩
    "kite":             "\U0001FA81",       # 🪁
    "8ball":            "\U0001F3B1",       # 🎱

    # Requested additions
    "canned_food":      "\U0001F9C6",       # 🥫
    "bar":              "\U0001F37A",       # 🍺
    "badge":            "\U0001F4DB",       # 📛
    "bulb":             "\U0001F4A1",       # 💡
    "paintbrush":       "\U0001F58C",       # 🖌
    "button":           "\U0001F518",       # 🔘 (closest circular button shape)
    "flag":             "\U0001F6A9",       # 🚩
    "checkered_flag":   "\U0001F3C1",       # 🏁
    "crayon":           "\U0001F58D",       # 🖍
    "paperclip":        "\U0001F4CE",       # 📎
    "needle":           "\U0001FAA1",       # 🪡

    # Other misc
    "trash":            "\U0001F5D1",       # 🗑
    "fire":             "\U0001F525",       # 🔥
    "camera":           "\U0001F4F7",       # 📷
    "clothes":          "\U0001F455",       # 👕  (generic fallback)
    "dress":            "\U0001F457",       # 👗
    "jeans":            "\U0001F456",       # 👖
    "shoe":             "\U0001F45F",       # 👟
    "sock":             "\U0001F9E6",       # 🧦
    "scarf":            "\U0001F9E3",       # 🧣
    "glove":            "\U0001F9E4",       # 🧤
    "coat":             "\U0001F9E5",       # 🧥
    "tie":              "\U0001F454",       # 👔
    "bikini":           "\U0001F459",       # 👙
    "purse":            "\U0001F45C",       # 👜
    "hat":              "\U0001F9E2",       # 🧢
    "glasses":          "\U0001F453",       # 👓
    "ring":             "\U0001F48D",       # 💍
    # Finance / communication
    "envelope":         "\U00002709",       # ✉
    "mailbox":          "\U0001F4EC",       # 📬
    # Entertainment
    "theater":          "\U0001F3AD",       # 🎭
    "clapperboard":     "\U0001F3AC",       # 🎬
    "megaphone":        "\U0001F4E3",       # 📣
    "bell":             "\U0001F514",       # 🔔
    "cleaning":         "\U0001F9F9",       # 🧹
    "recycle":          "\U0000267B",       # ♻
    # Hazard / Safety
    "radioactive":      "\U00002622",       # ☢
    "biohazard":        "\U00002623",       # ☣
    "prohibited":       "\U0001F6AB",       # 🚫
    "no_smoking":       "\U0001F6AD",       # 🚭
    "no_littering":     "\U0001F6AF",       # 🚯
    "no_pedestrians":   "\U0001F6B7",       # 🚷
    "no_bicycles":      "\U0001F6B3",       # 🚳
    "non_potable_water": "\U0001F6B1",      # 🚱
    "no_phones":        "\U0001F4F5",       # 📵
    "no_under_18":      "\U0001F51E",       # 🔞
    "shield":           "\U0001F6E1",       # 🛡
    "sword":            "\U00002694",       # ⚔
    # Vehicles
    "pickup_truck":     "\U0001F6FB",       # 🛻
    "minivan":          "\U0001F690",       # 🚐
    # Food / Veg
    "eggplant":         "\U0001F346",       # 🍆
    "cucumber":         "\U0001F952",       # 🥒
    "bell_pepper":      "\U0001FAD1",       # 🫑
    "sweet_potato":     "\U0001F360",       # 🍠
    "chestnut":         "\U0001F330",       # 🌰
    "leafy_greens":     "\U0001F96C",       # 🥬
    "bagel":            "\U0001F96F",       # 🥯
    "hotpot":           "\U0001FAD5",       # 🫕
    # Plants
    "potted_plant":     "\U0001FAB4",       # 🪴
    "hibiscus":         "\U0001F33A",       # 🌺
    "lotus":            "\U0001FAB7",       # 🪷
    "coral":            "\U0001FAB8",       # 🪸
    "nest":             "\U0001FABA",       # 🪺
    # Animals
    "beetle":           "\U0001FAB2",       # 🪲
    "moose":            "\U0001FACE",       # 🫎  (Unicode 15)
    "goose":            "\U0001FABF",       # 🪿  (Unicode 15)
    "crow":             "\U0001F426‍\U00002B1B",  # 🐦‍⬛ (ZWJ — black bird)
    "polar_bear":       "\U0001F43B‍\U00002744",  # 🐻‍❄️ (ZWJ)
    "baby":             "\U0001F476",       # 👶
    "art":              "\U0001F3A8",       # 🎨
    "gaming":           "\U0001F3AE",       # 🎮
    "chess":            "\U0000265F",       # ♟
    "card_spade":       "\U00002660",       # ♠
    "card_club":        "\U00002663",       # ♣
    "card_diamond":     "\U00002666",       # ♦
    "card_heart":       "\U00002665",       # ♥
    "star":             "\U00002B50",       # ⭐
    "time":             "\U000023F0",       # ⏰
    "dice_icon":        "\U0001F3B2",       # 🎲
    "puzzle_icon":      "\U0001F9E9",       # 🧩
    "circus":           "\U0001F3AA",       # 🎪
    "boomerang":        "\U0001FA83",       # 🪃
    "yoyo":             "\U0001FA80",       # 🪀
    "dart":             "\U0001F3AF",       # 🎯
    "diving":           "\U0001F93F",       # 🤿
    "headphones_icon":  "\U0001F3A7",       # 🎧
    "banjo_icon":       "\U0001FA95",       # 🪕
    "accordion":        "\U0001FA97",       # 🪗

    # Faces (new expressions)
    "face_melt":        "\U0001FAE0",       # 🫠
    "face_salute":      "\U0001FAE1",       # 🫡
    "face_peek":        "\U0001FAE3",       # 🫣

    # Home / objects
    "teddy_bear":       "\U0001F9F8",       # 🧸
    "nesting_dolls":    "\U0001FA86",       # 🪆
    "mousetrap":        "\U0001FA94",       # 🪤
    "headstone":        "\U0001FAA6",       # 🪦
    "hut":              "\U0001F6D6",       # 🛖
    "cityscape":        "\U0001F3D9",       # 🏙
    "road":             "\U0001F6E3",       # 🛣

    # Sports
    "roller_skate":     "\U0001F6FC",       # 🛼

    # Health
    "xray":             "\U0001FA7B",       # 🩻

    # Globe
    "globe_meridians":  "\U0001F310",       # 🌐

    # Buildings
    "office_building":  "\U0001F3E2",       # 🏢
    "school_building":  "\U0001F3EB",       # 🏫
    "castle":           "\U0001F3F0",       # 🏰
    "church":           "\U000026EA",       # ⛪
    "stadium":          "\U0001F3DF",       # 🏟
    "museum":           "\U0001F3DB",       # 🏛
    "bank":             "\U0001F3E6",       # 🏦
    "hospital_building": "\U0001F3E5",      # 🏥

    # Ham radio
    "antenna":          "\U0001F4E1",       # 📡

    # Barber / voting
    "barber_pole":      "\U0001F488",       # 💈
    "ballot_box":       "\U0001F5F3",       # 🗳

    # Electrical
    "battery":          "\U0001F50B",       # 🔋
    "plug":             "\U0001F50C",       # 🔌

    # Spiritual / religious
    "angel":            "\U0001F47C",       # 👼
    "halo_face":        "\U0001F607",       # 😇
    "cross":            "\U0000271D",       # ✝
    "star_of_david":    "\U00002721",       # ✡

    # ── Country flags (Regional Indicator pairs — rendered via Noto Color Emoji) ──
    "flag_ac": "\U0001F1E6\U0001F1E8",  # 🇦🇨 Ascension Island
    "flag_ad": "\U0001F1E6\U0001F1E9",  # 🇦🇩 Andorra
    "flag_ae": "\U0001F1E6\U0001F1EA",  # 🇦🇪 UAE
    "flag_af": "\U0001F1E6\U0001F1EB",  # 🇦🇫 Afghanistan
    "flag_ag": "\U0001F1E6\U0001F1EC",  # 🇦🇬 Antigua & Barbuda
    "flag_ai": "\U0001F1E6\U0001F1EE",  # 🇦🇮 Anguilla
    "flag_al": "\U0001F1E6\U0001F1F1",  # 🇦🇱 Albania
    "flag_am": "\U0001F1E6\U0001F1F2",  # 🇦🇲 Armenia
    "flag_ao": "\U0001F1E6\U0001F1F4",  # 🇦🇴 Angola
    "flag_aq": "\U0001F1E6\U0001F1F6",  # 🇦🇶 Antarctica
    "flag_ar": "\U0001F1E6\U0001F1F7",  # 🇦🇷 Argentina
    "flag_as": "\U0001F1E6\U0001F1F8",  # 🇦🇸 American Samoa
    "flag_at": "\U0001F1E6\U0001F1F9",  # 🇦🇹 Austria
    "flag_au": "\U0001F1E6\U0001F1FA",  # 🇦🇺 Australia
    "flag_aw": "\U0001F1E6\U0001F1FC",  # 🇦🇼 Aruba
    "flag_ax": "\U0001F1E6\U0001F1FD",  # 🇦🇽 Åland Islands
    "flag_az": "\U0001F1E6\U0001F1FF",  # 🇦🇿 Azerbaijan
    "flag_ba": "\U0001F1E7\U0001F1E6",  # 🇧🇦 Bosnia & Herzegovina
    "flag_bb": "\U0001F1E7\U0001F1E7",  # 🇧🇧 Barbados
    "flag_bd": "\U0001F1E7\U0001F1E9",  # 🇧🇩 Bangladesh
    "flag_be": "\U0001F1E7\U0001F1EA",  # 🇧🇪 Belgium
    "flag_bf": "\U0001F1E7\U0001F1EB",  # 🇧🇫 Burkina Faso
    "flag_bg": "\U0001F1E7\U0001F1EC",  # 🇧🇬 Bulgaria
    "flag_bh": "\U0001F1E7\U0001F1ED",  # 🇧🇭 Bahrain
    "flag_bi": "\U0001F1E7\U0001F1EE",  # 🇧🇮 Burundi
    "flag_bj": "\U0001F1E7\U0001F1EF",  # 🇧🇯 Benin
    "flag_bl": "\U0001F1E7\U0001F1F1",  # 🇧🇱 St. Barthélemy
    "flag_bm": "\U0001F1E7\U0001F1F2",  # 🇧🇲 Bermuda
    "flag_bn": "\U0001F1E7\U0001F1F3",  # 🇧🇳 Brunei
    "flag_bo": "\U0001F1E7\U0001F1F4",  # 🇧🇴 Bolivia
    "flag_bq": "\U0001F1E7\U0001F1F6",  # 🇧🇶 Caribbean Netherlands
    "flag_br": "\U0001F1E7\U0001F1F7",  # 🇧🇷 Brazil
    "flag_bs": "\U0001F1E7\U0001F1F8",  # 🇧🇸 Bahamas
    "flag_bt": "\U0001F1E7\U0001F1F9",  # 🇧🇹 Bhutan
    "flag_bv": "\U0001F1E7\U0001F1FB",  # 🇧🇻 Bouvet Island
    "flag_bw": "\U0001F1E7\U0001F1FC",  # 🇧🇼 Botswana
    "flag_by": "\U0001F1E7\U0001F1FE",  # 🇧🇾 Belarus
    "flag_bz": "\U0001F1E7\U0001F1FF",  # 🇧🇿 Belize
    "flag_ca": "\U0001F1E8\U0001F1E6",  # 🇨🇦 Canada
    "flag_cc": "\U0001F1E8\U0001F1E8",  # 🇨🇨 Cocos Islands
    "flag_cd": "\U0001F1E8\U0001F1E9",  # 🇨🇩 Congo - Kinshasa
    "flag_cf": "\U0001F1E8\U0001F1EB",  # 🇨🇫 Central African Republic
    "flag_cg": "\U0001F1E8\U0001F1EC",  # 🇨🇬 Congo - Brazzaville
    "flag_ch": "\U0001F1E8\U0001F1ED",  # 🇨🇭 Switzerland
    "flag_ci": "\U0001F1E8\U0001F1EE",  # 🇨🇮 Côte d'Ivoire
    "flag_ck": "\U0001F1E8\U0001F1F0",  # 🇨🇰 Cook Islands
    "flag_cl": "\U0001F1E8\U0001F1F1",  # 🇨🇱 Chile
    "flag_cm": "\U0001F1E8\U0001F1F2",  # 🇨🇲 Cameroon
    "flag_cn": "\U0001F1E8\U0001F1F3",  # 🇨🇳 China
    "flag_co": "\U0001F1E8\U0001F1F4",  # 🇨🇴 Colombia
    "flag_cp": "\U0001F1E8\U0001F1F5",  # 🇨🇵 Clipperton Island
    "flag_cr": "\U0001F1E8\U0001F1F7",  # 🇨🇷 Costa Rica
    "flag_cu": "\U0001F1E8\U0001F1FA",  # 🇨🇺 Cuba
    "flag_cv": "\U0001F1E8\U0001F1FB",  # 🇨🇻 Cape Verde
    "flag_cw": "\U0001F1E8\U0001F1FC",  # 🇨🇼 Curaçao
    "flag_cx": "\U0001F1E8\U0001F1FD",  # 🇨🇽 Christmas Island
    "flag_cy": "\U0001F1E8\U0001F1FE",  # 🇨🇾 Cyprus
    "flag_cz": "\U0001F1E8\U0001F1FF",  # 🇨🇿 Czechia
    "flag_de": "\U0001F1E9\U0001F1EA",  # 🇩🇪 Germany
    "flag_dg": "\U0001F1E9\U0001F1EC",  # 🇩🇬 Diego Garcia
    "flag_dj": "\U0001F1E9\U0001F1EF",  # 🇩🇯 Djibouti
    "flag_dk": "\U0001F1E9\U0001F1F0",  # 🇩🇰 Denmark
    "flag_dm": "\U0001F1E9\U0001F1F2",  # 🇩🇲 Dominica
    "flag_do": "\U0001F1E9\U0001F1F4",  # 🇩🇴 Dominican Republic
    "flag_dz": "\U0001F1E9\U0001F1FF",  # 🇩🇿 Algeria
    "flag_ea": "\U0001F1EA\U0001F1E6",  # 🇪🇦 Ceuta & Melilla
    "flag_ec": "\U0001F1EA\U0001F1E8",  # 🇪🇨 Ecuador
    "flag_ee": "\U0001F1EA\U0001F1EA",  # 🇪🇪 Estonia
    "flag_eg": "\U0001F1EA\U0001F1EC",  # 🇪🇬 Egypt
    "flag_eh": "\U0001F1EA\U0001F1ED",  # 🇪🇭 Western Sahara
    "flag_er": "\U0001F1EA\U0001F1F7",  # 🇪🇷 Eritrea
    "flag_es": "\U0001F1EA\U0001F1F8",  # 🇪🇸 Spain
    "flag_et": "\U0001F1EA\U0001F1F9",  # 🇪🇹 Ethiopia
    "flag_eu": "\U0001F1EA\U0001F1FA",  # 🇪🇺 European Union
    "flag_fi": "\U0001F1EB\U0001F1EE",  # 🇫🇮 Finland
    "flag_fj": "\U0001F1EB\U0001F1EF",  # 🇫🇯 Fiji
    "flag_fk": "\U0001F1EB\U0001F1F0",  # 🇫🇰 Falkland Islands
    "flag_fm": "\U0001F1EB\U0001F1F2",  # 🇫🇲 Micronesia
    "flag_fo": "\U0001F1EB\U0001F1F4",  # 🇫🇴 Faroe Islands
    "flag_fr": "\U0001F1EB\U0001F1F7",  # 🇫🇷 France
    "flag_ga": "\U0001F1EC\U0001F1E6",  # 🇬🇦 Gabon
    "flag_gb": "\U0001F1EC\U0001F1E7",  # 🇬🇧 UK
    "flag_gd": "\U0001F1EC\U0001F1E9",  # 🇬🇩 Grenada
    "flag_ge": "\U0001F1EC\U0001F1EA",  # 🇬🇪 Georgia
    "flag_gf": "\U0001F1EC\U0001F1EB",  # 🇬🇫 French Guiana
    "flag_gg": "\U0001F1EC\U0001F1EC",  # 🇬🇬 Guernsey
    "flag_gh": "\U0001F1EC\U0001F1ED",  # 🇬🇭 Ghana
    "flag_gi": "\U0001F1EC\U0001F1EE",  # 🇬🇮 Gibraltar
    "flag_gl": "\U0001F1EC\U0001F1F1",  # 🇬🇱 Greenland
    "flag_gm": "\U0001F1EC\U0001F1F2",  # 🇬🇲 Gambia
    "flag_gn": "\U0001F1EC\U0001F1F3",  # 🇬🇳 Guinea
    "flag_gp": "\U0001F1EC\U0001F1F5",  # 🇬🇵 Guadeloupe
    "flag_gq": "\U0001F1EC\U0001F1F6",  # 🇬🇶 Equatorial Guinea
    "flag_gr": "\U0001F1EC\U0001F1F7",  # 🇬🇷 Greece
    "flag_gs": "\U0001F1EC\U0001F1F8",  # 🇬🇸 South Georgia
    "flag_gt": "\U0001F1EC\U0001F1F9",  # 🇬🇹 Guatemala
    "flag_gu": "\U0001F1EC\U0001F1FA",  # 🇬🇺 Guam
    "flag_gw": "\U0001F1EC\U0001F1FC",  # 🇬🇼 Guinea-Bissau
    "flag_gy": "\U0001F1EC\U0001F1FE",  # 🇬🇾 Guyana
    "flag_hk": "\U0001F1ED\U0001F1F0",  # 🇭🇰 Hong Kong
    "flag_hm": "\U0001F1ED\U0001F1F2",  # 🇭🇲 Heard & McDonald Islands
    "flag_hn": "\U0001F1ED\U0001F1F3",  # 🇭🇳 Honduras
    "flag_hr": "\U0001F1ED\U0001F1F7",  # 🇭🇷 Croatia
    "flag_ht": "\U0001F1ED\U0001F1F9",  # 🇭🇹 Haiti
    "flag_hu": "\U0001F1ED\U0001F1FA",  # 🇭🇺 Hungary
    "flag_ic": "\U0001F1EE\U0001F1E8",  # 🇮🇨 Canary Islands
    "flag_id": "\U0001F1EE\U0001F1E9",  # 🇮🇩 Indonesia
    "flag_ie": "\U0001F1EE\U0001F1EA",  # 🇮🇪 Ireland
    "flag_il": "\U0001F1EE\U0001F1F1",  # 🇮🇱 Israel
    "flag_im": "\U0001F1EE\U0001F1F2",  # 🇮🇲 Isle of Man
    "flag_in": "\U0001F1EE\U0001F1F3",  # 🇮🇳 India
    "flag_io": "\U0001F1EE\U0001F1F4",  # 🇮🇴 British Indian Ocean Territory
    "flag_iq": "\U0001F1EE\U0001F1F6",  # 🇮🇶 Iraq
    "flag_ir": "\U0001F1EE\U0001F1F7",  # 🇮🇷 Iran
    "flag_is": "\U0001F1EE\U0001F1F8",  # 🇮🇸 Iceland
    "flag_it": "\U0001F1EE\U0001F1F9",  # 🇮🇹 Italy
    "flag_je": "\U0001F1EF\U0001F1EA",  # 🇯🇪 Jersey
    "flag_jm": "\U0001F1EF\U0001F1F2",  # 🇯🇲 Jamaica
    "flag_jo": "\U0001F1EF\U0001F1F4",  # 🇯🇴 Jordan
    "flag_jp": "\U0001F1EF\U0001F1F5",  # 🇯🇵 Japan
    "flag_ke": "\U0001F1F0\U0001F1EA",  # 🇰🇪 Kenya
    "flag_kg": "\U0001F1F0\U0001F1EC",  # 🇰🇬 Kyrgyzstan
    "flag_kh": "\U0001F1F0\U0001F1ED",  # 🇰🇭 Cambodia
    "flag_ki": "\U0001F1F0\U0001F1EE",  # 🇰🇮 Kiribati
    "flag_km": "\U0001F1F0\U0001F1F2",  # 🇰🇲 Comoros
    "flag_kn": "\U0001F1F0\U0001F1F3",  # 🇰🇳 St. Kitts & Nevis
    "flag_kp": "\U0001F1F0\U0001F1F5",  # 🇰🇵 North Korea
    "flag_kr": "\U0001F1F0\U0001F1F7",  # 🇰🇷 South Korea
    "flag_kw": "\U0001F1F0\U0001F1FC",  # 🇰🇼 Kuwait
    "flag_ky": "\U0001F1F0\U0001F1FE",  # 🇰🇾 Cayman Islands
    "flag_kz": "\U0001F1F0\U0001F1FF",  # 🇰🇿 Kazakhstan
    "flag_la": "\U0001F1F1\U0001F1E6",  # 🇱🇦 Laos
    "flag_lb": "\U0001F1F1\U0001F1E7",  # 🇱🇧 Lebanon
    "flag_lc": "\U0001F1F1\U0001F1E8",  # 🇱🇨 St. Lucia
    "flag_li": "\U0001F1F1\U0001F1EE",  # 🇱🇮 Liechtenstein
    "flag_lk": "\U0001F1F1\U0001F1F0",  # 🇱🇰 Sri Lanka
    "flag_lr": "\U0001F1F1\U0001F1F7",  # 🇱🇷 Liberia
    "flag_ls": "\U0001F1F1\U0001F1F8",  # 🇱🇸 Lesotho
    "flag_lt": "\U0001F1F1\U0001F1F9",  # 🇱🇹 Lithuania
    "flag_lu": "\U0001F1F1\U0001F1FA",  # 🇱🇺 Luxembourg
    "flag_lv": "\U0001F1F1\U0001F1FB",  # 🇱🇻 Latvia
    "flag_ly": "\U0001F1F1\U0001F1FE",  # 🇱🇾 Libya
    "flag_ma": "\U0001F1F2\U0001F1E6",  # 🇲🇦 Morocco
    "flag_mc": "\U0001F1F2\U0001F1E8",  # 🇲🇨 Monaco
    "flag_md": "\U0001F1F2\U0001F1E9",  # 🇲🇩 Moldova
    "flag_me": "\U0001F1F2\U0001F1EA",  # 🇲🇪 Montenegro
    "flag_mf": "\U0001F1F2\U0001F1EB",  # 🇲🇫 St. Martin
    "flag_mg": "\U0001F1F2\U0001F1EC",  # 🇲🇬 Madagascar
    "flag_mh": "\U0001F1F2\U0001F1ED",  # 🇲🇭 Marshall Islands
    "flag_mk": "\U0001F1F2\U0001F1F0",  # 🇲🇰 North Macedonia
    "flag_ml": "\U0001F1F2\U0001F1F1",  # 🇲🇱 Mali
    "flag_mm": "\U0001F1F2\U0001F1F2",  # 🇲🇲 Myanmar
    "flag_mn": "\U0001F1F2\U0001F1F3",  # 🇲🇳 Mongolia
    "flag_mo": "\U0001F1F2\U0001F1F4",  # 🇲🇴 Macao
    "flag_mp": "\U0001F1F2\U0001F1F5",  # 🇲🇵 Northern Mariana Islands
    "flag_mq": "\U0001F1F2\U0001F1F6",  # 🇲🇶 Martinique
    "flag_mr": "\U0001F1F2\U0001F1F7",  # 🇲🇷 Mauritania
    "flag_ms": "\U0001F1F2\U0001F1F8",  # 🇲🇸 Montserrat
    "flag_mt": "\U0001F1F2\U0001F1F9",  # 🇲🇹 Malta
    "flag_mu": "\U0001F1F2\U0001F1FA",  # 🇲🇺 Mauritius
    "flag_mv": "\U0001F1F2\U0001F1FB",  # 🇲🇻 Maldives
    "flag_mw": "\U0001F1F2\U0001F1FC",  # 🇲🇼 Malawi
    "flag_mx": "\U0001F1F2\U0001F1FD",  # 🇲🇽 Mexico
    "flag_my": "\U0001F1F2\U0001F1FE",  # 🇲🇾 Malaysia
    "flag_mz": "\U0001F1F2\U0001F1FF",  # 🇲🇿 Mozambique
    "flag_na": "\U0001F1F3\U0001F1E6",  # 🇳🇦 Namibia
    "flag_nc": "\U0001F1F3\U0001F1E8",  # 🇳🇨 New Caledonia
    "flag_ne": "\U0001F1F3\U0001F1EA",  # 🇳🇪 Niger
    "flag_nf": "\U0001F1F3\U0001F1EB",  # 🇳🇫 Norfolk Island
    "flag_ng": "\U0001F1F3\U0001F1EC",  # 🇳🇬 Nigeria
    "flag_ni": "\U0001F1F3\U0001F1EE",  # 🇳🇮 Nicaragua
    "flag_nl": "\U0001F1F3\U0001F1F1",  # 🇳🇱 Netherlands
    "flag_no": "\U0001F1F3\U0001F1F4",  # 🇳🇴 Norway
    "flag_np": "\U0001F1F3\U0001F1F5",  # 🇳🇵 Nepal
    "flag_nr": "\U0001F1F3\U0001F1F7",  # 🇳🇷 Nauru
    "flag_nu": "\U0001F1F3\U0001F1FA",  # 🇳🇺 Niue
    "flag_nz": "\U0001F1F3\U0001F1FF",  # 🇳🇿 New Zealand
    "flag_om": "\U0001F1F4\U0001F1F2",  # 🇴🇲 Oman
    "flag_pa": "\U0001F1F5\U0001F1E6",  # 🇵🇦 Panama
    "flag_pe": "\U0001F1F5\U0001F1EA",  # 🇵🇪 Peru
    "flag_pf": "\U0001F1F5\U0001F1EB",  # 🇵🇫 French Polynesia
    "flag_pg": "\U0001F1F5\U0001F1EC",  # 🇵🇬 Papua New Guinea
    "flag_ph": "\U0001F1F5\U0001F1ED",  # 🇵🇭 Philippines
    "flag_pk": "\U0001F1F5\U0001F1F0",  # 🇵🇰 Pakistan
    "flag_pl": "\U0001F1F5\U0001F1F1",  # 🇵🇱 Poland
    "flag_pm": "\U0001F1F5\U0001F1F2",  # 🇵🇲 St. Pierre & Miquelon
    "flag_pn": "\U0001F1F5\U0001F1F3",  # 🇵🇳 Pitcairn Islands
    "flag_pr": "\U0001F1F5\U0001F1F7",  # 🇵🇷 Puerto Rico
    "flag_ps": "\U0001F1F5\U0001F1F8",  # 🇵🇸 Palestinian Territories
    "flag_pt": "\U0001F1F5\U0001F1F9",  # 🇵🇹 Portugal
    "flag_pw": "\U0001F1F5\U0001F1FC",  # 🇵🇼 Palau
    "flag_py": "\U0001F1F5\U0001F1FE",  # 🇵🇾 Paraguay
    "flag_qa": "\U0001F1F6\U0001F1E6",  # 🇶🇦 Qatar
    "flag_re": "\U0001F1F7\U0001F1EA",  # 🇷🇪 Réunion
    "flag_ro": "\U0001F1F7\U0001F1F4",  # 🇷🇴 Romania
    "flag_rs": "\U0001F1F7\U0001F1F8",  # 🇷🇸 Serbia
    "flag_ru": "\U0001F1F7\U0001F1FA",  # 🇷🇺 Russia
    "flag_rw": "\U0001F1F7\U0001F1FC",  # 🇷🇼 Rwanda
    "flag_sa": "\U0001F1F8\U0001F1E6",  # 🇸🇦 Saudi Arabia
    "flag_sb": "\U0001F1F8\U0001F1E7",  # 🇸🇧 Solomon Islands
    "flag_sc": "\U0001F1F8\U0001F1E8",  # 🇸🇨 Seychelles
    "flag_sd": "\U0001F1F8\U0001F1E9",  # 🇸🇩 Sudan
    "flag_se": "\U0001F1F8\U0001F1EA",  # 🇸🇪 Sweden
    "flag_sg": "\U0001F1F8\U0001F1EC",  # 🇸🇬 Singapore
    "flag_sh": "\U0001F1F8\U0001F1ED",  # 🇸🇭 St. Helena
    "flag_si": "\U0001F1F8\U0001F1EE",  # 🇸🇮 Slovenia
    "flag_sj": "\U0001F1F8\U0001F1EF",  # 🇸🇯 Svalbard & Jan Mayen
    "flag_sk": "\U0001F1F8\U0001F1F0",  # 🇸🇰 Slovakia
    "flag_sl": "\U0001F1F8\U0001F1F1",  # 🇸🇱 Sierra Leone
    "flag_sm": "\U0001F1F8\U0001F1F2",  # 🇸🇲 San Marino
    "flag_sn": "\U0001F1F8\U0001F1F3",  # 🇸🇳 Senegal
    "flag_so": "\U0001F1F8\U0001F1F4",  # 🇸🇴 Somalia
    "flag_sr": "\U0001F1F8\U0001F1F7",  # 🇸🇷 Suriname
    "flag_ss": "\U0001F1F8\U0001F1F8",  # 🇸🇸 South Sudan
    "flag_st": "\U0001F1F8\U0001F1F9",  # 🇸🇹 São Tomé & Príncipe
    "flag_sv": "\U0001F1F8\U0001F1FB",  # 🇸🇻 El Salvador
    "flag_sx": "\U0001F1F8\U0001F1FD",  # 🇸🇽 Sint Maarten
    "flag_sy": "\U0001F1F8\U0001F1FE",  # 🇸🇾 Syria
    "flag_sz": "\U0001F1F8\U0001F1FF",  # 🇸🇿 Eswatini
    "flag_ta": "\U0001F1F9\U0001F1E6",  # 🇹🇦 Tristan da Cunha
    "flag_tc": "\U0001F1F9\U0001F1E8",  # 🇹🇨 Turks & Caicos Islands
    "flag_td": "\U0001F1F9\U0001F1E9",  # 🇹🇩 Chad
    "flag_tf": "\U0001F1F9\U0001F1EB",  # 🇹🇫 French Southern Territories
    "flag_tg": "\U0001F1F9\U0001F1EC",  # 🇹🇬 Togo
    "flag_th": "\U0001F1F9\U0001F1ED",  # 🇹🇭 Thailand
    "flag_tj": "\U0001F1F9\U0001F1EF",  # 🇹🇯 Tajikistan
    "flag_tk": "\U0001F1F9\U0001F1F0",  # 🇹🇰 Tokelau
    "flag_tl": "\U0001F1F9\U0001F1F1",  # 🇹🇱 Timor-Leste
    "flag_tm": "\U0001F1F9\U0001F1F2",  # 🇹🇲 Turkmenistan
    "flag_tn": "\U0001F1F9\U0001F1F3",  # 🇹🇳 Tunisia
    "flag_to": "\U0001F1F9\U0001F1F4",  # 🇹🇴 Tonga
    "flag_tr": "\U0001F1F9\U0001F1F7",  # 🇹🇷 Turkey
    "flag_tt": "\U0001F1F9\U0001F1F9",  # 🇹🇹 Trinidad & Tobago
    "flag_tv": "\U0001F1F9\U0001F1FB",  # 🇹🇻 Tuvalu
    "flag_tw": "\U0001F1F9\U0001F1FC",  # 🇹🇼 Taiwan
    "flag_tz": "\U0001F1F9\U0001F1FF",  # 🇹🇿 Tanzania
    "flag_ua": "\U0001F1FA\U0001F1E6",  # 🇺🇦 Ukraine
    "flag_ug": "\U0001F1FA\U0001F1EC",  # 🇺🇬 Uganda
    "flag_um": "\U0001F1FA\U0001F1F2",  # 🇺🇲 U.S. Outlying Islands
    "flag_un": "\U0001F1FA\U0001F1F3",  # 🇺🇳 United Nations
    "flag_us": "\U0001F1FA\U0001F1F8",  # 🇺🇸 United States
    "flag_uy": "\U0001F1FA\U0001F1FE",  # 🇺🇾 Uruguay
    "flag_uz": "\U0001F1FA\U0001F1FF",  # 🇺🇿 Uzbekistan
    "flag_va": "\U0001F1FB\U0001F1E6",  # 🇻🇦 Vatican City
    "flag_vc": "\U0001F1FB\U0001F1E8",  # 🇻🇨 St. Vincent & Grenadines
    "flag_ve": "\U0001F1FB\U0001F1EA",  # 🇻🇪 Venezuela
    "flag_vg": "\U0001F1FB\U0001F1EC",  # 🇻🇬 British Virgin Islands
    "flag_vi": "\U0001F1FB\U0001F1EE",  # 🇻🇮 U.S. Virgin Islands
    "flag_vn": "\U0001F1FB\U0001F1F3",  # 🇻🇳 Vietnam
    "flag_vu": "\U0001F1FB\U0001F1FA",  # 🇻🇺 Vanuatu
    "flag_wf": "\U0001F1FC\U0001F1EB",  # 🇼🇫 Wallis & Futuna
    "flag_ws": "\U0001F1FC\U0001F1F8",  # 🇼🇸 Samoa
    "flag_xk": "\U0001F1FD\U0001F1F0",  # 🇽🇰 Kosovo
    "flag_ye": "\U0001F1FE\U0001F1EA",  # 🇾🇪 Yemen
    "flag_yt": "\U0001F1FE\U0001F1F9",  # 🇾🇹 Mayotte
    "flag_za": "\U0001F1FF\U0001F1E6",  # 🇿🇦 South Africa
    "flag_zm": "\U0001F1FF\U0001F1F2",  # 🇿🇲 Zambia
    "flag_zw": "\U0001F1FF\U0001F1FC",  # 🇿🇼 Zimbabwe

    # ── Marks / symbols ──────────────────────────────────────────────────────
    "cross_mark":       "\U0000274C",       # ❌
    "check_mark":       "\U00002705",       # ✅
    "abc":              "\U0001F524",       # 🔤
    "abacus":           "\U0001F9EE",       # 🧮
    "numbers":          "\U0001F522",       # 🔢

    # ── Geometric shapes ─────────────────────────────────────────────────────
    "circle":           "\U0001F535",       # 🔵
    "square":           "\U0001F7E6",       # 🟦
    "triangle":         "\U0001F53A",       # 🔺

    # ── Objects / places ─────────────────────────────────────────────────────
    "factory":          "\U0001F3ED",       # 🏭
    "gun":              "\U0001F52B",       # 🔫 (water pistol — the only firearm emoji)
    "label":            "\U0001F3F7",       # 🏷
    "memo":             "\U0001F4DD",       # 📝
    "calendar":         "\U0001F4C5",       # 📅
    "stopwatch":        "\U000023F1",       # ⏱
    "hourglass":        "\U0000231B",       # ⌛
    "world_map":        "\U0001F5FA",       # 🗺
    "fuel_pump":        "\U000026FD",       # ⛽

    # ── Faces (new expressions) ──────────────────────────────────────────────
    "face_exhale":      "\U0001F62E‍\U0001F4A8",  # 😮‍💨 (ZWJ — exhaling)

    # ── New this session ─────────────────────────────────────────────────────
    "hiking_boot":      "\U0001F97E",       # 🥾
    "military_helmet":  "\U0001FA96",       # 🪖
    "underwear":        "\U0001FA72",       # 🩲
    "cigarette":        "\U0001F6AC",       # 🚬
    "yarn":             "\U0001F9F6",       # 🧶
    "ok_hand":          "\U0001F44C",       # 👌
    "computer_mouse":   "\U0001F5B1",       # 🖱
    "computer_keyboard": "\U00002328",      # ⌨
    "skier":            "\U000026F7",       # ⛷
    "card_joker":       "\U0001F0CF",       # 🃏
    "misc_box":         "\U0001F587",       # 🖇 linked paperclips
    "fire_extinguisher": "\U0001F9EF",      # 🧯
    "sign":             "\U0001FAA7",       # 🪧
    "coffin":           "\U000026B0",       # ⚰
    "funeral_urn":      "\U000026B1",       # ⚱

    # ── Moon phases ───────────────────────────────────────────────────────────
    "moon_new":             "\U0001F311",   # 🌑
    "moon_waxing_crescent": "\U0001F312",   # 🌒
    "moon_first_quarter":   "\U0001F313",   # 🌓
    "moon_waxing_gibbous":  "\U0001F314",   # 🌔
    "moon_full":            "\U0001F315",   # 🌕
    "moon_waning_gibbous":  "\U0001F316",   # 🌖
    "moon_last_quarter":    "\U0001F317",   # 🌗
    "moon_waning_crescent": "\U0001F318",   # 🌘

    # ── Zodiac animals / symbols ──────────────────────────────────────────────
    "ram":              "\U0001F40F",       # 🐏  (Aries)
    "ox":               "\U0001F402",       # 🐂  (Taurus)
    "wheat":            "\U0001F33E",       # 🌾  (Virgo — harvest maiden)
    "scales":           "\U00002696",       # ⚖   (Libra)

    # ── Colored hearts ────────────────────────────────────────────────────────
    "heart_orange":     "\U0001F9E1",       # 🧡
    "heart_yellow":     "\U0001F49B",       # 💛
    "heart_green":      "\U0001F49A",       # 💚
    "heart_blue":       "\U0001F499",       # 💙
    "heart_purple":     "\U0001F49C",       # 💜
    "heart_brown":      "\U0001F90E",       # 🤎
    "heart_black":      "\U0001F5A4",       # 🖤
    "heart_white":      "\U0001F90D",       # 🤍
    "heart_pink":       "\U0001FA77",       # 🩷

    # ── Colored circles ───────────────────────────────────────────────────────
    "circle_red":       "\U0001F534",       # 🔴
    "circle_orange":    "\U0001F7E0",       # 🟠
    "circle_yellow":    "\U0001F7E1",       # 🟡
    "circle_green":     "\U0001F7E2",       # 🟢
    "circle_purple":    "\U0001F7E3",       # 🟣
    "circle_brown":     "\U0001F7E4",       # 🟤
    "circle_black":     "\U000026AB",       # ⚫
    "circle_white":     "\U000026AA",       # ⚪

    # ── Colored squares ───────────────────────────────────────────────────────
    "square_red":       "\U0001F7E5",       # 🟥
    "square_orange":    "\U0001F7E7",       # 🟧
    "square_yellow":    "\U0001F7E8",       # 🟨
    "square_green":     "\U0001F7E9",       # 🟩
    "square_purple":    "\U0001F7EA",       # 🟪
    "square_brown":     "\U0001F7EB",       # 🟫

    # ── Weather extras ────────────────────────────────────────────────────────
    "cloudy":           "\U0001F325",       # 🌥
    "rainy":            "\U0001F327",       # 🌧
    "foggy":            "\U0001F32B",       # 🌫
    "snowy_cloud":      "\U0001F328",       # 🌨

    # ── Signs / objects ──────────────────────────────────────────────────────
    "restroom_sign":    "\U0001F6BB",       # 🚻
    "hole":             "\U0001F573",       # 🕳
    "splat":            "\U0001F4A5",       # 💥

    # ── Media controls ────────────────────────────────────────────────────────
    "play_button":      "\U000025B6",       # ▶
    "pause_button":     "\U000023F8",       # ⏸
    "stop_button":      "\U000023F9",       # ⏹
    "record_button":    "\U000023FA",       # ⏺
    "fast_forward":     "\U000023E9",       # ⏩
    "rewind_button":    "\U000023EA",       # ⏪
    "next_track":       "\U000023ED",       # ⏭
    "prev_track":       "\U000023EE",       # ⏮
    "shuffle":          "\U0001F500",       # 🔀
    "repeat_button":    "\U0001F501",       # 🔁

    # ── Directional arrows ────────────────────────────────────────────────────
    "arrow_up":         "\U00002B06",       # ⬆
    "arrow_down":       "\U00002B07",       # ⬇
    "arrow_left":       "\U00002B05",       # ⬅
    "arrow_right":      "\U000027A1",       # ➡
    "arrow_up_right":   "\U00002197",       # ↗
    "arrow_down_right": "\U00002198",       # ↘
    "arrow_down_left":  "\U00002199",       # ↙
    "arrow_up_left":    "\U00002196",       # ↖
    "arrow_back":       "\U0001F519",       # 🔙
    "rotate_cw":        "\U0001F503",       # 🔃
    "rotate_ccw":       "\U0001F504",       # 🔄

    # ── Pointing fingers ──────────────────────────────────────────────────────
    "pointing_up":      "\U0001F446",       # 👆
    "pointing_down":    "\U0001F447",       # 👇
    "pointing_left":    "\U0001F448",       # 👈
    "pointing_right":   "\U0001F449",       # 👉
    "pointing_index":   "\U0000261D",       # ☝  (one finger / attention)

    # ── Info / question / exclamation ─────────────────────────────────────────
    "info_symbol":      "\U00002139",       # ℹ
    "question_mark":    "\U00002753",       # ❓
    "exclamation_mark": "\U00002757",       # ❗

    # ── Clock faces — on the hour ─────────────────────────────────────────────
    "clock_1":          "\U0001F550",       # 🕐
    "clock_2":          "\U0001F551",       # 🕑
    "clock_3":          "\U0001F552",       # 🕒
    "clock_4":          "\U0001F553",       # 🕓
    "clock_5":          "\U0001F554",       # 🕔
    "clock_6":          "\U0001F555",       # 🕕
    "clock_7":          "\U0001F556",       # 🕖
    "clock_8":          "\U0001F557",       # 🕗
    "clock_9":          "\U0001F558",       # 🕘
    "clock_10":         "\U0001F559",       # 🕙
    "clock_11":         "\U0001F55A",       # 🕚
    "clock_12":         "\U0001F55B",       # 🕛

    # ── Clock faces — half past ───────────────────────────────────────────────
    "clock_1_30":       "\U0001F55C",       # 🕜
    "clock_2_30":       "\U0001F55D",       # 🕝
    "clock_3_30":       "\U0001F55E",       # 🕞
    "clock_4_30":       "\U0001F55F",       # 🕟
    "clock_5_30":       "\U0001F560",       # 🕠
    "clock_6_30":       "\U0001F561",       # 🕡
    "clock_7_30":       "\U0001F562",       # 🕢
    "clock_8_30":       "\U0001F563",       # 🕣
    "clock_9_30":       "\U0001F564",       # 🕤
    "clock_10_30":      "\U0001F565",       # 🕥
    "clock_11_30":      "\U0001F566",       # 🕦
    "clock_12_30":      "\U0001F567",       # 🕧
}
