import json

class Event: # -UNFINISHED- #
    def __init__(self,dict={},floor=0,event='Twirl'):

        if len(dict)>0 and dict['floor'] != None and dict['eventType'] != None:
            self.data = dict
            return

        data = {
            "floor": floor or 1,
            "eventType": event or 'Twirl'
        }

        if data["eventType"] == 'SetSpeed':
            data["speedType"] = 'Bpm'
            data["beatsPerMinute"] = 100
            data["bpmMultiplier"] = 1
        
        self.data = data
    
    def getProperty(self,prop: str):
        return self.data[prop]

    def setProperty(self,prop: str,val):
        if prop != 'eventType':
            shouldChange = [True]

            if self.data["eventType"] == 'Twirl':
                shouldChange[0] = False
            elif self.data["eventType"] == 'SetSpeed':
                if prop == 'speedType':
                    if val != 'Bpm' and val != 'Multiplier':
                        shouldChange[0] = False
            
            if shouldChange[0] == True:
                self.data[prop]=val or self.data[prop]

class Level:
    def __init__(self,name: str):
        self.data = {
            "name": name + '.adofai',
            "level": {
                "angleData": [],
                "settings": {
                    "version": 11,
                    "artist": "", 
                    "specialArtistType": "None", 
                    "artistPermission": "", 
                    "song": "", 
                    "author": "", 
                    "separateCountdownTime": "Enabled", 
                    "previewImage": "", 
                    "previewIcon": "", 
                    "previewIconColor": "003f52", 
                    "previewSongStart": 0, 
                    "previewSongDuration": 10, 
                    "seizureWarning": "Disabled", 
                    "levelDesc": "", 
                    "levelTags": "", 
                    "artistLinks": "", 
                    "difficulty": 1, 
                    "requiredMods": [],
                    "songFilename": "", 
                    "bpm": 100, 
                    "volume": 100, 
                    "offset": 0, 
                    "pitch": 100, 
                    "hitsound": "Kick", 
                    "hitsoundVolume": 100, 
                    "countdownTicks": 4,
                    "trackColorType": "Single", 
                    "trackColor": "debb7b", 
                    "secondaryTrackColor": "ffffff", 
                    "trackColorAnimDuration": 2, 
                    "trackColorPulse": "None", 
                    "trackPulseLength": 10, 
                    "trackStyle": "Standard", 
                    "trackGlowIntensity": 100, 
                    "trackAnimation": "None", 
                    "beatsAhead": 3, 
                    "trackDisappearAnimation": "None", 
                    "beatsBehind": 4,
                    "backgroundColor": "000000", 
                    "showDefaultBGIfNoImage": "Enabled", 
                    "bgImage": "", 
                    "bgImageColor": "ffffff", 
                    "parallax": [100, 100], 
                    "bgDisplayMode": "FitToScreen", 
                    "lockRot": "Disabled", 
                    "loopBG": "Disabled", 
                    "unscaledSize": 100,
                    "relativeTo": "Player", 
                    "position": [0, 0], 
                    "rotation": 0, 
                    "zoom": 100, 
                    "pulseOnFloor": "Enabled", 
                    "startCamLowVFX": "Disabled",
                    "bgVideo": "", 
                    "loopVideo": "Disabled", 
                    "vidOffset": 0, 
                    "floorIconOutlines": "Disabled", 
                    "stickToFloors": "Enabled", 
                    "planetEase": "Linear", 
                    "planetEaseParts": 1, 
                    "planetEasePartBehavior": "Mirror", 
                    "customClass": "",
                    "legacyFlash": False,
                    "legacyCamRelativeTo": False,
                    "legacySpriteTiles": False 
                },
                "actions": [],
                "decorations": []
            }
        }

    def addTile(self,angle,relative):
        if relative:
            if len(self.data["level"]["angleData"]) != 0:
                lastAngle = self.data["level"]["angleData"][len(self.data["level"]["angleData"])-1]
                self.data["level"]["angleData"].append((angle + lastAngle) % 360)
            else:
                self.data["level"]["angleData"].append((angle + 180) % 360)
        else:
            _angle = [angle]
            if _angle[0] != 999:
                _angle[0] %= 360
            
            self.data["level"]["angleData"].append(_angle[0])
    
    def addEvent(self, event: Event):
        if event.data['floor'] and event.data['floor']>len(self.getTiles())-1:
            for _ in range(event.data['floor']-len(self.getTiles())):
                self.addTile(0, False)
        
        if event.data['eventType'] == 'AddDecoration':
            self.data["level"]["decorations"].append(event.data)
        else:
            self.data["level"]["actions"].append(event.data)
    
    def addDecoration(self, deco: Event):
        if deco.data['eventType'] == 'AddDecoration':
            self.addEvent(deco)
    
    def setSettings(self,name: str,val):
        self.data["level"]["settings"][name] = val

    def getEvents(self):
        return self.data["level"]["actions"]

    def getTiles(self):
        return self.data["level"]["angleData"]

    def export(self,path: str):
        file = open(path + self.data["name"], 'w')

        file.write(json.dumps(self.data["level"]))

        file.close()
