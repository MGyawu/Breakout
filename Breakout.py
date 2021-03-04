#Team Members: Mead Gyawu and Ethan Gavin
#CS101 
import turtle  # Using Turtle and Screen classes
import random  # Using randint

class Ball:
    """
    A class representing a ball on the screen
    
    Attributes
    ----------
    turtle : Turtle 
        A Turtle type object from the module turtle
    x : float
        The x coordinate of the ball
    y : float
        The y coordinate of the ball
    radius : float
        The radius of the ball
    velocity : list
        The x and y components of the velocity of the ball
    color : string
        The color of the ball
    
    Methods
    -------
    update()
        Update the ball location and exploding status each time it is called
    collide(other)
        Check for collision with another ball
    swap_velocity(other)
        Bounce this ball off another ball
    draw()
        Draw the ball on the screen
    """
    
    def __init__(self, t, x , y , radius, vx, vy, color):
        """
        Parameters
        ----------
        t : turtle
            A turtle type object from the module turtle
        radius : float
            The radius of the ball
        x : float
            The x coordinate of the ball
        y : float
            The y coordinate of the ball
        vx : float
            The x component of the ball velocity
        vy : float
            The y component of the ball velocity
        velocity : list
            The x and y components of the velocity of the ball
        color : string
            The color of the ball
        """
        # Store the parameters in the new object atributes
        self.turtle = t
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity = [vx, vy]
        self.color = color
        
        
    def update(self, paddle,bricks):
        """
        Update the ball status:
        - Check if the ball should bounce off the window edges
        - Update position using the velocity
        """
        # Acquire the screen instance from the turtle
        screen = turtle.Screen()
        
        # Store current screen properties
        width = screen.window_width() 
        height = screen.window_height()
        
        bounceDir = self.collide_with_rect(paddle)
#         bounceDir2 = []
#         for i in bricks:
#             if i.visible == True:
#                 bounceDir2.append(self.collide_with_rect(i))
        
        # Check for boundaries
        if (self.x - self.radius <= -width//2) or (self.x + self.radius >= width//2):
            self.velocity[0] *= -1
        if (self.y + self.radius >= height//2): #(self.y - self.radius <= -height//2) or (self.y + self.radius >= height//2):
            self.velocity[1] *= -1
        
        if len(bounceDir) > 0:
            for i in bounceDir:
                print(i)
                if i == 't' or i == 'b':
                    self.velocity[1] *= -1
                if i == 'l' or i == 'r':
                    self.velocity[0] *= -1
        for i in bricks:
            if i.visible:
                 bounceDir2 = self.collide_with_rect(i)
                 for j in bounceDir2:
                     print(j)
                     if j == 't' or j == 'b':
                         self.velocity[1] *= -1
                     if j == 'l' or j == 'r':
                         self.velocity[0] *= -1
                     i.visible = False
#         if len(bounceDir2) > 0:
#             for i in range(len(bounceDir2)):
#                 for j in range(len(bounceDir2[i])):
#                     print(bounceDir2[i][j])
#                     if bounceDir2[i][j] == 't' or bounceDir2[i][j] == 'b':
#                         self.velocity[1] *= -1
#                         #bricks[i].visible = False
#                     if bounceDir2[i][j] == 'l' or bounceDir2[i][j] == 'r':
#                         self.velocity[0] *= -1
#                         #bricks[i].visible = False
#                     bricks[i].visible = False
                    
                
        
        # Update position with velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        
    def collide(self, other):
        """
        Check if this ball is colliding with another ball
        
        Parameters
        ----------
        other : ball
            Another ball to be checked for collision
        """
        
        # Evaluate the difference in coordinates between this and other
        dx = self.x - other.x
        dy = self.y - other.y
        
        # Check if the balls collided
        return (self.radius + other.radius) * (self.radius + other.radius) >= (dx * dx + dy * dy)
    
    def collide_with_rect(self, rect):
        '''
        This function will be used to test for collisions between the ball and a rectangular object (e.g., the paddle or a brick). It will return a list of strings that tells us which surface(s) (if any) the ball should bounce of off. The possible values are 't' (top), 'b' (bottom), 'r' (right), and 'l' (left). This will return a list in case the ball bounces off two faces at once (i.e., it hit a corner).
        '''
        sides = []
        OldY = self.y - self.velocity[1]
        OldX = self.x - self.velocity[0]
        if (self.x + self.radius) > (rect.x) and (self.x - self.radius) < (rect.x + rect.width):
            if OldY > rect.y >= self.y:
                sides.append('t')
            elif OldY <= rect.y - rect.height < self.y:
                sides.append('b')
        if(self.y + self.radius) > (rect.y - rect.height) and (self.y - self.radius) < rect.y:
            if OldX  > rect.x + rect.width >= self.x:
                sides.append('r')
            elif OldX <= rect.x < self.x:
                sides.append('l')
        return sides
    
    def swap_velocity(self, other):
        """
        Bounce this ball off another ball
        
        Parameters
        ----------
        other : ball
            Another ball to bounce off
        """
        # Swap the velocities to simulate bouncing
        old_velocity = self.velocity
        self.velocity = other.velocity
        other.velocity = old_velocity
        
        
    def draw(self):
        """
        Draw the ball on the screen
        """
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.dot(self.radius * 2, self.color)
        
        

class Scene:
    """
    A class implementing the multiple ball scene
    
    Attributes
    ----------
    screen : Screen
        A Screen type object from the module turtle
    turtle : Turtle
        A Turtle type object from the module turtle
        
    
    Methods
    -------
    initialize_objs()
        Create the gamefield by adding the balls
    run()
        Determines the game dynamic frame by frame (one frame for each call)
    done()
        Exit the program
    """
    def __init__(self):
        # Create a screen object (singleton) and set it up
        self.screen = turtle.Screen()
        self.screen.setup(0.5, 0.5)  # Use half with and half height of your current screen
        self.screen.tracer(False)
        self.screen.colormode(255)
        
        # Create an invisible turtle object
        self.turtle = turtle.Turtle(visible=False)
        
        # Initialize the scene
        self.initialize_objs()
        
        self.paddle = Paddle(self.turtle,80,20,'black')
    
        # Defines users' interactions we should listen for
        self.screen.onkey(self.done, 'q')  # Check if user pushed 'q'
        
        # As soon as the event loop is running, set up to call the self.run() method
        self.screen.ontimer(self.run, 0)
    
        # Tell the turtle screen to listen to the users' interactions
        self.screen.listen()
        
        # Start the event loop
        self.screen.mainloop()
        
    def initialize_objs(self):
        """
        Initializes the scene
        """
        # Defines the size of the game field       
        width = self.screen.window_width() - 20
        height = self.screen.window_height() - 20
        self.ball = Ball(self.turtle,
                         0,
                         0,
                         10,
                         -random.randint(0,3),  #random.randint(-1, 1),
                         -random.randint(0,3),  #random.randint(-1, 1),
                         (random.randint(0, 255),
                          random.randint(0, 255),
                          random.randint(0, 255)))
        while self.ball.velocity[0]== 0:
            self.ball.velocity[0] = -random.randint(0,3)
        while self.ball.velocity[1] == 0:
            self.ball.velocity[1] = -random.randint(0,3)
        self.bricks = []
        Edge = -(width/2)
        brickLength = width/10
        while Edge < (width/2):
            self.bricks.append(Brick(self.turtle,Edge,height//2 - 50, brickLength,50,(255,0,0)))
            Edge+=brickLength
        Edge = -(width/2)
        while Edge < (width/2):
            self.bricks.append(Brick(self.turtle,Edge,height//2 - 100, brickLength,50,(255,0,0)))
            Edge+=brickLength
        Edge = -(width/2)
        while Edge < (width/2):
            self.bricks.append(Brick(self.turtle,Edge,height//2 - 150, brickLength,50,(255,0,0)))
            Edge+=brickLength
        
    def run(self):
        """
        Determines the game dynamic frame by frame (one frame for each call)
        """
        # Clear the screen
        self.turtle.clear()
        height = self.screen.window_height() - 20

        
        for i in self.bricks:
            i.draw()
        
        self.paddle.update()
        self.paddle.draw()
        
        self.ball.update(self.paddle,self.bricks)
        self.ball.draw()
            
        # Update the overall screen
        self.screen.update()
        
        # Call the self.run() method
        if  self.ball.y >= -height//2 - self.ball.radius:
            self.screen.ontimer(self.run, 0)
        
    def done(self):
        """
        Exit the program
        """
        self.screen.bye()

class Paddle:
    def __init__(self,t,width,height,color):
        '''
        initializes the paddle with its initial position, dimensions, and color
        '''
        self.turtle = t
        self.width = width
        self.height = height
        self.color = color
        self.y = -200
        self.x = 0
    
    def draw(self):
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)
        self.turtle.pendown()
        self.turtle.begin_fill()
        self.turtle.fillcolor(self.color)
        for i in range (2):
            self.turtle.forward(self.width)
            self.turtle.right(90)
            self.turtle.forward(self.height)
            self.turtle.right(90)
        self.turtle.end_fill()
            
    def update(self):
        self.x = turtle.getcanvas().winfo_pointerx() - 2*turtle.getcanvas().winfo_rootx() - self.width/2
        
class Brick:
    def __init__(self, t, x, y, width, height, color):
        self.turtle = t
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.visible = True
        
    def draw(self):
        if self.visible == True:
            self.turtle.penup()
            self.turtle.goto(self.x, self.y)
            self.turtle.pendown()
            self.turtle.begin_fill()
            self.turtle.fillcolor(self.color)
            for i in range (2):
                self.turtle.forward(self.width)
                self.turtle.right(90)
                self.turtle.forward(self.height)
                self.turtle.right(90)
            self.turtle.end_fill()
        
# Draw the scene
scene = Scene()


