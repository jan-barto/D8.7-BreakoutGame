import random
from turtle import Turtle, Screen
import time


class BreakoutGame:
    # --- SECTION INIT ---
    # --- SECTION FRAME AND TEXT ---
    # --- SECTION PADDLE ---
    # --- SECTION BALL ---
    # --- SECTION BRICKS ---
    # --- SECTION GAME ITSELF ---

    def __init__(self):
        self.screen = Screen()
        self.screen.setup(1100, 600)
        self.screen.bgcolor("black")
        self.screen.title("The Breakout Game")
        self.drawing_t = Turtle()
        self.paddle = Turtle()

        self.brick = None
        self.bricks = None
        self.ball = None
        self.moves_options = None

        self.speed = 0.005
        self.limits_x = 530
        self.limits_y = 280
        self.score = 0
        self.lives = 3

        self.screen.listen()
        self.screen.onkeypress(lambda: self.paddle_move("to_the_left"), "Left")
        self.screen.onkeypress(lambda: self.paddle_move("to_the_right"), "Right")

        self.screen.tracer(0)
        self.draw_frame_with_score_and_lives()
        self.paddle_setting()
        self.bricks_setting()
        self.ball_setting()

        self.game()

    # --- SECTION FRAME AND TEXT ---
    def draw_frame_with_score_and_lives(self):
        self.drawing_t.clear()
        self.drawing_t.color("white")
        self.drawing_t.hideturtle()
        self.drawing_t.penup()
        self.drawing_t.goto(self.limits_x, self.limits_y)
        self.drawing_t.pendown()
        for _ in range(2):
            self.drawing_t.right(90)
            self.drawing_t.forward(2 * self.limits_y)
            self.drawing_t.right(90)
            self.drawing_t.forward(2 * self.limits_x)
        self.drawing_t.penup()
        self.drawing_t.goto(self.limits_x, self.limits_y)
        self.drawing_t.write(f"Score: {self.score}      Lives: {self.lives}/3", align="right",
                             font=("Verdana", 12, "italic"))

    def draw_game_over(self):
        self.drawing_t.goto(0, -20)
        self.drawing_t.write(f"   Game Over.\nYour score: {self.score}",
                             align="center",
                             font=("Verdana", 40, "bold"))

    def draw_game_won(self):
        self.drawing_t.goto(0, -20)
        self.drawing_t.write(f"!!! You won !!!", align="center", font=("Verdana", 40, "bold"))

    # --- SECTION PADDLE ---
    def paddle_setting(self):
        self.paddle.color("white")
        self.paddle.penup()
        self.paddle.shape("square")
        self.paddle.setheading(90)
        self.paddle.shapesize(5, 0.5)
        self.paddle.goto((0, -250))

    def paddle_move(self, direction):
        new_x = self.paddle.xcor()
        if direction == "to_the_left" and self.paddle.xcor() > -self.limits_x + 60:
            new_x -= 20
        elif direction == "to_the_right" and self.paddle.xcor() < self.limits_x - 60:
            new_x += 20
        y = self.paddle.ycor()
        self.paddle.goto(new_x, y)

    # --- SECTION BALL ---
    def ball_setting(self):
        self.ball = Turtle()
        self.ball.penup()
        self.ball.shape("circle")
        self.ball.color("white")
        self.ball.shapesize(0.8)
        self.ball.goto((0, -220))
        self.ball.x_move = random.choice([-4, 4])
        self.ball.y_move = 6
        self.ball_change_moves_by_bounce()

    def ball_move(self):
        new_x = self.ball.xcor() + self.ball.x_move
        new_y = self.ball.ycor() + self.ball.y_move
        self.ball.goto(new_x, new_y)

    def ball_change_moves_by_bounce(self):
        self.moves_options = [(5, 4), (6, 4), (4, 5), (5, 5)]
        new_move = random.choice(self.moves_options)
        if self.ball.x_move < 0:
            self.ball.x_move = new_move[0] * -1
        else:
            self.ball.x_move = new_move[0]
        if self.ball.y_move < 0:
            self.ball.y_move = new_move[1] * -1
        else:
            self.ball.y_move = new_move[1]

    # --- SECTION BRICKS ---
    def bricks_setting(self):
        x_cors = [pos_x for pos_x in range(-460, +500, 70)]
        y_cors = [pos_y for pos_y in range(150, 250, 20)]
        color_options = ["#59D5E0", "#F5DD61", "#FAA300", "#F4538A", "purple"]
        # print(x_cors)
        # print(y_cors)
        color = 0
        self.bricks = []
        for y_cor in y_cors:
            for x_cor in x_cors:
                self.brick = Turtle()
                self.bricks.append(self.brick)
                self.brick.color(color_options[color])
                self.brick.penup()
                self.brick.shape("square")
                self.brick.setheading(90)
                self.brick.shapesize(3, 0.7)
                self.brick.goto((x_cor, y_cor))
            color += 1

    # --- SECTION GAME ITSELF ---
    def game(self):
        while True:
            self.ball_move()
            time.sleep(self.speed)
            self.screen.update()

            # detect collision with side walls
            if self.ball.xcor() > self.limits_x - 10 or self.ball.xcor() < -self.limits_x + 18:
                self.ball.x_move *= -1

            # detect collision with top wall
            if self.ball.ycor() > self.limits_y - 18:
                self.ball.y_move *= -1

            # detect collision with paddle
            if abs(self.ball.xcor() - self.paddle.xcor()) < 50 and - 250 < self.ball.ycor() < -242:
                self.ball.y_move *= -1

            # detect losing the ball
            if self.ball.ycor() < - self.limits_y - 50:
                self.ball.x_move = random.choice([3, 4, 5]) * random.choice([-1, 1])
                self.ball.y_move = 6
                self.ball.goto((0, -220))
                self.paddle.goto((0, -250))
                self.lives -= 1
                self.draw_frame_with_score_and_lives()
                if self.lives == 0:
                    self.draw_game_over()
                    break

            # detect collision with brick
            for a_brick in self.bricks:
                hit = False
                # bounce in y
                if abs(self.ball.ycor() - a_brick.ycor()) < 4 and abs(self.ball.xcor() - a_brick.xcor()) < 25:
                    hit = True
                    self.ball.y_move *= -1
                    print('y')
                # bounce in x
                elif abs(self.ball.xcor() - a_brick.xcor()) < 30 and abs(self.ball.ycor() - a_brick.ycor()) < 4:
                    hit = True
                    self.ball.x_move *= -1
                    print('x')
                if hit:
                    a_brick.color("black")
                    self.bricks.remove(a_brick)
                    self.ball_change_moves_by_bounce()
                    self.score += 1
                    self.draw_frame_with_score_and_lives()
                    # increasing speed
                    if self.score != 0 and self.score % 5 == 0:
                        self.speed *= 0.4
                        print(f"{self.speed:.20f}")
                    # if someone hits the last brick:
                    if not self.bricks:
                        self.draw_game_won()
                        break


app = BreakoutGame()
app.screen.mainloop()
