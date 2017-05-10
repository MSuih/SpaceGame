DELETE FROM NextSituation;
DELETE FROM OwnedItems;
DELETE FROM Command;
DELETE FROM Item;
DELETE FROM Player;
DELETE FROM Situation;
DELETE FROM SystemsForType;
DELETE FROM System;
DELETE FROM SystemType;
DELETE FROM WeaponsForShip;
DELETE FROM WeaponsForType;
DELETE FROM Weapon;
DELETE FROM Ship;
DELETE FROM ShipType;
ALTER TABLE Player AUTO_INCREMENT = 1;

INSERT INTO ShipType (id, maxHealth) VALUES
	-- Ship type 1 is reserved for player's ship
	(1, 200);
	
INSERT INTO Situation (id, description) VALUES 
	-- Situation 1 is reserved for the situation the game starts in
	(1, "\"Welcome to the crew, soldier. You completed your basic training with excelent grades, so I'm hoping you continue your good work in our ranks as well. Come see me on the bridge once you're ready.\" \n\nThe captain leaves you alone as he marches through the door into the HALLWAY. Perhaps you should follow him as well."),
	(2, "The hallway is empty and quite narrow. The floor is covered with grating - you can see all sorts of cables and pipes underneath it. \n\nThe hallway has many red-colored doors leading to different parts of the ship. Some of them interes you: the doorway to ARMORY with a keycard reader next to it, scent of food is coming from DINING HALL and the doorway to BRIDGE is the largest one out of them all."),
	(3, "Upon entering the bridge the first thing that you see are the large monitors that cover most of the wall space. The biggest one in the middle almost covers the front wall and displays a view from the front of the ship. The smaller ones surronding it display view from internal cameras in addition to all sorts of statistic and metrics.\n\nMost of the seats are empty, but there are still handful of people working on the consoles scattered around the room. In the middle is the CAPTAIN, who is reading some sort of report from his handheld display. The large door at the back of the room lead to HALLWAY."),
	(4, "\"Captain, sir!\" you announce yourself to the captain. He glances at you and puts the report down. \"Please take a seat, private\"\n\nIn 15 minutes the captain has explained the purpose of this mission and your role in it as a combat systems expert. There was quite a lot to learn, but you're confident that you'll soak it in while operating here. \"Head to the armory for your weapons and then speak with Sabrina over there\", he points at the brunette girl sitting in front of one of the consoles. \"She'll show you to your desk and instruct you on how it operates. If you do not have any other questions you may leave\""),
	(5, "The bridge seems even quieter now than when you first entered. It does make sense, however: the ship will travel fine on it's own. The only thing the crew needs to worry about is monitoring vitals and alerting others if something unexpected happens.\n\nThe captains chair is empty right now. SABRINA is currently checking the status of various systems that keep the ship operational. The large door at the back of the room leads to HALLWAY.");
	
INSERT INTO Item (id, name, visible) VALUES 
	(1, "Head to armory token", 0),
	(2, "Pistol", 1),
	(3, "Bridge introduction token", 0);
	
INSERT INTO Command (id, command) VALUES
	(1, "GOTO"),
	(2, "TALK"),
	(3, "LEAVE");
	
INSERT INTO nextSituation
	(fromSituation, command, target, toSituation, description, requires, requiredAmount, removeItem, rewards, rewardedAmount)
VALUES 
	(1, 1, "hallway", 2, null, null, 0, 0, null, 0),
	(2, 1, "armory", 2, "You look at the doorway to armory. The thick steel door would take a lot of muscle to force open even if you had a crowbar. There is a keycard reader on the wall next to it, but you do not have a card that would fit into it. You could press the button next to it and talk your way in, but that doesnt seem like a great idea either. You decide to turn around and leave the door alone for now.", null, 0, 0, null, 0),
	(2, 1, "bridge", 3, null, null, 0, 0, null, 0),
	(3, 1, "hallway", 2, null, null, 0, 0, null, 0),
	(3, 2, "captain", 4, null, null, 0, 0, 1, 1), 
	(4, 3, "conversation", 5, null, null, 0, 0, 3, 1),
	(2, 1, "bridge", 5, null, 3, 1, 0, null, 0),
	(5, 1, "hallway", 2, null, null, 0, 0, null, 0),
	(5, 2, "sabrina", 5, "\"So you're the new guy. Hello, I'm Sabrina\" the girl responds and you shake hands. \"I'd love to chat, but I'm quite busy right now. And if I heard correctly you were supposed to head into the armory too. Come back once you've picked your weapon and I should be done with this too.\"", 1, 1, 0, null, 0);