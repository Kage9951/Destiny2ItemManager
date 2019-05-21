# Destiny2ItemManager
Is your vault filled with the brim with armor? Looking for a way to quickly sort through it all? Look no further because this is the solution for you! 

Over the past Season of the Drifter with all the new armor added I was looking for a way to easily optimize my inventory. I decided  to make my own script to manage it. This started in powershell and later moved to python. This was meant to help introduce me to python and yes my code may be a bit sloppy due to it.

This script uses tags from Destiny Item Manager (DIM) to mark what gear to keep. The tags differ depending how the gear is matched. First the script simply looks at what YOU define the recommended perks are and marks items found as 'keep'. These are defined in the RecommendedPerks.csv. Within that CSV you define the name of the perk, the minimum to keep (Currently hard coded to 1 since a recent update required a change in how to implement it), and the weight of the perk to YOU. The weight is a nice little feature I added to allow it to further optimize gear choices, so that it would pick per say \[Pump Action (weight 2), Remote Connection (weight 2)\] over \[Pump Action (weight 2), Precision Weapon Targeting (weight 1)\]. Those weights are free for you to customize on what perks you prefer and the script will still keep at least one of every perk you define in the CSV.

The second part then goes through and finds any defined Perk Sets and marks them as 'favorite'. Perk Sets are sets of perks that YOU define. The script will look for any armor that matches ALL of the defined perks. This allows you to explictly put any of YOUR god rolls. An example for me would be this for my gloves: \[Enhanced Grenade Launcher Loader, Light Arms Loader, Rifle Loader, Shotgun Scavenger, Sniper Scavenger\]. If that happened to be in my vault that gear would be marked as 'favorite'.

For me this has reduced my vault entirely to 146 pieces of Legendary Armor across ALL my characters. And has been a life saver in terms of time spent looking through my vault.

Another thing to note about perks. In DIM the following are an example of what is defined as a perk: 

\[Heavy Hunter Armor*,Plasteel Reinforcement Mod,Restorative Mod*,Paragon Mod*,Masterwork*,Mercury Vex Chrome*,Ashes to Assets,Pump Action*,Remote Connection,Rocket Launcher Reserves,Shotgun Reserves*\]

This includeds shaders and mods if that interesets you. (I used Riven's Curse as a perk to make sure I always have a full set of revire dawn).

# Usage

  Using Destiny Item Manager(https://app.destinyitemmanager.com/)
  
  Go to Settings (Gear Icon)
  
  Go all the way down to Spreadsheets
  
  Click on Armor
  
  Save file as DestinyArmor.csv
  
  Move file to location of the python script
  
  Run the Script
  
  Then Drag DestinyArmorExport.csv back into the spreadsheets section of DIM
  
