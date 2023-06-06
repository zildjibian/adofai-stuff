import ADOFAI
import librosa
import math

settings = {
    "audioPath": './filename.ogg',
    "levelName": 'level',

    "resample": 1,
    "minRatio": 2/1,
    "minDelta": 10
}

print('Loading...')

wave, sr = librosa.load(settings['audioPath'], sr=44100)

print('Resampling...')

wave_resample = librosa.resample(y=wave, orig_sr=sr, target_sr=sr/settings['resample'])
sample_rate = sr/settings['resample']

level = ADOFAI.createLevel(settings['levelName'])

print('Exporting...')

prevVolume = 1
pause = 0

bpm = 2000000
bpm2 = sample_rate * 60

tiles = 0

lowestVolume = 0
highestVolume = 0

for i in range(len(wave_resample)):
    vol = wave_resample[i-1] * 100

    doDelta = False
    delta = 0

    if vol < lowestVolume:
        lowestVolume = vol
        
    if vol > highestVolume:
        highestVolume = vol
    else: doDelta = True

    if doDelta:
        delta = abs(highestVolume - lowestVolume)
        lowestVolume = 0
        highestVolume = 0

        if delta/prevVolume >= settings['minRatio'] and delta >= settings['minDelta']:
            if pause > 0:
                event = ADOFAI.Event({ "floor": 1, "eventType": "Pause", "duration": 1, "countdownTicks": 0, "angleCorrectionDir": -1 })
                event.setProperty('floor', tiles)

                if pause * (bpm/bpm2) < 2:
                    level.addTile(180 + 180 * (bpm/bpm2) * pause, True)
                elif pause * (bpm/bpm2) >= 2:
                    event.setProperty('duration', (pause * (bpm/bpm2)) + ((pause * (bpm/bpm2)) % 2))

                    level.addTile(180 - (180 * ((pause * (bpm/bpm2)) % 2)), True)
                    level.addEvent(event)

                tiles += 1

            if delta != prevVolume:
                event = ADOFAI.Event({ "floor": 1, "eventType": "SetHitsound", "gameSound": "Hitsound", "hitsound": "Kick", "hitsoundVolume": 0 })
                event.setProperty('floor', tiles)
                event.setProperty('hitsoundVolume', delta)

                level.addEvent(event)
            pause = 0
        else: pause += 1

        prevVolume = max(delta,1)
    else: pause+=1

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
