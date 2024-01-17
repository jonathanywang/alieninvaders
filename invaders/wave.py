"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Jonathan Wang (jyw38) and Derek Wang (dkw48)
# 12/11/2023
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien
    # objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _direction: determines the direction of aliens as they move
    # Invariant: _direction is either 1 or -1
    #
    # Attribute _fireWhen: the random amount of steps required for alien to
    # shoot a bolt
    # Invariant: _fireWhen is a random integer between 1 and BOLT_RATE
    #
    # Attribute _steps: the steps an alien takes up until it shoots a bolt
    # Invariant: _steps is an integer
    #
    # Attribute _playerBoltPresent: determines whether or not a bolt shot from
    # the player is present in the list of bolts and/or on the screen
    # Invariant: _playerBoltPresent is a boolean value
    #
    # Attribute _edge: determines whether or not an alien has reached close
    # enough to the edge to move down and in the opposite direction
    # Invariant: _edge is a boolean value
    #
    # Attribute _coordinates: the coordinates of the ship right before it is
    # destroyed by a bolt and is used to resume game
    # Invariant: _coordinates is a size two tuple of ints or floats
    #
    # Parameters:_paused  creates a GLabel that shows that the game will
    # not continue
    # and prevents update wave
    # Invariant: _pause is a GLabel;
    #
    # Parameters:_lose creates a GLabel that shows that the player has lost
    # the game
    # Invariant: _lose is a Glabel
    #
    # Parameters:_win creates a Glable that shows that the player has won the
    # game
    # Invariant: _win is a GLabel
    #
    #Parameters:_winner is a boolean that signifies who has won the game
    # Invarinat: _winner is a boolean
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def resetFireWhen(self):
        """
        Resets the steps it takes for when an alien fires.

        Sets the steps back to zero and then sets the hidden attribute
        _fireWhen (the amount of steps needed to fire) to a random int
        between 1 and BOLT_RATE.
        """
        self._steps = 0
        self._fireWhen = random.randint(1, BOLT_RATE)


    def getLives(self):
        """
        Getter for returning the amount of lives remaining.
        """
        return self._lives


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes all the hidden attributes within Wave and creates a ship
        and alien object. These attributes include the bolts, line, and many
        of the visual aspects on the game board.
        """
        self.appendAlien()
        self._ship = Ship()
        self._dline = GPath(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
        linewidth = 2, linecolor = DARK_GREY)
        self._time = 0
        self._direction = 1
        self._bolts = []
        self._fireWhen = random.randint(1, BOLT_RATE)
        self._steps = 0
        self._playerBoltPresent = False
        self._edge = False
        self._lives = 3
        self.coordinates = (0,0)
        self._paused = GLabel(text="Press 'S' to Continue", \
        font_name = ARCADE_FONT, font_size = ARCADE_LARGE, \
        linecolor = 'blue', x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        self._lose = GLabel(text="YOU'VE LOST! :(", font_name = ARCADE_FONT, \
        font_size = ARCADE_LARGE, linecolor = 'blue', x = GAME_WIDTH/2, \
        y = GAME_HEIGHT/2)
        self._win = GLabel(text="WOO, YOU'VE WON! :D", \
        font_name = ARCADE_FONT, font_size = ARCADE_LARGE, \
        linecolor = 'blue', x = GAME_WIDTH/2, y = GAME_HEIGHT/2)
        self._winner = False


# UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def updateWave(self, input, dt):
        """
        Update method for Wave class. Updates the ship for at every frame
        and moves the ship, aliens, and laser bolts on the screen.

        Parameter input: takes the input attribute from Invaders to use.
        Precondition: input is an instance of GInput

        Parameter dt: the time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(input, GInput)
        assert isinstance(dt, int) or isinstance(dt, float)
        self.updateShip(input)
        self.updateAlien(dt)
        self.updateBolt(input)
        if self.getWin() == True:
            self._winner = True


    def updateShip(self, input):
        """
        Update method for Ship. Allows for the movement of the ship across
        the x axis.

        Parameter input: takes the input attribute from Invaders to use.
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput)
        if self._ship != None:
            self._ship.moveShip(input)


    def updateAlien(self,dt):
        """
        Update method for Alien. Updates when and which Aliens shoot bolts
        and detects movement, particularly direction.

        Parameter dt: the time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float)
        if self.alienTimer(dt):
            self.whenAlienShoot()
            self.whichAlienShoot()
            self.detectEdge()
            if self._edge == True:
                self._direction = - self._direction
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        if self._edge == True:
                            self.moveAlienDown(alien)
                        self.moveAlienHorizontal(alien)
            self._edge = False


    def alienTimer(self,dt):
        """
        Sets time when alien will shoot. Increments so that it returns True
        whenever the specified time has been reached.

        Parameter dt: the time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt, int) or isinstance(dt, float)
        self._time += dt
        if self._time >= ALIEN_SPEED:
            self._time = 0
            self._steps += 1
            return True
        else:
            return False


    def moveAlienHorizontal(self,alien):
        """
        Moves Alien in the horizontal direction. Moves alien across the x axis
        and shoots whenever alien walks (depending on which and when)

        Parameter alien: the alien object selected from the list of aliens:
        _aliens.
        Precondition: alien is an instance of Alien
        """
        assert isinstance(alien, Alien)
        alien.x += ALIEN_H_WALK * self._direction
        self.whenAlienShoot()


    def moveAlienDown(self,alien):
        """
        Moves Alien in the vertical direction. Moves alien across the y axis.

        Parameter alien: the alien object selected from the list of aliens:
        _aliens.
        Precondition: alien is an instance of Alien
        """
        assert isinstance(alien, Alien)
        alien.y -= ALIEN_V_WALK


    def detectEdge(self):
        """
        Detects the edge of the game screen and turns _edge attribute to True
        when alien is within ALIEN_H_SEP from the very edge of the screen. This
        is used to signal the aliens to move down and away from the edge.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if (alien.x >= GAME_WIDTH-ALIEN_H_SEP-ALIEN_WIDTH) \
                    or (alien.x <= ALIEN_H_SEP+ALIEN_WIDTH):
                        self._edge = True


    def whenAlienShoot(self):
        """
        Determines when alien shoots. If shooter is a living alien, it will
        fire a bolt.
        """
        if self._steps == self._fireWhen:
            shooter = self.whichAlienShoot()
            if shooter != None:
                self.newAlienBolts(shooter.x, shooter.y)
                self.resetFireWhen()


    def whichAlienShoot(self):
        """
        Determines which alien shoots. It gets the bottom most alien that is
        still alive and chooses them to be the ones shooting the bolts.
        """
        bottom = []
        for i in range(ALIENS_IN_ROW):
            bottom.append(None)
        for row in self._aliens:
            for i in range(len(row)):
                if row[i] != None:
                    if bottom[i] == None:
                        bottom[i] = row[i]
                    elif row[i].x < bottom[i].x:
                        bottom[i] = row[i]
        while None in bottom:
            bottom.remove(None)
        if bottom != []:
            index = random.randrange(0, len(bottom))
            return bottom[index]
        else:
            return None


    def updateBolt(self,input):
        """
        Update method for the Bolts. It controls the movements and collisions
        of the bolts.

        Parameter input: takes the input attribute from Invaders to use.
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput)
        if self._ship != None:
            self.newShipBolts(input)
        for bolt in self._bolts:
            self.moveBolts(bolt)
            self.collides(bolt)


    def moveBolts(self, bolt):
        """
        Move method for bolts. Ensures that bolts are removed once they go off
        the screen and removes them from the list of bolts.

        Parameter bolt: the bolt object chosen from the list of bolts
        Precondition: bolt is an instance of Bolt
        """
        assert isinstance(bolt, Bolt)
        bolt.y += bolt._velocity
        if bolt.y >= GAME_HEIGHT:
            self._bolts.remove(bolt)
            self._playerBoltPresent = False
        if bolt.y <= 0:
            self._bolts.remove(bolt)


    def newShipBolts(self, input):
        """
        Creates a new bolt shot from the Ship object through pressing the
        spacebar. It appends that bolt to the bolt list as well.

        Parameter input: takes the input attribute from Invaders to use.
        Precondition: input is an instance of GInput
        """
        assert isinstance(input, GInput)
        if input.is_key_pressed('spacebar') and self._playerBoltPresent == False:
            newBolt = Bolt(self._ship.x, isPlayerBolt = True)
            self._bolts.append(newBolt)
            self._playerBoltPresent = True


    def newAlienBolts(self, x, y):
        """
        Creates new bolts shot from the Alien objects automatically. It also
        appends these bolts to the bolt list as well.

        Parameter x: the x coordinate of the center of the alien bolt
        Precondiiton: x is an int or float

        Parameter y: the y coordinate of the center of the alien bolt
        Precondition: y is an int or float
        """
        assert isinstance(x, int) or isinstance(x, float)
        assert isinstance(y, int) or isinstance(y, float)
        alienBolt = Bolt(x=x, y=y - 1/2*ALIEN_HEIGHT - 1/2 * BOLT_HEIGHT, \
        isPlayerBolt = False)
        self._bolts.append(alienBolt)


    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def drawWave(self, state, view):
        """
        Draw Wave method for creating all the visuals during the wave,
        including the aliens, the ship, and the defensive line. It also
        draws out the text for when the game is paused and when the game is
        completed.

        Parameter state: the current state of the game
        Precondition: one of the following states: STATE_INACTIVE,
        STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED. STATE_CONTINUE,
        and STATE_COMPLETE

        Parameter view: the game view used in drawing from Invaders
        Precondition: view is an instance of GView
        """
        assert isinstance(view, GView)
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            bolt.draw(view)
        if state == STATE_PAUSED:
            self._paused.draw(view)
        if state == STATE_COMPLETE and self._winner == False:
            self._lose.draw(view)
        if state == STATE_COMPLETE and self._winner == True:
            self._win.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION
    def appendAlien(self):
        """
        Method for appending Aliens into the list _aliens. Row and columns
        are dependent on given constants. Distances between each alien and
        distances from the edge of the game screen are given.
        """
        self._aliens = []
        currenty =  \
        GAME_HEIGHT - ALIEN_CEILING - (ALIEN_ROWS - 0.5) * ALIEN_HEIGHT \
        - ALIEN_V_SEP * (ALIEN_ROWS - 1)
        sourceIndex = 0
        for r in range(ALIEN_ROWS):
            self._aliens.append([])
            currentx = ALIEN_H_SEP + 1/2 * ALIEN_WIDTH
            for a in range(ALIENS_IN_ROW):
                currentx = currentx + (ALIEN_H_SEP + ALIEN_WIDTH)
                self._aliens[r].append(Alien(currentx, currenty, \
                ALIEN_IMAGES[sourceIndex]))
            currenty = currenty + (ALIEN_V_SEP + ALIEN_HEIGHT)
            if r % 2 == 1:
                sourceIndex = sourceIndex + 1
                if sourceIndex == len(ALIEN_IMAGES):
                    sourceIndex = 0


    def collides(self, bolt):
        """
        Detects if a bolt collides with either the ship or an alien. In the
        case that it does, it will remove that bolt and the ship/alien.

        Parameter bolt: the bolt object chosen from the list of bolts
        Precondition: bolt is an instance of Bolt
        """
        assert isinstance(bolt, Bolt)
        for row in self._aliens:
            for i in range(len(row)):
                if isinstance(row[i], Alien) and self._ship != None:
                    if row[i].alienCollides(bolt):
                        row[i] = None
                        self._bolts.remove(bolt)
                        self._playerBoltPresent = False
                    if self._ship.shipCollides(bolt):
                        self._coordinates = (self._ship.x, self._ship.y)
                        self._ship = None
                        self._bolts.remove(bolt)
                        self._playerBoltPresent = False
                        self._lives -= 1


    def manageLives(self):
        """
        Gets whether or not the ship is None. Determines if player loses life.
        """
        if self._ship == None:
            return True


    def redrawShip(self):
        """
        Method for redrawing ship after ship is hit by bolt and lives > 0.
        """
        self._ship = Ship(x = self._coordinates[0], y = self._coordinates[1])


    def getDip(self):
        """
        Returns True if any alien goes below the defensive line.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None and (alien.y - ALIEN_HEIGHT/2) < DEFENSE_LINE:
                    return True


    def getWin(self):
        """
        Returns True if each alien in the list _aliens is None. Otherwise,
        returns False.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    return False
        return True
