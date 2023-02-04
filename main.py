from uuid import uuid4
import PySimpleGUI as sg
import ua_objects as ua
import pickle as pkl


def start():
    '''
    define a start function that
    either opens a save file or starts a new game
    '''

    #init a start window that either starts a new game or loads an existing game
    sg.theme('Topanga')
    layout =[
        [sg.Text("Welcome to Universal Assemblers")],
        [sg.Text("Select a save file"), sg.Input(), sg.FileBrowse(), sg.Button("Ok")],
        [sg.Button("New Game")]
    ]

    window = sg.Window('Welcome to Universal Assemblers', layout)
    #open the window and loop to handle events
    while True:
        #close window if closed event
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        #if user selects new game make a game graph
        if event == "New Game":
            G = ua.gameGraph(100, 0.01)
            window.close()
        #if user selects ok event try to open save file
        if event == "Ok":
            selected_file = values[0]
            if selected_file is None:
                sg.Popup('Oops! No save file was selected, please select a \'*.pickle\' file')
            else:
                try: 
                    with open('{selec}'.format(selec=selected_file), 'rb') as f:
                        #load game map --> this may be updated to be a broader game object
                        G =pkl.load(f)
                    sg.Popup('Game Loaded!')
                    window.close()
                except:
                    sg.Popup('Oops! Please select a \'*.pickle\' file')

    window.close()
    return G



def main():
    #G = ua.gameGraph(100, 0.001)
    #with open('save.pickle', 'wb') as f
    G = start()
    #define color theme of GUI
    sg.theme('Topanga')
    #sun = ua.Location(3,1,2,None)
    path = "location.png"
    #sun["image"].savefig(path)
    #print(sun["name"])
    #arrange the local map and object description elements in a single column

    G.image.savefig(path)
    local_col = [
        [sg.Text(key = '-MAP NAME-')],
        [sg.Image(filename = path, key = '-MAP IMAGE-', background_color = '#F9EFE8', size = (1000, 600))],
        #[sg.HorizontalSeparator()],
        [sg.Text('This will be game object descriptors')],
        [sg.Listbox(values = [], enable_events = True, key = '-OBJECT LIST-', size = (900, 400))]  
        ]

    #arrange the available actions into a column
    action_col = [
        [sg.Text('These will be the Game Actions')],
        [sg.Listbox(values =[], enable_events = True, key = '-ACTION LIST-', size = (900, 1000))]
        ]
    #group the game area together (local map + description) + available actions
    game_area = [sg.Column(local_col, size = (1000,1030)), sg.VerticalSeparator(), sg.Column(action_col, size = (920, 1030))]
    
    #set a layout for the window which includes a top ribbon (may remove later when i figure out how to edit the ribbon)
    layout = [[sg.Frame('Top Ribbon', [[sg.Text('This will be the top ribbon')]], size = (1920, 50))],
        [game_area]]
    #instantiate a window
    window = sg.Window('Universal Assemblers', layout, size = (1920,1080))
    #print("Suns children: {children}" .format(children = sun["children"]))
    #print("testing parent: {name} and also {child}" .format(name = sun["name"], child = sun["children"][0]["parent"]["name"]))
    while True:
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Close':
            break
    window.close()
    return

if __name__ == "__main__":
    main()