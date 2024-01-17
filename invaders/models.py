"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# YOUR NAME(S) AND NETID(S) HERE: Jonathan Wang (jyw38) and Derek Wang (dkw48)
# DATE COMPLETED HERE: 12/11/2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    # need
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,x=GAME_WIDTH/2,y=SHIP_BOTTOM + 1/2*SHIP_HEIGHT, \
    source=SHIP_IMAGE):
        """Initilizes a ship at the specified coordinates, dimensions, and
        source image

        Parameters: x which specifies where x coordinate of the center of
        the ship is; the default value is the center

        Precondition: x is an int or a float  between 1/2 SHIP WIDTH
        AND GAME_WIDTH - 1/2 SHIP WIDTH


        Parameter: y specifics the y coordinate of the center of theship ;
        this should never changed during the game. Default value is given by
        SHIP_BOTTOM

        Precondition: y a an int or float  1/2 SHIP_HEIGHT and
        DEFENSE_LINE - 1/2 SHIP_HEIGHT

        Parameter: an image to be used to represent the Ship image
        Precondition: source is a GImage object
        """
        super().__init__(x=x, y=y, width=SHIP_WIDTH, height=SHIP_HEIGHT, \
        source=source)
        assert (x >= 1/2 * SHIP_WIDTH) and (x <= GAME_WIDTH - 1/2 *SHIP_HEIGHT)
        assert (y >= 1/2 * SHIP_HEIGHT) and \
        (y <= DEFENSE_LINE - 1/2 *SHIP_HEIGHT)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def shipCollides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)
        if self.contains((bolt.left, bolt.top)) or \
        self.contains((bolt.right, bolt.top)) or \
        self.contains((bolt.left, bolt.bottom)) or \
        self.contains((bolt.right, bolt.bottom)):
            if bolt.isPlayerBolt() == False:
                return True
            else:
                return False


    def moveShip(self,input):
        """
        Changes the x value of the Ship so that it moves left and right

        Precondition: input is a GInput Object
        """
        da = 0
        if input.is_key_down('left'):
            da = da - SHIP_MOVEMENT
        if input.is_key_down('right'):
            da = da + SHIP_MOVEMENT
        current = self.x + da
        current = max(current, SHIP_WIDTH/2)
        current = min(current, GAME_WIDTH - SHIP_WIDTH/2)
        self.x = current
    # COROUTINE METHOD TO ANIMATE THE SHIP

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    # HIDDEN ATTRIBUTES
    # Attribute: _x gets the x specification (MUTABLE)
    # Invariant: _x has to be a valid integer

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)


    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,x,y,source):
        """
        Initializes creation of the Alien Object

        Parameters: x is the x coordinate of the center of the Alien
        Precondition: x is a float or int within the gameboard

        Parameters: y is the y coordinate of the center of the Alein
        Precondition: y is a float or int within the gameboard

        Parameters: source is a GInput
        Precondition: source is a GInput Object

        Parameter: width is the number of pixels the ship is wide
        Precondition: width is a positive integer

        """
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT, \
        source=source)


    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def alienCollides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt, Bolt)
        if self.contains((bolt.left, bolt.top)) or \
        self.contains((bolt.right, bolt.top)) or \
        self.contains((bolt.left, bolt.bottom)) or \
        self.contains((bolt.right, bolt.bottom)):
            if bolt.isPlayerBolt() == True:
                return True
            else:
                return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute: _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # Attribute: _isPLayerBolt: whether a bolt is shot from the player
    # Invariant: _isPLayerBolt is a boolean

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    def setVelocity(self, BOLT_SPEED):
        """
        Sets the velocity to BOLT_SPEED this is in reference to the
        global variable. Modifies the speed to include magnitude

        Precondtion: BOLT_SPEED is a positive int
        """
        assert isinstance(BOLT_SPEED, int)
        assert BOLT_SPEED > 0
        if self._isPlayerBolt == True:
            self._velocity = BOLT_SPEED
        else:
            self._velocity = -BOLT_SPEED


    def getVelocity(self):
        """
        Returns the veolocity of the bolt,
        """
        return self._velocity


    def getisPlayerBolt(self):
        """
        Return self._isPlayerBolt which tells whether the player or aliens
        fired it
        """
        return self._isPlayerBolt


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def isPlayerBolt(self):
        """
        Returns a boolean that tells whether a bolt is fired form the player
        """
        return self._isPlayerBolt


    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y = SHIP_BOTTOM + SHIP_HEIGHT + BOLT_HEIGHT/2, \
        fillcolor = RED_COLOR, isPlayerBolt = True, velocity = BOLT_SPEED, \
        width = BOLT_WIDTH, height = BOLT_HEIGHT):
        """
        Initiilizes creation of Bolt Object

        Parameters: x is the x coordinate of center of the bolt
        Precondition: x is an int float

        Parameters: y is the y coordinate of the center of the Bolt
        Precondition: y is an int or a float (DEFAULT IS SHIP_BOTTOM +
        SHIP_HEIGHT + BOLT_HEIGHT/2)

        Parameter: fillcolor is the color of the bolt
        Precondition: fillcolor is an RGB Object (DEFAULT IS RED_COLOR)

        Parameter: isPlayerBolt is a Boolean that tells whether something is
        fired from the plyer
        Precondition: isPlayerBolt is a Boolean (DEFAULT IS TRUE)

        Parameter velocity is a mutable attribute that controls how fast the
        aliens shoot
        Precondition: BOLT_SPEED is an int (DEFAULT BOLT_SPEED)

        Parmeter: width is the number of pixels that the Bolt is wide
        Precondition: width is a positive integer (DEFAULT BOLT_WIDTH)

        Parameter: height is the number of pixels the Bolt is tall
        Precondition: height is a positive integer (DEFAULT BOLT_HEIGHT)
        """
        assert isinstance(isPlayerBolt, bool)
        assert isinstance(BOLT_SPEED, int) or isinstance(BOLT_SPEED)
        #isPlayerBolt allows us to limit fire rate of player and also important
        # for collision detection
        self._isPlayerBolt = isPlayerBolt
        #can determin how fast bolts go along with direction
        self.setVelocity( BOLT_SPEED)
        if isPlayerBolt:
            fillcolor = BLUE_COLOR
        super().__init__(x = x, y = y, width = BOLT_WIDTH, \
        height = BOLT_HEIGHT, fillcolor = fillcolor, linecolor = DARK_GREY)
        self._isPlayerBolt = isPlayerBolt


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
