import os
import json
import requests
# from django.core.files.storage import FileSystemStorage
# from midi2audio import FluidSynth
from importlib import import_module
TMIDIX = import_module('tegridy-tools.tegridy-tools.TMIDIX')


def generateMusic():
    #@title Querry API and play/plot results

    #@markdown Custom MIDI or self-continuation
    use_loaded_custom_MIDI = False #@param {type:"boolean"}
    trim_custom_MIDI_tokens = 512 #@param {type:"slider", min:64, max:4096, step:64}

    #@markdown Select a genre from dropdown menu
    genre = 'chopin' #@param ["random", "chopin", "mozart", "rachmaninoff", "ladygaga", "country", "disney", "jazz", "bach", "beethoven", "journey", "thebeatles", "video", "broadway", "franksinatra", "bluegrass", "tchaikovsky", "liszt", "everything", "ragtime", "andrehazes", "cocciante", "thecranberries", "ligabue", "metallica", "traffic", "philcollins", "nineinchnails", "thepretenders", "sugarray", "grandfunkrailroad", "ron", "ellington", "fleetwoodmac", "thebeachboys", "kool & the gang", "foreigner", "tlc", "scottjames", "benfoldsfive", "smashmouth", "oasis", "allsaints", "donnasummer", "weezer", "bjork", "mariahcarey", "berte", "cheaptrick", "caroleking", "thecars", "gganderson", "robertpalmer", "zucchero", "alicecooper", "vanhalen", "brucehornsby", "coolio", "jimmybuffett", "lobo", "badcompany", "eminem", "creedenceclearwaterrevival", "deeppurple", "shearinggeorge", "robbiewilliams", "dalla", "ub40", "lindaronstadt", "sinatra", "inxs", "jonimitchell", "michaeljackson", "last", "devo", "shaniatwain", "korn", "brooksgarth", "sweet", "thewho", "roxette", "bowiedavid", "beegees", "renefroger", "mina", "estefangloria", "mccartney", "theventures", "carboni", "simplyred", "santana", "jewel", "meatloaf", "giorgia", "nofx", "rickymartin", "thecure", "thetemptations", "tozzi", "beck", "eiffel65", "jenniferlopez", "reelbigfish", "patsycline", "richardcliff", "styx", "acdc", "brucespringsteen", "michaelgeorge", "blondie", "pinkfloyd", "oldfieldmike", "redhotchilipeppers", "therollingstones", "morandi", "heart", "robertaflack", "pantera", "alabama", "jethrotull", "hanson", "mosch", "ludwigvanbeethoven", "dvorak", "chrisrea", "guns n' roses", "duranduran", "ericclapton", "bettemidler", "bwitched", "gordonlightfoot", "thegrassroots", "chicago", "whitezombie", "michaelbolton", "paulsimon", "marillion", "thepointersisters", "theanimals", "cher", "haydn", "aerosmith", "supertramp", "littleriverband", "america", "tonyorlando", "tompetty", "thecorrs", "aliceinchains", "kiss", "prince", "toto", "vanmorrison", "wagner", "cashjohnny", "annielennox", "enya", "thedoobiebrothers", "thetragicallyhip", "rush", "laurapausini", "stevemillerband", "simonandgarfunkel", "fiorellamannoia", "olivianewton-john", "carlysimon", "elvispresley", "vangelis", "bobdylan", "bbking", "vengaboys", "paoli", "thehollies", "alainsouchon", "pooh", "raf", "fiorello", "lionelrichie", "jimihendrix", "theeverlybrothers", "limpbizkit", "donhenley", "georgeharrison", "threedognight", "johnmellencamp", "carpenters", "raycharles", "basie", "billyocean", "scorpions", "royorbison", "whitneyhouston", "ironmaiden", "jovanotti", "alanjackson", "barrymanilow", "hueylewis", "kennyloggins", "chopinfrederic", "talkingheads", "themonkees", "rem", "jeanmicheljarre", "michelezarrillo", "eurythmics", "thedoors", "guesswho", "miller", "thefourseasons", "matiabazar", "tompettyandtheheartbreakers", "chickcorea", "scottjoplin", "amedeominghi", "bryanadams", "paulaabdul", "rossivasco", "billyjoel", "daniele", "claudedebussy", "gilbert & sullivan", "chakakhan", "nirvana", "garbage", "andreabocelli", "johnnyrivers", "emerson, lake & palmer", "theallmanbrothersband", "zappa", "boston", "mango", "barbrastreisand", "willsmith", "ozzyosbourne", "janetjackson", "antonellovenditti", "u2", "humperdinckengelbert", "jamiroquai", "zero", "chuckberry", "spicegirls", "ledzeppelin", "masini", "thekinks", "eagles", "billyidol", "alanismorissette", "joecocker", "jimcroce", "bobmarley", "blacksabbath", "stonetemplepilots", "silverchair", "paulmccartney", "blur", "nek", "greenday", "thepolice", "depechemode", "rageagainstthemachine", "madonna", "rogerskenny", "brooks & dunn", "883", "thedrifters", "amygrant", "herman", "toriamos", "eltonjohn", "britneyspears", "lennykravitz", "celentano", "ringostarr", "neildiamond", "aqua", "oscarpeterson", "joejackson", "moby", "collinsphil", "leosayer", "takethat", "electriclightorchestra", "pearljam", "marcanthony", "borodin", "petshopboys", "stevienicks", "hollybuddy", "turnertina", "annaoxa", "zztop", "sting", "themoodyblues", "ruggeri", "creed", "claudebolling", "renzoarbore", "erasure", "elviscostello", "airsupply", "tinaturner", "leali", "petergabriel", "nodoubt", "bread", "huey lewis & the news", "brandy", "level42", "radiohead", "georgebenson", "wonderstevie", "thesmashingpumpkins", "cyndilauper", "rodstewart", "bush", "ramazzotti", "bobseger", "theshadows", "gershwin", "cream", "biagioantonacci", "steviewonder", "nomadi", "direstraits", "davidbowie", "amostori", "thealanparsonsproject", "johnlennon", "crosbystillsnashandyoung", "battiato", "kansas", "clementi", "richielionel", "yes", "brassensgeorges", "steelydan", "jacksonmichael", "buddyholly", "earthwindandfire", "natkingcole", "therascals", "bonjovi", "alanparsons", "backstreetboys", "glencampbell", "howardcarpendale", "thesupremes", "villagepeople", "blink-182", "jacksonbrowne", "sade", "lynyrdskynyrd", "foofighters", "2unlimited", "battisti", "hall & oates", "stansfieldlisa", "genesis", "boyzone", "theoffspring", "tomjones", "davematthewsband", "johnelton", "neilyoung", "dionnewarwick", "aceofbase", "marilynmanson", "taylorjames", "rkelly", "grandi", "sublime", "edvardgrieg", "tool", "bachjohannsebastian", "patbenatar", "celinedion", "queen", "soundgarden", "abba", "drdre", "defleppard", "dominofats", "realmccoy", "natalieimbruglia", "hole", "spinners", "arethafranklin", "reospeedwagon", "indian", "movie", "scottish", "irish", "african", "taylorswift", "shakira", "blues", "latin", "katyperry", "world", "kpop", "africandrum", "michaelbuble", "rihanna", "gospel", "beyonce", "chinese", "arabic", "adele", "kellyclarkson", "theeagles", "handel", "rachmaninov", "schumann", "christmas", "dance", "punk", "natl_anthem", "brahms", "rap", "ravel", "burgmueller", "other", "schubert", "granados", "albeniz", "mendelssohn", "debussy", "grieg", "moszkowski", "godowsky", "folk", "mussorgsky", "kids", "balakirev", "hymns", "verdi", "hummel", "deleted", "delibes", "saint-saens", "puccini", "satie", "offenbach", "widor", "songs", "stravinsky", "vivaldi", "gurlitt", "alkan", "weber", "strauss", "traditional", "rossini", "mahler", "soler", "sousa", "telemann", "busoni", "scarlatti", "stamitz", "classical", "jstrauss2", "gabrieli", "nielsen", "purcell", "donizetti", "kuhlau", "gounod", "gibbons", "weiss", "faure", "holst", "spohr", "monteverdi", "reger", "bizet", "elgar", "czerny", "sullivan", "shostakovich", "franck", "rubinstein", "albrechtsberger", "paganini", "diabelli", "gottschalk", "wieniawski", "lully", "morley", "sibelius", "scriabin", "heller", "thalberg", "dowland", "carulli", "pachelbel", "sor", "marcello", "ketterer", "rimsky-korsakov", "ascher", "bruckner", "janequin", "anonymous", "kreutzer", "sanz", "joplin", "susato", "giuliani", "lassus", "palestrina", "smetana", "berlioz", "couperin", "gomolka", "daquin", "herz", "campion", "walthew", "pergolesi", "reicha", "polak", "holborne", "hassler", "corelli", "cato", "azzaiolo", "anerio", "gastoldi", "goudimel", "dussek", "prez", "cimarosa", "byrd", "praetorius", "rameau", "khachaturian", "machaut", "gade", "perosi", "gorzanis", "smith", "haberbier", "carr", "marais", "glazunov", "guerrero", "cabanilles", "losy", "roman", "hasse", "sammartini", "blow", "zipoli", "duvernoy", "aguado", "cherubini", "victoria", "field", "andersen", "poulenc", "d'aragona", "lemire", "krakowa", "maier", "rimini", "encina", "banchieri", "best", "galilei", "warhorse", "gypsy", "soundtrack", "encore", "roblaidlow", "nationalanthems", "benjyshelton", "ongcmu", "crosbystillsnashyoung", "smashingpumpkins", "aaaaaaaaaaa", "alanismorrisette", "animenz", "onedirection", "nintendo", "disneythemes", "gunsnroses", "rollingstones", "juliancasablancas", "abdelmoinealfa", "berckmansdeoliveira", "moviethemes", "beachboys", "davemathews", "videogamethemes", "moabberckmansdeoliveira", "unknown", "cameronleesimpson", "johannsebastianbach", "thecarpenters", "elo", "nightwish", "blink182", "emersonlakeandpalmer", "tvthemes"]

    #@markdown Select instruments
    piano = True #@param {type:"boolean"}
    strings = True #@param {type:"boolean"}
    winds = True #@param {type:"boolean"}
    drums = True #@param {type:"boolean"}
    harp = True #@param {type:"boolean"}
    guitar = True #@param {type:"boolean"}
    bass = True #@param {type:"boolean"}

    #@markdown Generation settings
    number_of_tokens_to_generate = 800 #@param {type:"slider", min:64, max:1024, step:8}
    temperature = 1 #@param {type:"slider", min:0.1, max:2, step:0.1}
    truncation = 0 #@param {type:"integer"}

    INSTRUMENTS = ["piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano",
                   "piano", "piano", "piano", "piano", "piano",
                   "violin", "violin", "cello", "cello", "bass", "bass", "guitar", "guitar",
                   "flute", "flute", "clarinet", "clarinet", "trumpet", "trumpet", "harp", "harp",
                   'drum', 'drum']

    TRACKS_OUT_INDEX = {"piano": 0, "violin": 3, "cello": 4, "bass": 2, "guitar": 1, "flute": 8,
                   "clarinet": 7, "trumpet": 6, "harp": 5, "drum": 9}

    VOLUMES = [0, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 80, 0, 80, 0, 80, 0, 80, 0, 80,
               0, 80, 0, 80, 0, 80, 0, 100, 0]

    if use_loaded_custom_MIDI:
      DELAY_MULTIPLIER = 10
    else:
      DELAY_MULTIPLIER = 20

    c_encoding = '4096'

    genreList = ["chopin","mozart","rachmaninoff","ladygaga","country","disney","jazz","bach","beethoven","journey","thebeatles","video","broadway","franksinatra","bluegrass","tchaikovsky","liszt","everything","ragtime","andrehazes","cocciante","thecranberries","ligabue","metallica","traffic","philcollins","nineinchnails","thepretenders","sugarray","grandfunkrailroad","ron","ellington","fleetwoodmac","thebeachboys","kool & the gang","foreigner","tlc","scottjames","benfoldsfive","smashmouth","oasis","allsaints","donnasummer","weezer","bjork","mariahcarey","berte","cheaptrick","caroleking","thecars","gganderson","robertpalmer","zucchero","alicecooper","vanhalen","brucehornsby","coolio","jimmybuffett","lobo","badcompany","eminem","creedenceclearwaterrevival","deeppurple","shearinggeorge","robbiewilliams","dalla","ub40","lindaronstadt","sinatra","inxs","jonimitchell","michaeljackson","last","devo","shaniatwain","korn","brooksgarth","sweet","thewho","roxette","bowiedavid","beegees","renefroger","mina","estefangloria","mccartney","theventures","carboni","simplyred","santana","jewel","meatloaf","giorgia","nofx","rickymartin","thecure","thetemptations","tozzi","beck","eiffel65","jenniferlopez","reelbigfish","patsycline","richardcliff","styx","acdc","brucespringsteen","michaelgeorge","blondie","pinkfloyd","oldfieldmike","redhotchilipeppers","therollingstones","morandi","heart","robertaflack","pantera","alabama","jethrotull","hanson","mosch","ludwigvanbeethoven","dvorak","chrisrea","guns n' roses","duranduran","ericclapton","bettemidler","bwitched","gordonlightfoot","thegrassroots","chicago","whitezombie","michaelbolton","paulsimon","marillion","thepointersisters","theanimals","cher","haydn","aerosmith","supertramp","littleriverband","america","tonyorlando","tompetty","thecorrs","aliceinchains","kiss","prince","toto","vanmorrison","wagner","cashjohnny","annielennox","enya","thedoobiebrothers","thetragicallyhip","rush","laurapausini","stevemillerband","simonandgarfunkel","fiorellamannoia","olivianewton-john","carlysimon","elvispresley","vangelis","bobdylan","bbking","vengaboys","paoli","thehollies","alainsouchon","pooh","raf","fiorello","lionelrichie","jimihendrix","theeverlybrothers","limpbizkit","donhenley","georgeharrison","threedognight","johnmellencamp","carpenters","raycharles","basie","billyocean","scorpions","royorbison","whitneyhouston","ironmaiden","jovanotti","alanjackson","barrymanilow","hueylewis","kennyloggins","chopinfrederic","talkingheads","themonkees","rem","jeanmicheljarre","michelezarrillo","eurythmics","thedoors","guesswho","miller","thefourseasons","matiabazar","tompettyandtheheartbreakers","chickcorea","scottjoplin","amedeominghi","bryanadams","paulaabdul","rossivasco","billyjoel","daniele","claudedebussy","gilbert & sullivan","chakakhan","nirvana","garbage","andreabocelli","johnnyrivers","emerson, lake & palmer","theallmanbrothersband","zappa","boston","mango","barbrastreisand","willsmith","ozzyosbourne","janetjackson","antonellovenditti","u2","humperdinckengelbert","jamiroquai","zero","chuckberry","spicegirls","ledzeppelin","masini","thekinks","eagles","billyidol","alanismorissette","joecocker","jimcroce","bobmarley","blacksabbath","stonetemplepilots","silverchair","paulmccartney","blur","nek","greenday","thepolice","depechemode","rageagainstthemachine","madonna","rogerskenny","brooks & dunn","883","thedrifters","amygrant","herman","toriamos","eltonjohn","britneyspears","lennykravitz","celentano","ringostarr","neildiamond","aqua","oscarpeterson","joejackson","moby","collinsphil","leosayer","takethat","electriclightorchestra","pearljam","marcanthony","borodin","petshopboys","stevienicks","hollybuddy","turnertina","annaoxa","zztop","sting","themoodyblues","ruggeri","creed","claudebolling","renzoarbore","erasure","elviscostello","airsupply","tinaturner","leali","petergabriel","nodoubt","bread","huey lewis & the news","brandy","level42","radiohead","georgebenson","wonderstevie","thesmashingpumpkins","cyndilauper","rodstewart","bush","ramazzotti","bobseger","theshadows","gershwin","cream","biagioantonacci","steviewonder","nomadi","direstraits","davidbowie","amostori","thealanparsonsproject","johnlennon","crosbystillsnashandyoung","battiato","kansas","clementi","richielionel","yes","brassensgeorges","steelydan","jacksonmichael","buddyholly","earthwindandfire","natkingcole","therascals","bonjovi","alanparsons","backstreetboys","glencampbell","howardcarpendale","thesupremes","villagepeople","blink-182","jacksonbrowne","sade","lynyrdskynyrd","foofighters","2unlimited","battisti","hall & oates","stansfieldlisa","genesis","boyzone","theoffspring","tomjones","davematthewsband","johnelton","neilyoung","dionnewarwick","aceofbase","marilynmanson","taylorjames","rkelly","grandi","sublime","edvardgrieg","tool","bachjohannsebastian","patbenatar","celinedion","queen","soundgarden","abba","drdre","defleppard","dominofats","realmccoy","natalieimbruglia","hole","spinners","arethafranklin","reospeedwagon","indian","movie","scottish","irish","african","taylorswift","shakira","blues","latin","katyperry","world","kpop","africandrum","michaelbuble","rihanna","gospel","beyonce","chinese","arabic","adele","kellyclarkson","theeagles","handel","rachmaninov","schumann","christmas","dance","punk","natl_anthem","brahms","rap","ravel","burgmueller","other","schubert","granados","albeniz","mendelssohn","debussy","grieg","moszkowski","godowsky","folk","mussorgsky","kids","balakirev","hymns","verdi","hummel","deleted","delibes","saint-saens","puccini","satie","offenbach","widor","songs","stravinsky","vivaldi","gurlitt","alkan","weber","strauss","traditional","rossini","mahler","soler","sousa","telemann","busoni","scarlatti","stamitz","classical","jstrauss2","gabrieli","nielsen","purcell","donizetti","kuhlau","gounod","gibbons","weiss","faure","holst","spohr","monteverdi","reger","bizet","elgar","czerny","sullivan","shostakovich","franck","rubinstein","albrechtsberger","paganini","diabelli","gottschalk","wieniawski","lully","morley","sibelius","scriabin","heller","thalberg","dowland","carulli","pachelbel","sor","marcello","ketterer","rimsky-korsakov","ascher","bruckner","janequin","anonymous","kreutzer","sanz","joplin","susato","giuliani","lassus","palestrina","smetana","berlioz","couperin","gomolka","daquin","herz","campion","walthew","pergolesi","reicha","polak","holborne","hassler","corelli","cato","azzaiolo","anerio","gastoldi","goudimel","dussek","prez","cimarosa","byrd","praetorius","rameau","khachaturian","machaut","gade","perosi","gorzanis","smith","haberbier","carr","marais","glazunov","guerrero","cabanilles","losy","roman","hasse","sammartini","blow","zipoli","duvernoy","aguado","cherubini","victoria","field","andersen","poulenc","d'aragona","lemire","krakowa","maier","rimini","encina","banchieri","best","galilei","warhorse","gypsy","soundtrack","encore","roblaidlow","nationalanthems","benjyshelton","ongcmu","crosbystillsnashyoung","smashingpumpkins","aaaaaaaaaaa","alanismorrisette","animenz","onedirection","nintendo","disneythemes","gunsnroses","rollingstones","juliancasablancas","abdelmoinealfa","berckmansdeoliveira","moviethemes","beachboys","davemathews","videogamethemes","moabberckmansdeoliveira","unknown","cameronleesimpson","johannsebastianbach","thecarpenters","elo","nightwish","blink182","emersonlakeandpalmer","tvthemes"]
    if genre == 'random':
    	genre = genreList[secrets.randbelow(len(genreList))]

    print('Starting up...')

    headers = {"Content-Type": "application/json"}

    data = json.dumps({

    				"genre": "chopin",

    				"instrument":{
    					"piano": piano,
    					"strings": strings,
    					"winds": winds,
    					"drums": drums,
    					"harp": harp,
    					"guitar": guitar,
    					"bass": bass
    				},

    			"encoding": c_encoding,

    			"temperature": temperature,

    			"truncation": truncation,

    			"generationLength": number_of_tokens_to_generate,

    			"audioFormat": "audio/ogg"})

    print('Requesting data from the MuseNet API. Please wait...')
    response = requests.post('https://musenet.openai.com/sample', headers=headers, data=data)

    print('Decoding...')
    res = response.json()
    print('Done!')

    print('Parsing data...')

    FNAME = 'MuseNet-Composition'

    encoding = [int(y) for y in res['completions'][0]['encoding'].split()]

    song = []
    delta_times = 0
    for token in encoding:
    			if 0 <= token < 3840:
    					note = token % 128
    					idx = token // 128
    					velocity = VOLUMES[idx]
    					instrument = INSTRUMENTS[idx]
    					channel = TRACKS_OUT_INDEX[instrument]
    					delay = delta_times

    					if velocity > 0:
    						song.append(['note_on', delay * DELAY_MULTIPLIER, channel, note, velocity])
    						delta_times = 0

    					else:
    						song.append(['note_off', delay * DELAY_MULTIPLIER, channel, note, velocity])
    						delta_times = 0

    			elif 3840 <= token <= 3968:
    					note = token % 128
    					idx = token // 128
    					velocity = VOLUMES[idx]
    					instrument = INSTRUMENTS[idx]
    					channel = TRACKS_OUT_INDEX[instrument]
    					delay = delta_times

    					if velocity > 0:
    						song.append(['note_on', delay* DELAY_MULTIPLIER, channel, note, velocity])
    						delta_times = 0

    					else:
    						song.append(['note_off', (delay+1) * DELAY_MULTIPLIER, channel, note, 0])
    						delta_times = 0

    			elif 3968 < token < 4096:
    					delta_times = token % 128

    			elif token == 4096:
    				pass

    			else:
    					pass

    print('Converting to MIDI. Please stand-by...')

    output_signature = 'MuseNet Companion'
    track_name = 'Project Los Angeles'
    number_of_ticks_per_quarter = 1000

    list_of_MIDI_patches = [0, 24, 32, 40, 42, 46, 56, 71, 73, 0, 0, 0, 0, 0, 0, 0]
    output_file_name = FNAME
    text_encoding='ISO-8859-1'

    output_header = [number_of_ticks_per_quarter,
    										[['track_name', 0, bytes(output_signature, text_encoding)]]]

    patch_list = [['patch_change', 0, 0, list_of_MIDI_patches[0]],
    										['patch_change', 0, 1, list_of_MIDI_patches[1]],
    										['patch_change', 0, 2, list_of_MIDI_patches[2]],
    										['patch_change', 0, 3, list_of_MIDI_patches[3]],
    										['patch_change', 0, 4, list_of_MIDI_patches[4]],
    										['patch_change', 0, 5, list_of_MIDI_patches[5]],
    										['patch_change', 0, 6, list_of_MIDI_patches[6]],
    										['patch_change', 0, 7, list_of_MIDI_patches[7]],
    										['patch_change', 0, 8, list_of_MIDI_patches[8]],
    										['patch_change', 0, 9, list_of_MIDI_patches[9]],
    										['patch_change', 0, 10, list_of_MIDI_patches[10]],
    										['patch_change', 0, 11, list_of_MIDI_patches[11]],
    										['patch_change', 0, 12, list_of_MIDI_patches[12]],
    										['patch_change', 0, 13, list_of_MIDI_patches[13]],
    										['patch_change', 0, 14, list_of_MIDI_patches[14]],
    										['patch_change', 0, 15, list_of_MIDI_patches[15]],
    										['track_name', 0, bytes(track_name, text_encoding)]]

    output = output_header + [patch_list + song]

    midi_data = TMIDIX.opus2midi(output, text_encoding)

    # fs = FileSystemStorage()
    # filename = fs.save(output_file_name, midi_data)
    # uploaded_file_url = fs.url(filename)


    with open('media/musics/'+ output_file_name + '.mid', 'wb') as midi_file:
        	   midi_file.write(midi_data)
        	   midi_file.close()

    # synth_path = Path('static\salon\sf2\FluidR3_GM.sf2')
    # FluidSynth(synth_path, 16000).midi_to_audio(str(output_file_name + '.mid'), str(output_file_name + '.wav'))
    # display(Audio(str(output_file_name + '.wav'), rate=16000))
    #
    # print('Done! Enjoy! :)')

    return str(output_file_name + '.mid')
    # return uploaded_file_url
