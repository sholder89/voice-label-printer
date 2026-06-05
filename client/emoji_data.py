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
    "shack":            "radio",
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
    "toxic":            "warning",
    "poison":           "warning",
    "unsafe":           "warning",
    "do not drop":      "warning",
    "flammable":        "warning",
    "biohazard":        "warning",

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
    "son":              "boy",
    "nephew":           "boy",
    "brother":          "boy",
    "girl":             "girl",
    "lass":             "girl",
    "daughter":         "girl",
    "niece":            "girl",
    "sister":           "girl",
    "elder":            "elder",
    "elderly":          "elder",
    "senior":           "elder",
    "grandpa":          "elder",
    "grandma":          "elder",
    "grandfather":      "elder",
    "grandmother":      "elder",
    "grandparent":      "elder",
    "old man":          "elder",
    "old woman":        "elder",
    "family":           "family",
    "household":        "family",
    "relatives":        "family",
    "parents":          "family",
    "couple":           "couple",
    "partners":         "couple",
    "husband":          "couple",
    "wife":             "couple",
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
    "rancher":          "cowboy",
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
    "groom":            "tuxedo",
    "suit":             "tuxedo",
    "worker":           "worker",
    "construction":     "worker",
    "builder":          "worker",
    "hard hat":         "worker",
    "skull":            "skull",
    "death":            "skull",
    "poison":           "skull",
    "toxic":            "skull",
    "pirate skull":     "skull",
    "ghost":            "ghost",
    "spooky":           "ghost",
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
    "nurse":            "prof_medical",
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
    "developer":        "prof_coder",
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
    "metal":            "rock_on",
    "horns":            "rock_on",
    "fist bump":        "fist_bump",
    "raised fist":      "fist_bump",

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
    "restricted":       "prohibited",
    "off limits":       "prohibited",
    "shield":           "shield",
    "protection":       "shield",
    "armor":            "shield",
    "secure":           "shield",
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
    "hen":              "rooster",
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
    "bug":              "bug",
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
    "polar bear":       "bear",
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
    "moose":            "deer",
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
    "geese":            "duck",
    "goose":            "duck",
    "cacti":            "cactus",
    "fungi":            "mushroom",
    "octopi":           "octopus",
    "cacti":            "cactus",

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
    "cold":             "snowflake",
    "frozen":           "snowflake",
    "freeze":           "snowflake",
    "refrigerate":      "snowflake",
    "keep cold":        "snowflake",
    "keep frozen":      "snowflake",
    "freezer":          "snowflake",
    "winter":           "snowflake",
    "snow":             "snowflake",
    "blizzard":         "snowflake",
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
    "leaves":           "autumn",
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
    "frosty":           "snowman",
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
    "sunflower":        "sunflower",
    "sunflowers":       "sunflower",
    "tulip":            "tulip",
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
    "mushroom":         "mushroom",
    "fungi":            "mushroom",
    "clover":           "clover",
    "lucky":            "clover",
    "shamrock":         "clover",
    "leaf":             "leaf",
    "fallen leaf":      "leaf",
    "wave":             "wave_water",
    "ocean":            "wave_water",
    "sea":              "wave_water",
    "surfing":          "surfer",
    "mountain":         "mountain",
    "mountains":        "mountain",
    "hiking":           "mountain",
    "volcano":          "volcano",
    "island":           "island",
    "earth":            "earth",
    "globe":            "earth",
    "world":            "earth",
    "planet earth":     "earth",

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
    "ufo":              "ufo",
    "flying saucer":    "ufo",
    "flying saucer":    "ufo",
    "planet":           "saturn",
    "saturn":           "saturn",
    "solar system":     "saturn",
    "telescope":        "telescope",
    "stargazing":       "telescope",
    "observatory":      "telescope",
    "moon":             "moon",
    "lunar":            "moon",
    "crescent":         "moon",
    "comet":            "comet",
    "meteor":           "comet",
    "asteroid":         "comet",
    "shooting star":    "comet",
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
    "battery":          "lightning",
    "charger":          "lightning",
    "voltage":          "lightning",
    "generator":        "lightning",
    "solar":            "lightning",
    "wires":            "lightning",
    "power supply":     "lightning",
    "outlet":           "lightning",
    "electrical":       "lightning",
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
    "developer":        "computer",
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
    "internet":         "computer",
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
    "movies":           "tv",
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
    "grapes":           "grapes",
    "strawberry":       "strawberry",
    "strawberries":     "strawberry",
    "berries":          "strawberry",
    "blueberries":      "blueberry",
    "blueberry":        "blueberry",
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
    "wrap":             "burrito",
    "sandwich":         "sandwich",
    "sub":              "sandwich",
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
    "groceries":        "food",
    "meal prep":        "food",
    "leftovers":        "food",
    "recipe":           "food",
    "baking":           "food",
    "pantry":           "food",
    "dessert":          "food",
    "meal":             "food",
    "snack":            "food",
    "treat":            "food",

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
    "nut":              "peanut",
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
    "keyboard":         "piano",
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
    "badminton":        "tennis",
    "golf":             "golf",
    "bowling":          "bowling",
    "volleyball":       "volleyball",
    "skiing":           "skiing",
    "snowboarding":     "skiing",
    "swimming":         "swimming",
    "swimmer":          "swimming",
    "swim":             "swimming",
    "lifeguard":        "swimming",
    "surfing":          "surfer",
    "surfer":           "surfer",
    "surf":             "surfer",
    "surfs":            "surfer",
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
    "hiker":            "climbing",
    "hiking":           "climbing",
    "trekking":         "climbing",
    "trekker":          "climbing",
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
    "rollerskating":    "skateboard",
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
    "playstation":      "gaming",
    "xbox":             "gaming",
    "nintendo":         "gaming",
    "arcade":           "gaming",
    "boardgames":       "gaming",
    "cards":            "gaming",
    "dice":             "dice_icon",
    "die":              "dice_icon",
    "d6":               "dice_icon",
    "d20":              "dice_icon",
    "tabletop":         "dice_icon",
    "poker":            "gaming",
    "lego":             "gaming",
    "playing cards":    "card_spade",
    "card deck":        "card_spade",
    "card game":        "card_spade",
    "spades":           "card_spade",
    "clubs":            "card_club",
    "diamonds":         "card_diamond",
    "hearts card":      "card_heart",
    "puzzle":           "puzzle_icon",
    "jigsaw":           "puzzle_icon",
    "brainteaser":      "puzzle_icon",

    # ── Art / Craft ──────────────────────────────────────────────────────────
    "art":              "art",
    "craft":            "art",
    "paint":            "art",
    "drawing":          "art",
    "brushes":          "art",
    "canvas":           "art",
    "markers":          "art",
    "yarn":             "thread",
    "thread":           "thread",
    "sewing thread":    "thread",
    "knitting":         "thread",
    "crochet":          "thread",
    "embroidery":       "thread",
    "sewing":           "thread",
    "fabric":           "thread",
    "scrapbook":        "art",
    "watercolor":       "art",
    "sculpture":        "art",
    "pottery":          "clay",
    "ceramics":         "clay",
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
    "restroom":         "toilet",
    "lavatory":         "toilet",
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
    "dental":           "toothbrush",
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
    "nails":            "tools",
    "screws":           "tools",
    "bolts":            "tools",
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
    "jigsaw":           "saw_tool",
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
    "schematic":        "ruler_tri",
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
    "bronze":           "metal",
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
    "pottery":          "clay",
    "ceramics":         "clay",
    "ceramic":          "clay",
    "earthenware":      "clay",
    "terracotta":       "clay",
    "terra cotta":      "clay",
    "stoneware":        "clay",
    "porcelain":        "clay",
    "bisque":           "clay",

    # ── Parts / Fasteners ────────────────────────────────────────────────────
    "nut":              "nut_bolt",
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
    "tires":            "car",
    "motor":            "car",
    "engine":           "car",
    "fuel":             "car",
    "brakes":           "car",
    "windshield":       "car",
    "maintenance":      "car",
    "detailing":        "car",
    "racing":           "racing",
    "formula":          "racing",
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
    "sailing":          "boat",
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
    "subway":           "train",
    "metro":            "train",
    "helicopter":       "helicopter",
    "boat":             "boat",
    "sailing":          "boat",
    "sailboat":         "boat",
    "nautical":         "boat",
    "speedboat":        "speedboat",
    "ferry":            "speedboat",
    "parachute":        "parachute",
    "skydiving":        "parachute",

    # ── Health / Medical ─────────────────────────────────────────────────────
    "bandages":         "firstaid",
    "first aid":        "firstaid",
    "band-aid":         "firstaid",
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
    "shipping":         "mail",
    "return":           "mail",
    "send":             "mail",
    "package":          "package_box",
    "parcel":           "package_box",
    "box":              "package_box",
    "crate":            "package_box",
    "shipping":         "package_box",
    "parcel":           "mail",
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
    "wallet":           "money",
    "coins":            "money",
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
    "valentine":        "heart",
    "valentines":       "heart",
    "party":            "party",
    "celebration":      "party",
    "confetti":         "party",
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
    "film":             "camera",
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
    "timer":            "time",
    "alarm":            "time",
    "schedule":         "time",
    "deadline":         "time",
    "appointment":      "time",
    "reminder":         "time",
    "weekly":           "time",
    "daily":            "time",
    "monthly":          "time",
    "calendar":         "time",
    "countdown":        "time",
    "annual":           "time",
    "hourglass":        "time",
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

    # ── Buildings / Places ───────────────────────────────────────────────────
    "office building":  "office_building",
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
}


# ── Emoji lookup ──────────────────────────────────────────────────────────────
# Use plain Unicode codepoints — no variation selectors (U+FE0F).

_ICON_EMOJIS = {
    # Warning / safety
    "warning":          "⚠",           # ⚠
    "snowflake":        "❄",           # ❄
    "lightning":        "⚡",           # ⚡

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
    "girl":             "\U0001F467",       # 👧
    "elder":            "\U0001F474",       # 👴
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
    "jellyfish":        "\U0001F421",       # 🐡  (no single-codepoint jellyfish; blowfish is closest)
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
    "knot":             "\U0001FA22",       # 🪢

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
    # Animals
    "beetle":           "\U0001FAB2",       # 🪲
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

    # Buildings
    "office_building":  "\U0001F3E2",       # 🏢
    "school_building":  "\U0001F3EB",       # 🏫
    "castle":           "\U0001F3F0",       # 🏰
    "church":           "\U000026EA",       # ⛪
    "stadium":          "\U0001F3DF",       # 🏟
    "theater":          "\U0001F3A4",       # 🎤 (fallback)
    "museum":           "\U0001F3DB",       # 🏛
    "bank":             "\U0001F3E6",       # 🏦
    "hospital_building": "\U0001F3E5",      # 🏥

    # Ham radio
    "antenna":          "\U0001F4E1",       # 📡
}
