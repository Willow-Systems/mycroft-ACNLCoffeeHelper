# Copyright 2017, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import json
from adapt.intent import IntentBuilder

from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG


class AcnlCoffeeSkill(MycroftSkill):
    def __init__(self):
        super(AcnlCoffeeSkill, self).__init__(name="AcnlCoffeeSkill")

    @intent_handler(IntentBuilder("").require("Ask").require("Animal"))
    def handle_intent(self, message):
        # Extract what the user asked about
	self.speak("Let me see")
        villager = message.data.get("Animal")
	beans = self._lookup(villager, "beans")
	milk = self._lookup(villager, "milk")
	sugar = self._lookup(villager, "sugar")
	self.speak_dialog('answers', {'villager': villager, 'milk': milk, 'sugar': sugar + " spoonfuls", 'beans': beans})

    def _lookup(self, searchterm, item):
	#Currently this searches the list 3 times, but it does mean you can ask for just one thing (e.g. sugar)
	try:
		jsonfile = open("/opt/mycroft/skills/skill-acnlCoffee/acnlcoffee.json","r")
		jsonstring = jsonfile.read()

		decoded = json.loads(jsonstring)
		for x in decoded['villagers']:
		        if (x['name'].lower() == searchterm.lower()):
				if (item.lower() == "beans"):
					return x["beans"]
				elif (item.lower() == "milk"):
					strmilk = x["milk"]
					if (strmilk != "No"):
						strmilk = strmilk + " of"
					return strmilk
				elif (item.lower() == "sugar"):
					return x["sugar"]	

	except Exception as e:
            LOG.error("Error: {0}".format(e))

#    @intent_handler(IntentBuilder("").require("Ask"))
#    def handle_intent_2(self,message):
#        #animal = message.data.get("Animal")
#	self.speak_dialog('answers', {'animal': "Turd", 'milk': "some", 'sugar': "loads", 'beans': "baked beans"})

def create_skill():
    return AcnlCoffeeSkill()
