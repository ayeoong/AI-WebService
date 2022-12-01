import json
import requests
from importlib import import_module
import random

TMIDIX = import_module('tegridy-tools.tegridy-tools.TMIDIX')


def generateMusic(tags):

	genre_list = ["random", "chopin", "mozart", "rachmaninoff", "ladygaga", "country", "disney", "jazz", "bach", "beethoven", "journey", "thebeatles", "video", "broadway", "franksinatra", "bluegrass", "tchaikovsky", "liszt", "everything", "ragtime", "andrehazes", "cocciante", "thecranberries", "ligabue", "metallica", "traffic", "philcollins", "nineinchnails", "thepretenders", "sugarray", "grandfunkrailroad", "ron", "ellington", "fleetwoodmac", "thebeachboys", "kool & the gang", "foreigner", "tlc", "scottjames", "benfoldsfive", "smashmouth", "oasis", "allsaints", "donnasummer", "weezer", "bjork", "mariahcarey", "berte", "cheaptrick", "caroleking", "thecars", "gganderson", "robertpalmer", "zucchero", "alicecooper", "vanhalen", "brucehornsby", "coolio", "jimmybuffett", "lobo", "badcompany", "eminem", "creedenceclearwaterrevival", "deeppurple", "shearinggeorge", "robbiewilliams", "dalla", "ub40", "lindaronstadt", "sinatra", "inxs", "jonimitchell", "michaeljackson", "last", "devo", "shaniatwain", "korn", "brooksgarth", "sweet", "thewho", "roxette", "bowiedavid", "beegees", "renefroger", "mina", "estefangloria", "mccartney", "theventures", "carboni", "simplyred", "santana", "jewel", "meatloaf", "giorgia", "nofx", "rickymartin", "thecure", "thetemptations", "tozzi", "beck", "eiffel65", "jenniferlopez", "reelbigfish", "patsycline", "richardcliff", "styx", "acdc", "brucespringsteen", "michaelgeorge", "blondie", "pinkfloyd", "oldfieldmike", "redhotchilipeppers", "therollingstones", "morandi", "heart", "robertaflack", "pantera", "alabama", "jethrotull", "hanson", "mosch", "ludwigvanbeethoven", "dvorak", "chrisrea", "guns n' roses", "duranduran", "ericclapton", "bettemidler", "bwitched", "gordonlightfoot", "thegrassroots", "chicago", "whitezombie", "michaelbolton", "paulsimon", "marillion", "thepointersisters", "theanimals", "cher", "haydn", "aerosmith", "supertramp", "littleriverband", "america", "tonyorlando", "tompetty", "thecorrs", "aliceinchains", "kiss", "prince", "toto", "vanmorrison", "wagner", "cashjohnny", "annielennox", "enya", "thedoobiebrothers", "thetragicallyhip", "rush", "laurapausini", "stevemillerband", "simonandgarfunkel", "fiorellamannoia", "olivianewton-john", "carlysimon", "elvispresley", "vangelis", "bobdylan", "bbking", "vengaboys", "paoli", "thehollies", "alainsouchon", "pooh", "raf", "fiorello", "lionelrichie", "jimihendrix", "theeverlybrothers", "limpbizkit", "donhenley", "georgeharrison", "threedognight", "johnmellencamp", "carpenters", "raycharles", "basie", "billyocean", "scorpions", "royorbison", "whitneyhouston", "ironmaiden", "jovanotti", "alanjackson", "barrymanilow", "hueylewis", "kennyloggins", "chopinfrederic", "talkingheads", "themonkees", "rem", "jeanmicheljarre", "michelezarrillo", "eurythmics", "thedoors", "guesswho", "miller", "thefourseasons", "matiabazar", "tompettyandtheheartbreakers", "chickcorea", "scottjoplin", "amedeominghi", "bryanadams", "paulaabdul", "rossivasco", "billyjoel", "daniele", "claudedebussy", "gilbert & sullivan", "chakakhan", "nirvana", "garbage", "andreabocelli", "johnnyrivers", "emerson, lake & palmer", "theallmanbrothersband", "zappa", "boston", "mango", "barbrastreisand", "willsmith", "ozzyosbourne", "janetjackson", "antonellovenditti", "u2", "humperdinckengelbert", "jamiroquai", "zero", "chuckberry", "spicegirls", "ledzeppelin", "masini", "thekinks", "eagles", "billyidol", "alanismorissette", "joecocker", "jimcroce", "bobmarley", "blacksabbath", "stonetemplepilots", "silverchair", "paulmccartney", "blur", "nek", "greenday", "thepolice", "depechemode", "rageagainstthemachine", "madonna", "rogerskenny", "brooks & dunn", "883", "thedrifters", "amygrant", "herman", "toriamos", "eltonjohn", "britneyspears", "lennykravitz", "celentano", "ringostarr", "neildiamond", "aqua", "oscarpeterson", "joejackson", "moby", "collinsphil", "leosayer", "takethat", "electriclightorchestra", "pearljam", "marcanthony", "borodin", "petshopboys", "stevienicks", "hollybuddy", "turnertina", "annaoxa", "zztop", "sting", "themoodyblues", "ruggeri", "creed", "claudebolling", "renzoarbore", "erasure", "elviscostello", "airsupply", "tinaturner", "leali", "petergabriel", "nodoubt", "bread", "huey lewis & the news", "brandy", "level42", "radiohead", "georgebenson", "wonderstevie", "thesmashingpumpkins", "cyndilauper", "rodstewart", "bush", "ramazzotti", "bobseger", "theshadows", "gershwin", "cream", "biagioantonacci", "steviewonder", "nomadi", "direstraits", "davidbowie", "amostori", "thealanparsonsproject", "johnlennon", "crosbystillsnashandyoung", "battiato", "kansas", "clementi", "richielionel", "yes", "brassensgeorges", "steelydan", "jacksonmichael", "buddyholly", "earthwindandfire", "natkingcole", "therascals", "bonjovi", "alanparsons", "backstreetboys", "glencampbell", "howardcarpendale", "thesupremes", "villagepeople", "blink-182", "jacksonbrowne", "sade", "lynyrdskynyrd", "foofighters", "2unlimited", "battisti", "hall & oates", "stansfieldlisa", "genesis", "boyzone", "theoffspring", "tomjones", "davematthewsband", "johnelton", "neilyoung", "dionnewarwick", "aceofbase", "marilynmanson", "taylorjames", "rkelly", "grandi", "sublime", "edvardgrieg", "tool", "bachjohannsebastian", "patbenatar", "celinedion", "queen", "soundgarden", "abba", "drdre", "defleppard", "dominofats", "realmccoy", "natalieimbruglia", "hole", "spinners", "arethafranklin", "reospeedwagon", "indian", "movie", "scottish", "irish", "african", "taylorswift", "shakira", "blues", "latin", "katyperry", "world", "kpop", "africandrum", "michaelbuble", "rihanna", "gospel", "beyonce", "chinese", "arabic", "adele", "kellyclarkson", "theeagles", "handel", "rachmaninov", "schumann", "christmas", "dance", "punk", "natl_anthem", "brahms", "rap", "ravel", "burgmueller", "other", "schubert", "granados", "albeniz", "mendelssohn", "debussy", "grieg", "moszkowski", "godowsky", "folk", "mussorgsky", "kids", "balakirev", "hymns", "verdi", "hummel", "deleted", "delibes", "saint-saens", "puccini", "satie", "offenbach", "widor", "songs", "stravinsky", "vivaldi", "gurlitt", "alkan", "weber", "strauss", "traditional", "rossini", "mahler", "soler", "sousa", "telemann", "busoni", "scarlatti", "stamitz", "classical", "jstrauss2", "gabrieli", "nielsen", "purcell", "donizetti", "kuhlau", "gounod", "gibbons", "weiss", "faure", "holst", "spohr", "monteverdi", "reger", "bizet", "elgar", "czerny", "sullivan", "shostakovich", "franck", "rubinstein", "albrechtsberger", "paganini", "diabelli", "gottschalk", "wieniawski", "lully", "morley", "sibelius", "scriabin", "heller", "thalberg", "dowland", "carulli", "pachelbel", "sor", "marcello", "ketterer", "rimsky-korsakov", "ascher", "bruckner", "janequin", "anonymous", "kreutzer", "sanz", "joplin", "susato", "giuliani", "lassus", "palestrina", "smetana", "berlioz", "couperin", "gomolka", "daquin", "herz", "campion", "walthew", "pergolesi", "reicha", "polak", "holborne", "hassler", "corelli", "cato", "azzaiolo", "anerio", "gastoldi", "goudimel", "dussek", "prez", "cimarosa", "byrd", "praetorius", "rameau", "khachaturian", "machaut", "gade", "perosi", "gorzanis", "smith", "haberbier", "carr", "marais", "glazunov", "guerrero", "cabanilles", "losy", "roman", "hasse", "sammartini", "blow", "zipoli", "duvernoy", "aguado", "cherubini", "victoria", "field", "andersen", "poulenc", "d'aragona", "lemire", "krakowa", "maier", "rimini", "encina", "banchieri", "best", "galilei", "warhorse", "gypsy", "soundtrack", "encore", "roblaidlow", "nationalanthems", "benjyshelton", "ongcmu", "crosbystillsnashyoung", "smashingpumpkins", "aaaaaaaaaaa", "alanismorrisette", "animenz", "onedirection", "nintendo", "disneythemes", "gunsnroses", "rollingstones", "juliancasablancas", "abdelmoinealfa", "berckmansdeoliveira", "moviethemes", "beachboys", "davemathews", "videogamethemes", "moabberckmansdeoliveira", "unknown", "cameronleesimpson", "johannsebastianbach", "thecarpenters", "elo", "nightwish", "blink182", "emersonlakeandpalmer", "tvthemes"]
	genre_dict = {'none': ['random', 'chopin', 'disney', 'video', 'broadway', 'ragtime', 'kool & the gang', 'alicecooper', 'creedenceclearwaterrevival', 'last', 'jewel', 'meatloaf', 'giorgia', 'patsycline', 'mosch', 'kiss', 'enya', 'pooh', 'fiorello', 'limpbizkit', 'jovanotti', 'chopinfrederic', 'tompettyandtheheartbreakers', 'gilbert & sullivan', 'nirvana', 'emerson, lake & palmer', 'zappa', 'bobmarley', 'blacksabbath', 'thepolice', 'brooks & dunn', 'herman', 'electriclightorchestra', 'elviscostello', 'huey lewis & the news', 'blink-182', 'hall & oates', 'indian', 'movie', 'scottish', 'irish', 'african', 'world', 'africandrum', 'michaelbuble', 'chinese', 'adele', 'christmas', 'dance', 'natl_anthem', 'burgmueller', 'other', 'moszkowski', 'folk', 'kids', 'balakirev', 'hymns', 'hummel', 'deleted', 'songs', 'gurlitt', 'weber', 'traditional', 'nielsen', 'kuhlau', 'gibbons', 'rubinstein', 'diabelli', 'gottschalk', 'morley', 'heller', 'thalberg', 'carulli', 'marcello', 'ketterer', 'ascher', 'bruckner', 'janequin', 'anonymous', 'kreutzer', 'susato', 'giuliani', 'smetana', 'gomolka', 'daquin', 'herz', 'campion', 'walthew', 'polak', 'cato', 'azzaiolo', 'anerio', 'goudimel', 'prez', 'gade', 'gorzanis', 'smith', 'haberbier', 'cabanilles', 'losy', 'roman', 'sammartini', 'blow', 'zipoli', 'duvernoy', 'aguado', 'victoria', 'field', "d'aragona", 'lemire', 'krakowa', 'maier', 'rimini', 'encina', 'best', 'gypsy', 'soundtrack', 'encore', 'roblaidlow', 'nationalanthems', 'benjyshelton', 'ongcmu', 'aaaaaaaaaaa', 'animenz', 'nintendo', 'disneythemes', 'abdelmoinealfa', 'berckmansdeoliveira', 'moviethemes', 'videogamethemes', 'moabberckmansdeoliveira', 'unknown'], 'classical': ['mozart', 'rachmaninoff', 'bach', 'beethoven', 'tchaikovsky', 'liszt', 'shearinggeorge', 'ludwigvanbeethoven', 'dvorak', 'haydn', 'wagner', 'claudedebussy', 'borodin', 'gershwin', 'clementi', 'edvardgrieg', 'bachjohannsebastian', 'handel', 'rachmaninov', 'schumann', 'brahms', 'schubert', 'granados', 'albeniz', 'mendelssohn', 'debussy', 'grieg', 'godowsky', 'mussorgsky', 'verdi', 'delibes', 'saint-saens', 'puccini', 'satie', 'offenbach', 'widor', 'stravinsky', 'vivaldi', 'alkan', 'strauss', 'rossini', 'mahler', 'sousa', 'telemann', 'busoni', 'scarlatti', 'jstrauss2', 'gabrieli', 'purcell', 'donizetti', 'gounod', 'faure', 'holst', 'spohr', 'monteverdi', 'reger', 'bizet', 'elgar', 'czerny', 'shostakovich', 'franck', 'albrechtsberger', 'paganini', 'wieniawski', 'lully', 'sibelius', 'scriabin', 'dowland', 'pachelbel', 'sor', 'rimsky-korsakov', 'lassus', 'berlioz', 'couperin', 'pergolesi', 'reicha', 'holborne', 'hassler', 'corelli', 'dussek', 'cimarosa', 'rameau', 'khachaturian', 'machaut', 'marais', 'glazunov', 'hasse', 'cherubini', 'poulenc', 'banchieri', 'johannsebastianbach'], 'electronic dance music': ['ladygaga', 'donnasummer', 'bjork', 'robbiewilliams', 'estefangloria', 'eiffel65', 'jenniferlopez', 'cher', 'jamiroquai', 'spicegirls', 'madonna', 'toriamos', 'britneyspears', 'moby', 'marcanthony', 'petshopboys', 'amostori', 'villagepeople', 'shakira', 'katyperry', 'rihanna'], 'blues': ['country', 'jazz', 'tompetty', 'jacksonbrowne', 'dominofats'], 'rock': ['journey', 'ligabue', 'traffic', 'nineinchnails', 'grandfunkrailroad', 'ron', 'fleetwoodmac', 'foreigner', 'cheaptrick', 'vanhalen', 'badcompany', 'deeppurple', 'korn', 'bowiedavid', 'mccartney', 'acdc', 'brucespringsteen', 'pinkfloyd', 'oldfieldmike', 'therollingstones', 'heart', 'jethrotull', 'hanson', "guns n' roses", 'ericclapton', 'marillion', 'theanimals', 'aerosmith', 'supertramp', 'littleriverband', 'america', 'toto', 'thedoobiebrothers', 'thetragicallyhip', 'stevemillerband', 'donhenley', 'threedognight', 'hueylewis', 'rem', 'thedoors', 'guesswho', 'bryanadams', 'rossivasco', 'theallmanbrothersband', 'ozzyosbourne', 'u2', 'ledzeppelin', 'billyidol', 'joecocker', 'jimcroce', 'stonetemplepilots', 'silverchair', 'paulmccartney', 'lennykravitz', 'ringostarr', 'pearljam', 'zztop', 'petergabriel', 'bread', 'bush', 'bobseger', 'theshadows', 'cream', 'direstraits', 'davidbowie', 'crosbystillsnashandyoung', 'yes', 'steelydan', 'bonjovi', 'glencampbell', 'lynyrdskynyrd', 'foofighters', 'davematthewsband', 'neilyoung', 'marilynmanson', 'soundgarden', 'defleppard', 'reospeedwagon', 'punk', 'crosbystillsnashyoung', 'gunsnroses', 'rollingstones', 'davemathews'], 'psychedelic rock': ['thebeatles'], 'holiday': ['franksinatra', 'sinatra', 'stamitz', 'palestrina', 'byrd', 'praetorius', 'perosi'], 'country music': ['bluegrass'], 'alternative/indie': ['everything', 'thecranberries', 'benfoldsfive', 'oasis', 'weezer', 'devo', 'nofx', 'thecure', 'beck', 'reelbigfish', 'styx', 'redhotchilipeppers', 'duranduran', 'vangelis', 'talkingheads', 'billyjoel', 'garbage', 'blur', 'rogerskenny', 'joejackson', 'themoodyblues', 'creed', 'nodoubt', 'radiohead', 'thesmashingpumpkins', 'thealanparsonsproject', 'kansas', 'theoffspring', 'taylorjames', 'hole', 'sullivan', 'smashingpumpkins', 'juliancasablancas'], 'pop': ['andrehazes', 'cocciante', 'philcollins', 'sugarray', 'smashmouth', 'allsaints', 'mariahcarey', 'berte', 'caroleking', 'thecars', 'robertpalmer', 'zucchero', 'jimmybuffett', 'lobo', 'lindaronstadt', 'inxs', 'jonimitchell', 'beegees', 'renefroger', 'carboni', 'simplyred', 'rickymartin', 'tozzi', 'richardcliff', 'michaelgeorge', 'chrisrea', 'bettemidler', 'bwitched', 'chicago', 'michaelbolton', 'tonyorlando', 'thecorrs', 'laurapausini', 'simonandgarfunkel', 'fiorellamannoia', 'olivianewton-john', 'carlysimon', 'thehollies', 'raf', 'theeverlybrothers', 'carpenters', 'billyocean', 'whitneyhouston', 'kennyloggins', 'themonkees', 'michelezarrillo', 'eurythmics', 'matiabazar', 'amedeominghi', 'paulaabdul', 'daniele', 'andreabocelli', 'mango', 'antonellovenditti', 'masini', 'thekinks', 'eagles', 'alanismorissette', 'nek', '883', 'eltonjohn', 'celentano', 'neildiamond', 'collinsphil', 'leosayer', 'takethat', 'hollybuddy', 'annaoxa', 'sting', 'ruggeri', 'renzoarbore', 'airsupply', 'leali', 'level42', 'cyndilauper', 'rodstewart', 'ramazzotti', 'biagioantonacci', 'nomadi', 'battiato', 'buddyholly', 'backstreetboys', 'battisti', 'stansfieldlisa', 'johnelton', 'aceofbase', 'patbenatar', 'abba', 'natalieimbruglia', 'taylorswift', 'kellyclarkson', 'theeagles', 'soler', 'alanismorrisette', 'onedirection'], 'metal': ['metallica', 'pantera', 'whitezombie', 'ironmaiden'], 'r&b/soul': ['thepretenders', 'tlc', 'brucehornsby', 'mina', 'santana', 'thetemptations', 'robertaflack', 'thegrassroots', 'paulsimon', 'thepointersisters', 'prince', 'elvispresley', 'lionelrichie', 'raycharles', 'royorbison', 'alanjackson', 'barrymanilow', 'thefourseasons', 'chakakhan', 'johnnyrivers', 'willsmith', 'janetjackson', 'humperdinckengelbert', 'thedrifters', 'stevienicks', 'turnertina', 'tinaturner', 'brandy', 'wonderstevie', 'steviewonder', 'richielionel', 'earthwindandfire', 'therascals', 'thesupremes', 'sade', 'tomjones', 'dionnewarwick', 'rkelly', 'queen', 'realmccoy', 'spinners', 'arethafranklin', 'beyonce'], 'jazz': ['ellington', 'basie', 'chickcorea', 'scottjoplin', 'oscarpeterson', 'claudebolling', 'georgebenson', 'natkingcole', 'joplin', 'cameronleesimpson'], "children's music": ['classical'], 'dance/electronic': ['scottjames', 'coolio', 'eminem', 'michaeljackson', 'roxette', 'theventures', 'morandi', 'bbking', 'vengaboys', 'paoli', 'georgeharrison', 'jeanmicheljarre', 'chuckberry', 'erasure', 'johnlennon', 'jacksonmichael', '2unlimited', 'genesis', 'grandi', 'weiss'], 'schlager & volksmusik': ['gganderson', 'barbrastreisand', 'howardcarpendale', 'carr'], 'k-pop': ['dalla'], 'reggae': ['ub40'], 'country': ['shaniatwain', 'brooksgarth', 'alabama', 'cashjohnny'], 'latin urbano': ['sweet', 'annielennox'], 'gospel': ['thewho'], 'indian film pop': ['blondie', 'vanmorrison', 'scorpions'], 'folk': ['gordonlightfoot', 'bobdylan', 'sanz', 'gastoldi'], 'alternative rock': ['aliceinchains'], 'progressive metal': ['rush', 'tool'], 'chanson': ['alainsouchon', 'brassensgeorges', 'celinedion'], 'hip-hop/rap': ['jimihendrix', 'miller', 'aqua', 'drdre'], 'french indie': ['johnmellencamp'], 'uk rap': ['boston'], 'pop rock': ['zero'], 'new age': ['greenday'], 'industrial music': ['depechemode'], 'nu metal': ['rageagainstthemachine'], 'christian': ['amygrant'], 'japanese rock': ['alanparsons'], 'indonesian hip hop': ['boyzone'], 'afroswing': ['sublime'], 'folk music': ['blues'], 'world music': ['latin'], 'pop music': ['kpop'], 'spirituals': ['gospel'], 'arabic pop music': ['arabic'], 'rhythm and blues': ['rap'], 'impressionism in music': ['ravel'], 'musica tropicale': ['guerrero'], 'j-pop': ['galilei'], 'war': ['warhorse']}    

	genre_data = [x for x in tags if x in genre_list]
	genre_kind = [x for x in tags if x in genre_dict.keys()]
	
	if genre_data != []:
		random.shuffle(genre_data)
		genre = genre_data[0]
	elif genre_kind != []:
		genre_keys = [genre_key for tokens in tags for genre_key in genre_dict.keys() if tokens in genre_key]
		random.shuffle(genre_keys)
		genre = genre_dict[genre_keys[0]][0]
	else:
		random.shuffle(genre_list)
		genre = genre_list[0]


	random_num = random.randrange(4, 8)
	instruments_tf = [False, False, False, False, False, False, False]
	for i in range(random_num):
		instruments_tf[i] = True
	random.shuffle(instruments_tf)

	instruments_list = ['piano', 'strings', 'winds', 'drums', 'harp', 'guitar', 'bass']
	for i, ins in enumerate(instruments_list):
		if ins in tags:
			instruments_tf = [False, False, False, False, False, False, False]
			instruments_tf[i] = True
	print(instruments_tf)
		
	#@markdown Select instruments
	piano = instruments_tf[0] #@param {type:"boolean"}
	strings = instruments_tf[1] #@param {type:"boolean"}
	winds = instruments_tf[2] #@param {type:"boolean"}
	drums = instruments_tf[3] #@param {type:"boolean"}
	harp = instruments_tf[4] #@param {type:"boolean"}
	guitar = instruments_tf[5] #@param {type:"boolean"}
	bass = instruments_tf[6] #@param {type:"boolean"}

	#@markdown Generation settings
	number_of_tokens_to_generate = 800 #@param {type:"slider", min:64, max:1024, step:8}
	temperature = 1 #@param {type:"slider", min:0.1, max:2, step:0.1}
	truncation = 20 #@param {type:"integer"}

	INSTRUMENTS = ["piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "piano", "violin", "violin", "cello", "cello", "bass", "bass", "guitar", "guitar", "flute", "flute", "clarinet", "clarinet", "trumpet", "trumpet", "harp", "harp", 'drum', 'drum']
	TRACKS_OUT_INDEX = {"piano": 0, "violin": 3, "cello": 4, "bass": 2, "guitar": 1, "flute": 8, "clarinet": 7, "trumpet": 6, "harp": 5, "drum": 9}
	VOLUMES = [0, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 80, 0, 100, 0]
	

	DELAY_MULTIPLIER = 20
	c_encoding = '4096'

	print('Starting up...')

	headers = {"Content-Type": "application/json"}

	data = json.dumps({"genre": genre,
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

	print(data)

	response = requests.post('https://musenet.openai.com/sample', headers=headers, data=data)

	print('Decoding...')
	res = response.json()
	print('Done!')
	
	print('Parsing data...')

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
 
	return midi_data
