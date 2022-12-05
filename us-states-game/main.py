import turtle
import pandas


screen = turtle.Screen()
screen.title(f"U.S. States Game")
# Download image to be used as turtle
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pandas.read_csv("50_states.csv")

all_states = data.state.to_list()


guessed_states = []

while len(guessed_states) <= 50:
    answer_state = screen.textinput(title=f"Guess the state {len(guessed_states)}/50",
                                    prompt="What's another state's name?").title()
    if answer_state == "Exit":
        states_to_learn = []
        for state in all_states:
            if state not in guessed_states:
                states_to_learn.append(state)
        break
    if answer_state in all_states:
        guessed_states.append(answer_state)
        state_data = data[data.state == answer_state]
        x_cor = int(state_data.x)
        y_cor = int(state_data.y)

        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(x_cor, y_cor)
        t.write(f"{answer_state}", align="center", font=("Arial", 8, "normal"))

    else:
        print("Incorrect answer")




data = pandas.DataFrame(states_to_learn)
data.to_csv("states_to learn.csv")


def get_mouse_click_coor(x, y):
    print(x, y)


turtle.onscreenclick(get_mouse_click_coor)
# Mainloop keeps the screen open
turtle.mainloop()

