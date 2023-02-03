# Universal Assemblers

## Game Description
Universal Assemblers is a sim game inspired by Universal Paperclips and Von Nuemann Probes. The game simulates a sentient artificial intelligence as it explores and manipulates the cosmos to its will.

## Game Appearance
UA features a GUI with 3 panes, and a top ribbon.

### The Local Map Pane
The Local Map will feature the celestial object that has been selected in the **Object List**.

### The Object Pane
The object list features a description of the main celestial object referenced in the local map. Any child object of the celestial object desplayed will be clickable in this pane. 
Once clicked, the map will update to that child object and its description, it will also list clickable links to any of its child objects if available. 

Objects include:
	1. Galaxy
	2. Solar System
	3. Planet System
	4. Moon
	5. Asteroid Belt

###Actions Pane
The Actions pane will present any opportunities avalilable to you. Available actions will change based on the local area selected in addition to global actions pertaining to your race of Universal Assemblers. 
Some actions will have prerequisites

Constructions possible at multiple scales: 
Military Base (surface, orbital, solar [minor or major solar object])
Brain (Orbital, or Solar)
Factory (surface, orbital, solar [minor or major solar object])
	factories can either be production or warehousing objects
Habitat (surface, orbital, solar [minor or major solar object])


Actions Include: 
	0. Allocate and Schedule
		a.Schedule
			This scheduler allows you to allocate Universal Assemblers within the local area to a list of actions.
			Actions will be conducted in cronological order. Any action that cannot be completed will fail and be skipped.
			Schedules can be saved and set to terminate on certain conditions: 
				Conditions: 
					Quantity of object is met
		b. Allocate
			After a schedule is made, allocate a percentage or number of Assemblers in the local area to the task. 

	1. Research
		a. Ecology
		b. Military
		c. Engineering
		d. Automation
	2. Build
		a. Solar System Constuctions
			1. Space Station
				a. Halo World (habitat)
				b. Factory
				c. Military Base
				d.
				e. Warp Ring (cannot be mixed)
			2. Dyson Swarm (M)
				a. Brain
				b. Power
			3. Ring World (M)
				a. Habitat
				b. Factory
				c. Military
				d. Mixed
			4. Stellar engine (M)
		b. Orbital Constructions
			1. space elevator (M)
			2. military satilite
			3. magnetic field
			4. Orbital Space Station
			5. Brain
		c. Surface constructions

	3. Mine / Disassemble
	4. Exterminate
	5. Explore / Travel

	7. Tracker
		The tracker action opens an additional window that shows local and global stats for your playthrough this will also feature easter eggs e.g. race designation 
		Race Designations include Berserkers, Seeders, Builders, Slavers, Miners, Terraformers
		A Race can have multiple race designations with the bolded one indicating the main designation
		Stats Tracked: 
			1. assemblers
			2. discovered solar systems
			3. alien life forms discovered
			4. alien life forms exterminated
			5. alien life forms converted
			6. alien life forms enslaved
			7. megastructures built
			8. resources mined
			9. planets terraformed
			10. technologies learned
