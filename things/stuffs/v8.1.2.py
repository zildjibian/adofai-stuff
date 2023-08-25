# https://youtu.be/_iKQJiS4VM0

import soundfile
import ADOFAI as ADOFAI

settings = {
	"audioPath": 'berdly_theme.ogg',
	"levelName": 'iswearthisisfinal',

	"minVolume": 5,
	"minPause": 1
}

print('Loading...')

wave, sr = soundfile.read(settings['audioPath'])

print('Processing...')

prevVolume = 1
prev = 1
pause = 0

bpm = 2000000
bpm2 = sr * 60

tiles = 0

tileTimes = []

temp = [[], None]
prev = [None] # true = +; false = -;

def lmin(list):
	num = 0
	for i in list:
		if i < num: num = i
	return num

def lmax(list):
	num = 0
	for i in list:
		if i > num: num = i
	return num

lastCheck = 0

for i in range(len(wave)):
	vol = wave[i-1]; vol = (vol[0] + vol[1]) / 2
	if prev[0] != None:
		if (prev[0] == True and vol < 0) or (prev[0] == False and vol > 0):
			dict = {
				"start": temp[1],
				"end": i,
				"volume": None
			}
			if prev[0]: dict['volume'] = lmax(temp[0])
			else: dict['volume'] = lmin(temp[0])
			tileTimes.append(dict)
			
			temp[1] = i
			temp[0] = []
			prev[0] = vol > 0
	else: prev[0] = vol > 0; temp[1] = i

	if (i / len(wave) * 100) - lastCheck >= 5:
		print('-', str(lastCheck + 5) + '% Complete')
		lastCheck += 5
	
	temp[0].append(vol)

prevVolume = [0]
prevTime = [0]

audioData = []

for d in tileTimes:
	volume = d["volume"]
	if volume > 0:
		start = d['start']
		volume = abs(prevVolume[0] - volume)
		audioData.append({
			"volume": volume,
			"time": start
		})
	prevVolume[0] = d['volume']

print('- 100% Complete')

print('Exporting...')

level = ADOFAI.Level(settings["levelName"])

prevVolume = 0
prevTime = [0]

for d in audioData:
	if True:
		volume = d['volume'] * 100
		if volume >= settings['minVolume']:
			if True:
				pauseFormat = (d['time'] - prevTime[0]) * (bpm/bpm2)

				if pauseFormat >= settings['minPause']:
					event = ADOFAI.Event({ "floor": 1, "eventType": "Pause", "duration": 1, "countdownTicks": 0, "angleCorrectionDir": -1 })
					event.setProperty('floor', tiles)

					if pauseFormat < 2:
						level.addTile(180 + 180 * pauseFormat, True)
					elif pauseFormat >= 2:
						event.setProperty('duration', pauseFormat + (pauseFormat % 2))

						level.addTile(180 - (180 * (pauseFormat % 2)), True)
						level.addEvent(event)

					tiles += 1

			if volume != prevVolume:
				event = ADOFAI.Event({ "floor": 1, "eventType": "SetHitsound", "gameSound": "Hitsound", "hitsound": "Kick", "hitsoundVolume": 0 })
				event.setProperty('floor', tiles)
				
				event.setProperty('hitsoundVolume', volume)

				level.addEvent(event)

			prevTime[0] = d['time']
			prevVolume = max(volume,1)


if len(level.getTiles()) > 25000:
	print('WARNING! THIS MAP HAS ' + str(len(level.getTiles())) + " TILES!")
else:
	print('Generated ' + str(len(level.getTiles())) + " Tiles!")

level.setSettings('bpm', bpm)
level.setSettings('zoom', 750)
level.setSettings('trackDisappearAnimation', 'Fade')
level.setSettings('beatsBehind', 0)

level.export('./')

print('Exported!')