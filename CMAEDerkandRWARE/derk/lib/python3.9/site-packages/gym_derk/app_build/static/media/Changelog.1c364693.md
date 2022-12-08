$$ 0.26.0 2020-10-07T08:43:40Z
ELO based ranking & matchmaking
- Each player now has an associated ELO rating, which is updated when you battle someone.
- There are five fixed divisions; Diamond, Ruby, Gold, Silver and Copper. Your rating determines your division.
- Matchmaking is based on ELO ratings. The selection is weighted to favour teams you're likely to have an even matchup with (not too hard, not too easy), but you always have a chance to fight any active team.
- You need to play a minimum of five matches to show up in the rankings.

$$ 0.25.24 2020-09-15T08:28:02Z
Python Reinforcement Learning Environment
I'm happy to announce that there is now an OpenAI reinforcement learning environment based on the game available called [Derk's Gym website](https://gym.derkgame.com)!

$$ 0.25.23 2020-08-16T10:50:41Z
Load Derkling brain from another Derkling

$$ 0.25.22 2020-08-14T16:10:17Z
Limit number of runs when using scheduling

$$ 0.25.21 2020-08-10T13:59:13Z
Add item stats to item tooltips
Such as damage, cast time, cooldown etc.

$$ 0.25.20 2020-08-10T11:47:25Z
Kill, victory and loss bounties added
When a unit is "pushed" (e.g. Magnum), their fall damage is attributed to the one that pushed them.

$$ 0.25.19 2020-08-07T16:22:01Z
Move bounties to Derklings
The bounties are now associated with the Derklings themselves, rather than with the training setup. There is also a "presets" feature where you can save and load bounty configurations. This also made it possible to do "dual" training again (train both sides at the same time), which has been re-enabled.

$$ 0.25.18 2020-08-06T07:59:27Z
Bug fix: "Statue takes damage" bounty

$$ 0.25.17 2020-08-05T17:17:47Z
Edit bounties in main menu

$$ 0.25.16 2020-08-05T15:32:09Z
Deterministic focus
Focus was previously determined by CDF sampling the decision outputs from the Derkling. This meant that a Derkling couldn't precisly determine which enemy to focus on, but could only give them higher likelyhood to be choosen. This has now been replaced with a simple argmax. The reason for sampling was originally to give battles variation; I wanted each battle to be unique, and sampling outputs was an easy way to do so. But as the game has evolved there are now other factors that ensure that each battle is unique, reducing the need for this.

$$ 0.25.15 2020-08-05T14:39:26Z
Bug fix: attachment slots wrong order when creature is "away".

$$ 0.25.14 2020-08-04T16:00:23Z
Nerf Cleaver: Casting is aborted when the target goes out of range.
This tweak applies to all abilities; a target must remain in range for an ability to "hit", and channeling abilities (Heal, Vampire gland) will stop channeling if the target goes out of range. To be considered "in range", the target must also be in front of the caster.

$$ 0.25.13 2020-08-04T13:43:18Z
Tweak matchmaking
Matchinmaking is reworked in this version. Instead of each opponent in the same group having an equal chance to be choosen, they are now weighted by the "points opportunity". For each opponent in your group, you have a maximum of 10 potential points since they are a best of five, and a victory counts as two points. So if you for instance have one victory and one tie against a particular opponent, then you'll have 3p (this is how it worked before this patch as well). Since the maximum is 10p, you have a 7p "opportunity", which is also the weight for the chance of choosing this opponent. There's also an indicator added next to each opponent, which will tell you what your current "best of five" state is.

$$ 0.25.12 2020-08-03T16:09:06Z
Derkling tags
It's now possible to "tag" your Derklings, to easier arrange them into groups!

$$ 0.25.11 2020-08-03T09:18:01Z
Nerf helium bubble: Remove "is on ground" requirement for casting abilities
Abilities can now be cast when the Derkling is in the air. This means that they can cast abilities while being in a helium bubble.

$$ 0.25.10 2020-08-03T08:56:13Z
Save/Load/Reset brains

$$ 0.25.9 2020-08-03T07:52:09Z
Manual gold bonus
If you see a behaviour you'd like to reward a bit extra, you can now do that with the "manual gold bonus" button! The reward can be configured in "Misc bounties".

$$ 0.25.8 2020-08-02T08:31:59Z
Bugfix: Use correct bounties in scheduled training

$$ 0.25.7 2020-08-01T07:57:53Z
Stack items

$$ 0.25.6 2020-07-31T10:46:08Z
End battle when all units are dead

$$ 0.25.5 2020-07-31T09:07:26Z
Fix repeating impact effect on statue bug

$$ 0.25.4 2020-07-30T19:33:25Z
Better bounty
- Thank you everone who's contributing suggestions, ideas and bug reports! This first patch since the launch is an implementation for the current top suggestion: "Bounty sets".
- In this patch the bounty system has been rework to be both simpler and more flexible. Instead of assigning bounties to things, you now configure bounties for each of your trainee Derklings. This opens up for lots of fun things to explore, for instance you can configure one of them to focus on healing a specific teammate, or create defensive Derklings that prefer to stay at home.
- You can now have multiple training configurations, and they each have their own set of bounties associated with them.
- And finally, you can now schedule training of these configurations to make it even easier to train your Derklings exactly as you want them!

$$ 0.25.3 2020-07-09T08:46:44Z
Time scaling
It's now possible to discount gold earned later in the battle, to encourage them to be more active early on.

$$ 0.25.2 2020-07-06T19:48:44Z

- New trombone item that forces all enemies to focus on the trombone player.
- Don't give gold for over-healing

$$ 0.25.1 2020-07-06T10:09:17Z

- Various performance optimizations
- Trying out argmaxing decisions instead of cdf sampling
- (Somewhat) random starting positions
- New "auto" camera in training
- Hide UI button
- Free camera in replays + camera animation

$$ 0.25.0 2020-06-24T16:54:04Z
Gold!
- The big change in this version is that the reward function now can be tweaked in detail using "bounty" for different objectives. This should enable more detailed control over training.
- The Derkligs doesn't "see" themselves in Senses and Decisions now.
- Units that would have been and "empty space" in Senses and Decisions are now replaced with the friendly or enemy statue.
- Both of these tweaks should help moving between different numbers of units.

$$ 0.24.4 2020-06-20T18:51:27Z
New decision visualization!
Available when "advanced training" is enabled under user settings.

$$ 0.23.3 2020-06-20T18:30:40Z
Fix bug that reversed the battle results

$$ 0.23.2 2020-06-18T13:42:29Z
Train both sides simultaneously
It's now possible to train both "Trainees" and "Opponents" at the same time!

$$ 0.23.1 2020-06-17T09:57:28Z
Replays
It's now possible to publish a replay of a battle, and to view other players replays!

$$ 0.23.0 2020-06-13T10:13:15Z

- Replace Mana with Cooldowns
- Reduce Vampire gland damage
- Increase cooldowns for all guns
- Fix battle score in notifications
- Tweak dummies drop rate

$$ 0.22.0 2020-06-11T13:28:43Z
Cast slot and focus outputs from the brain are now CDF sampled

$$ 0.21.0 2020-06-09T09:48:25Z

- We have a name for the creatures: Derklings!
- Complete rework of how Derklings percieve other units; they now "see" all other units, and they can choose to focus on any of them. This enables much better team coordination, as well as making it easier for indiviuals to strategize around targets.
- Training opponents are now spawned left to right (same as trainees and battle team).
- When "Advanced training" is enabled (can be enabled from the user settings in the top right corner) you now also have access to a senses and decisions visualization.
- Reset season since the new brains are quite different.

$$ 0.20.9 2020-06-03T12:27:31Z

- Tweak curiosity and breeding
- Change "precipice" senses to "height" senses; this makes it possible for the creatures to sense a wall in front of them, as well as a precipice.

$$ 0.20.8 2020-06-02T13:01:02Z

- Remove creature lives/hearts
- Solo/duo/team battlegrounds
- Reset season

$$ 0.20.7 2020-06-01T09:21:35Z

- Turtle with a gun dummy unit
- Back precipice sensor
- Min range for ranged items
- Slightly lower rotation speed for crabs
- Fix frog legs
- Statues; stationary team objects each worth 13 points (as much as killing all units in a team)
- Curiosity: The dino's will now try to explore things they haven't experienced before, rather than repeating themselves
- "All arenas" view in training
- Map updated
- Training graphs based on elitism pick rather than all arenas
- Improve attack/defense dropdown moved into "Advanced training settings", which can be enabled from the user settings
- Training for fixed number of rounds removed
- Positional sense
- Sort inventory button
- Items can now be deleted
- Fix score in battle notifications

$$ 0.20.6  2020-05-26T11:59:57Z

- Show drop targets
- Fix main menu flickering

$$ 0.20.5 2020-05-22T23:26:50Z
Make crabs not jump off cliffs

$$ 0.20.4 2020-05-22T19:31:04Z
Better selection algo based on cumulative hitpoints

$$ 0.20.3 2020-05-22T15:26:00Z

- Change Paralyzing dart mana cost to 60 (from 30)
- Improve sound effects
- Ducks roam until hit now
- Drop tables tweaked

$$ 0.20.2 2020-05-13T15:42:50Z

- Disable revive item for now
- Show disabled items as rubble
- Training graphs
- Turbo mode
- Optimize performance

$$ 0.20.1 2020-05-13T11:19:50Z
User sound settings

$$ 0.20.0 2020-05-12T09:40:33Z
Re-release of new alpha
