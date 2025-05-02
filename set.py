import PySimpleGUI as sg
from random import sample
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Kártyatulajdonságok
number = [0, 1, 2]
shape = [0, 1, 2]
colour = [0, 1, 2]
fill = [0, 1, 2]

# Összes tulajdonságú kártya legyártása (Descartes módszer szerűen)
deck = list(itertools.product(number, shape, colour, fill))

# 1 kártya kirajzolása adott helyre
def draw_card(ax, cardDraw):
    ax.set_aspect('equal')  # ugyanolyan az x és y egységhossza
    ax.axis('off')  # tengelyek eltűntetése

    x0, y0 = 0, 0
    width = 0.8
    height = 1.6

    # 
    ax.set_xlim(-0.05, width + 0.05) 
    ax.set_ylim(-0.05, height + 0.05)

    # Kártyák kerete
    card_rect = patches.FancyBboxPatch(
        (x0, y0), width, height,
        boxstyle="round,pad=0.02", # lekerekítés
        linewidth=2, edgecolor='gray', facecolor='white'
    )
    ax.add_patch(card_rect)

    # Színkódolás
    colors = {0: 'red', 1: 'green', 2: 'purple'}

    # Formák középre igazítása
    total_height = (cardDraw[0]+1) * 0.3
    y_center = y0 + height / 2
    start_y = y_center + total_height / 2 - 0.15
    ys = [start_y - i * 0.3 for i in range((cardDraw[0]+1))]  #közepei a formáknak

    for y in ys:  #végigmegy a formákon
        # Formák mérete
        form_width = 0.3
        form_height = 0.214

        if cardDraw[1] == 0: # rombusz
            shape = patches.Polygon([
                [x0 + width/2, y + form_height / 2],
                [x0 + width/2 + form_width/2, y],
                [x0 + width/2, y - form_height / 2],
                [x0 + width/2 - form_width/2, y]
            ], closed=True, edgecolor=colors[cardDraw[2]], facecolor='none')

        elif cardDraw[1] == 1: # ovális
            shape = patches.Ellipse(
                (x0 + width/2, y), form_width, form_height,
                edgecolor=colors[cardDraw[2]], facecolor='none')

        elif cardDraw[1] == 2: # téglalap (alapból hullámjel az eredeti játékben)
            shape = patches.FancyBboxPatch(
                (x0 + width/2 - form_width/2, y - form_height/2),
                form_width, form_height,
                boxstyle="round,pad=0.02",
                edgecolor=colors[cardDraw[2]], facecolor='none')
        else:
            continue

        # Kitöltés
        if cardDraw[3] == 0: # teli
            shape.set_facecolor(colors[cardDraw[2]])
        elif cardDraw[3] == 1: # üres
            shape.set_facecolor('none')
        elif cardDraw[3] == 2: # csíkos
            shape.set_facecolor('white')
            shape.set_hatch('///////')

        ax.add_patch(shape)

# SET-ek megszámolása
def setNum(cardSetNumber, n):
    numberOfSets = 0
    for i in range(0, n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                if ((cardSetNumber[i][0] + cardSetNumber[j][0] + cardSetNumber[k][0]) % 3 == 0 and 
                    (cardSetNumber[i][1] + cardSetNumber[j][1] + cardSetNumber[k][1]) % 3 == 0 and 
                    (cardSetNumber[i][2] + cardSetNumber[j][2] + cardSetNumber[k][2]) % 3 == 0 and 
                    (cardSetNumber[i][3] + cardSetNumber[j][3] + cardSetNumber[k][3]) % 3 == 0):
                    numberOfSets += 1
    return numberOfSets

# SET-ek eltárolása
def findSets(cardSet, n):
    foundSets = []
    for i in range(0, n-2):
        for j in range(i+1, n-1):
            for k in range(j+1, n):
                if ((cardSet[i][0] + cardSet[j][0] + cardSet[k][0]) % 3 == 0 and 
                    (cardSet[i][1] + cardSet[j][1] + cardSet[k][1]) % 3 == 0 and 
                    (cardSet[i][2] + cardSet[j][2] + cardSet[k][2]) % 3 == 0 and 
                    (cardSet[i][3] + cardSet[j][3] + cardSet[k][3]) % 3 == 0):
                    foundSets.append(sorted([cardSet[i], cardSet[j], cardSet[k]], key = lambda card: (card[0], card[2], card[3], card[1])))
    return foundSets

# matplotlib ábrák kirajzolása a képernyőre
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both')
    return figure_canvas_agg

# Kezdő képernyő elkészítése
def create_start_window():
    layout = [
        [sg.Text('SET', font=('Helvetica', 24), justification='center', size=(20, 1))],
        [sg.Text('Enter the number of cards to play with:')],
        [sg.Input(key='-NUM_CARDS-', size=(5, 1), enable_events=True, focus=True)],
        [sg.Button('Start Game')]
    ]
    window = sg.Window('SET Game', layout, finalize=True, element_justification='center')
    
    # Enter is működjön úgy, ahogy a 'Start Game' gomb
    window['-NUM_CARDS-'].bind("<Return>", "_Enter")
    
    return window

# A játékablak elkészítése
def create_game_window(card_set):
    # Kártyák ábrázolása matplotlib-el
    n = len(card_set)
    rows, cols = 3, math.ceil(n / 3)
    fig, axes = plt.subplots(rows, cols, figsize=(9, 2 * rows))
    
    # Lapok indexeinek meghatározása
    for i, card in enumerate(card_set):
        r = i % 3
        c = i // 3 #egészrész
        draw_card(axes[r][c], card)
    
    # Felesleges kártyahelyek üresen hagyása
    if n % 3 != 0:
        for i in range(n % 3, 3):
            fig.delaxes(axes[i][n // 3])
    
    plt.tight_layout()
    
    layout = [
        [sg.Canvas(key='-CANVAS-')],
        [sg.Text('How many sets do you see?'), sg.Input(key='-GUESS-', size=(5, 1), enable_events=True, focus=True)], 
        [sg.Button('Submit Guess'), sg.Button('Help')],
        [sg.Text('', key='-HELP_TEXT-', visible=False)]
    ]
    
    window = sg.Window('SET Game', layout, finalize=True, element_justification='center')
    window.move(300,0) #ablak helyének beállítása
    window.force_focus()
    
    # Enter is működjön
    window['-GUESS-'].bind("<Return>", "_Enter")
    
    # Kártyák kirajzolása a képernyőre
    fig_canvas_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    
    return window, fig_canvas_agg

# Az eredményablak elkészítése
def create_result_window(correct_answer, user_guess):
    result_text = f"The correct answer is {correct_answer}. You guessed {user_guess}."
    feedback = "Correct!" if int(user_guess) == correct_answer else "Try again!"
    
    layout = [
        [sg.Text(result_text)],
        [sg.Text(feedback)],
        [sg.Button('New Game'), sg.Button('Show Sets'), sg.Button('Exit')]
    ]
    
    return sg.Window('Game Result', layout, finalize=True, element_justification='center')

# Ablak készítése a SET-ek megmutatásához
def create_sets_window(found_sets):
    if not found_sets:
        layout = [
            [sg.Text('No sets found!')],
            [sg.Button('Back')]
        ]
        return sg.Window('Sets', layout, finalize=True, element_justification='center'), None #visszatérési érték ablak és egy ábra(ami itt nincs)
    
    # SET-ek kirajzolása
    num_sets = len(found_sets)
    fig, axes = plt.subplots(num_sets, 3, figsize=(6, 2 * num_sets))
    
    if num_sets == 1:
        for i, card in enumerate(found_sets[0]):
            draw_card(axes[i], card)
    else:
        for set_idx, set_cards in enumerate(found_sets):
            for card_idx, card in enumerate(set_cards):
                draw_card(axes[set_idx][card_idx], card)
    
    plt.tight_layout()
    
    figure_canvas = FigureCanvasTkAgg(fig, None)
    figure_canvas.draw()
    
    fig_width = fig.get_figwidth() * fig.dpi
    fig_height = fig.get_figheight() * fig.dpi
    
    # Create a frame to hold the canvas
    layout = [
        [sg.Text('Sets Found:', font=('Helvetica', 14))],
        [sg.Column(
            [[sg.Canvas(size=(int(fig_width), int(fig_height)), key='-SETS_CANVAS-')]],
            scrollable=True, 
            vertical_scroll_only=True,
            size=(650, 500),  #a kártyákat tartalmazó rész mérete 
            expand_x=True, #automatikusan nagyobb lesz, hogy kitöltse a rendelkezésre álló teret
            expand_y=True
        )],
        [sg.Button('Back')]
    ]
    
    window = sg.Window('Sets', layout, finalize=True, element_justification='center')
    
    window.move(300,0)
    window.force_focus()
    
    canvas = window['-SETS_CANVAS-'].TKCanvas
    
    # Kép rárajzolása a vászonra
    figure_canvas = FigureCanvasTkAgg(fig, canvas)
    figure_canvas.draw()
    figure_canvas_widget = figure_canvas.get_tk_widget()
    figure_canvas_widget.pack(side='top', fill='both', expand=1)
    
    # Az egészet meg lehessen nézni
    canvas.configure(scrollregion=canvas.bbox('all'))
    
    return window, fig_canvas_agg

#kezdőállapot
start_window = create_start_window()
game_window, result_window, sets_window = None, None, None
fig_canvas_agg, sets_fig_canvas_agg = None, None
game_data = {}

# Event loop
while True:
    window, event, values = sg.read_all_windows()

    #ablak bezárása
    if event == sg.WIN_CLOSED:
        window.close()
        if window == sets_window: #SET-nél csak térjen vissza az előző ablakra
            sets_window = None
        else: break
    
    # Események a kezdő képernyőn
    elif window == start_window:
        if event == '-NUM_CARDS-':
            # Csak számokat lehet írni inputnak
            if values['-NUM_CARDS-'] and not values['-NUM_CARDS-'][-1].isdigit():
                start_window['-NUM_CARDS-'].update(values['-NUM_CARDS-'][:-1])
        
        elif event == 'Start Game' or event == '-NUM_CARDS-' + '_Enter':
            try:
                n = int(values['-NUM_CARDS-'])
                if n < 6:  # Minimum 6 kártyásak a játékok
                    sg.popup('Please enter at least 6.')
                    continue
                if n > 27:  # Maximum 27 kártyásak
                    sg.popup('Please enter at most 27.')
                    continue
                
                # n kártya generálása
                card_set = sample(deck, n)
                num_sets = setNum(card_set, n)
                
                # Játék ablak készítése
                if game_window:
                    game_window.close()
                game_window, fig_canvas_agg = create_game_window(card_set)
                
                # Adatok elmentése
                game_data = {
                    'card_set': card_set,
                    'n': n,
                    'num_sets': num_sets
                }
                
                # Kezdő ablak elrejtése
                start_window.hide()
                
            except ValueError:
                sg.popup('Please enter a valid number.')
    
    # Játékablak eseményei
    elif window == game_window:
        #Segítség gomb
        if event == 'Help':
            helpnumber = game_data['n'] * (game_data['n']-1) * (game_data['n']-2) / 474
            helpnumber = round(helpnumber, 2)
            window['-HELP_TEXT-'].update(f"Expected number of sets: {helpnumber}", visible=True)
        
        # megoldás megadása gomb
        elif event == 'Submit Guess' or event == '-GUESS-' + '_Enter':
            try:
                guess = values['-GUESS-']
                if not guess.isdigit():
                    sg.popup('Please enter a valid number.')
                    continue
                
                # Játékablak becsukása érvényes tipp leadása után
                if fig_canvas_agg:
                    plt.close('all')
                game_window.close()
                game_window = None
                
                # Eredmény ablak megnyitása
                result_window = create_result_window(game_data['num_sets'], guess)
                
            except ValueError:
                sg.popup('Please enter a valid number.')
    
    # Eredmény ablak eseményei
    elif window == result_window:
        if event == 'New Game':
            # Eredmény ablak becsukása
            result_window.close()
            result_window = None
            
            # Kezdőképernyő megjelenítése
            start_window.un_hide()
        
        elif event == 'Show Sets':
            # SET-ek megkeresése
            found_sets = findSets(game_data['card_set'], game_data['n'])
            
            # SET-ek ablakának megnyitása
            sets_window, sets_fig_canvas_agg = create_sets_window(found_sets)
        
        elif event == 'Exit':
            break
    
    # SET-ek ablakának eseményei
    elif window == sets_window:
        if event == 'Back':
            # SET-ek ablakának bezárása
            if sets_fig_canvas_agg:
                plt.close('all')
            sets_window.close()
            sets_window = None