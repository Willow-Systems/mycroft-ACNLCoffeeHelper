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
import os
from os.path import join, isfile, abspath, dirname
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
	if not beans:
		self.speak_dialog('novillager', {'villager': villager})
	else:
		self.speak_dialog('answers', {'villager': villager, 'milk': milk, 'sugar': sugar, 'beans': beans})

    def _lookup(self, searchterm, item):
	#Currently this searches the list 3 times, but it does mean you can ask for just one thing (e.g. sugar)
	try:
		fpath = join(abspath(dirname(__file__)), 'acnlcoffee.json')
		jsonfile = open(fpath,"r")
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
				    strsugar = x["sugar"]
                                    if (strsugar != "1"):
                                        strsugar = strsugar + " spoonfuls"
                                    else:
                                        strsugar = strsugar + " spoonful"
                                    return strsugar

	except Exception as e:
            LOG.error("Error: {0}".format(e))

def create_skill():
    return AcnlCoffeeSkill()
