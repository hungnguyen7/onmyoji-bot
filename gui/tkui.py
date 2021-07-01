import json
import tkinter as tk
import tkinter.messagebox
import webbrowser
from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.url = 'http://www.onmyojibot.com'
        self.source_url = 'https://github.com/AcademicDog/onmyoji_bot'
        self.master = master
        self.master.iconbitmap('img/icon/OnmyojiBot.ico')
        self.master.wm_title('OnmyojiBot')
        self.pack()

        # Initialization parameters
        self.run_section = 0
        self.run_mode = tk.IntVar()
        self.run_submode = tk.IntVar()
        self.max_times = tk.IntVar()

        self.watchdog_enable = tk.BooleanVar()
        self.max_win_time = tk.IntVar()
        self.max_op_time = tk.IntVar()

        self.explore_mode = tk.IntVar(value=0)
        self.gouliang_1 = tk.BooleanVar(value=False)
        self.gouliang_2 = tk.BooleanVar(value=True)
        self.gouliang_3 = tk.BooleanVar(value=True)
        self.gouliang_4 = tk.BooleanVar(value=False)
        self.gouliang_5 = tk.BooleanVar(value=False)
        self.fight_boss_enable = tk.BooleanVar()
        self.slide_shikigami = tk.BooleanVar()
        self.slide_shikigami_progress = tk.IntVar()
        self.change_shikigami = 1

        self.debug_enable = tk.BooleanVar()

        self.run_mode.set(0)
        self.run_submode.set(0)
        self.max_times.set(0)
        self.watchdog_enable.set(True)
        self.max_win_time.set(100)
        self.max_op_time.set(20)
        self.fight_boss_enable.set(False)
        self.slide_shikigami.set(True)
        self.slide_shikigami_progress.set(10)
        self.debug_enable.set(False)

        # Create a menu bar
        self.create_menubar()

        # Create title
        self.create_title()

        # Create client options
        self.create_client()

        # Create tab
        self.create_section()

        # Create options
        self.create_frame0()
        self.create_frame1()
        self.create_frame2()
        self.create_frame3()

        # Creation times menu
        self.create_times()

        # Create advanced menu
        self.create_advance()

        # Create log
        self.create_log()

        # Create action buttons
        self.create_command()

    def create_menubar(self):
        '''
        Create a menu bar
        '''
        menubar = tk.Menu(self.master)

        # Create menu items
        menu1 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu1)
        menu1.add_command(label='Start', command=self.start_onmyoji)
        menu1.add_command(label='Exit', command=self.stop_onmyoji)

        # advanced options
        menu2 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Advanced", menu=menu2)
        menu2.add_command(label='Custom delay', command=self.delay_dialog)

        # help
        menu3 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Help', menu=menu3)
        menu3.add_command(label='On', command=self.say_hi)
        menu3.add_command(label='Instructions for use', command=self.help)
        menu3.add_separator()
        menu3.add_command(label='Donate', command=self.donate)

        # Set up
        self.master.config(menu=menubar)

    def create_title(self):
        # title
        tk.Label(self.master, text='OnmyojiBot',
                 font='Helvetica 20 bold').pack(anchor=tk.W)
        tk.Label(
            self.master, text=self.url).pack(anchor=tk.W)

        # home page
        self.main_frame1 = tk.Frame(self.master)
        self.main_frame2 = tk.Frame(self.master)
        self.main_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_client(self):
        '''
        Create client options
        '''
        self.client = ttk.Combobox(self.main_frame2)
        self.client['value'] = ('Onmyoji Steam version-default resolution', 'Simulator-1136*640 (100% zoom)')
        self.client.pack(fill=tk.X, padx=2, pady=2)
        self.client.current(0)
        self.client.config(state='readonly')

    def create_section(self):
        '''
        Create the main tab
        '''
        self.section = ttk.Notebook(self.main_frame1)

        # Create tab 1-Soul
        self.frame0 = tk.Frame(self.section)
        self.section.add(self.frame0, text='Soul')

        # Create tab 2-Evo
        self.frame1 = tk.Frame(self.section)
        self.section.add(self.frame1, text='Evolve')

        # Create tab 3-Explore
        self.frame2 = tk.Frame(self.section, padx=5, pady=5)
        self.section.add(self.frame2, text='Exploration')

        # Create Tab 4-About
        self.frame3 = tk.Frame(self.section)
        self.section.add(self.frame3, text='Information')

        self.section.pack(fill=tk.BOTH, expand=True)

    def create_frame0(self):
        '''
        Soul parameters
        '''
        # Game mode
        mode = tk.LabelFrame(self.frame0, text='Mode')
        mode.pack(padx=5, pady=5, fill=tk.BOTH)
        self.run_mode = tk.IntVar()
        self.run_mode.set(0)
        tk.Radiobutton(mode, text='Single player', variable=self.run_mode,
                       value=0).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(mode, text='As a driver', variable=self.run_mode,
                       value=1).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(mode, text='As a passenger', variable=self.run_mode,
                       value=2).grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(mode, text='Desktop version double open', variable=self.run_mode,
                       value=3).grid(row=1, column=1, sticky=tk.W)

        # Game script
        submode = tk.LabelFrame(self.frame0, text='Change food (do not lock the lineup)')
        submode.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Radiobutton(submode, text='Orichi', variable=self.run_submode,
                       value=0).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(submode, text='Greed-Anger-Foolery', variable=self.run_submode,
                       value=1).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(submode, text='Himiko', variable=self.run_submode,
                       value=2).grid(row=1, column=0, sticky=tk.W)

        # Mark shikigami
        mitama_mark = tk.Frame(self.frame0, padx=5, pady=5)
        mitama_mark.pack(fill=tk.X, expand=True)
        tk.Label(mitama_mark, text='Mark shikigami:').pack(side=tk.LEFT)
        self.mitama_team_mark = ttk.Combobox(mitama_mark, width=10)
        self.mitama_team_mark['value'] = (
            'Unmarked', 'The first shikigami', 'The second shikigami', 'The third shikigami', 'The 4th shikigami', 'The fifth shikigami')
        self.mitama_team_mark.pack(fill=tk.X, expand=True, padx=2)
        self.mitama_team_mark.current(0)
        self.mitama_team_mark.config(state='readonly')

    def create_frame1(self):
        '''
        Evo parameters
        '''
        text = tk.Text(self.frame1, height=5, width=25)
        text.pack(padx=5, pady=5, expand=True, fill=tk.BOTH, anchor=tk.NW)
        text.insert(tk.END, 'Select the Evo and the number of layers you want to play, and click the start button.')
        text.config(state=tk.DISABLED)

    def create_frame2(self):
        '''
        Explore parameters
        '''
        # 副本选择
        submode = tk.LabelFrame(self.frame2, text='Mode')
        submode.pack(fill=tk.BOTH, expand=True)
        tk.Radiobutton(submode, text='Single player', variable=self.explore_mode,
                       value=0, command=lambda: self.gouliang_state(1)).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(submode, text='As a driver', variable=self.explore_mode,
                       value=1, command=lambda: self.gouliang_state(2)).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(submode, text='As a passenger', variable=self.explore_mode,
                       value=2, command=lambda: self.gouliang_state(1)).grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(submode, text='Desktop version double open', variable=self.explore_mode,
                       value=3, command=lambda: self.gouliang_state(3)).grid(row=1, column=1, sticky=tk.W)

        # food settings
        food = tk.LabelFrame(self.frame2, text='Change food (do not lock the lineup)')
        food.pack(fill=tk.BOTH, expand=True)
        self.gouliang_l = tk.Checkbutton(
            food, text='Left', variable=self.gouliang_1)
        self.gouliang_l.grid(row=0, column=0)
        self.gouliang_m = tk.Checkbutton(
            food, text='In', variable=self.gouliang_2)
        self.gouliang_m.grid(row=0, column=1)
        self.gouliang_r = tk.Checkbutton(
            food, text='Right', variable=self.gouliang_3)
        self.gouliang_r.grid(row=0, column=2)
        tk.Label(food, text='Single/Team player').grid(row=0, column=3, sticky=tk.W)

        self.gouliang_lb = tk.Checkbutton(
            food, text='Left', variable=self.gouliang_4)
        self.gouliang_lb.grid(row=1, column=0)
        self.gouliang_rb = tk.Checkbutton(
            food, text='Right', variable=self.gouliang_5)
        self.gouliang_rb.grid(row=1, column=2)
        tk.Label(food, text='Team leader').grid(row=1, column=3, sticky=tk.W)
        self.gouliang_lb.config(state=tk.DISABLED)
        self.gouliang_rb.config(state=tk.DISABLED)

        # Change food settings
        tk.Checkbutton(self.frame2, text='Change dog food drag and drop progress bar, progress:',
                       variable=self.slide_shikigami).pack(anchor=tk.W)
        tk.Scale(self.frame2, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=0,
                 variable=self.slide_shikigami_progress).pack(fill=tk.X)
        self.cmb = ttk.Combobox(self.frame2)
        self.cmb['value'] = ('Change material', 'Replace N shiki', 'Replace R shiki')
        self.cmb.pack(fill=tk.X, padx=2)
        self.cmb.current(self.change_shikigami)
        self.cmb.config(state='readonly')

        # Hit BOSS settings
        tk.Checkbutton(self.frame2, text='Hit BOSS after the end',
                       variable=self.fight_boss_enable).pack(anchor=tk.W)

    def create_frame3(self):
        '''
        on
        '''
        text = tk.Text(self.frame3, height=5, width=25)
        text.pack(expand=True, fill=tk.BOTH)
        text.insert(
            tk.END, 'Website：%s\n\n' % (self.url))
        text.insert(
            tk.END, 'Source code：%s\n\n' % (self.source_url))
        text.insert(
            tk.END, 'Exchange Q group：592055060\n\n')
        text.insert(
            tk.END, 'If you think the script action is too slow, please go to the advanced menu to customize the delay.')
        text.config(state=tk.DISABLED)

    def create_times(self):
        '''
        Number of games
        '''
        times = tk.LabelFrame(self.main_frame1, text='Times setting')
        times.pack(padx=5, fill=tk.X, anchor=tk.W)
        timeframe1 = tk.Frame(times)
        timeframe1.pack(anchor=tk.W)
        tk.Label(timeframe1, text='Number of games (0=unlimited times):').pack(side=tk.LEFT)
        tk.Entry(timeframe1, width=6, textvariable=self.max_times).pack()
        self.end_operation = ttk.Combobox(times)
        self.end_operation['value'] = ('Close the script after the end', 'Close the script and game after the end')
        self.end_operation.pack(fill=tk.X, padx=2, pady=2)
        self.end_operation.current(0)
        self.end_operation.config(state='readonly')

    def create_advance(self):
        '''
        Advanced menu
        '''
        advance = tk.LabelFrame(self.main_frame1, text='')
        advance.pack(padx=5, pady=5, fill=tk.X, side=tk.BOTTOM)
        tk.Checkbutton(advance, text='Debug mode',
                       variable=self.debug_enable).pack(anchor=tk.W)
        tk.Checkbutton(advance, text='Automatically shut down onmyoji after timeout',
                       variable=self.watchdog_enable).pack(anchor=tk.W)
        frame = tk.Frame(advance)
        frame.pack(anchor=tk.W)
        tk.Label(frame, text='  Screen timeout time (seconds):').grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.max_win_time,
                 width=5).grid(row=0, column=1)
        tk.Label(frame, text='  Operation timeout (seconds):').grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.max_op_time,
                 width=5).grid(row=1, column=1)

    def create_log(self):
        '''
        Parameter display
        '''
        tk.Label(self.main_frame2, text='Operating parameters:').pack(anchor=tk.W)
        self.params = tk.Text(self.main_frame2, height=20, width=28)
        self.params.pack(anchor=tk.NW, fill=tk.BOTH,
                         padx=5, pady=5, expand=True)
        self.params.config(state=tk.DISABLED)

    def create_command(self):
        '''
        Button
        '''
        button_area = tk.Frame(self.main_frame2)
        button_area.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        tk.Button(button_area, text='Begin',
                  command=self.start_onmyoji).pack(fill=tk.X)
        tk.Button(button_area, text='End',
                  command=self.stop_onmyoji).pack(fill=tk.X)

    def show_params(self):
        self.get_gouliang()
        self.params.config(state=tk.NORMAL)
        self.params.insert(tk.END, '########1.0.1.0304########\n')
        self.params.insert(tk.END, 'client: ' + str(self.client.current()))
        self.params.insert(tk.END, '\nrun_section: ' +
                           str(self.section.index('current')))
        self.params.insert(tk.END, '\nrun_mode: '+str(self.run_mode.get()))
        self.params.insert(tk.END, '\nrun_submode: ' +
                           str(self.run_submode.get()))
        self.params.insert(tk.END, '\nmax_times: ' + str(self.max_times.get()))
        self.params.insert(tk.END, '\nend_operation: ' +
                           str(self.end_operation.current()))
        self.params.insert(tk.END, '\nwatchdog_enable: ' +
                           str(self.watchdog_enable.get()))
        self.params.insert(tk.END, '\nmax_win_time: ' +
                           str(self.max_win_time.get()))
        self.params.insert(tk.END, '\nmax_op_time: ' +
                           str(self.max_op_time.get()))
        self.params.insert(tk.END, '\nmitama_team_mark: ' +
                           str(self.mitama_team_mark.current()))
        self.params.insert(tk.END, '\nexplore_mode: ' +
                           str(self.explore_mode.get()))
        self.params.insert(tk.END, '\ngouliang: ' + str(self.gouliang))
        self.params.insert(tk.END, '\ngouliang_b: ' + str(self.gouliang_b))
        self.params.insert(tk.END, '\nfight_boss_enable: ' +
                           str(self.fight_boss_enable.get()))
        self.params.insert(tk.END, '\nslide_shikigami: ' +
                           str(self.slide_shikigami.get()))
        self.params.insert(tk.END, '\nslide_shikigami_progress: ' +
                           str(self.slide_shikigami_progress.get()))
        self.params.insert(tk.END, '\nchange_shikigami: ' +
                           str(self.cmb.current()))
        self.params.insert(tk.END, '\ndebug_enable: ' +
                           str(self.debug_enable.get())+'\n')
        self.params.insert(tk.END, '##########################\n\n')
        self.params.see(tk.END)
        self.params.config(state=tk.DISABLED)

    def say_hi(self):
        '''
        test
        '''
        tk.messagebox.showinfo(
            "OnmyojiBot", 'Website：%s\n\nSource code：%s\n\nExchange Q group：592055060' % (self.url, self.source_url))

    def delay_dialog(self):
        pw = DelayDialog(self)
        self.wait_window(pw)

    def help(self):
        '''
        Instructions for use
        '''
        Q = tk.messagebox.askyesno(
            "Instructions for use", 'For detailed instructions, please refer to%s\n\nWhether to visit?' % (self.url))
        if Q:
            webbrowser.open(self.url)

    def donate(self):
        '''
        Donate
        '''
        Q = tk.messagebox.askyesno(
            "Donate", 'Do what you can, 1 point is enough.\n\nGo to donate?')
        if Q:
            webbrowser.open('https://doc.onmyojibot.com/zh/latest/donate.html')

    def gouliang_state(self, state):
        '''
        Disable food option
             :param state: 1-Only enable 3 food, 2-Disable 3 food, 3-Enable all
        '''
        if state == 1:
            self.gouliang_4.set(False)
            self.gouliang_5.set(False)
            self.gouliang_l.config(state=tk.NORMAL)
            self.gouliang_m.config(state=tk.NORMAL)
            self.gouliang_r.config(state=tk.NORMAL)
            self.gouliang_lb.config(state=tk.DISABLED)
            self.gouliang_rb.config(state=tk.DISABLED)
        elif state == 2:
            self.gouliang_1.set(False)
            self.gouliang_2.set(False)
            self.gouliang_3.set(False)
            self.gouliang_l.config(state=tk.DISABLED)
            self.gouliang_m.config(state=tk.DISABLED)
            self.gouliang_r.config(state=tk.DISABLED)
            self.gouliang_lb.config(state=tk.NORMAL)
            self.gouliang_rb.config(state=tk.NORMAL)
        elif state == 3:
            self.gouliang_l.config(state=tk.NORMAL)
            self.gouliang_m.config(state=tk.NORMAL)
            self.gouliang_r.config(state=tk.NORMAL)
            self.gouliang_lb.config(state=tk.NORMAL)
            self.gouliang_rb.config(state=tk.NORMAL)

    def get_gouliang(self):
        '''
        Calculate food coordinates
        '''
        # Former food
        self.gouliang = []
        if self.gouliang_1.get():
            self.gouliang.append(1)
        if self.gouliang_2.get():
            self.gouliang.append(2)
        if self.gouliang_3.get():
            self.gouliang.append(3)

        # Post food
        self.gouliang_b = []
        if self.gouliang_4.get():
            self.gouliang_b.append(4)
        if self.gouliang_5.get():
            self.gouliang_b.append(5)

    def start_onmyoji(self):
        self.show_params()

    def stop_onmyoji(self):
        pass


class DelayDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('Delay setting')
        self.parent = parent

        # parameter
        self.delay = {
            1: [tk.IntVar(value=1000), tk.IntVar(value=1500)],
            2: [tk.IntVar(value=1300), tk.IntVar(value=2100)],
            3: [tk.IntVar(value=1800), tk.IntVar(value=3000)],
            4: [tk.IntVar(value=2500), tk.IntVar(value=4000)],
            5: [tk.IntVar(value=3000), tk.IntVar(value=5000)]}

        # Delay mechanism
        row1 = tk.Frame(self)
        row1.pack(fill=tk.X)
        tk.Label(row1, text='Delay mechanism：').pack(anchor=tk.W)
        text = tk.Text(row1, height=11, width=40)
        text.pack(expand=True, fill=tk.BOTH)
        text.insert(tk.END, '1- A total of 5 delays, the script randomly selects one of the 1-5 delays as the main delay,\
At the same time, one of the 1- 3 delays is selected as the secondary delay. Multiply the random coefficient on this basis.\n\n')
        text.insert(tk.END, '2- Refresh the selection every 5 minutes, the calculation unit is milliseconds.\n\n')
        text.insert(tk.END, '3- The main delay is used for the delay of general operations such as screenshots and image recognition, and the secondary delay is mainly used for settlement.\n\n')
        text.insert(tk.END, '4- Do not worry about why this table will not change every time you reopen it. The parameter exists in delay.json, and the restart is valid.\n\n')
        text.config(state=tk.DISABLED)

        #parameter settings
        row2 = tk.Frame(self)
        row2.pack(fill=tk.X)
        tk.Label(row2, text='First level: ').grid(row=0, column=0)
        tk.Label(row2, text='Lowest').grid(row=0, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[1][0]).grid(
            row=0, column=3)
        tk.Label(row2, text='Highest').grid(row=0, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[1][1]).grid(
            row=0, column=5)

        tk.Label(row2, text='Level 2: ').grid(row=1, column=0)
        tk.Label(row2, text='Lowest').grid(row=1, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[2][0]).grid(
            row=1, column=3)
        tk.Label(row2, text='Highest').grid(row=1, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[2][1]).grid(
            row=1, column=5)

        tk.Label(row2, text='Level 3: ').grid(row=2, column=0)
        tk.Label(row2, text='Lowest').grid(row=2, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[3][0]).grid(
            row=2, column=3)
        tk.Label(row2, text='Highest').grid(row=2, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[3][1]).grid(
            row=2, column=5)

        tk.Label(row2, text='Level 4: ').grid(row=3, column=0)
        tk.Label(row2, text='Lowest').grid(row=3, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[4][0]).grid(
            row=3, column=3)
        tk.Label(row2, text='Highest').grid(row=3, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[4][1]).grid(
            row=3, column=5)

        tk.Label(row2, text='Level 5: ').grid(row=4, column=0)
        tk.Label(row2, text='Lowest').grid(row=4, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[5][0]).grid(
            row=4, column=3)
        tk.Label(row2, text='Highest').grid(row=4, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[5][1]).grid(
            row=4, column=5)

        # Button
        row3 = tk.Frame(self)
        row3.pack(anchor=tk.E)
        tk.Button(row3, text='Set', command=self.confirm).grid(row=0, column=0)
        tk.Button(row3, text='Cancel', command=self.cancel).grid(row=0, column=1)

    def confirm(self):
        mydelay = {
            1: [self.delay[1][0].get(), self.delay[1][1].get() - self.delay[1][0].get()],
            2: [self.delay[2][0].get(), self.delay[2][1].get() - self.delay[2][0].get()],
            3: [self.delay[3][0].get(), self.delay[3][1].get() - self.delay[3][0].get()],
            4: [self.delay[4][0].get(), self.delay[4][1].get() - self.delay[4][0].get()],
            5: [self.delay[5][0].get(), self.delay[5][1].get() - self.delay[5][0].get()]}
        jsObj = json.dumps(mydelay)
        with open('delay.json', 'w') as f:
            f.write(jsObj)
        self.destroy()

    def cancel(self):
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
