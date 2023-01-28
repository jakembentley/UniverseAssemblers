import PySimpleGUI as sg


def main():
    #define color theme of GUI
    sg.theme('Topanga')
    
    #arrange the local map and object description elements in a single column
    local_col = [
        [sg.Text(key = '-MAP NAME-')],
        [sg.Image(key = '-MAP IMAGE-', background_color = '#F9EFE8', size = (1000, 600))],
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

    #display the window until it is closed or the application is exited
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        break
    window.close()
    return

if __name__ == "__main__":
    main()